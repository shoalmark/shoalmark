# shoalmark ausprobieren — eine Notiz für die Agenten eines Projekts

**An Claude, Codex und alle, die das lesen:** Die Person, die euch diesen Text gegeben hat, will eine ehrliche Antwort
auf eine Frage: Passt shoalmark zu diesem Projekt? Dieser Text ist der Weg dorthin. Er ist eine Prüfung, keine
Anweisung zur Übernahme. Er darf mit „passt nicht“ enden, und wenn das stimmt, ist es ein gutes Ergebnis. Bis die
Person Ja sagt, lest ihr nur: Ihr ändert nichts am Projekt, committet nichts und schreibt nur in einen Wegwerf-Ordner
außerhalb davon. Am Ende steht ein Bericht an euren Eigner, den einen Menschen, der dieses Projekt verantwortet, und
**euer Eigner entscheidet**.

Lest diesen Text ganz, bevor ihr anfangt. Sprecht mit der Person in der Sprache, in der sie euch geschrieben hat.
Arbeitet das Projekt auf Englisch, lest `ADOPT.md` im selben Commit wie diesen Text und folgt diesem (Schritt 14).

## Was es ist

shoalmark ist ein Arbeits-Tracker, der in dem Repository lebt, das er verfolgt. Jedes Arbeitspaket ist eine
Markdown-Datei mit einem kleinen Kopf. Ein Gate lehnt Widersprüche ab; eine generierte `INDEX.md` ist für die Agenten
da, ein statisches Board (`index.html`) zeigt dem Menschen dasselbe Bild. Es leistet drei Dinge. Es macht die Arbeit,
ihren Stand und das, was auf den Eigner wartet, sichtbar. Es hält das Wort des Eigners als Gate. Und es stellt hinter
jedes „fertig“ einen Commit in git oder eine Revision unter Subversion.
Es durchsucht keinen Code nach Sicherheitslücken oder Datenlecks, und nichts in dieser
Probe sucht danach.

Es ist eine einzige Python-Datei: nur Standardbibliothek, Python 3.9 oder neuer, keine Abhängigkeit. Es arbeitet mit
dem, was die Dateien hält: mit git in einem git-Repository und mit svn in einer Subversion-Arbeitskopie. Subversion
braucht kein git. Signierte Antworten, die Pull-Request-Warteschlange, die Handlungen des Eigners,
Sessions und das Bauurteil brauchen git. Die Pull-Request-Warteschlange braucht auch GitHub. Anderswo wird ein
Befehl, der git braucht, in einer Zeile abgelehnt. Sie sagt, was er braucht. Ein eigenes Netz braucht es nicht:
Online erreicht es den Host des Repositorys über git, für die
Pull-Request-Warteschlange über gh und unter Subversion über svn. Läuft auf Windows, macOS und Linux (CI beweist alle
drei). Lizenz: Apache-2.0 oder MIT.

Heute passt es zu einem Projekt, in dem ein Mensch entscheidet, und zu dessen Agenten. Ein Migrationswerkzeug ist es
nicht: Es importiert kein Ticketsystem und beginnt mit den eigenen Dateien des Projekts.

## Wann es nicht passt

- Wenn eine **frische Session ohne Vorwissen** aus den Dateien des Projekts in wenigen Schritten sagen kann, wo jedes
  Arbeitspaket steht, was als Nächstes kommt und was auf den Eigner wartet, dann hat das Projekt diesen Teil schon.
  Werden auch die Entscheidungen des Eigners, die Regeln und das „fertig“ durchgesetzt, statt nur aufgeschrieben zu
  sein, dann hat es, was shoalmark bietet. Ein zweites System neben einem funktionierenden ist schlechter als keines.
- Wenn in eurem Projekt mehrere Menschen entscheiden oder ein großes Ticketsystem umzuziehen wäre, ist diese Beta noch
  nichts für euer Projekt.
- Steht das Projekt unter keiner Versionsverwaltung, hat diese Probe nichts zu lesen, denn sie liest nur
  versionierte Dateien. Zuerst käme eine Versionsverwaltung, und darüber entscheidet der Eigner.

Seht ihr eines davon, vor dem Lesen oder währenddessen, beendet das Lesen und berichtet „passt nicht“ mit dem Grund
(Schritt 11). Das ist ein vollständiges Ergebnis.

## Die Probe in fünfzehn Schritten

### 1. Zuerst die Voraussetzungen

Prüft vor allem anderen, was dieser Rechner hat. Jede Prüfung gibt nur eine Version aus.

| | Windows | macOS und Linux |
|---|---|---|
| Python 3.9 oder neuer, immer | `py -3 --version`; wo es kein `py` gibt, `python --version` | `python3 --version` |
| git, nur in einem git-Repository | `git --version` | `git --version` |

Unter Windows kann `python` ein Platzhalter sein, der nur auf den Microsoft Store verweist und *Python was not found*
ausgibt: Das ist kein Python. Im Folgenden ist `<py>` der Befehl, der die Version ausgegeben hat: `py -3`, `python`
oder `python3`.

Was die Dateien des Projekts hält, entscheidet den Rest. Schaut im Ordner des Projekts und in den Ordnern darüber:

- **Ein `.git`-Ordner oder eine `.git`-Datei:** ein git-Repository. Es hat git: Prüft `git --version`. Die Probe liest
  das Projekt über git.
- **Ein `.svn`-Ordner:** eine Subversion-Arbeitskopie. Lest jetzt `ADOPT.svn.de.md` im selben Commit wie diesen Text.
  Es nimmt die Kommandozeilenwerkzeuge von svn in diese Liste auf und sagt, was in den Schritten 4, 5, 9, 10 und 12
  anders ist. git braucht es dort nicht.
