#!/bin/sh
# FM-006's page: the guard's refusal, run in a scratch repository with the tool of shoalmark main (88c7b0c).
# An invented Owner (you@example.org, a key with no passphrase — tier 0) and a seat (implementer@seat).
# Run: sh demo.sh <a shoalmark checkout at 88c7b0c> > demo.out 2>&1 — demo.out beside it is the run docs/triage.md quotes (2026-09-26,
# the GtM seat, 8e509911/gtm-2). Keys and times are made fresh on every run, so another run prints other commit ids.
set -u
T=$(cd "${1:?usage: sh demo.sh <a shoalmark checkout, e.g. at 88c7b0c>}" && pwd) || exit 1; W=$(mktemp -d)
D=$W/demo; rm -rf "$D"; mkdir -p "$D"; cd "$D" || exit 1
git init -q --bare origin.git; git init -q -b main library; cd library || exit 1
git remote add origin "$D/origin.git"
cp "$T/shoalmark.py" .; cp -R "$T/vendor" .
ssh-keygen -q -t ed25519 -N "" -f "$D/owner_key" -C you@example.org
echo "you@example.org $(cat "$D/owner_key.pub")" > "$D/allowed_signers"
git config gpg.format ssh; git config gpg.ssh.allowedSignersFile "$D/allowed_signers"
OWNER="-c user.name=Owner -c user.email=you@example.org -c user.signingkey=$D/owner_key"
python3 shoalmark.py --init --key LIB >/dev/null
printf '\n[seats]\nowner = "you@example.org signed"\nimplementer = "implementer@seat"\n' >> shoalmark.toml
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
for k,v in (("for","the village library's lending, all of it: members, loans, returns and the shelf in one record the librarian trusts"),
            ("so that","a member finds a book and the librarian finds a member in one look, and nothing on loan is lost"),
            ("never","lend what the catalogue does not hold, or drop a member's record before their last loan is back")):
    i=s.index(f"- **{k}** — *e.g."); j=s.index("\n",i); s=s[:i]+f"- **{k}** {v}"+s[j:]
s=s.replace("\n1.\n","\n1. The loan desk runs on a tagged release.\n2. A pull request merges only with a review's evidence file on its head.\n")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null; git add -A
git $OWNER commit -q -S -m "the Owner writes his intent and his current path"
git push -q -u origin main 2>/dev/null; git remote set-head origin main
echo "== the Owner's commit"; git log -1 --format='%h %ae %G? %GS %s'

echo; echo "== 1. a seat's commit on a branch changes path line 2 (no hooks installed yet); then --check"
git config user.name "Implementer seat"; git config user.email implementer@seat
git switch -q -c lib/001-faster-merges
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("2. A pull request merges only with a review's evidence file on its head.","2. A pull request merges when its tests pass.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py; echo "regenerate exit $?"; git add -A; git commit -q -m "LIB-001: path line 2, shorter"
git log -1 --format='%h %ae %G? %s'
python3 shoalmark.py --check; echo "exit $?"

echo; echo "== 2. the hooks installed; a seat's commit that changes the intent"
git switch -q main; python3 shoalmark.py --install-hook >/dev/null
git switch -q -c lib/002-a-better-intent
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("and nothing on loan is lost","and nothing on loan is ever lost")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null; git add -A; git commit -q -m "LIB-002: the intent, sharpened"; echo "commit exit $?"; git log -1 --format='%h %ae %s'
git restore -q -S -W . ; git switch -q main

echo; echo "== 3. the Owner makes path line 2's change himself, signed; then --check"
git switch -q -c lib/003-the-owners-own
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("2. A pull request merges only with a review's evidence file on its head.","2. A pull request merges only with a review's evidence file on its head, and its tests green.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null; git add -A; git $OWNER commit -q -S -m "path line 2: tests green too"; echo "commit exit $?"
git log -1 --format='%h %ae %G? %GS %s'
python3 shoalmark.py --check; echo "exit $?"

echo; echo "== 4. the tier-0 limit: a process on the Owner's account, his key without a passphrase, signs as him"
git switch -q main; git switch -q -c lib/004-signed-with-his-key
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("2. A pull request merges only with a review's evidence file on its head.","2. A pull request merges when its tests pass.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null; git add -A; git $OWNER commit -q -S -m "path line 2, signed with the Owner's key"; echo "commit exit $?"
git log -1 --format='%h %ae %G? %GS %s'
python3 shoalmark.py --check; echo "exit $?"
