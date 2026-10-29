---
description: "Eine Woche mit shoalmark in vier Schritten: dein Teil daran, was es nicht tut und wie du es mit deinen Agenten ausprobierst."
---

# So funktioniert's

shoalmark legt die Arbeit deines Projekts als Textdateien im Projekt selbst ab, sodass jeder Agent, der daran arbeitet, denselben aktuellen Stand liest. Es zeigt dir zuerst, was auf deine Antwort wartet, und seine Prüfungen melden Arbeit, die als ausgeliefert markiert ist, wenn keine gespeicherte Änderung (ein Commit) in der Historie des Projekts dahintersteht.

## Eine Woche in vier Schritten

**Was dein Wort braucht, wartet darauf; kein Agent antwortet für dich.**

1. **Die Agenten arbeiten und halten fest, wo die Arbeit steht.** Jedes Arbeitspaket ist eine Markdown-Datei mit dem, was jetzt gilt, und dem nächsten Schritt. Einen Wechsel zu *Shipped* ohne Commit dahinter melden die Prüfungen.
2. **Was nur du entscheiden kannst, wird zu einer Frage.** Braucht ein Agent deine Entscheidung, schreibt er sie als einen Satz auf, mit den Optionen und seinem Vorschlag, und macht mit anderer Arbeit weiter. Zwischen den Stand-ups unterbricht dich niemand, außer für etwas, das sich nicht rückgängig machen lässt.
3. **Du setzt dich dran, wann immer es dir passt.** Das Stand-up gibt die Tagesordnung aus: zuerst deine Entscheidungen, jede mit ihrer Wartezeit und dem, was sie aufhält. Du antwortest mit einem Befehl pro Frage; er schreibt deine Antwort als Commit, mit deinem Schlüssel signiert, sobald du das Signieren einschaltest.
4. **Die Agenten handeln auf deine Antwort, und ein Reviewer urteilt vor dem Merge.** Eine Rolle mit dem Recht dazu hält deine Antwort im Arbeitspaket fest und macht weiter. Bevor Arbeit zu einem Merge kommt, prüft sie ein Reviewer; das Board sagt, ob dessen Durchgang unabhängig war, also aus einer anderen Session kam als der Code. Das ist eine Meldung, kein Beweis. `--queue` zeigt die offenen Pull Requests in der Reihenfolge, in der sie zu mergen sind.

<figure class="week" markdown="0">
<div class="week-card"><h3 class="t">FM-024</h3><p class="src">work-tracker/FM-024-….md · 2026-09-28</p>
<pre lang="en">next: owner
ask: "Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "all three: --statusline, … | the status line only: … | the rule only: …"
ask-proposal: "all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</pre></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card board"><h3 class="t">Board</h3>
<div class="wk-board" lang="en"><p><i>##</i> <b class="hot">waiting for you: 3</b></p>
<p><span class="id">FM-024</span> Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them? · a ruling <span class="chip">accept</span><span class="chip">reject</span></p></div></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card"><h3 class="t">4127dba</h3><p class="src">git commit · 2026-09-28</p>
<pre lang="en"><span class="del">-next: owner</span>
<span class="add">+next: build</span>
<span class="add">+answer: "accepted - all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</span>
<span class="add">+answered: 2026-09-28</span>
<span class="add">+answered-by: …</span></pre></div>
<figcaption>Aus shoalmarks eigenem Repository: eine Frage, vom Arbeitspaket über das Board bis zur Antwort des Eigners – ein signierter Commit, der im Arbeitspaket drei Zeilen hinzufügt und <code>next</code> von <code>owner</code> auf <code>build</code> setzt. Die Auszüge sind wörtlich und bleiben deshalb englisch; jedes … markiert einen Schnitt.</figcaption>
</figure>

**Nicht alles braucht dich.** Eine Rolle, die das Recht zum Schließen hat, schließt Arbeit ab, ohne dich zu fragen. Mit dem Werkzeug ausgeliefert sind drei Rollen mit festen Rechten: planner darf fragen, schließen und sichten, reviewer sichten, builder nichts. Für jede weitere Rolle legst du die Rechte selbst fest. Antworten darf nur, wem du das Recht dazu gibst, und standardmäßig bist das nur du.

**Wie fest „kein Agent antwortet für dich“ gilt, bestimmt deine Signatur.** Eine Signatur beweist den Schlüssel, nicht die Hand: Wer deinen Schlüssel benutzen kann, kann in deinem Namen antworten. Es gibt vier Stufen, von einem Schlüssel, den alles unter deinem Konto benutzen kann, bis zu einem, der deine Berührung braucht. [Deine Antwort ist dein Commit](signing.md) hilft dir bei der Wahl.

## Dein Teil

- **Einmal:** Du schreibst in die `TRIAGE.md` drei Zeilen in deinen eigenen Worten (wofür das Repository da ist, was gilt, wenn es funktioniert, und was niemand tun darf, um dorthin zu kommen) und den aktuellen Weg, also was zuerst kommt. Dazu richtest du einmal deine Signatur ein, in etwa zehn Minuten.
- **Jede Woche:** ein Stand-up, wann immer es dir passt, und ein Befehl pro Antwort.
- **Der Rest steht auf dem Board:** Deine Agenten sind angehalten, jede Session mit dem zu beenden, was auf dich wartet, und das Board stellt es ganz oben hin.

## Was shoalmark nicht tut

- Es prüft deinen Code nicht auf Sicherheitsprobleme und sucht nicht nach Datenlecks.
- Es beweist nicht, dass Arbeit richtig ist. Seine Prüfungen melden einen Wechsel zu *Shipped* ohne Commit dahinter; ob dieser Commit seinen Zweck erfüllt, klärt ein Review.
- Es ist kein Migrationswerkzeug: Es importiert kein Ticketsystem und beginnt mit der eigenen Arbeit deines Repositorys.
- Es passt heute zu Projekten, in denen eine Person das Sagen hat. Mehrere Menschen, die das Sagen haben, sind in dieser Beta nicht getestet.
- Es braucht Python 3.9 oder neuer; ein git-Repository braucht ein installiertes `git`. Unter Subversion läuft es ohne installiertes `git`, aus dem Release-Archiv, und jeder Lauf sagt dort, was er nicht prüfen kann: Commit-Signaturen und vom Server authentifizierte Autoren.
  Es braucht keinen eigenen Server, keine eigene Datenbank und kein eigenes Konto.

## Ausprobieren

--8<-- "how-it-works.de.md"

## Weiterlesen

- [In zehn Minuten eingerichtet](setup.md)
- [Deine Antwort ist dein Commit](signing.md)
- [Dein Wort in der TRIAGE.md](triage.md)
- [Das Stand-up](standup.md)