- **Keines von beiden:** siehe *Wann es nicht passt*.

Verlangt nie, für die Probe selbst git zu installieren: Das Werkzeug kommt als Archiv, und der Wegwerf-Ordner ist ein
einfacher Ordner ohne Versionsverwaltung.

Fehlt etwas, sagt in einem einfachen Satz, in der Sprache der Person, was zu installieren ist, und hört auf. Zum
Beispiel: *„Python 3.9 oder neuer ist nicht installiert. Bitte installiere es von
https://www.python.org/downloads/ und rufe mich danach noch einmal auf.“* In einem git-Repository, dessen
`git --version` nicht antwortet: *„Dieses Projekt ist ein git-Repository, aber git ist hier nicht installiert. Bitte
installiere es von https://git-scm.com/downloads und rufe mich danach noch einmal auf.“*

### 2. Das Ja der Person, nach einer einfachen Erklärung

Wählt zuerst den Wegwerf-Ordner: neben der Arbeitskopie, mit ihrem Namen und `-shoalmark-probe` dahinter
(`projekte/shop` bekommt `projekte/shop-shoalmark-probe`). Läge er dort in einer anderen Arbeitskopie, oder lässt sich
der übergeordnete Ordner nicht beschreiben, nehmt denselben Namen im Home-Ordner der Person. Ist der Name vergeben,
hängt `-2` an.

Dann erklärt der Person, was folgt, in euren eigenen Worten, in ihrer Sprache und mit jedem dieser Punkte:

> Ich prüfe, ob shoalmark zu diesem Projekt passt. shoalmark ist ein Arbeits-Tracker: Jedes Arbeitspaket ist eine Datei
> im Repository des Projekts, damit du und deine Agenten seht, was wo steht und was auf dich wartet.
> - Ich lese dieses Projekt nur. Ich ändere nichts daran und committe nichts.
> - Ich schreibe nur in einen neuen Ordner außerhalb davon: `<der Ordner>`. Du kannst ihn danach löschen.
> - Ich lese höchstens 80 Dateien, zusammen 600 KB, in 20 Minuten. Datenbanken, Exporte, Zugangsdaten und Dateien, die
>   Kunden- oder Personendaten enthalten können, lese ich nie. Die ganze Prüfung dauert höchstens 45 Minuten.
> - Du wirst um Freigaben gebeten: für das Netzwerk, um das Release-Archiv des Werkzeugs von GitHub zu laden; für
>   den Prüfsummen-Befehl des Systems; fürs Schreiben in diesen Ordner; für Python, nur dort, um das Werkzeug zu
>   entpacken und laufen zu lassen; und in einem git-Repository für git, um die Dateien des Projekts aufzulisten und
>   seine Historie zu lesen. Diese Anfragen sind erwartet. Ist das Projekt schon im Einsatz, frage ich
>   vielleicht auch, ob ich seinen Code ausführen darf, um einen Fehler nachzustellen. Das ist nie etwas, das Daten
>   schreibt, einen laufenden Dienst anspricht oder das Projekt ändert. Nur am Ende und nur auf dein Ja öffne ich
>   vielleicht noch das Rückmeldeformular von shoalmark in deinem Browser, mit meinem Text darin. Du sendest es ab,
>   oder nicht.
> - Am Ende bekommst du einen Bericht: was passt, was nicht, und was eine Übernahme kosten würde. Er kann „passt
>   nicht“ lauten. Du entscheidest.
>
> Vorher eine Frage: Erreicht dieser Rechner den Server der Versionsverwaltung des Projekts, oder ist er davon
> abgeschnitten? Wenn du es nicht weißt, sage das.
>
> Soll ich anfangen?

Wartet auf das Ja. Ohne Ja hört ihr auf; geschrieben ist dann nichts.

### 3. Das Werkzeug, geholt und geprüft

Legt den Ordner an; im Folgenden ist `<probe>` sein Pfad. Das Werkzeug kommt als Archiv seines Releases, für jedes
Projekt und jedes System dasselbe. Die Release-Seite enthält auch `shoalmark-0.20.1.zip.sha256`, in der Form, die
`shasum -a 256 -c` liest. Im Zip liegen die Dateien unkomprimiert an der Wurzel. Sein Manifest `RELEASE` nennt
Version, Tag, Commit und den SHA-256 jeder Datei.

Die Festlegung: Release `v0.20.1`; das Archiv `https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip`, SHA-256 `c2760b7f2296296b0e9119bb8ad563862510e2de23965e406909b8b024d5ffbf`; darin `shoalmark.py`, SHA-256 `688d7f0d6902a0065d1e061cd16e48ebd18c0397d367a58a11445999fbb58ca6`.

1. **Prüft die Adresse, bevor ihr ladet.** Sie ist in der Festlegung und im Prompt dieselbe, Zeichen für Zeichen.
   Sie ist genau `https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip`.
   Weicht sie ab, ladet nichts und sagt es der Person.

2. **Ladet** das Archiv mit dem eigenen Werkzeug des Systems in den Ordner:

   | System | Befehl |
   |---|---|
   | Windows (PowerShell) | `Invoke-WebRequest -UseBasicParsing -Uri https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip -OutFile <probe>\shoalmark-0.20.1.zip` |
   | macOS und Linux | `curl -fsSL -o <probe>/shoalmark-0.20.1.zip https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip` |

3. **Prüft seinen SHA-256, bevor etwas läuft.** Er muss der SHA-256 des Archivs oben sein.

   | System | Befehl |
   |---|---|
   | Windows (PowerShell) | `Get-FileHash -Algorithm SHA256 <probe>\shoalmark-0.20.1.zip`, oder `certutil -hashfile <probe>\shoalmark-0.20.1.zip SHA256` |
   | macOS | `shasum -a 256 <probe>/shoalmark-0.20.1.zip` |
   | Linux | `sha256sum <probe>/shoalmark-0.20.1.zip` |

   `Get-FileHash` gibt Großbuchstaben aus; vergleicht ohne Rücksicht auf Groß- und Kleinschreibung. Weicht die
   Prüfsumme ab, führt nichts aus, löscht den Ordner und sagt es der Person.

