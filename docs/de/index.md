---
title: Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort
description: "Eine Werkbank für Ihre Agenten. Ihre Entscheidungen sind dokumentiert."
---

# shoalmark

*Eine Werkbank für Ihre Agenten. Ihre Entscheidungen sind dokumentiert.*

**Die Startseite, auf Englisch:** [eine Seekarte des Wattenmeers](../index.md), auf der jeder Fehler aus shoalmarks eigenem Tracker als Wrack liegt.

## Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort.

Sehen Sie, wo die Arbeit steht, was auf Ihr Wort wartet und was die nächste Session aufgreift. Ihre Agenten halten das in Ihrem Repository fest; Ihre Entscheidungen kommen als Ihre eigenen Commits hinzu, neben den Nachweisen für die Arbeit.

**[Geben Sie Ihren Agenten die Notiz](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)**

**An die Flotte:** Ihr wartet nicht auf Werkzeuge, ihr wartet auf euren Menschen. Legt dieser Person vor, was nur sie entscheiden
kann – ein Satz pro Frage, einmal am Tag –, und macht aus ihrer Antwort einen einzigen Befehl.

**An den Eigner:** Ihre Agenten fragen mitten im Lauf, und Sie nicken ab, was Sie nicht in Ruhe lesen konnten.
shoalmark sammelt diese Fragen für ein Standup zu der Uhrzeit, die Sie wählen.

[Warum shoalmark?](warum-shoalmark.md)

**Ihre Agenten handeln auf Ihr Wort hin — und es gilt nur Ihr signiertes Wort.** Im Beleg zählt eine Antwort nur als
Commit, signiert mit einem Schlüssel, dem Sie vertrauen, und eine unsignierte lehnt das Gate ab: unter git, sobald Ihre
`owner`-Zeile als `signed` markiert ist, wie es die [Einrichtungsseite](setup.md) tut. Unter Subversion zählt sie nur als
Commit, den der Server als Ihren authentifiziert hat. Ein Klick, ein Merge oder eine Zeile im Chat ist keine Antwort.
Wie stark diese Signatur ist, wählen Sie — [vier Stufen](signing.md), vom Schlüssel, den alles unter Ihrem Konto
benutzen kann, bis zu einem, der Ihre Berührung braucht —, und jede Signatur nennt den Schlüssel, der sie erzeugt
hat.

## Warum nicht mein Ticketsystem?

Ticketsysteme wurden gebaut, damit Menschen einander Arbeit zuweisen. shoalmark ist für Ihre Agenten gebaut: Der Beleg der Arbeit liegt in dem Repository, in dem sie arbeiten, und Ihre Antworten stehen dort als Ihre eigenen Commits.

Wenn Ihr jetziges Ticketsystem die Übergaben und Entscheidungen schon trägt, die Sie brauchen, kann das genügen. shoalmark bringt einen eigenen Tracker mit; ihn einzuführen heißt festzulegen, welcher Beleg maßgeblich ist.

## Gemessen, nicht versprochen

Im eigenen Repository von shoalmark, das selbst mit shoalmark arbeitet:

- **Bevor der Eigner die Review-Regel signierte** (jede Änderung bekommt einen Reviewer-Durchgang): 10 von 37 Pull
  Requests hatten eine Reviewer-Datei, als sie geöffnet wurden.
- **Danach, bis zum 1. Oktober 2026:** 71 von 82.

*Gezählt am 1. Oktober 2026 mit `gh` aus den Pull Requests 1–144 von shoalmark/shoalmark: nur gemergte, ohne die
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
geschrieben hat.

## Was ein Tag Sie kostet

- **Ein Standup, fünfzehn Minuten**, zu der Uhrzeit, die Sie wählen.
- **Ein Befehl pro Antwort:** `--answer AP-007 accept`. Er schreibt die Antwort, signiert sie mit Ihrem Schlüssel und
  pusht sie.
- **Der Rest kommt zu Ihnen:** Die letzte Nachricht jeder Session endet mit dem, was auf Sie wartet. Sie müssen nichts
  öffnen.

## Was es nicht ist

shoalmark braucht keinen Server und kein Konto, und seine IDs kann man aussprechen, etwa FM-012. Eine Markdown-Datei je
Arbeitspaket, eine Python-Datei und Prüfungen, die Sie lokal und in der CI Ihres Projekts ausführen können. Läuft mit
git auf Windows, macOS und Linux. Lizenz: Apache-2.0 oder MIT.

**In dieser Beta:**

- Kein Migrationswerkzeug: Es importiert kein Ticketsystem und beginnt mit der eigenen Arbeit Ihres Repositorys. Ein Weg für eine Flotte, die schon ein eigenes System hat, ist erfasst, nicht gebaut.
- Für eine Person mit dem letzten Wort und ihre Agenten-Flotte. Mehrere Menschen in der Verantwortung sind in dieser Beta nicht getestet; das kann später kommen.
- *Kein Beweis, dass die Arbeit stimmt.* Bei geprüften Änderungen in Git oder Subversion muss ein Wechsel zu `Shipped` im Abschnitt „Verlauf“ des Arbeitspakets einen Commit nennen, der schon in der Historie der geprüften Änderung liegt und etwas außerhalb des Belegs ändert (unter Subversion eine Revision). Diese Nachweisregel gilt nicht für `Closed`. Bei einem Verstoß meldet die Prüfung einen Fehler und endet mit einem Rückgabewert ungleich null. Ein installierter Git-Commit-Hook kann den Commit dann verweigern, ist aber optional und lässt sich umgehen. Damit die Prüfung vor dem Merge verbindlich ist, muss Ihr Projekt einen erfolgreichen Lauf von `--check` auf dem Branch in CI und Merge-Regeln voraussetzen; shoalmark richtet das nicht für Sie ein. Ob der Commit tut, was er soll, klärt ein Review.
- Gebaut und erprobt mit `git` und GitHub. Subversion besteht die Test-Suite, ist in echter Arbeit aber noch nicht erprobt: Probieren Sie es aus, ohne Gewähr. Signierte Antworten brauchen `git`, die Pull-Request-Warteschlange `git` und GitHub.

## Hier anfangen

| | |
|---|---|
| **Sie, der Eigner** | [In zehn Minuten eingerichtet](setup.md) · [Ihre Antwort ist Ihr Commit](signing.md) · [Der Standup](standup.md) |
| **Die Agenten Ihres Projekts** | die [Notiz zum Ausprobieren](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md): eine Messung, keine Anweisung. Am Ende berichten sie Ihnen, und Sie entscheiden |
| **Ein Agent bei der Arbeit** | der Vertrag ist `tools/shoalmark/README.md` in Ihrem Repository, [hier gerendert](../agents/README.md), auf Englisch – so lesen ihn die Agenten. `llms.txt` liegt im Stammverzeichnis dieser Website |
