"""Bounded archive/common acquisition regressions, using actual CLI entry."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import time


def run_archive_integration_controls(fm, check, archive):
    """RV-3071/RV-3072: administrative writes and missing source proof refuse."""
    started = time.monotonic()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    svn, svnadmin, git = (shutil.which(exe) for exe in ('svn', 'svnadmin', 'git'))
    if not all((svn, svnadmin, git)):
        raise RuntimeError('archive regression fixture setup requires svn, svnadmin and git')
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory).resolve()
        empty = base / 'empty PATH'; empty.mkdir()
        no_tools = dict(env, PATH=str(empty), PYTHONDONTWRITEBYTECODE='1')

        def project(name):
            server, wc = base / (name + '-server'), base / name
            subprocess.run([svnadmin, 'create', str(server)], check=True, capture_output=True, env=env, timeout=30)
            subprocess.run([svn, 'checkout', '-q', server.as_uri(), str(wc)], check=True, capture_output=True, env=env, timeout=30)
            return wc

        def source(name):
            path = base / name
            shutil.copytree(archive, path)
            return path

        def snapshot(path):
            return {str(p.relative_to(path)): ('link', os.readlink(p)) if p.is_symlink() else
                    ('dir', None) if p.is_dir() else ('file', p.read_bytes()) for p in path.rglob('*')}

        def run(src, wc, destination, *, fault=None, environment=no_tools):
            argv = [sys.executable, str(src / 'shoalmark.py'), '--root', str(wc), '--vendor', str(destination)]   # R17: no bypass flag
            if fault is not None:
                wrapper = base / 'source fault.py'
                wrapper.write_text('''import importlib.util,subprocess,sys
tool,fault=sys.argv[1:3]
s=importlib.util.spec_from_file_location('tested_tool',tool);fm=importlib.util.module_from_spec(s);s.loader.exec_module(fm)
original=fm.vcs_process
def injected(program,*args,**kwargs):
    if kwargs.get('source') and program=='git' and args==('rev-parse','--show-toplevel'):
        if fault=='permission':raise PermissionError('present Git is not executable')
        if fault=='launcher':raise FileNotFoundError('present Git launcher is broken')
        if fault=='empty':return subprocess.CompletedProcess([],0,'','')
        if fault=='unknown128':return subprocess.CompletedProcess([],128,'','unexpected source failure')
        return subprocess.CompletedProcess([],2,'','injected Git failure')
    return original(program,*args,**kwargs)
fm.vcs_process=injected
raise SystemExit(fm.main(sys.argv[3:]))
''', encoding='utf-8')
                argv = [sys.executable, str(wrapper), str(src / 'shoalmark.py'), fault, *argv[2:]]
            return subprocess.run(argv, cwd=wc, env=environment, capture_output=True, text=True,
                                  encoding='utf-8', errors='replace', timeout=30)

        complete = source('complete archive')
        for name, nested in [('root', False), ('nested', True)]:
            wc = project('admin-' + name)
            admin = wc / 'nested/.svn' if nested else wc / '.svn'
            admin.mkdir(parents=True, exist_ok=True)
            before = snapshot(wc)
            result = run(complete, wc, admin / 'tool')
            check(f'RV-3071: actual CLI refuses {name} SVN administration before writes',
                  result.returncode == fm.EXIT_LINT and len(result.stderr.strip().splitlines()) == 1
                  and not result.stdout and snapshot(wc) == before)
        wc = project('positive')
        result = run(complete, wc, wc / 'tools/shoalmark')
        check('RV-3071/RV-3072: complete archive still copies with both production tools absent',
              result.returncode == 0 and (wc / 'tools/shoalmark/PIN').is_file()
              and all(shutil.which(exe, path=no_tools['PATH']) is None for exe in ('git', 'svn')))
        for name, text in [('malformed', 'malformed\n'), ('dangling', 'gitdir: missing-directory\n')]:
            src, wc = source('source-' + name), project('target-' + name)
            (src / '.git').write_text(text, encoding='utf-8')
            before = snapshot(wc)
            result = run(src, wc, wc / 'tools/shoalmark', environment=env)
            check(f'RV-3072: actual CLI refuses {name} source metadata before writes',
                  result.returncode == fm.EXIT_LINT and len(result.stderr.strip().splitlines()) == 1
                  and not result.stdout and snapshot(wc) == before)
        for fault in ('status', 'permission', 'launcher', 'empty', 'unknown128'):
            wc = project('fault-' + fault); before = snapshot(wc)
            result = run(complete, wc, wc / 'tools/shoalmark', fault=fault, environment=env)
            check(f'RV-3072: checked source {fault} failure refuses through actual entry before writes',
                  result.returncode == fm.EXIT_LINT and len(result.stderr.strip().splitlines()) == 1
                  and not result.stdout and snapshot(wc) == before)
        # An actual linked Git working tree exercises its own AND common administrative destinations.
        host = base / 'git host'
        subprocess.run([git, 'init', '-q', str(host)], check=True, capture_output=True, env=env, timeout=30)
        subprocess.run([git, '-C', str(host), '-c', 'core.hooksPath=' + os.devnull, '-c', 'commit.gpgsign=false',
                        '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '--allow-empty', '-qm', 'fixture'], check=True, capture_output=True, env=env, timeout=30)
        linked = base / 'linked consumer'
        subprocess.run([git, '-C', str(host), '-c', 'core.hooksPath=' + os.devnull,
                        'worktree', 'add', '--detach', str(linked)], check=True, capture_output=True, env=env, timeout=30)
        dirs = subprocess.check_output([git, '-C', str(linked), 'rev-parse', '--absolute-git-dir', '--git-common-dir'], env=env).decode().splitlines()
        for name, admin in zip(('own', 'common'), dirs):
            path = (linked / admin).resolve(); before = snapshot(path)
            result = run(complete, linked, path / 'forbidden-tool', environment=env)
            check(f'RV-3071: actual CLI refuses linked Git {name} administration before writes',
                  result.returncode == fm.EXIT_LINT and len(result.stderr.strip().splitlines()) == 1
                  and not result.stdout and snapshot(path) == before)
        # Alias setup is optional only where the host refuses to create a directory symlink.
        wc = project('alias'); alias = wc / 'alias'
        try:
            alias.symlink_to(wc / '.svn', target_is_directory=True)
        except (OSError, NotImplementedError):
            alias_case = {'skipped': 1, 'reason': 'directory symlinks unavailable on this host'}
        else:
            before = snapshot(wc); result = run(complete, wc, alias / 'forbidden-tool')
            check('RV-3071: actual CLI refuses resolved administrative alias before writes',
                  result.returncode == fm.EXIT_LINT and len(result.stderr.strip().splitlines()) == 1
                  and not result.stdout and snapshot(wc) == before)
            alias_case = {'skipped': 0}
    return {'seconds': round(time.monotonic() - started, 3), **alias_case}