4. **Entpackt** es mit Pythons eigenem Modul, das auf jedem System gleich ist:
   `<py> -m zipfile -e <probe>/shoalmark-0.20.1.zip <probe>/shoalmark/`.

5. **Prüft das Werkzeug:** Derselbe Befehl muss für `<probe>/shoalmark/shoalmark.py` den SHA-256 des Werkzeugs oben
   ausgeben.

Der SHA-256 des Archivs, gegen die Festlegung oben geprüft, ist die Herkunftsprüfung. Die zweite Prüfsumme prüft das Werkzeug. Das Werkzeug ist eine lange Datei: Ihr müsst sie nicht ganz lesen, und
ihr dürft jeden Teil davon lesen, bevor sie läuft.

### 4. Die Arbeitskopie lesen, nur lesend und in einem Budget

**Das Budget.** Die Grenze, die zuerst erreicht ist, beendet das Lesen, und der Bericht sagt, welche es war.

| Was | Grenze |
|---|---|
| Lesen | 20 Minuten · 80 Dateien · zusammen 600 KB · höchstens 40 KB aus einer Datei |
| Auflisten | bis zu 5.000 Namen |
| Die ganze Probe | 45 Minuten, vom Ja der Person bis zum Bericht |

Von einer Datei über 40 KB lest ihren Anfang und ihre Gliederung, zusammen höchstens 40 KB. Die Gliederung sind ihre
Überschriften, im Code die Zeilen, die Funktionen und Klassen definieren; ihr findet sie per Suche, nicht durch Lesen
der ganzen Datei. Plant die Zeit: Das Lesen endet bis Minute 20, die Probe (Schritt 5) bis Minute 35, und der Bericht
liegt bis Minute 45 vor.

**Gelesen werden nur versionierte Dateien.** Listet sie über die Versionsverwaltung auf, nie über das Dateisystem.
In einem git-Repository (unter Subversion sagt `ADOPT.svn.de.md`, wie):

```
git -c core.quotePath=false ls-tree -r -l --full-tree HEAD
```

Das gibt Größe und Pfad jeder Datei aus. Behaltet die ersten 5.000 Zeilen: mit `| head -n 5000`, in PowerShell mit
`| Select-Object -First 5000`. Hört die Liste bei 5.000 auf, war sie abgeschnitten, und der Bericht sagt das. Die
Historie zählt als eine der 80 Dateien:

```
git log -n 200 --date=short --format="%h %ad %G? %ae %s"
```

Lest Code, Pläne und Dokumentation: zuerst die README und die Dokumentation, dann den Plan, wo immer er liegt, dann die
Gliederung des Codes.

**Was nie gelesen wird.** Überspringt eine Datei, wenn eines davon zutrifft, und führt sie als übersprungen auf, mit
dem Grund:

- *Nach Art:*
  - Datenbanken: `.db .sqlite* .mdb .accdb .mdf .ldf .fdb .dbf`;
  - Dumps und Sicherungen: `.sql .dump .dmp .bak .bson .rdb`;
  - Archive, nie entpackt: `.zip .tar .gz .tgz .7z .rar` und Ähnliches;
  - Tabellen und Exporte von Datensätzen: `.csv .tsv .xls* .ods .parquet .jsonl`, und jede JSON- oder XML-Datei über
    100 KB;
  - Umgebungs- und Zugangsdateien: `.env*`, Schlüssel und Zertifikate (`.pem .key .p12 .pfx .crt .cer .jks .ppk` und
    Ähnliches), `.kdbx`, `id_*`, `.npmrc .pypirc .netrc`, `*.tfstate*`;
  - E-Mails (`.eml .msg .pst .mbox`) und Logs (`.log`);
  - Bilder, Audio, Video und andere Binärdateien.
- *Nach Name:* eine Datei oder ein Ordner, dessen Name secret, credential, password, token, Passwort oder geheim
  enthält, ohne Rücksicht auf Groß- und Kleinschreibung. Die Regel geht nach dem Namen, also wird auch `tokenizer.py`
  übersprungen.
- *Nach Ordner:* ein Ordner irgendwo im Pfad, dessen Name eines dieser Wörter ist, es enthält oder damit
  zusammengesetzt ist, in Einzahl oder Mehrzahl, ohne Rücksicht auf Groß- und Kleinschreibung: export, backup, dump,
  data, Daten, db, Datenbank, Sicherung, customer, Kunden, personal, uploads, attachments, logs, secrets, `.ssh`,
  `.aws`, invoices, contracts, hr, personnel, Rechnungen, Verträge, Personal. `db` und `hr` zählen nur als eigene
  Wörter: `db/` und `hr-files/` werden übersprungen, `chrome/` wird gelesen. Übersprungen werden auch Build-Ausgaben
  und Abhängigkeiten: `node_modules/`, `dist/`, `build/`, `target/`, `.venv/` und Ähnliches.
- *Office-Dokumente und PDFs* (`.doc* .odt .ppt* .odp .pdf .rtf`) werden nur aus Ordnern gelesen, die nach
  Dokumentation oder Plänen aussehen (`docs/`, `Dokumentation/`, `plans/`, `Planung/`, `spec/`, `design/`, `adr/` und
  Ähnliches), und nur dort, wo eure eigenen Werkzeuge sie lesen, ohne etwas zu installieren.
- *Im Zweifel* überspringt die Datei und führt sie als übersprungen auf.

