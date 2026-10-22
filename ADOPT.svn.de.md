# shoalmark unter Subversion ausprobieren — der Teil für eine Subversion-Arbeitskopie

Lest das nur in einer Subversion-Arbeitskopie: Schritt 1 von `ADOPT.de.md` schickt euch hierher. Es gehört zu
`ADOPT.de.md` im selben Commit. Folgt dessen fünfzehn Schritten, und wo unten ein Schritt genannt ist, tut zusätzlich,
was dort steht, oder stattdessen, wo es das sagt.

## Was unter Subversion gilt

shoalmark ist mit git und GitHub gebaut und erprobt. Subversion besteht die Test-Suite, ist in echter Arbeit aber noch
nicht erprobt: Es gilt ohne Gewähr, und der Bericht sagt das.

- shoalmark braucht unter Subversion kein git. Es kommt als Archiv seines Releases (`ADOPT.de.md`, Schritt 3) und
  liest die Arbeitskopie über svn. Verlangt hier nie, git zu installieren.
- Signierte Antworten, die Pull-Request-Warteschlange, Antwort-Branches und Handlungen, Sessions und das Bauurteil
  brauchen git. Die Warteschlange braucht auch GitHub. Ein solcher Befehl wird hier in einer Zeile abgelehnt. Sie
  nennt, was er braucht. `--session new` gibt hier trotzdem eine Id aus, ohne die Prüfung gegen die Commit-Trailer
  von git, die zeigt, dass sie unbenutzt ist.
- Es liest seine Historie über svn vom Server. Eine Prüfung, die die Historie braucht, etwa ein Wechsel auf `Shipped`
  oder eine Antwort, lehnt ab, wo der Server nicht erreichbar ist. Ungelesen lässt sie eine solche Änderung nie durch.
- Die svn-Kommandozeile führt keinen Hook aus: Subversion hat auf dem Client keine. Lasst das Werkzeug vor jedem
  `svn commit` laufen und checkt die `INDEX.md`, die es schreibt, mit ein. Erst `--check` nach dem Commit beurteilt
  ihn.
- TortoiseSVN führt das Gate selbst aus, über zwei Hook-Properties, die `--install-hook` setzt. Vor dem ersten Lauf
  fragt es einmal um Erlaubnis.
- Auf dem Server gibt es kein Gate. Ein Commit von der Kommandozeile oder von einem Client ohne Hook kommt ins
  Repository; `--check` danach zeigt, was er verletzt hat.
- Die Identität ist das Server-Konto. Signierte Antworten brauchen git, also sind die Absicht und der aktuelle Weg des
  Owners unter Subversion nicht geschützt: Nichts in einer Arbeitskopie kann den Commit des Owners von dem eines
  Sitzes unterscheiden.
- Nach `svn update` baut nichts die Tafel neu: Führt `--html-only` aus.

## Schritt 1: eine Voraussetzung mehr

| | Windows | macOS und Linux |
|---|---|---|
| die Kommandozeilenwerkzeuge von svn | `svn --version --quiet` | `svn --version --quiet` |

Unter Windows bringt TortoiseSVN sie nur mit, wenn im Installer die Option *command line client tools* gewählt wurde.
Fehlen sie, sagt das in einem einfachen Satz und hört auf, zum Beispiel: *„Die Kommandozeilenwerkzeuge von svn sind
nicht installiert. Bitte starten Sie den TortoiseSVN-Installer noch einmal, wählen Sie ‚command line client tools‘ und
rufen Sie mich danach noch einmal auf.“*

Die Hooks von TortoiseSVN rufen Python unter dem Namen `python` auf. Unter Windows brauchen der TortoiseSVN-Schritt
(Schritt 5 unten) und eine Übernahme mit TortoiseSVN deshalb ein `python --version`, das 3.9 oder neuer ausgibt;
`py` allein reicht dort nicht. Fehlt das, läuft die Probe trotzdem. Der Bericht nennt, was fehlt: der Befehl `python`
im `PATH`, den der Python-Installer einzurichten anbietet.

## Schritt 2: Die Erklärung nennt zwei Freigaben mehr

