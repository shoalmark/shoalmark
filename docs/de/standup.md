# Das Stand-up — wann immer es dir passt

*Menschen haben Sprechzeiten. Agenten haben Budgets. Dazwischen liegt eine Runde, wann immer es dir passt.*

Alles, was auf dich wartet, steht in der ersten Zeile des Boards und in einem Befehl:

```
python3 tools/shoalmark/shoalmark.py --standup
```

Er gibt die Tagesordnung einer Runde aus, nach Art geordnet: zuerst **Entscheidungen** (antworte; eine
vorläufige Antwort ist eine Antwort), dann was nur **deine Hände** tun können, in der Reihenfolge, die am meisten
Arbeit freigibt, dann was **Belege klären** könnten, ohne dich, dann **Knöpfe**. Jeder Punkt ist eine Frage, mit der
Wartezeit und dem, was sie aufhält. Nach den Fragen kommen **deine Handlungen, mit ihrer Zeit** — versäumte und
überfällige zuerst, dann was fällig wird, dann was noch keinen Termin hat.

## Wann

Wann immer es dir passt: Der Stand-up-Prompt des Boards liegt einen Klick entfernt bereit, oder du führst `--standup`
selbst aus. Eine feste Uhrzeit ist freiwillig:

```
standup = "09:00"          # in shoalmark.toml — Ortszeit; leer, die Voreinstellung, setzt keine
standup_minutes = 15
```

Die erste Zeile der Tagesordnung trägt die Uhrzeit, wenn eine gesetzt ist, und die Dauer. Einen Termin in deinem Kalender
legst du, wenn du einen willst, selbst an: Das Werkzeug schreibt keine Kalenderdatei und zeigt keine Benachrichtigung
(R9). **Mehrere Repositories?** Eine Runde reicht für alle: der nächste Abschnitt.

## Mehrere Repositories, eine Runde

```
python3 tools/shoalmark/shoalmark.py --standup ~/code/notes-app ~/work/client-site ~/code/side-project
```

Eine Tagesordnung, nach Art geordnet, über die Repositories, die du nennst — jeder Punkt mit seinem Repository. Jedes
wird gelesen, wie es steht: ein git-Repository mit seinem Branch und seinem Commit, eine Subversion-Arbeitskopie mit ihrer
Revision, ein einfacher Ordner, wie er ist. Ein Ordner, der sich nicht lesen lässt, wird mit dem Grund genannt und
nirgends gezählt. Jede Zahl gehört einem Repository und wird dann addiert: FM-001 in zwei Repositories sind zwei Punkte.

Es führt nichts von ihnen aus — kein eigenes Werkzeug eines Repositorys, keinen Deriver, keinen Hook und kein
konfiguriertes Programm, und es holt nichts — und es schreibt nichts, weder in einem Repository noch anderswo. git und svn
startet es aus den absoluten Einträgen von PATH außerhalb der genannten Repositories; wo keiner eines enthält, werden die
Ordner, die es brauchen, mit dem Grund genannt. Es sagt,
was dadurch ungelesen bleibt: ob ein git-Arbeitsbaum Änderungen hat, was `git status` dort sagt; und was das eigene
`--standup` eines Repositorys auf diesen Wegen liest — die Warteschlange der Pull Requests und, wo ein Repository
`[seats]` hat, wer gefragt hat. Du antwortest in jedem Repository wie bisher, und sein eigenes `--standup` dort sagt
den Rest.

Auf dem Board trägt der Kasten mit dem, was auf dich wartet, zwei Knöpfe: **Stand-up-Prompt** vor den Sessions des letzten Tages
und **Abschluss-Prompt** an seinem Ende. Jeder kopiert einen festen Prompt für die Session, die du nutzt — Claude Code, Codex
oder eine andere: der eine bittet sie, deine Runde nach dieser Tagesordnung zu halten, einen Punkt nach dem anderen; der andere,
den Tag aus dem Verlauf vorzulesen und nichts zu ändern. Keiner führt etwas aus, und eine Nachricht ist nie eine Antwort: Deine
Entscheidung hält der Befehl fest, den du selbst ausführst. Die Prompts sind englisch.

## Was die Agenten damit tun

Vor dem Stand-up steht jede Frage an dich als `ask:` im Arbeitspaket: ein Satz, den du beantworten kannst. Zwischen den
Stand-ups unterbricht dich niemand, außer für etwas, das sich nicht rückgängig machen lässt. Die letzte Nachricht jeder
Session endet mit `--owner`: dieselbe Liste, damit sie zu dir kommt, ohne dass du etwas öffnest.

## Antworten