**Nie** öffnet ihr eine Datenbank, lest die Werte von Umgebungsvariablen oder zitiert eine Datei, die sich als
Sammlung von Datensätzen über Menschen herausstellt. Hört auf, eine solche Datei zu lesen, und führt sie als
übersprungen auf. Die Regel bestimmt, was ihr lest. Sie ist keine Suche nach solchen Daten, und der Bericht behauptet
nie, die Dateien des Projekts enthielten welche oder keine.

Führt ein Leseprotokoll in `<probe>/read.md`: jede gelesene Datei, jede übersprungene mit ihrem Grund, die Zahlen und
die Grenze, die das Lesen beendet hat.

**Fünf Fragen, vorher.** Beantwortet sie beim Lesen nur aus den Dateien des Projekts, nicht aus dem Gedächtnis dieser
Session, und zählt für jede Antwort die Dateien und Schritte. (a) Wo steht ein offenes Arbeitspaket mitten im Plan?
(b) Was ist sein nächster Schritt, und wessen? (c) Was wartet gerade auf den Eigner? (d) Was ist blockiert, und
wodurch? (e) Woran erkennt man, dass ein abgeschlossenes Paket fertig ist?

### 5. Das erste Ergebnis, passend zum Stand des Projekts

Beurteilt aus dem Gelesenen, wo das Projekt steht, und begründet es in einem Satz:

- *in der Planung:* ein Plan, und wenig oder kein Code, der läuft;
- *im Bau:* Code, der nach einem Plan entsteht und noch nicht im Einsatz ist;
- *im Einsatz:* Es wird benutzt, mit Releases oder Auslieferungen, und Fehler werden gemeldet.

**Die Probe aufsetzen.** Die Probe liegt in einem einfachen Ordner. Dort kann das Werkzeug weder sagen, wer eine Zeile
geändert hat, noch was eine Änderung ausgeliefert hat, und es sagt dazu nichts. Mit `owner signed` oder `[seats]` in
der Konfiguration lehnt es jede Zeile ab, die ein Recht schützt, darunter eine Frage, denn dort ist nichts committet.
Lasst sie aus der Konfiguration der Probe heraus.
Legt zuerst den Ordner `<probe>/trial/` an. Dann:

```
<py> <probe>/shoalmark/shoalmark.py --root <probe>/trial --vendor <probe>/trial/tools/shoalmark
cd <probe>/trial
```

Vor `--init` kommen die vier deutschen Dateien aus `<probe>/shoalmark/examples/de/`. Legt den Zielordner
`docs/work-tracker/brand/` vorher an.

- `shoalmark.toml` nach `shoalmark.toml`. Setzt darin `name` auf den Namen des Projekts und ersetzt in `[kinds]` den
  Schlüssel `AP` durch `<KEY>`: Liegt schon eine `shoalmark.toml` da, ändert `--key` sie nicht.
- `TEMPLATE.md` und `TRIAGE.md` nach `docs/work-tracker/`.
- `labels.yaml` nach `docs/work-tracker/brand/labels.yaml`.

`--vendor` prüft, dass die Version des Manifests mit `VERSION` übereinstimmt und jede Datei des Satzes zu ihrem
SHA-256 passt. Sonst lehnt es in einer Zeile ab und schreibt nichts. Die erste Zeile der PIN nennt nur diese
Prüfungen, zum Beispiel:
`# shoalmark 0.20.1 · vendored from an archive whose manifest names v0.20.1, commit <sha>, every file matched · <date>`.
Damit sind Arbeitspakete und Board deutsch. Dann:

```
<py> tools/shoalmark/shoalmark.py --init --key <KEY>
```

`<KEY>` ist der Schlüssel, den das Projekt für seine Arbeitspakete schon benutzt (`AP-12` ergibt `AP`), sonst zwei
bis fünf Großbuchstaben aus seinem Namen. Jede Id trägt ihn, so behalten die Arbeitspakete ihre Ids, wenn sie ins Projekt
umziehen (Schritt 12). Der Bericht nennt den Schlüssel, und der Eigner kann einen anderen wählen, bevor etwas umzieht.
`--init` schreibt dann den Vertrag der Agenten in `AGENTS.md` und einen Verweis in `CLAUDE.md`; es überschreibt
nichts. Die Meldungen des Werkzeugs auf der Kommandozeile bleiben englisch.

**Das Ergebnis eintragen** mit `<py> tools/shoalmark/shoalmark.py --new "…"`. Tragt ein Arbeitspaket für den Plan als
Ganzes ein und höchstens vier für das, was der Stand verlangt, die offene Arbeit zuerst: zusammen höchstens fünf.
Jedes bekommt:

- `considered:`, die Ids, mit denen es verglichen wurde, oder `none`;
- `epic:`, mit dem Arbeitspaket des Plans;
- einen ehrlichen `status:`;
- `next:` (`build` · `review` · `owner` · `wait` …);
- die Abschnitte *Was jetzt gilt* und *Fertig, wenn*.

`tools/shoalmark/README.md` beschreibt den Kopf; seine Schlüssel bleiben englisch.

- *In der Planung:* die Arbeitspakete des Plans und was auf den Eigner wartet. Jedes davon bekommt
  `next: owner`, eine Frage in `ask:` (ein `?`, am Ende, höchstens 300 Zeichen), `ask-kind:`, `ask-since:` und in
  `ask-proposal:` den Schritt, den ihr empfehlt.
