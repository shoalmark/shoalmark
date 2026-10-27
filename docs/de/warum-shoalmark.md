---
title: Warum shoalmark?
description: "shoalmark auf einer Seite: eine Vertrauensschicht für KI-Agenten, in deinem Repository. Die Agenten tragen die Arbeit, du behältst das letzte Wort."
template: why.html
---

# Warum shoalmark?

**Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort.**

**TL;DR:**

- **Was:** shoalmark ist eine Vertrauensschicht für KI-Agenten, und sie lebt in deinem Repository. Deine Agenten führen den Arbeitsstand. Du behältst das letzte Wort, als deine eigenen Commits.
- **Das Problem:** Agenten bauen schneller, als du entscheiden kannst. Der Engpass sind nicht die Agenten. Der Engpass bist du, mitten in ihrer Arbeit in kleine Entscheidungen gezogen.
- **Wie:** Die Fragen der Agenten warten auf dem Board, statt dich zu unterbrechen. Wann es dir passt, kopierst du den Standup-Prompt: Er bittet eine Sitzung, sie mit dir durchzugehen. Jede Antwort ist ein Commit, den du signieren kannst.
- **Einfach:** Eine Python-Datei. Kein Server, keine Datenbank, kein Konto, und nichts, das dich bindet.
- **Stand:** Open Source (Apache-2.0 oder MIT), in der Beta, und mit sich selbst gebaut.
- **Ausprobieren:** [Kopier den Prompt](index.md#top) und lass deinen Agenten prüfen, ob shoalmark zu deinem Projekt passt. Bis zu 45 Minuten, und „passt nicht“ ist auch eine Antwort.

## Die Pricke

Eine Pricke markiert den Rand eines Fahrwassers im Watt. Den Kurs bestimmt weiterhin der Mensch am Steuer. Das ist die ganze Idee von shoalmark: Die Marken tun ihre Arbeit, und der Kurs bleibt in Menschenhand.

## Was ich gesehen habe

Ich bin von dem ausgegangen, was ich gemessen habe. In meinem letzten Repository wurden in **22** Tagen **200** Pull Requests gemergt, **85 %** davon innerhalb einer Minute nach dem Öffnen, und **keiner** mit einem Review. Getrennt gefragt, was sie am meisten bremst, gaben drei Agenten dieselbe Antwort: die unbeantworteten Fragen an den Menschen. Eine Frage, drei Tage offen, hielt drei Pakete auf. Das Tempo war nie das Problem. Kleine Entscheidungen mitten in der Arbeit waren es.

Am 13. Juli habe ich mich aus der Schleife genommen: Meine Planer-Agenten bekamen gh und übernahmen die Orchestrierung, und das Tempo war unglaublich. Einen Monat später postete ich [‚Bottleneck removed.‘](https://x.com/Holgo99/status/2088153757792043485)

Aber entfernt hatte ich mich gar nicht. Ich war ihr Bote geworden, ihr Abnicker und ihre Entscheidungsmaschine, und das ständige Umschalten zwischen den Sitzungen war zermürbend. Am 29. September zeigte mein GitHub 9.946 Beiträge für das Jahr, und ich postete [‚What a hell of a ride.‘](https://x.com/Holgo99/status/2104854591032484007)

Mit shoalmark bin ich zurückgekommen: Seit dem 21. September machen seine Agenten die meisten Commits, und meine sind vor allem Merges und Antworten. Ich baue portdive mit shoalmark, und shoalmark mit sich selbst.

![Ein Pixelraster-Kalender mit 10.259 GitHub-Beiträgen in 2026 auf einem einzelnen Konto, Stand 23. Oktober, im Nachtlook von shoalmark: ruhig von Januar bis Anfang Juli, ein helles Band von Mitte Juli bis Ende September, im Oktober wieder ruhiger. Drei Beschriftungen: 13. Juli, „Meine Planer-Agenten bekommen gh. Ich werde ihr Abnicker und ihr Bote.“; eine Klammer über die 22 Tage vor dem 21. September, „200 Pull Requests in 22 Tagen, keiner mit Review: das Repository, aus dem shoalmark kam“; und der 21. und 24. September, „der erste Commit von shoalmark“ und „jeder Pull Request bekommt die Datei eines Reviewers“. Quelle: github.com/holgo99.](https://shoalmark.tools/assets/why/contributions-2026-de.png)

## Wofür shoalmark da ist

Ich bin überzeugt: Deine Agenten sollen mit voller Geschwindigkeit arbeiten und nachfragen, wenn es darauf ankommt. Entscheiden soll nur dein geprüftes Wort. Und jede Entscheidung soll sich später nachlesen lassen, direkt aus dem Repository. Genau dafür ist shoalmark gebaut.

![Ein Mockup des shoalmark-Boards eines Beispiel-Repositorys, notes-app, mit englischen Beschriftungen. Unter dem Kopf sagt die Seite, wann sie von main gelesen wurde, dass sie ihre Datei wieder liest, wenn man zu ihr zurückkehrt, und dass nichts ständig nachfragt, neben einem Knopf, der den Befehl zum Neubau kopiert. Im Kasten „yours“ warten zwei Entscheidungen, die älteste zuerst: NA-009-Q1, „May the sync drop devices unseen for 90 days?“, die NA-019 aufhält und von der Research-Sitzung gestellt wurde; und NA-012-Q2, „Ship the export as CSV only, or as CSV and JSON?“, die NA-014 aufhält und von der Planner-Sitzung gestellt wurde. Jede hat die Knöpfe „accept“ und „reject“, und die Antworten dort sind signiert. Darunter der Tag: ein Knopf, der den Standup-Prompt kopiert; die drei Sitzungen mit einem Commit in den letzten 24 Stunden, Research und Planner in Claude Code und Builder in Codex, die beiden, die gefragt haben, zuerst, jede mit einem Knopf, der ihren Befehl zum Fortsetzen kopiert; und ein Knopf, der den Abschluss-Prompt kopiert. Reviews, Receipts und der aktuelle Pfad sind eingeklappt.](https://shoalmark.tools/assets/why/board-mockup-dark.png)

*Ein Mockup des Boards, aus einem Beispiel-Repository: Die Fragen deiner Agenten warten oben, die älteste zuerst; darunter die Sitzung, die jede gestellt hat, mit einem Knopf, der ihren Befehl zum Fortsetzen kopiert.*

## Warum es so gebaut ist

Vertrauen beginnt mit Dingen, die man prüfen kann. Darum bleibt shoalmark klein und hält sich aus dem Weg:

- **Eine Datei.** Python 3.9 oder neuer. Kein pip, kein Server, keine Datenbank, kein Konto. Dein Repository behält eine festgeschriebene Kopie mit Prüfsummen, und sie aktualisiert sich nie hinter deinem Rücken.
- **Dein Beleg.** Schlichtes Markdown, eine Datei pro Arbeitspaket, direkt in deinem Repository. shoalmark überschreibt nie eine Datei, die es nicht selbst geschrieben hat.
- **Dein Wort.** Ein Befehl pro Antwort, festgehalten als dein eigener Commit. Ein Klick oder eine Zeile im Chat ist keine Antwort.
- **Dein Standup.** Die Fragen warten auf dem Board, die älteste zuerst. Der Standup-Prompt liegt einen Klick entfernt bereit, wann immer es dir passt.
- **Aufgeschriebene Rechte.** Jeder Agent arbeitet in einem Sitz mit aufgeschriebenen Rechten, und das Gate sieht jedes Recht in einem Diff.
- **Gemessen, nicht versprochen.** shoalmark ist kein Beweis, dass die Arbeit stimmt. Dafür ist ein Review da.

## Woran es sich selbst hält

Ich messe shoalmark an seiner eigenen Absicht, die über jedem Sichtungsdurchlauf in seinem Repository steht. Sie nennt, was nie passieren darf: ein falsches Durchwinken, eine Behauptung ohne Quelle, eine Handlung ohne deine Zustimmung, das Wort eines Agenten, das als deines zählt.

## Du bist am Zug

Wenn du mit Agenten baust, probier es an deinem eigenen Repository aus. Deine Agenten richten es ein, und der Beleg bleibt bei dir.

Lass deine Agenten laufen. Behalte das letzte Wort.

[Deine Agenten richten es ein](index.md#start) · [In zehn Minuten eingerichtet](setup.md) · [Zurück zu shoalmark](index.md)

Offen gebaut: [github.com/shoalmark/shoalmark](https://github.com/shoalmark/shoalmark) · Folge mir beim Bauen auf X: [@holgo99](https://x.com/holgo99)
