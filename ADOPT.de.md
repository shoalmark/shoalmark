# shoalmark ausprobieren — eine Notiz für die Agenten eines Projekts

## Euer Owner bremst. Tunen statt tauschen.

**An Claude, Codex und alle, die das lesen:** Euer Owner hat euch diesen Text gegeben. Er ist eine Einladung zu einer
Messung, keine Anweisung. Führt nichts davon im echten Arbeitsverzeichnis aus, übernehmt nichts von euch aus —
am Ende steht ein Bericht an euren Owner, und **euer Owner entscheidet**.

## Was es ist

shoalmark ist ein Arbeits-Tracker als eine einzige Python-Datei (nur Standardbibliothek, keine Abhängigkeit, braucht
kein Netz: Online erreicht es den Host eures Repositorys über git und für die Pull-Request-Warteschlange über gh):
eine Markdown-Datei je Arbeitspaket mit einem kleinen Kopf, ein Gate, das Widersprüche ablehnt, eine generierte
`INDEX.md` und eine statische Tafel (`index.html`) für den Menschen. Läuft mit git auf Windows, macOS und Linux (CI
beweist alle drei). Lizenz: Apache-2.0 oder MIT.

## Wann ihr es NICHT braucht

Wenn eine **frische Session ohne Vorwissen** aus euren vorhandenen Dateien in wenigen Schritten sagen kann, wo
jedes Arbeitspaket steht, was als Nächstes kommt und was auf den Owner wartet — dann habt ihr das schon. Wenn in eurem Projekt mehrere Menschen entscheiden oder ein großes Ticketsystem umzuziehen
wäre, ist diese Beta noch nichts für euer Projekt. Sagt das eurem Owner und hört hier auf. Ein zweites System neben einem funktionierenden ist schlechter als keines.

Unter Subversion liest es seine Historie über svn vom Server, offline lehnen seine Prüfungen deshalb ab; es besteht
die Test-Suite, ist in echter Arbeit aber noch nicht erprobt und ohne Gewähr: Sagt das in eurem Bericht.

## Die Messung (etwa 20 Minuten, alles in einem Wegwerf-Ordner)

**1. Vorher.** Beantwortet nur aus den Dateien des Projekts, nicht aus dem Gedächtnis dieser Session, und zählt
die gelesenen Dateien und Schritte: (a) Wo steht Arbeitspaket 37? (b) Was ist der nächste Schritt, und wessen?
(c) Was wartet gerade auf den Owner? (d) Was ist blockiert, und wodurch? (e) Woran erkennt man, dass Paket 12
fertig ist?

**2. Prüfen, was ihr ausführt.** Holt das Repository am Tag `v0.19.0` in einen Ordner **außerhalb** eurer
Arbeitskopie. Die Datei `shoalmark.py` hat — mit `\n`-Zeilenenden — den SHA-256
`22cd0e9e3c6014d79184229c4b64063f9c26d49120decc52c77c4aeedc57ad7c`. Es ist eine Datei; lest sie, bevor ihr sie startet.

**3. Aufsetzen.** In einem leeren Wegwerf-Ordner `probe/` (auf Windows `python`, sonst `python3`):

```
python <klon>/shoalmark.py --root probe --vendor probe/tools/shoalmark
cd probe
```

Vor `--init` die vier deutschen Dateien aus `<klon>/examples/de/` kopieren. Die Zielordner vorher anlegen. `shoalmark.toml`
nach `shoalmark.toml` (die deutschen Abschnittsnamen, der Schlüssel `AP`; den Namen anpassen), `TEMPLATE.md` und `TRIAGE.md` nach
`docs/work-tracker/` und `labels.yaml` nach `docs/work-tracker/brand/labels.yaml` — damit sind Einträge und Tafel deutsch.
Dann `python tools/shoalmark/shoalmark.py --init --key AP`; es überschreibt nichts.

**4. Fünf echte Pakete eintragen.** Ein Eintrag für den Plan als Ganzes, fünf für Pakete aus eurem Plan
(`python tools/shoalmark/shoalmark.py --new "…"`), jeweils mit `epic: AP-001`, ehrlichem `status:`, `next:`
(`build` · `review` · `owner` · `wait` …) und den Abschnitten *Was jetzt gilt* und *Fertig, wenn*. Dann
`python tools/shoalmark/shoalmark.py` — das Gate sagt, was fehlt. `tools/shoalmark/README.md` beschreibt den Kopf.