Auf dem Board trägt jede Frage **annehmen** und **ablehnen**. Beides öffnet einen Dialog mit der Frage, ihren
Möglichkeiten (die vom Agenten empfohlene zuerst) und dem, was sie aufhält; beim Annehmen kannst du eine Änderung
mitgeben, beim Ablehnen sagst du, warum. OK gibt dir einen Befehl — `python3 tools/shoalmark/shoalmark.py --answer
AP-007-Q1 accept` —, der deine Antwort als Commit schreibt, mit deinem Schlüssel signiert, sobald du das Signieren
einschaltest. Die Antwort ist dein eigener Commit: [Deine Antwort ist dein Commit](signing.md).

## Deine Handlungen, mit ihrer Zeit

Manche Antworten sind Zusagen: *ja, ich lese die Produktion um sieben*. Was folgt, ist eine Handlung, die nur du tun
kannst, und sie hat eine Zeit — `due:` im Arbeitspaket, und ein Fenster danach (`window:`, 60 Minuten, wenn nichts
anderes dasteht). Das Board listet deine Handlungen unter den Fragen, jede **fällig**, **überfällig** nach ihrer Zeit
oder **versäumt**, wenn ihr Fenster ohne Ergebnis verstrichen ist. Eine zugesagte Handlung steht als deine Zusage da — die
Option, die du gewählt hast —, die Frage, die sie beantwortet, klein darunter. Jede trägt zwei Knöpfe: **erledigt** fragt, wo das
Ergebnis liegt — der Pfad genügt: der Beleg ergänzt, was das Repository über die Datei weiß, wer sie wann hinzugefügt
hat und bei einer Prüfung ihr Urteil —, und gibt dir `python3 tools/shoalmark/shoalmark.py --done AP-007 "evidence/AP-007/read.md"`;
**verschieben** fragt nach der neuen Zeit und gibt dir `--due AP-007 <time>`. Beides wird signiert wie eine Antwort
und auf dem Branch committet, auf dem du stehst; gepusht wird nichts.

## Wo deine Antwort landet

Was du beantwortest oder tust, ist ein Commit von dir, auf dem Branch, auf dem du stehst, mit deinem Schlüssel signiert,
sobald du das Signieren einschaltest: `--answer`, `--done`, `--due` und `--revoke` legen keinen Branch an und pushen
nichts. Jeder dieser Befehle nennt danach Branch und Commit und baut das Board neu, und die Seite, auf die du
zurückkommst, zeigt deine Antwort oder Handlung auf diesem Branch sofort: Die Frage verlässt *wartet auf dich*, und eine
erledigte Handlung verlässt *deine Handlungen*. Das zählt erst, wenn dieser Commit auf dem Standard-Branch liegt: Pushe
ihn oder merge den Branch, der ihn enthält. Ein Checkout ohne diesen Commit — der Standard-Branch, bevor der Commit dort
liegt, oder ein anderer Rechner — zeigt die Frage oder die Handlung weiter als offen.

Um eine Antwort zurückzunehmen, führe `python3 tools/shoalmark/shoalmark.py --revoke AP-007-Q1 "<why>"` aus, mit der ID
der beantworteten Frage; um eine erledigte Handlung zurückzunehmen, `--revoke AP-007 "<why>"`, mit der ID ihres
Arbeitspakets. Das Board hat dafür keinen Knopf. Beides ist ein neuer Commit, nie ein Überschreiben: Die zurückgenommene
Antwort kommt in den Verlauf des Arbeitspakets; bei einer erledigten Handlung kommt die Rücknahme in ihren Beleg unter
*Handlungen*, und die Handlung ist wieder offen.

Einladungen und Benachrichtigungen gibt es nicht mehr (R9): `--invite`, `--notify` und `--standup DATEI.ics` sagen das
in einer Zeile. Wo eine frühere Version eine Kalenderdatei, einen Zeitplan oder seinen Zustand auf deinem Rechner
hinterlassen hat, nennen `--standup` und `--owner` jedes Stück, bis du es entfernst, und das README sagt, wie.

## Welches Review unabhängig war

Bevor Arbeit bei dir zum Mergen ankommt, prüft sie ein Reviewer, und sein Urteils-Commit nennt den Stand, den er
geprüft hat (`Reviewed: <sha>`). Jeder Commit eines Agenten nennt außerdem seine Session. Deshalb zählt das Board die
Urteile der Woche: **unabhängig** — der Reviewer lief in einer anderen Session als der, die die Arbeit gebaut hat —
oder **gleiche Session** — ein Sub-Agent der Session des Erbauers, also eine zweite Meinung aus demselben Lauf. Ein
READY ist so viel wert, wie seine Zählung sagt; du siehst sie, bevor du auf Merge drückst.
