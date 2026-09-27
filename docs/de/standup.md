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
überfällige zuerst, dann was fällig wird, dann was noch keinen Termin hat.

## Die Einladung

```
standup = "09:00"          # in shoalmark.toml — Ortszeit
standup_minutes = 15
python3 tools/shoalmark/shoalmark.py --standup standup.ics
```

Die Datei in den Kalender importieren: werktags, zu dieser Uhrzeit. **Mehrere Repositories?** Jedes bekommt einen
eigenen Termin, und sie dürfen sich nicht überschneiden. Nur Ihr Kalender sieht alle zugleich, deshalb kommt die
Einladung als Kalenderdatei.

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
Ergebnis liegt, und gibt Ihnen `python3 tools/shoalmark/shoalmark.py --done AP-007 "evidence/AP-007/read.md"`;
**verschieben** fragt nach der neuen Zeit und gibt Ihnen `--due AP-007 <Zeit>`. Beides wird signiert und gepusht wie
eine Antwort.

Zwei Erinnerungen, wenn Sie wollen. `--invite AP-007` schreibt die Handlung als Kalenderdatei — ihre Zeit, ihr
Fenster, eine Erinnerung 30 Minuten vorher — neben die Belege des Arbeitspakets; importieren Sie sie. `--notify`
zeigt eine Systembenachrichtigung für jede Handlung, die in 30 Minuten fällig, überfällig oder versäumt ist, jede
einmal; planen Sie den Aufruf selbst ein (das README hat eine cron- und eine launchd-Zeile).

## Welches Review unabhängig war

Bevor Arbeit bei Ihnen zum Mergen ankommt, prüft sie ein Reviewer, und sein Urteils-Commit nennt den Stand, den er
geprüft hat (`Reviewed: <sha>`). Jeder Commit eines Agenten nennt außerdem seine Session. Deshalb zählt die Tafel die
Urteile der Woche: **unabhängig** — der Reviewer lief in einer anderen Session als der, die die Arbeit gebaut hat —
oder **gleiche Session** — ein Sub-Agent der Session des Erbauers, also eine zweite Meinung aus demselben Lauf. Ein
READY ist so viel wert, wie seine Zählung sagt; Sie sehen sie, bevor Sie auf Merge drücken.