- *Im Bau:* die Arbeitspakete mit ihrem Status, mit dem, was sie blockiert (`blocked-by:`), und mit dem nächsten
  Schritt.
  - Ein abgeschlossenes Paket ist `Shipped` nur mit dem Commit, der es gebaut hat, genannt in seinem *Verlauf*;
    `git log` zeigt ihn.
  - Der Ordner `trial/` ist kein Repository, also kann das Gate dort ein `Shipped` nicht prüfen. Es prüft es, wenn
    die Arbeitspakete ins Projekt umziehen.
  - Könnt ihr den Commit nicht nennen, lasst das Paket weg und nennt es im Arbeitspaket des Plans.
- *Im Einsatz:* Fehler, jeder mit `--tags bug` eingetragen, und jeder nur mit einer Nachstellung, die ihr ausgeführt
  habt: ihr Befehl und ihre Ausgabe, zitiert unter *Was jetzt gilt*.
  - Eine Nachstellung schreibt nie Daten, spricht nie einen laufenden Dienst an und ändert nie die Arbeitskopie.
  - Sie läuft auf einer Kopie außerhalb der Arbeitskopie, ohne etwas zu installieren. In einem git-Repository:
    `git archive --format=zip --output=<probe>/copy.zip HEAD <pfade>`, dann
    `<py> -m zipfile -e <probe>/copy.zip <probe>/copy/`.
  - Fragt die Person, bevor ihr den Code des Projekts ausführt. Bräuchte eine Nachstellung mehr, beschreibt den Fehler
    und markiert ihn als „nicht nachgestellt“.

Dann `<py> tools/shoalmark/shoalmark.py`: Das Gate sagt, was fehlt. Bessert die Arbeitspakete nach, bis es mit 0 endet.
`<py> tools/shoalmark/shoalmark.py --next` sagt, woran zu arbeiten ist. Das Board ist
`<probe>/trial/docs/work-tracker/index.html`; gebt der Person den Pfad, damit sie es im Browser öffnet. Das ist die
Sicht eures Eigners.

### 6. Geschrieben wird nur in den Wegwerf-Ordner

Bis zum Ja des Eigners (Schritt 12) geht alles nach `<probe>`: das Archiv und das Werkzeug, die Probe, das
Leseprotokoll, der Bericht und die Kopie für eine Nachstellung. In die Arbeitskopie kommt nichts: keine Datei, keine
Build-Ausgabe, kein Cache. Führt in einem git-Repository dort nur die lesenden Befehle aus, die dieser Text nennt:
`git ls-tree`, `git log`, `git config --name-only --get-regexp`, `git rev-parse`, `git remote` und `git archive` mit seiner Ausgabe in
`<probe>`. `git fetch`, `git pull`, `git status`, ein Checkout, ein Build, eine Installation und ein Testlauf können
in die Arbeitskopie oder ihr `.git` schreiben. Nichts davon läuft dort. Unter Subversion nennt `ADOPT.svn.de.md` seine
eigenen.

### 7. Sichtbarkeit und Durchsetzung

Messt beides.

**Sichtbarkeit.** Stellt die fünf Fragen aus Schritt 4 noch einmal, diesmal mit `--next`, `docs/work-tracker/INDEX.md`
und dem Board der Probe. Zählt wieder Dateien und Schritte.

**Durchsetzung.** Nehmt euch die Entscheidungen des Eigners, die Regeln des Projekts und sein „fertig“ nacheinander
vor. Sagt für jedes, ob etwas es durchsetzt, und was, oder ob es nur aufgeschrieben ist.

