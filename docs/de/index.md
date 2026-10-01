---
title: Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort
description: "Ein Arbeits-Tracker in Ihrem Repository, für Ihre Agenten: Nichts geht ohne Commit dahinter als „fertig“ durch, und was auf Ihr Wort wartet, steht ganz oben."
---

# shoalmark

*Eine Pricke im Watt – sie hält die Flotte im Fahrwasser.*

**Die Startseite, auf Englisch:** [eine Seekarte des Wattenmeers](../index.md), auf der jeder Fehler aus shoalmarks eigenem Tracker als Wrack liegt.

## Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort.

Ticketsysteme wurden gebaut, damit Menschen einander Arbeit zuweisen. shoalmark ist für Ihre Agenten gebaut: Die Arbeit liegt in Ihrem Repository, nichts geht ohne Commit dahinter als fertig durch, und was auf Ihr Wort wartet, steht ganz oben.

**[Geben Sie Ihren Agenten die Notiz](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)**

**An die Flotte:** Ihr wartet nicht auf Werkzeuge, ihr wartet auf euren Menschen. Legt dieser Person vor, was nur sie entscheiden
kann – ein Satz pro Frage, einmal am Tag –, und macht aus ihrer Antwort einen einzigen Befehl.

**An den Eigner:** Ihre Agenten fragen mitten im Lauf, und Sie nicken ab, was Sie nicht in Ruhe lesen konnten.
shoalmark sammelt diese Fragen und legt sie Ihnen einmal am Tag vor.

**Ihre Agenten handeln auf Ihr Wort hin — und es gilt nur Ihr signiertes Wort.** Im Beleg zählt eine Antwort nur als
Commit, signiert mit einem Schlüssel, dem Sie vertrauen, und eine unsignierte lehnt das Gate ab: unter git, sobald Ihr
Sitz als `signed` markiert ist, wie es die [Einrichtungsseite](setup.md) tut. Unter Subversion zählt sie nur als
Commit, den der Server als Ihren authentifiziert hat. Ein Klick, ein Merge oder eine Zeile im Chat ist keine Antwort.
Wie stark diese Signatur ist, wählen Sie — [vier Stufen](signing.md), vom Schlüssel, den alles unter Ihrem Konto
benutzen kann, bis zu einem, der Ihre Berührung braucht —, und jede Signatur nennt den Schlüssel, der sie erzeugt
hat.

## Gemessen, nicht versprochen

Im eigenen Repository von shoalmark, das selbst mit shoalmark arbeitet:

- **Bevor der Eigner die Review-Regel signierte** (jede Änderung bekommt einen Reviewer-Durchgang): 10 von 37 Pull
  Requests hatten eine Reviewer-Datei, als sie geöffnet wurden.
- **Danach, bis zum 25. September 2026:** 12 von 15.

*Gezählt am 25. September 2026 mit `gh` aus den Pull Requests 1–69 von holgo99/shoalmark: nur gemergte, ohne die
eigenen Antwort-Branches des Eigners (`answer/…`). Einer zählt, wenn ein Commit, der eine Datei unter
`work-tracker/evidence/reviews/` anlegt oder ändert (Merge-Commits nicht mitgezählt), vor dem Öffnen des Pull
Requests datiert ist. Das Datum eines Commits sagt, wann er entstand, nicht wann er gepusht wurde: Die
Push-Ereignisse der Forge bestätigen die gezählten Pull Requests ab dem 24. September 2026, 05:18 UTC; ältere listet
sie nicht mehr. Die Regel ist die signierte Antwort des Eigners vom 24. September 2026, 11:07 Uhr MESZ.*

Was shoalmark dazu ausgibt, jeden Tag:

- **Ein Befehl, ein signierter Commit** pro Frage an den Eigner.
- **Die Tafel meldet zu jedem Review**, ob es aus einer anderen Session kam als der Code, den es prüfte. Das ist eine
  Meldung, kein Beweis: git kann es noch nicht belegen.

## Ihre Agenten richten es ein

1. Sie holen shoalmark beim Git-Tag eines Releases und legen eine festgeschriebene Kopie ins Repository, jede Datei
   mit Prüfsumme (`--vendor`).
2. `--init` schreibt die Konfiguration, die Triage-Datei und den Vertrag für Agenten.
3. Die Agenten lesen den Vertrag, das [README](../agents/README.md), und legen die Arbeit an: eine Markdown-Datei je
   Arbeitspaket.
4. **Sie** schreiben drei Zeilen in Ihren eigenen Worten: wofür das Repository da ist, was gilt, wenn es
   funktioniert, und was niemand tun darf, um dorthin zu kommen. Dann richten Sie einmal Ihre Signatur ein
   ([zehn Minuten](signing.md)).

**Sie verlieren nichts.** Was Sie heute schon festhalten, bleibt, wo es ist: shoalmark ändert nur, was es selbst
geschrieben hat. Der Weg für eine Agenten-Flotte, die schon ein eigenes System hat, ist als FM-026 erfasst und folgt.

## Was ein Tag Sie kostet

- **Ein Standup, fünfzehn Minuten**, zu der Uhrzeit, die Sie wählen. Die Einladung kommt als Kalenderdatei.
- **Ein Befehl pro Antwort:** `--answer AP-007 accept`. Er schreibt die Antwort, signiert sie mit Ihrem Schlüssel und
  pusht sie.
- **Der Rest kommt zu Ihnen:** Die letzte Nachricht jeder Session endet mit dem, was auf Sie wartet. Sie müssen nichts
  öffnen.

## Was es nicht ist

Kein Server, kein Konto, keine UUIDs. Eine Markdown-Datei je Arbeitspaket, eine Python-Datei und ein Gate bei jedem
Commit, das ablehnt, was sich widerspricht. Läuft mit git und Subversion, auf Windows, macOS und Linux. Lizenz:
Apache-2.0 oder MIT.

## Hier anfangen

| | |
|---|---|
| **Sie, der Eigner** | [In zehn Minuten eingerichtet](setup.md) · [Ihre Antwort ist Ihr Commit](signing.md) · [Der Standup](standup.md) |
| **Die Agenten Ihres Projekts** | die [Notiz zum Ausprobieren](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md): eine Messung, keine Anweisung. Am Ende berichten sie Ihnen, und Sie entscheiden |
| **Ein Agent bei der Arbeit** | der Vertrag ist `tools/shoalmark/README.md` in Ihrem Repository, [hier gerendert](../agents/README.md), auf Englisch – so lesen ihn die Agenten. `llms.txt` liegt im Stammverzeichnis dieser Website |
