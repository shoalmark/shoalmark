# Der Standup — einmal am Tag

*Menschen haben Sprechzeiten. Agenten haben Budgets. Dazwischen liegt ein fester Standup.*

Alles, was auf Sie wartet, steht in der ersten Zeile der Tafel und in einem Befehl:

```
python3 tools/shoalmark/shoalmark.py --standup
```

Er gibt die Tagesordnung eines Standups aus, nach Art geordnet: zuerst **Entscheidungen** (antworten Sie; eine
vorläufige Antwort ist eine Antwort), dann was nur **Ihre Hände** tun können, in der Reihenfolge, die am meisten
Arbeit freigibt, dann was **Belege klären** könnten, ohne Sie, dann **Knöpfe**. Jeder Punkt ist eine Frage, mit der
Wartezeit und dem, was sie aufhält. Nach den Fragen kommen **Ihre Handlungen, mit ihrer Zeit** — versäumte und
überfällige zuerst, dann was fällig wird, dann was noch keinen Termin hat — und zuletzt, was Sie beantwortet oder getan
haben und was **unterwegs** zu Ihrem Merge ist.

## Wann

```
standup = "09:00"          # in shoalmark.toml — Ortszeit
standup_minutes = 15
```

Die erste Zeile der Tagesordnung trägt diese Uhrzeit und Dauer. Den Termin in Ihrem Kalender legen Sie selbst an: das
Werkzeug schreibt keine Kalenderdatei und zeigt keine Benachrichtigung (R9). **Mehrere Repositories?** Ein Standup kann
sie alle halten: der nächste Abschnitt.

## Mehrere Repositories, ein Standup

```
python3 tools/shoalmark/shoalmark.py --standup ~/code/notes-app ~/work/client-site ~/code/side-project
```

Eine Tagesordnung, nach Art geordnet, über die Repositories, die Sie nennen — jeder Punkt mit seinem Repository. Jedes
wird gelesen, wie es steht: ein git-Repository mit seinem Branch und seinem Commit, eine Subversion-Arbeitskopie mit ihrer
Revision, ein einfacher Ordner, wie er ist. Ein Ordner, der sich nicht lesen lässt, wird mit dem Grund genannt und
nirgends gezählt. Jede Zahl gehört einem Repository und wird dann addiert: FM-001 in zwei Repositories sind zwei Punkte.

Es führt nichts von ihnen aus — kein eigenes Werkzeug eines Repositorys, keinen Deriver, keinen Hook und kein
konfiguriertes Programm, und es holt nichts — und es schreibt nichts, weder in einem Repository noch anderswo. git und svn
startet es aus den absoluten Einträgen von PATH außerhalb der genannten Repositories; wo keiner eines enthält, werden die
Ordner, die es brauchen, mit dem Grund genannt. Es sagt,
was dadurch ungelesen bleibt: ob ein git-Arbeitsbaum Änderungen hat, was `git status` dort sagt; und was das eigene
`--standup` eines Repositorys auf diesen Wegen liest — was Sie beantwortet oder getan haben und auf einem Antwort-Branch
unterwegs ist (eine Frage, die Sie beantwortet haben, steht hier bis zu Ihrem Merge), die Warteschlange der Pull
Requests und, wo ein Repository `[seats]` hat, wer gefragt hat. Sie antworten in jedem Repository wie bisher, und sein
eigenes `--standup` dort sagt den Rest.

## Was die Agenten damit tun

Vor dem Standup steht jede Frage an Sie als `ask:` im Arbeitspaket: ein Satz, den Sie beantworten können. Zwischen den
Standups unterbricht Sie niemand, außer für etwas, das sich nicht rückgängig machen lässt. Die letzte Nachricht jeder
Session endet mit `--owner`: dieselbe Liste, damit sie zu Ihnen kommt, ohne dass Sie etwas öffnen.

## Antworten

Auf der Tafel trägt jede Frage **annehmen** und **ablehnen**. Beides öffnet einen Dialog mit der Frage, ihren
Möglichkeiten (die vom Agenten empfohlene zuerst) und dem, was sie aufhält; beim Annehmen können Sie eine Änderung
mitgeben, beim Ablehnen sagen Sie, warum. OK gibt Ihnen einen Befehl — `python3 tools/shoalmark/shoalmark.py --answer
AP-007 accept` —, der die Antwort schreibt, mit Ihrem Schlüssel signiert und pusht. Die Antwort ist Ihr eigener
Commit: [Ihre Antwort ist Ihr Commit](signing.md).