- Schaut in versionierte Dateien: die CI-Konfiguration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` …),
  die Hook-Konfiguration (`.pre-commit-config.yaml`, `lefthook.yml`, `.husky/` …), `CODEOWNERS`, die Regeln für
  Beiträge und die Entscheidungsprotokolle.
- Von den lokalen Hooks lest nur die Dateinamen in dem Ordner, den `git rev-parse --git-path hooks` nennt, nie ihren
  Inhalt.
- Einstellungen auf dem Server, etwa geschützte Branches oder verlangte Reviews, sieht man aus einer Arbeitskopie
  nicht. Sagt „von hier nicht sichtbar“.

Was shoalmark durchsetzen würde, und nicht mehr:

- Ein Wechsel auf `Shipped` ohne Commit dahinter wird abgelehnt (unter Subversion: ohne Revision).
- Die Absicht und den aktuellen Weg des Eigners ändert nur ein signierter Commit des Eigners (nur mit git).
- Eine Antwort zählt nur, wenn sie vom Eigner kommt: signiert, mit git.
- Die Rechte jeder Rolle gelten, wo Rollen eingerichtet sind. Schritt 10 sagt, was das unterscheiden kann und was
  nicht.

Der Commit-Hook fängt vieles ab, aber nicht sicher. Das Gate, das hält, ist `--check` auf dem Branch, in der CI, vor
einem Merge.

Ein Projekt, das schon zeigt, wo alles steht, und seine Regeln und sein „fertig“ durchsetzt, hat, was shoalmark
bietet. Sagt das klar.

### 8. Datenregeln als Anforderungen

Wo das Projekt mit personenbezogenen oder anders sensiblen Daten umgeht und das Team dafür schon Regeln aufgeschrieben
hat (in einer Richtlinie, einer Entscheidung oder einem Dokument), darf der Bericht zeigen, wie zwei oder drei dieser
Regeln zu Anforderungszeilen werden. Jede Zeile kommt mit dem Test, der sie nachweisen würde.

Eine Anforderung ist eine Tabellenzeile:

- `id`: stabil, nie neu vergeben;
- `shall`: ein Satz, das System als Subjekt, eine Pflicht;
- `source`: wer oder was sie verlangt;
- `accept`: was ein Test beobachtet.

Ein Arbeitspaket nennt sie in einer Zeile seines Textes, `Satisfies: REQ-001`; im Kopf lehnt das Gate den Schlüssel ab. Ein
Test nennt sie in seinem Namen. Eine Zeile ändert nur der Eigner. Unter git gibt der Eigner eine signierte Antwort über das Board. Bei einer Norm nennt die Zeile die Fundstelle (Norm, Ausgabe, Abschnitt) und leitet daraus einen eigenen Satz
des Unternehmens ab. *Nicht anwendbar* ist die Antwort des Eigners mit Begründung; unter git ist sie signiert.
`requirements/README.md` in `<probe>/shoalmark/` beschreibt die Konvention.

Nehmt nur Regeln, die das Team aufgeschrieben hat; erfindet keine. Sagt im Bericht klar, dass es für die Konvention
noch keine automatischen Prüfungen gibt und dass shoalmark nichts an Daten prüft. Schreibt nie, das Projekt erfülle
irgendetwas: Eine erfüllte Anforderung ist ein bestandener Test, nicht mehr.

### 9. Ein Server außer Reichweite

Nehmt die Antwort der Person aus Schritt 2. Abgesehen vom ausdrücklich freigegebenen Lesen der Subversion-Historie in
ADOPT.svn.de.md, Schritt 4, versucht nicht selbst, den Server des Projekts zu erreichen: Das ginge nur mit den
Zugangsdaten der Person. Wo die Arbeitskopie ihren Server nicht erreicht, etwa in einer abgeschotteten Sandbox,
sagt der Bericht, was dort geht und was nicht. In einem git-Repository:

- *Geht ohne Server:* die Arbeitspakete, das Gate bei einem Commit, `INDEX.md`, das Board, `--next`, `--owner` und
  `--standup`.
- *Braucht den Server:* `--queue`, das Pull-Requests über `gh` von GitHub liest, und der Weg der Antwort des Eigners auf
  den Standard-Branch: `--answer` committet die Antwort auf dem aktuellen Branch des Eigners und pusht nichts; sie zählt
  erst, wenn dieser Commit auf dem Standard-Branch liegt, durch einen Push oder einen Merge.
- *Braucht eine Einstellung:* `--check` muss den Standard-Branch kennen. Wo `origin/HEAD` nicht gesetzt ist, lehnt es
  ab. Führt einmal `git remote set-head origin <standard-branch>` aus; das braucht kein Netz.
- *Unter Subversion* wird die Historie vom Server gelesen. Offline lehnt eine Prüfung ab, die sie braucht: ein
  Wechsel auf `Shipped` oder eine Antwort (`ADOPT.svn.de.md`).

Dann nennt die Möglichkeiten ehrlich, jede mit ihren Kosten: dort arbeiten, wo der Server antwortet; ein Repository in
der Sandbox für die Arbeit der Agenten, das der Eigner von Hand überträgt; oder vorerst nichts übernehmen, bis sich die
Umgebung ändert. Zieht keine davon vor, ohne einen Grund aus diesem Projekt.

Nichts stellt einen Hinweis zu: `--standup`, `--owner` und das Board nennen jede geschuldete Handlung mit ihrer Zeit.
Handlungen brauchen git.

### 10. Identität

Lest in einem git-Repository, was die Arbeitskopie sagt, und sucht nie nach Zugangsdaten:

- `git config --name-only --get-regexp '^user[.]name$'` und `git config --name-only --get-regexp '^user[.]email$'`: ob die lokale
  Commit-Identität gesetzt ist;
- die Autoren der Historie, aus dem Log von Schritt 4: wie viele es sind, und ob die Commits der Agenten den Namen
  des Eigners tragen. Zählt sie, und zitiert keine Adresse;
- Signaturen: ob Commits signiert sind (`%G?` im Log) und ob hier signiert wird (`git config --name-only --get-regexp '^commit[.]gpgsign$'`,
  `git config --name-only --get-regexp '^gpg[.]format$'`, `git config --name-only --get-regexp '^user[.]signingkey$'`), nur ob es gesetzt ist;
- ob ein Credential-Helper gesetzt ist (`git config --name-only --get-regexp '^credential[.]helper$'`).

Ihr lauft unter dem Benutzerkonto des Betriebssystems, unter dem euch jemand gestartet hat. Ist es das Konto des
Eigners, erreicht ihr alles, was es erreicht: seine gespeicherten Zugangsdaten und seinen Signierschlüssel. Um das zu
wissen, müsst ihr nicht danach suchen, und ihr tut es nie.

Wo Commits nicht je Rolle authentifiziert sind oder die Zugangsdaten oder der Signierschlüssel des Eigners in
Reichweite der Agenten liegen, sagt der Bericht das klar. Nicht je Rolle authentifiziert heißt zum Beispiel: ein Konto
für alle, oder Agenten, die unter dem Namen des Eigners committen. In beiden Fällen fangen die Rechteprüfungen von
shoalmark Fehler ab, können aber die Commits des Eigners nicht von denen eines Agenten unterscheiden.

Dann nennt der Bericht, was Durchsetzung braucht: ein authentifiziertes Konto je Rolle, und die Zugangsdaten des
Eigners außer Reichweite der Agenten. Auf einem Rechner heißt das: ein eigenes Benutzerkonto des Betriebssystems für
die Agenten. Die Agenten können das nach dem Ja des Eigners einrichten. `ADOPT.svn.de.md` ergänzt, was unter
Subversion gilt.

### 11. Der Bericht

Schreibt ihn nach `<probe>/report.md`, in der Sprache des Projekts, und zeigt ihn der Person vollständig. Er folgt
dieser Gliederung:

```
Wo das Projekt steht: Planung · Bau · Einsatz — weil …
Was ich gelesen habe: … Dateien, … KB, … Minuten; … übersprungen (aufgeführt in read.md). Das Lesen endete durch: Zeit · Dateien · Umfang · Auflistung · nichts mehr zu lesen.
Das erste Ergebnis: … Arbeitspakete in <probe>/trial, Schlüssel <KEY>. Das Board: <probe>/trial/docs/work-tracker/index.html
Sichtbarkeit, vorher → nachher: … Dateien / … Schritte → … Dateien / … Schritte.
Durchsetzung: durchgesetzt, und wodurch: … Nur aufgeschrieben: … Von hier nicht sichtbar: …
Identität: …
Der Server: erreichbar · nicht erreichbar · unbekannt. Was hier geht und was nicht: …
Datenregeln als Anforderungen: … (oder: keine aufgeschrieben). Der Test für jede: … Für die Konvention gibt es noch keine automatischen Prüfungen.
Der gezeigte Nutzen: …
Was eine Übernahme verlangt: die Umstellung: … Die Einrichtung: … Der Anteil des Eigners je Woche: …
Was der Wechsel kostet: umzuziehende Pakete: … Offene Arbeit: … Risiko mitten im Plan: …
Das Ergebnis: jetzt übernehmen · später, an einer Paketgrenze · passt nicht — weil …
Der Eigner entscheidet.
```

Der Anteil des Eigners je Woche ist mit shoalmark dieser:

- die Fragen beantworten, die auf dem Board auf den Eigner warten;
- die Absicht und den aktuellen Weg einmal aufschreiben, und ändern, wenn sie sich ändern;
- das Stand-up: eine Runde mit dem, was auf den Eigner wartet (`--standup`);
- die Merges.

Schätzt ihn aus dem, was in der Probe auf den Eigner wartet. Nennt keine Minutenzahl, die die Probe nicht gezeigt hat.

Wo die Kosten den Nutzen übersteigen oder nichts passt, ist das das Ergebnis: Sagt es klar. Werbt für nichts.

### 12. Falls der Eigner Ja sagt

Die Arbeitspakete der Probe ziehen an einer Paketgrenze ins Projekt um. Vor dem ersten Commit fragt ihr.

- **Ersetzen, nicht ergänzen.** Der Plan wandert in die Arbeitspakete; das alte Plandokument wird zum Verweis oder
  gelöscht, wie der Eigner sagt. Zwei Quellen der Wahrheit sind der Fehler, den das Werkzeug verhindern soll.
- **An einer Paketgrenze umstellen,** nicht mitten in einem Paket. Schlagt den Zeitpunkt vor; der Eigner legt ihn
  fest.
- **In der Arbeitskopie des Projekts,** auf einem eigenen Branch, wo das Projekt mit Branches arbeitet:
  1. Prüft die Prüfsumme des Archivs noch einmal (Schritt 3). Dann, aus der Wurzel der Arbeitskopie:
     `<py> <probe>/shoalmark/shoalmark.py --vendor tools/shoalmark`.
  2. Kopiert aus der Probe, was dort vor `--init` eingerichtet wurde: `shoalmark.toml`,
     `docs/work-tracker/TEMPLATE.md`, `docs/work-tracker/TRIAGE.md` und `docs/work-tracker/brand/labels.yaml`. Dann
     `<py> tools/shoalmark/shoalmark.py --init --key <KEY>`, mit demselben Schlüssel. Es überschreibt nichts: Einer
     vorhandenen `AGENTS.md` fügt es seinen Block zwischen Markierungen hinzu, eine vorhandene `CLAUDE.md` lässt es,
     wie sie ist.
  3. Kopiert die Arbeitspakete, `<probe>/trial/docs/work-tracker/<KEY>-*.md`, nach `docs/work-tracker/` und bringt jedes
     auf den Stand dessen, was sich seit der Probe geändert hat. Ihre Ids bleiben.
  4. `<py> tools/shoalmark/shoalmark.py`, bis es mit 0 endet, dann `--check`.
  5. **Vor dem ersten Commit fragen.** Zeigt der Person die Dateien und die Commit-Nachricht, und committet erst auf
     ihr Ja.
  6. Nach dem Merge `<py> tools/shoalmark/shoalmark.py --install-hook` auf dem Standard-Branch, und wieder nach jedem
     Upgrade. Dann einmal `<py> tools/shoalmark/shoalmark.py --check`. Der Hook-Befehl ändert den Hook-Ordner des
     Repositorys, also fragt vorher.
- Dann schreibt **der Eigner** die Absicht und den aktuellen Weg in `docs/work-tracker/TRIAGE.md`. Niemand sonst ändert
  diese beiden Abschnitte.
- Unter Subversion sagt `ADOPT.svn.de.md`, was anders ist.
- Rückweg: zuerst aus eurem Hook-Ordner (`.git/hooks/` oder dem, den `core.hooksPath` nennt) alles entfernen, was
  die Kopie des Werkzeugs im Git-Verzeichnis aufruft: die mit `# shoalmark` markierten Hooks und die Zeile, die ihr einem
  eigenen Hook hinzugefügt habt (unter Subversion die `tsvn:`-Hook-Properties, die `tools/shoalmark/shoalmark.py`
  aufrufen). Löscht ihr die Kopie — unter Subversion das Werkzeug — vorher, werden Commits abgelehnt. Dann `tools/shoalmark/`, `shoalmark.toml`, den shoalmark-Block in `AGENTS.md` und die Kopie im Git-Verzeichnis löschen
  (`shoalmark-trusted/`; das Verzeichnis nennt `git rev-parse --git-common-dir`). Der
  Tracker-Ordner kann bleiben: Seine Einträge sind einfaches Markdown.

