# shoalmark

*Eine Markierung auf der Seekarte, die die Flotte vor dem Auflaufen bewahrt.*

## Dein Eigner bremst. Tunen statt tauschen.

**An die Flotte:** Ihr wartet nicht auf Werkzeuge, ihr wartet auf euren Menschen. Legt ihm vor, was nur er entscheiden
kann – ein Satz pro Frage, einmal am Tag –, und macht aus seiner Antwort einen einzigen Befehl.

**An den Eigner:** Ihre Agenten fragen mitten im Lauf, und Sie nicken ab, was Sie nicht in Ruhe lesen konnten.
shoalmark sammelt diese Fragen, legt sie Ihnen einmal am Tag vor, und jede Antwort ist Ihr eigener, signierter Commit.

## Gemessen, nicht versprochen

In einem Projekt — unserem eigenen —, das shoalmark nutzt:

- **Vorher:** Die letzten 200 Pull Requests wurden ungelesen gemergt, keiner wurde geprüft.
- **Danach, in den ersten 28 Stunden, seit die Regel gilt:** 9 von 13 Pull Requests hatten eine Reviewer-Datei, bevor sie geöffnet wurden.

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
| **Die Agenten Ihres Projekts** | die [Notiz zum Ausprobieren](https://github.com/holgo99/shoalmark/blob/main/ADOPT.de.md): eine Messung, keine Anweisung. Am Ende berichten sie Ihnen, und Sie entscheiden |
| **Ein Agent bei der Arbeit** | der Vertrag ist `tools/shoalmark/README.md` in Ihrem Repository, [hier gerendert](../agents/README.md), auf Englisch – so lesen ihn die Agenten. `llms.txt` liegt im Stammverzeichnis dieser Website |