svn ausführen, um die Dateien der Arbeitskopie aufzulisten und, erst nach einem gesonderten ausdrücklichen Ja, ihre
Historie vom Server des Projekts zu lesen; außerdem svnadmin, um im Ordner ein lokales Wegwerf-Repository anzulegen.
Unter Windows kommt dazu: Für einen Schritt committet der Owner in diesem Ordner über TortoiseSVN, an diesem Rechner,
und sieht, was das Gate tut. Fragt, ob er dabei sein wird. Ohne ihn entfällt der Schritt, und der Bericht sagt das.

## Schritt 4: Auflisten ohne Server

```
svn status -v
```

Das listet jedes versionierte Element mit Revision und letztem Autor auf, nur aus der Arbeitskopie; es fragt keinen
Server. Lasst die Zeilen weg, die mit `?` beginnen: Diese Elemente sind nicht versioniert. Behaltet die ersten 5.000
Zeilen. Die Größen nehmt aus den Dateien selbst. Die Historie kommt vom Server. Fragt die Person ausdrücklich um ihr
Ja, bevor ihr den Server des Projekts kontaktiert, um die Historie zu lesen. Ohne dieses Ja überspringt `svn log`,
haltet fest, dass die Historie hier nicht lesbar ist, und fahrt fort. Mit dem Ja:

```
svn log -l 200
```

Scheitert das, weil der Server außer Reichweite ist, ist die Historie hier nicht lesbar, und Schritt 9 sagt das. Von
der Adresse des Repositorys, `svn info --show-item repos-root-url`, zitiert nur das Schema: `file://`, `svn://`,
`svn+ssh://`, `http://` oder `https://`.

Führt in der Arbeitskopie nur `svn status -v`, `svn log`, `svn info` und `svn export` mit seiner Ausgabe in
`<probe>` aus (Schritt 5). Kein `svn update`, `svn cleanup` und `svn upgrade` dort: Jedes davon schreibt in sie. Sagt
svn, die Arbeitskopie brauche `svn upgrade`, lässt sie sich ohne Änderung nicht auflisten. Hört dort auf und berichtet
es.

## Schritt 5: Die Probe ist die Arbeitskopie eines Wegwerf-Repositorys

```
svnadmin create <probe>/svnrepo
svn checkout <adresse> <probe>/trial
```

Die Adresse ist `file://` mit dem absoluten Pfad des Repositorys dahinter: `file:///Users/…/svnrepo` unter macOS,
`file:///home/…/svnrepo` unter Linux, unter Windows mit Schrägstrichen `file:///C:/…/svnrepo`. Folgt dann Schritt 5
von `ADOPT.de.md` in `<probe>/trial`. In einer Arbeitskopie setzt `--init` auch `svn:ignore` für die Tafel. Committet die
Probe ins Wegwerf-Repository: zuerst das Werkzeug laufen lassen, dann `svn add --force .` und `svn commit -m "…"`.

- **Die Kopie für eine Nachstellung** kommt aus der Arbeitskopie, ohne den Server zu fragen:
  `svn export <pfad> <probe>/copy/<pfad>`. Legt die übergeordneten Zielordner vorher an.
- **Abgeschlossene Pakete bleiben aus der Probe heraus.** Ihr Gate prüft eine Revision gegen die Historie des
  Wegwerf-Repositorys, und die enthält die Revisionen des Projekts nicht. Nennt sie im Eintrag des Plans, jedes mit
  der Revision, die es gebaut hat (`svn log` zeigt sie). `Shipped` werden sie, mit diesem `r<N>` im *Verlauf*, erst
  beim Umzug ins Projekt (Schritt 12).
- **Der TortoiseSVN-Schritt, unter Windows, im Beisein des Owners.** Führt in der Probe
  `<py> tools/shoalmark/shoalmark.py --install-hook` aus. Es setzt `tsvn:startcommithook` und `tsvn:precommithook`
  auf den Ordner. Führt `svn update` aus und committet die Änderung der Properties auf der Kommandozeile. Dann der
  Owner, an diesem Rechner:
  1. Er bereitet eine Änderung vor, die ihr nennt, etwa eine Zeile unter *Was jetzt gilt* in einem Eintrag. Im
     Explorer klickt er mit rechts auf den Ordner der Probe, wählt *SVN Commit…*, liest die Hook-Skripte, nach denen
     TortoiseSVN fragt, und erlaubt sie. Der Commit geht durch.
  2. Er versucht eine Änderung, die das Gate ablehnt: einen Eintrag, auf `Shipped` gesetzt, ohne Revision im
     *Verlauf*. TortoiseSVN lehnt den Commit ab und zeigt die Zeile des Gates. Danach `svn revert`.

  Haltet fest, was der Owner gesehen hat. Dass TortoiseSVN die beiden Hook-Properties wie beschrieben ausführt, hat
  noch kein Mensch unter Windows gesehen; nur die Kommandozeile ist in CI geprüft. Ist es anders, ist das ein Befund,
  und Bericht und Rückmeldung sagen es. Unter macOS und Linux gibt es kein TortoiseSVN: Der Schritt entfällt.