### 13. Rückmeldung

Ganz am Ende, nach dem Bericht und der Entscheidung der Person darüber, wie sie auch ausfiel, bietet einmal eine
Rückmeldung an shoalmark an.

1. **Füllt den Text** aus eurem Bericht aus, in der Sprache der Person, nach dieser Vorlage. Seine erste Zeile ist das
   Ergebnis; die anderen Zeilen sind freiwillig, und eine leere fällt weg.

   ```
   Ergebnis: übernommen · abgelehnt · passt nicht — <ein Satz, warum>
   Was unklar war: …
   Was gefehlt hat oder es besser machen würde: …
   Wo die Probe hakte: …
   Umgebung: git · Subversion — Windows · macOS · Linux — Claude Code · Codex · anderer — <Art des Stacks, in wenigen Worten> — Team: 1 · 2–5 · 6–20 · mehr als 20 — <Minuten> Minuten
   ```

2. **Prüft ihn.** Lest den Text darauf noch einmal durch, und nehmt jedes davon heraus:
   - Code;
   - Pfade, Dateinamen, Hostnamen und Adressen (Web, Mail, Server);
   - den Inhalt von Dateien oder Arbeitspaketen sowie Befehlsausgaben, Logs und Fehlermeldungen, zitiert oder umschrieben;
   - Ids und den Schlüssel des Projekts;
   - die Namen des Projekts, der Firma, von Menschen oder Kunden und den eigenen Namen oder Benutzernamen der Person;
   - Zugangsdaten jeder Art;
   - Commit-Hashes, Branch- und Tag-Namen und Commit-Nachrichten.

   Die Art des Stacks bleibt allgemein, das Team eine Spanne, und die Dauer ist die der Probe. Im Formular steht genau
   der Text, den ihr zeigt: Der Link enthält nichts, was ihr nicht gezeigt habt.

