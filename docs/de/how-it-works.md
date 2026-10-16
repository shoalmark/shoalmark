---
description: "Eine Woche mit shoalmark in vier Schritten: Ihr Teil daran, was es nicht tut und wie Sie es mit Ihren Agenten ausprobieren."
---

# So funktioniert's

shoalmark legt die Arbeit Ihres Projekts als Textdateien im Projekt selbst ab, sodass jeder Agent, der daran arbeitet, denselben aktuellen Stand liest. Es zeigt Ihnen zuerst, was auf Ihre Antwort wartet, und lässt Arbeit nur dann als „fertig“ gelten, wenn eine gespeicherte Änderung (ein Commit) im Verlauf des Projekts dahintersteht.

## Eine Woche in vier Schritten

**Was Ihr Wort braucht, wartet darauf; kein Agent antwortet für Sie.**

1. **Die Agenten arbeiten und halten fest, wo die Arbeit steht.** Jedes Arbeitspaket ist eine Markdown-Datei mit dem, was jetzt gilt, und dem nächsten Schritt. Ein „fertig“ ohne Commit dahinter lehnt das Gate ab.
2. **Was nur Sie entscheiden können, wird zu einer Frage.** Braucht ein Agent Ihre Entscheidung, schreibt er sie als einen Satz auf, mit den Optionen und seinem Vorschlag, und macht mit anderer Arbeit weiter. Zwischen den Standups unterbricht Sie niemand, außer für etwas, das sich nicht rückgängig machen lässt.
3. **Einmal am Tag sitzen Sie.** Zu der Uhrzeit, die Sie gewählt haben, gibt das Standup die Tagesordnung aus: zuerst Ihre Entscheidungen, jede mit ihrer Wartezeit und dem, was sie aufhält. Sie antworten mit einem Befehl pro Frage; er schreibt die Antwort, signiert sie mit Ihrem Schlüssel und pusht sie.
4. **Die Agenten handeln auf Ihre Antwort, und ein Reviewer urteilt vor dem Merge.** Ein Sitz mit dem Recht dazu hält Ihre Antwort im Arbeitspaket fest und macht weiter. Bevor Arbeit zu einem Merge kommt, prüft sie ein Reviewer; die Tafel sagt, ob dessen Durchgang unabhängig war, also aus einer anderen Session kam als der Code. Das ist eine Meldung, kein Beweis. `--queue` zeigt die offenen Pull Requests in der Reihenfolge, in der sie zu mergen sind.

<figure class="week" markdown="0">
<div class="week-card"><h3 class="t">FM-024</h3><p class="src">work-tracker/FM-024-….md · 2026-09-28</p>
<pre lang="en">next: owner
ask: "Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "all three: --statusline, … | the status line only: … | the rule only: …"
ask-proposal: "all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</pre></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card board"><h3 class="t">Tafel</h3>
<div class="wk-board" lang="en"><p><i>##</i> <b class="hot">waiting for you: 3</b></p>
<p><span class="id">FM-024</span> Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them? · a ruling <span class="chip">accept</span><span class="chip">reject</span></p></div></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card"><h3 class="t">4127dba</h3><p class="src">git commit · 2026-09-28</p>
<pre lang="en"><span class="del">-next: owner</span>
<span class="add">+next: build</span>
<span class="add">+answer: "accepted - all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</span>
<span class="add">+answered: 2026-09-28</span>
<span class="add">+answered-by: …</span></pre></div>
<figcaption>Aus shoalmarks eigenem Repository: eine Frage, vom Arbeitspaket über die Tafel bis zur Antwort des Eigners – ein signierter Commit, der im Arbeitspaket drei Zeilen hinzufügt und <code>next</code> von <code>owner</code> auf <code>build</code> setzt. Die Auszüge sind wörtlich und bleiben deshalb englisch; jedes … markiert einen Schnitt.</figcaption>
</figure>

**Nicht alles braucht Sie.** Ein Sitz, der das Recht zum Schließen hat, schließt Arbeit ab, ohne dass Sie gefragt werden. Mit dem Werkzeug ausgeliefert sind drei Sitze mit festen Rechten: planner darf fragen, schließen und sichten, reviewer sichten, builder nichts. Für jeden weiteren Sitz legen Sie die Rechte selbst fest. Antworten darf nur, wem Sie das Recht dazu geben, und standardmäßig sind das nur Sie.

**Wie fest „kein Agent antwortet für Sie“ gilt, bestimmt Ihre Signatur.** Eine Signatur beweist den Schlüssel, nicht die Hand: Wer Ihren Schlüssel benutzen kann, kann als Sie antworten. Es gibt vier Stufen, von einem Schlüssel, den alles unter Ihrem Konto benutzen kann, bis zu einem, der Ihre Berührung braucht. [Ihre Antwort ist Ihr Commit](signing.md) hilft bei der Wahl.

## Ihr Teil

- **Einmal:** Sie schreiben in die `TRIAGE.md` drei Zeilen in Ihren eigenen Worten (wofür das Repository da ist, was gilt, wenn es funktioniert, und was niemand tun darf, um dorthin zu kommen) und den aktuellen Weg, also was zuerst kommt. Dazu richten Sie einmal Ihre Signatur ein, in etwa zehn Minuten.
- **Jede Woche:** ein Standup je Werktag, fünfzehn Minuten zu der Uhrzeit, die Sie gewählt haben (so steht es in der Kalendereinladung; die Dauer lässt sich einstellen), und ein Befehl pro Antwort.
- **Der Rest kommt zu Ihnen:** Die letzte Nachricht jeder Session endet mit dem, was auf Sie wartet. Sie müssen nichts öffnen.

## Was shoalmark nicht tut

- Es prüft Ihren Code nicht auf Sicherheitsprobleme und sucht nicht nach Datenlecks.
- Es beweist nicht, dass Arbeit richtig ist. Das Gate lehnt ein „fertig“ ohne Commit dahinter ab; ob dieser Commit seinen Zweck erfüllt, klärt ein Review.
- Es ist kein Migrationswerkzeug: Es importiert kein Ticketsystem und beginnt mit der eigenen Arbeit Ihres Repositorys.
- Es passt heute zu Projekten, in denen eine Person das Sagen hat. Mehrere Menschen, die das Sagen haben, sind in dieser Beta nicht getestet.
- Es braucht Python 3.9 oder neuer und ein installiertes `git` — heute auch unter Subversion.
  Es braucht keinen eigenen Server und kein eigenes Konto.

## Ausprobieren

--8<-- "how-it-works.de.md"

## Weiterlesen

- [In zehn Minuten eingerichtet](setup.md)
- [Ihre Antwort ist Ihr Commit](signing.md)
- [Ihr Wort in der TRIAGE.md](triage.md)
- [Der Standup](standup.md)