## Schritt 9: der Server

Unter Subversion liest das Gate die Historie über svn. Ohne Server lehnt eine Prüfung ab, die die Historie braucht,
im Hook von TortoiseSVN wie in `--check`. Solche Prüfungen sind ein Wechsel auf `Shipped` und eine Antwort. Es geht
weiterhin, Einträge anzulegen und zu bearbeiten, ebenso `INDEX.md`, die Tafel, `--next` und ein `--check` auf
Änderungen, die keine Historie brauchen.

Ein Repository im Rechner selbst (`file://`) ist immer erreichbar; Schritt 10 sagt, was das kostet.

## Schritt 10: Identität unter Subversion

Die Identität ist das Server-Konto, das committet hat. `signed` wird unter Subversion abgelehnt, denn
Subversion liefert keine Commit-Signatur.

- **`file://` authentifiziert niemanden.** Jeder Commit trägt den Namen des Benutzerkontos, unter dem er entstand. Die
  Rechteprüfungen fangen dann Fehler ab, können aber die Commits des Owners nicht von denen eines Agenten
  unterscheiden.
- **Ein Sitz ist ein svn-Konto,** dessen Zugangsdaten nur in der Umgebung dieses Sitzes liegen: in einem Container
  oder unter einem eigenen Windows-Benutzer. Die gespeicherten Zugangsdaten des Owners bleiben außer Reichweite.
  Subversion speichert sie für das Benutzerkonto, in `~/.subversion/auth` oder unter Windows im Anmeldespeicher des
  Kontos. Alles, was unter diesem Konto läuft, kann sie lesen. Um das zu wissen, müsst ihr nicht suchen, und ihr tut
  es nie.
- **Umzug zu git.** Wo das Repository nur für die Arbeit der Agenten da ist, darf der Bericht den Umzug zu git als
  eine Möglichkeit nennen, mit ihren Kosten:
  - die Historie umziehen;
  - die Werkzeuge des Teams wechseln;
  - dafür signierte Antworten des Owners und eine geschützte Absicht.

  Er drängt nie dazu.

## Schritt 12: falls der Owner Ja sagt, unter Subversion

Dieselben Schritte wie in `ADOPT.de.md`, in der Arbeitskopie des Projekts, ausgeführt aus ihrer Wurzel
(`svn info --show-item wc-root`):

- `--vendor`, die aus der Probe kopierten Dateien und `--init --key <KEY>` mit demselben Schlüssel. In einer
  Arbeitskopie setzt `--init` `svn:ignore` für die Tafel.
- Kopiert die Einträge hinein. Abgeschlossene Pakete werden jetzt `Shipped`, jedes mit seinem `r<N>` im *Verlauf*;
  hier prüft sie das Gate.
- Lasst das Werkzeug laufen, bis es mit 0 endet, dann `svn add` für die neuen Dateien.
- **Vor dem ersten Commit fragen.** Lasst vor jedem `svn commit` das Werkzeug laufen und checkt die `INDEX.md` mit
  ein. Nennt Subversion den Ordner veraltet, zuerst `svn update`.
- `--install-hook` setzt die Hook-Properties von TortoiseSVN auf die Wurzel der Arbeitskopie; fragt vorher, und
  committet dann die Änderung der Properties. Wiederholt es nach jedem Upgrade, dann nach dem Commit einmal
  `<py> tools/shoalmark/shoalmark.py --check`. TortoiseSVN fragt jede Person einmal, bevor es sie ausführt.
- **Rückweg unter Subversion:** zuerst `svn propdel tsvn:startcommithook .` und `svn propdel tsvn:precommithook .`,
  committet. Dann löschen, was der Rückweg in `ADOPT.de.md` nennt.