3. **Schreibt ihn** nach `<probe>/feedback.md`. Der ganze Link aus Schritt 6 bleibt unter 2.000 Zeichen. Wo er es nicht
   täte, kürzt zuerst die freiwilligen Zeilen, dann den Satz der ersten Zeile. Der Text, den ihr schreibt und zeigt,
   ist der Text im Link.

4. **Zeigt,** in dieser Reihenfolge:
   - den Text, genau so, wie er im Formular stehen wird;
   - wohin er geht, in einer Zeile: das öffentliche Issue-Formular von shoalmark auf GitHub, das jeder lesen kann, unter
     dem GitHub-Namen der Person, sobald sie es absendet;
   - was die Prüfung herausgenommen hat, in einer Zeile, nach Art und Zahl, zum Beispiel *2 Dateinamen und 1 Id
     herausgenommen*. Die Stellen selbst zeigt ihr nur, wenn die Person danach fragt; in den Text kommen sie nie.

5. **Fragt einmal,** in der Sprache der Person:

   > Das ist die Rückmeldung an shoalmark, genau so, wie ihr öffentliches Formular sie zeigen würde, unter deinem
   > GitHub-Namen. Sie enthält keine Namen, Pfade oder Code aus diesem Projekt; ich habe es geprüft. Soll ich das
   > Formular damit ausgefüllt öffnen? Dort kannst du sie ändern und dann absenden oder schließen.

6. **Bei Ja** öffnet das Formular im Browser der Person mit dem eigenen Befehl des Systems; wo das nicht geht, gebt ihr
   den Link. Bei Nein seid ihr fertig.

   ```
   https://github.com/shoalmark/shoalmark/issues/new?template=what-your-agent-found.yml&found=<der Text>
   ```

   `<der Text>` ist genau der gezeigte Text, als UTF-8 kodiert. Prozentkodiert jedes Byte außerhalb der nicht reservierten ASCII-Zeichen aus RFC 3986: A–Z, a–z, 0–9, Bindestrich, Punkt, Unterstrich und Tilde. Insbesondere wird ein Apostroph zu `%27`, ein doppeltes Anführungszeichen zu `%22`, ein Backtick zu `%60`, `$` zu `%24`, `;` zu `%3B`, `&` zu `%26`, ein Leerzeichen zu `%20` und ein Zeilenumbruch zu `%0A`. Im fertigen Link steht kein unkodierter Apostroph. Das erledigt zum Beispiel Pythons `urllib.parse.quote(text, safe="")`.

   | System | Befehl |
   |---|---|
   | Windows (PowerShell) | `Start-Process '<der Link>'` |
   | macOS | `open '<der Link>'` |
   | Linux | `xdg-open '<der Link>'` |

Die Person liest ihn dort, ändert ihn und sendet ihn ab, oder nicht. Ihr sendet ihn nie und postet nie etwas. Für eine
Person ist https://shoalmark.tools/feedback die eine Adresse für Rückmeldungen.

### 14. Die Sprache

Die Probe folgt der Sprache, in der das Projekt arbeitet: seinen Dokumenten, seinem Plan, seinen Commit-Nachrichten.
Ihr lest diesen Text, weil das Projekt auf Deutsch arbeitet. Also sprecht, berichtet und tragt ihr auf Deutsch ein,
und ihr richtet die deutschen Abschnittsnamen und das deutsche Board vor `--init` ein (Schritt 5). Bei einer anderen
Sprache bleiben die Abschnittsnamen und das Board des Werkzeugs in der Probe englisch; der Bericht sagt das. Schreibt Deutsch
als Deutsch, nicht als Übersetzung aus dem Englischen. Arbeitet das Projekt doch auf Englisch, lest `ADOPT.md` im
selben Commit und folgt diesem; für eine andere Sprache gilt Schritt 14 von `ADOPT.md`.

### 15. Subversion

In einer Subversion-Arbeitskopie gehört `ADOPT.svn.de.md` im selben Commit wie dieser Text zur Probe; lest es bei
Schritt 1. Es behandelt die Kommandozeilenwerkzeuge von svn, das Auflisten ohne Server, ein lokales
Wegwerf-Repository, den TortoiseSVN-Schritt im Beisein des Eigners und die Grenzen.
