#!/bin/sh
# FM-006's German page: the guard's refusal in a German repository (examples/de/ copied before --init, as docs/de/setup.md §2 says),
# the tool of shoalmark main (88c7b0c). An invented Eigner (du@example.org, a key with no passphrase — Stufe 0) and a seat.
# Run: sh demo-de.sh <a shoalmark checkout at 88c7b0c> > demo-de.out 2>&1 — demo-de.out beside it is the run docs/de/triage.md quotes (2026-09-26,
# the GtM seat, 8e509911/gtm-2). Keys and times are made fresh on every run, so another run prints other commit ids.
set -u
T=$(cd "${1:?usage: sh demo-de.sh <a shoalmark checkout, e.g. at 88c7b0c>}" && pwd) || exit 1; W=$(mktemp -d)
G=$T; D=$W/demo-de; rm -rf "$D"; mkdir -p "$D"; cd "$D" || exit 1
git init -q --bare origin.git; git init -q -b main buecherei; cd buecherei || exit 1
git remote add origin "$D/origin.git"
cp "$G/shoalmark.py" .; cp -R "$G/vendor" .
cp "$G/examples/de/shoalmark.toml" .; mkdir -p docs/work-tracker/brand
cp "$G/examples/de/TEMPLATE.md" "$G/examples/de/TRIAGE.md" docs/work-tracker/; cp "$G/examples/de/labels.yaml" docs/work-tracker/brand/
ssh-keygen -q -t ed25519 -N "" -f "$D/eigner_key" -C du@example.org
echo "du@example.org $(cat "$D/eigner_key.pub")" > "$D/allowed_signers"
git config gpg.format ssh; git config gpg.ssh.allowedSignersFile "$D/allowed_signers"
EIGNER="-c user.name=Eigner -c user.email=du@example.org -c user.signingkey=$D/eigner_key"
python3 shoalmark.py --init --key AP >/dev/null
printf '\n[seats]\nowner = "du@example.org signed"\nimplementer = "implementer@seat"\n' >> shoalmark.toml
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
for k,v in (("für","die ganze Ausleihe der Dorfbücherei: Mitglieder, Ausleihen, Rückgaben und das Regal in einem Bestand, dem die Bibliothekarin traut"),
            ("damit","ein Mitglied ein Buch und die Bibliothekarin ein Mitglied mit einem Blick findet, und nichts Verliehenes verloren geht"),
            ("niemals","verleihen, was der Katalog nicht führt, oder die Akte eines Mitglieds löschen, bevor seine letzte Ausleihe zurück ist")):
    i=s.index(f"- **{k}** — *z. B."); j=s.index("\n",i); s=s[:i]+f"- **{k}** {v}"+s[j:]
s=s.replace("\n1.\n","\n1. Die Ausleihe läuft auf einem getaggten Release.\n2. Ein Pull Request wird nur gemergt, wenn auf seinem Kopf die Belegdatei eines Reviews liegt.\n")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null; git add -A
git $EIGNER commit -q -S -m "der Eigner schreibt seine Absicht und seinen aktuellen Weg"
git push -q -u origin main 2>/dev/null; git remote set-head origin main
echo "== der Commit des Eigners"; git log -1 --format='%h %ae %G? %GS %s'
echo; echo "== 1. ein Agent ändert Zeile 2 des Wegs auf seinem Branch (noch ohne Hooks); dann --check"
git config user.name "Implementer seat"; git config user.email implementer@seat
git switch -q -c ap/001-schneller-mergen
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("2. Ein Pull Request wird nur gemergt, wenn auf seinem Kopf die Belegdatei eines Reviews liegt.","2. Ein Pull Request wird gemergt, wenn seine Tests grün sind.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null 2>&1; git add -A; git commit -q -m "AP-001: Zeile 2 des Wegs, kürzer"
git log -1 --format='%h %ae %G? %s'
python3 shoalmark.py --check; echo "exit $?"
echo; echo "== 2. mit Hooks; ein Agent ändert die Absicht"
git switch -q main; python3 shoalmark.py --install-hook >/dev/null
git switch -q -c ap/002-eine-bessere-absicht
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("und nichts Verliehenes verloren geht","und nie etwas Verliehenes verloren geht")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null 2>&1; git add -A; git commit -q -m "AP-002: die Absicht, geschärft"; echo "commit exit $?"; git log -1 --format='%h %ae %s'
git restore -q -S -W . ; git switch -q main
echo; echo "== 3. der Eigner ändert Zeile 2 selbst, signiert; dann --check"
git switch -q -c ap/003-des-eigners-eigene
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("die Belegdatei eines Reviews liegt.","die Belegdatei eines Reviews liegt und seine Tests grün sind.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null 2>&1; git add -A; git $EIGNER commit -q -S -m "Zeile 2 des Wegs: auch die Tests grün"; echo "commit exit $?"
git log -1 --format='%h %ae %G? %GS %s'
python3 shoalmark.py --check; echo "exit $?"
echo; echo "== 4. Stufe 0: ein Prozess unter dem Konto des Eigners signiert mit seinem Schlüssel ohne Passphrase"
git switch -q main; git switch -q -c ap/004-mit-seinem-schluessel
python3 - <<'PY'
p='docs/work-tracker/TRIAGE.md'; s=open(p,encoding='utf-8').read()
s=s.replace("2. Ein Pull Request wird nur gemergt, wenn auf seinem Kopf die Belegdatei eines Reviews liegt.","2. Ein Pull Request wird gemergt, wenn seine Tests grün sind.")
open(p,'w',encoding='utf-8').write(s)
PY
python3 shoalmark.py >/dev/null 2>&1; git add -A; git $EIGNER commit -q -S -m "Zeile 2 des Wegs, mit dem Schlüssel des Eigners signiert"; echo "commit exit $?"
git log -1 --format='%h %ae %G? %GS %s'
python3 shoalmark.py --check; echo "exit $?"