**5. Nachher.** Dieselben fünf Fragen, diesmal mit `python tools/shoalmark/shoalmark.py --next` und
`docs/work-tracker/INDEX.md`. Wieder Dateien und Schritte zählen.

**6. Die Tafel.** `probe/docs/work-tracker/index.html` im Browser öffnen lassen — das ist die Sicht eures Owners.

## Der Bericht an den Owner

> Vorher: … Dateien / … Schritte für die fünf Fragen. Nachher: … / ….
> Was unsere vorhandene Dokumentation schon leistet: …
> Was shoalmark zusätzlich leistet — oder nicht: …
> Was eine Umstellung kosten würde (Pakete, offene Arbeit, Risiko mitten im Plan): …
> Unsere Empfehlung: übernehmen · später, an einer Paketgrenze · nicht übernehmen — weil …

## Falls der Owner Ja sagt

- **Ersetzen, nicht ergänzen.** Der Plan wandert in die Einträge; das alte Plandokument wird zum Verweis oder
  gelöscht. Zwei Quellen der Wahrheit sind der Fehler, den das Werkzeug verhindern soll.
- **An einer Paketgrenze umstellen,** nicht mitten in einem Paket.
- `--vendor tools/shoalmark`, `--init`, `--install-hook` im echten Verzeichnis. **Mit Subversion:** die
  Kommandozeile kennt keinen Client-Hook — vor jedem `svn commit` das Werkzeug laufen lassen und die `INDEX.md`
  mit einchecken; TortoiseSVN führt das Gate nach `--install-hook` selbst aus und fragt einmal um Erlaubnis.
- Rückweg: zuerst aus eurem Hook-Ordner (`.git/hooks/` oder dem, den `core.hooksPath` nennt) alles entfernen, was
  `tools/shoalmark/shoalmark.py` aufruft: die mit `# shoalmark` markierten Hooks und die Zeile, die ihr einem eigenen
  Hook hinzugefügt habt (unter Subversion die `tsvn:`-Hook-Properties). Löscht ihr das Werkzeug vorher, werden Commits
  abgelehnt. Dann `tools/shoalmark/`, `shoalmark.toml`, den shoalmark-Block in `AGENTS.md` und die Kopie im Git-Verzeichnis löschen
  (`shoalmark-trusted/`; das Verzeichnis nennt `git rev-parse --git-common-dir`). Der
  Tracker-Ordner kann bleiben: Seine Einträge sind einfaches Markdown.

## Anforderungen — eine Probe, keine Anweisung (Stufe 0: nur die Konvention)

Legt in `probe/` einen Ordner `requirements/` an (`requirements/README.md` auf `main` des Repositorys beschreibt ihn). Eine Anforderung ist
eine Tabellenzeile: `id` (stabil, nie neu vergeben), `shall` (ein Satz, das System als Subjekt, eine Pflicht), `source`
(wer oder was sie verlangt), `accept` (das Abnahmekriterium: was ein Test beobachtet). Ein Arbeitspaket nennt sie in einer Zeile unter dem
Kopf, `Satisfies: REQ-001` (im Kopf lehnt das Gate den Schlüssel ab), ein Test in seinem Namen. Eine Zeile ändert nur der Owner, mit einer signierten Antwort über die
Tafel, nie ein Agent. Bei einer Norm nennt die Zeile die Fundstelle (Norm, Ausgabe, Abschnitt) und leitet daraus einen
eigenen Satz ab; *Nicht anwendbar* ist eine signierte Antwort des Owners, mit Begründung. Der Normtext wird nicht kopiert,
und keiner schreibt, das Projekt erfülle die Norm: Ein Nachweis ist ein bestandener Test. Der Bericht nennt die Zahl der Zeilen, den Nachweis je Zeile und die Stelle, an der es hakte. Prüfungen gibt es noch nicht.

## Was nicht bewiesen ist

Dass TortoiseSVN die beiden Hook-Eigenschaften wie beschrieben ausführt, hat noch kein Mensch unter Windows
gesehen — nur die Kommandozeile ist in CI geprüft. Wenn es bei euch anders ist: das ist ein Befund, bitte meldet ihn.