## Ihre Handlungen, mit ihrer Zeit

Manche Antworten sind Zusagen: *ja, ich lese die Produktion um sieben*. Was folgt, ist eine Handlung, die nur Sie tun
können, und sie hat eine Zeit — `due:` im Arbeitspaket, und ein Fenster danach (`window:`, 60 Minuten, wenn nichts
anderes dasteht). Die Tafel listet Ihre Handlungen unter den Fragen, jede **fällig**, **überfällig** nach ihrer Zeit
oder **versäumt**, wenn ihr Fenster ohne Ergebnis verstrichen ist. Eine zugesagte Handlung steht als Ihre Zusage da — die
Option, die Sie gewählt haben —, die Frage, die sie beantwortet, klein darunter. Jede trägt zwei Knöpfe: **erledigt** fragt, wo das
Ergebnis liegt — der Pfad genügt: der Eintrag ergänzt, was das Repository über die Datei weiß, wer sie wann hinzugefügt
hat und bei einer Prüfung ihr Urteil —, und gibt Ihnen `python3 tools/shoalmark/shoalmark.py --done AP-007 "evidence/AP-007/read.md"`;
**verschieben** fragt nach der neuen Zeit und gibt Ihnen `--due AP-007 <Zeit>`. Beides wird signiert und gepusht wie
eine Antwort.

## Unterwegs — vor Ihrem Merge

Was Sie beantworten oder tun, ist ein signierter Commit auf `answer/<id>`, gepusht; der Standardzweig hat ihn erst nach
Ihrem Merge. Bis dahin liest die Tafel git, und die Seite, auf die Sie zurückkommen, zeigt es sofort: die Frage verlässt
*wartet auf Sie*, die Handlung verlässt *Ihre Handlungen*, und beide stehen unter **unterwegs** — Ihre Zusage oder Ihre
Antwort zuerst, dann was es ist: *beantwortet, unterwegs*, *erledigt, unterwegs — <wo das Ergebnis liegt>*,
*verschoben, unterwegs — fällig <Zeit>*, *zurückgenommen, unterwegs — <warum>* oder *Erledigung zurückgenommen,
unterwegs*; der Zweig, der Commit und seine Zeit, ob er signiert ist, und *Ihr Merge ist als Nächstes dran* — oder
*Ihr Merge wartet: …*, wo die Queue auf den Zweig wartet, meist auf den Commit eines Sitzes unter Ihrer Handlung. Eine
Antwort oder eine erledigte Handlung trägt einen Knopf, **zurücknehmen**, wo annehmen und ablehnen oder erledigt und
verschieben standen: er fragt, warum, und gibt Ihnen `python3 tools/shoalmark/shoalmark.py --revoke AP-007 "<warum>"` —
einen neuen signierten Commit darauf, auf demselben Zweig, nie ein Überschreiben. Eine Verschiebung trägt keinen; um sie
noch einmal zu verschieben, führen Sie `--due` auf ihrem Zweig aus. Nach Ihrem Merge liest jede wieder vom
Standardzweig; ein anderer Rechner zeigt nach einem Fetch dieselben Zeilen.

Einladungen und Benachrichtigungen gibt es nicht mehr (R9): `--invite`, `--notify` und `--standup DATEI.ics` sagen das
in einer Zeile. Wo eine frühere Version eine Kalenderdatei, einen Zeitplan oder seinen Zustand auf Ihrem Rechner
hinterlassen hat, nennen `--standup` und `--owner` jedes Stück, bis Sie es entfernen, und das README sagt, wie.

## Welches Review unabhängig war

Bevor Arbeit bei Ihnen zum Mergen ankommt, prüft sie ein Reviewer, und sein Urteils-Commit nennt den Stand, den er
geprüft hat (`Reviewed: <sha>`). Jeder Commit eines Agenten nennt außerdem seine Session. Deshalb zählt die Tafel die
Urteile der Woche: **unabhängig** — der Reviewer lief in einer anderen Session als der, die die Arbeit gebaut hat —
oder **gleiche Session** — ein Sub-Agent der Session des Erbauers, also eine zweite Meinung aus demselben Lauf. Ein
READY ist so viel wert, wie seine Zählung sagt; Sie sehen sie, bevor Sie auf Merge drücken.
