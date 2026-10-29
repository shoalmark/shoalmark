# In zehn Minuten eingerichtet

*Für die Person, der das Repository gehört. Es braucht Python 3.9 oder neuer; ein git-Repository braucht ein installiertes `git`. Unter Subversion läuft es ohne installiertes `git`, aus dem Release-Archiv, und jeder Lauf sagt dort, was er nicht prüfen kann: Commit-Signaturen und vom Server authentifizierte Autoren.*

## 1. Das Werkzeug ins Repository legen

```
git clone --branch v0.20.1 https://github.com/shoalmark/shoalmark ~/shoalmark   # ein Release: das, mit dem diese Seite erscheint, sauber geklont
cd <dein Repository>
python3 ~/shoalmark/shoalmark.py --vendor tools/shoalmark
```

`tools/shoalmark/` ist jetzt eine festgeschriebene Kopie: acht Dateien und ein `PIN` mit ihren Prüfsummen. Seine
erste Zeile sagt, aus welchem Release die Kopie stammt. `--vendor` übernimmt nur ein Release, das ganze Werkzeug genau
auf seinem Git-Tag und ohne lokale Änderungen, und lehnt alles andere ab, ohne eine Datei zu schreiben. Die Kopie
aktualisiert sich nie selbst: Du holst einen neueren Git-Tag und rufst `--vendor` erneut auf, und es zeigt dir, was
sich geändert hat. Unter Windows heißt der Befehl `python`, nicht `python3`.

## 2. Auf Deutsch umstellen, dann einrichten

Zuerst die vier Dateien aus `examples/de/` kopieren — `shoalmark.toml` (die Abschnittsnamen auf Deutsch), `TEMPLATE.md`,
`TRIAGE.md`, `brand/labels.yaml` —, den Namen und den Schlüssel in `shoalmark.toml` anpassen, dann:

```
python3 tools/shoalmark/shoalmark.py --init --key AP
```

`AP` ist dein Id-Präfix — Arbeitspakete heißen `AP-001`, `AP-002` … Kurz, und nach dem Projekt benannt, nicht nach einer
Art von Arbeit. Der Befehl schreibt `TRIAGE.md`, den Vertrag für Agenten in `AGENTS.md` und einen `CLAUDE.md`-Verweis.
Nichts wird überschrieben.

## 3. Das Gate verdrahten

```
python3 tools/shoalmark/shoalmark.py --install-hook
```

- **git:** einfache Hooks — der Index wird bei jedem Commit erzeugt und geprüft; ein Arbeitspaket, das sich widerspricht, wird abgelehnt.
- **Subversion:** die TortoiseSVN-Hook-Eigenschaften und `svn:ignore` für das Board. Die Subversion-Kommandozeile
  kennt keinen Client-Hook — der Vertrag sagt den Agenten, das Werkzeug vor jedem `svn commit` laufen zu lassen.
  `--check` nach dem Commit beurteilt ihn.

Ein Hook-Lauf und der Board-Lauf mit `--html-only` sind standardmäßig auf 60 s begrenzt; `SHOALMARK_BOARD_SECONDS` setzt die Grenze.
Ausdrückliche Befehle einer Person wie `--answer` und `--check` sind unbegrenzt, auch mit der Hook-Kopie.
Alle bisherigen Beschränkungen der Kopie bleiben bestehen. Für die Laufzeit liest das Werkzeug die geparsten Argumente:
Hook-Modi (`--session-check`, `--session-trailer`, `--commit-msg`, `--print-written`, `--tsvn-hook`, `--html-only`)
bleiben auch in gemischten Befehlen begrenzt. Ein einfacher, unbekannter oder fehlerhafter Aufruf der Kopie ist mehrdeutig
und bleibt begrenzt, auch von Hand.

## 4. Sagen, wer antwortet — und wer die Agenten sind

In `shoalmark.toml`:

```
owner = "sie@example.org signed"          # du, der Eigner — keine Rolle: deine Antworten sind signierte Commits, siehe „Deine Antwort ist dein Commit“

[seats]
planner     = "planner@seat"              # die Rollen der Agenten, jede mit eigener Identität
builder     = "builder@seat"
reviewer    = "reviewer@seat"
```

`owner` steht oben in der Datei, vor jeder Tabelle: Eine Zeile unter einer Tabellen-Kopfzeile gehört zu dieser Tabelle, und das
Werkzeug lehnt sie in jeder Tabelle außer `[seats]` ab, wo `owner` als alte Schreibweise weiter gilt. Unter Subversion steht für den Eigner (`owner`) dein Server-Konto, ohne `signed`: Der Server kennt dich schon. Jede Rolle committet unter
ihrer eigenen Identität, einmal in ihrem eigenen Worktree eingestellt
(`git config --worktree user.email builder@seat`), und hat nur ihre eigenen Rechte: Der Eigner (`owner`) antwortet, der
Planner fragt, schließt und sichtet, der Reviewer sichtet, der Builder baut. Die Rollen stehen unter `[seats]` und heißen `planner` und `builder`; `principal` und `implementer`, ihre früheren Namen, gelten weiter und haben dieselben Rechte. Das ältere
`answerers = ["ihrname"]` gilt weiter, wo es weder `owner` noch `[seats]` gibt. Eine Identität mit `signed` ist eine
E-Mail-Adresse und wird über SSH geprüft (siehe „Deine Antwort ist dein Commit“); jede andere lehnt das Werkzeug schon beim
Lesen der Konfiguration ab.

**Sessions.** Neben seiner Rolle trägt jeder Worktree eines Agenten `seat.session`, also den Lauf, zu dem er gehört,
und der Hook von `--install-hook` hängt ihn an jeden Commit an: `Session: <id>`, daneben den Worktree. Das Gate lehnt
den Commit einer Rolle ab, der keine Session dieser Rolle trägt; `--sessions` liest allein aus diesen Zeilen ab, wer
was wann und wo gemacht hat, und das Board zeigt, wer am letzten Tag gearbeitet hat. Das erledigen deine Agenten.
Deine eigenen Commits tragen keine Session: Deine Signatur ist dein Ausweis.

## 5. Zwei Dinge schreiben, die nur du kannst

`docs/work-tracker/TRIAGE.md` öffnen. **Die Absicht** — *für · damit · niemals*, in deinen Worten — und **der aktuelle
Weg**: was zuerst kommt. Agenten lesen beides vor jeder Bewertung. Alles andere überlässt du ihnen.

## 6. Das Board öffnen

`docs/work-tracker/index.html` — es ist git-ignoriert und wird neu gebaut, wenn das Werkzeug läuft, bei einem Commit, der ein
Arbeitspaket ändert, und gleich nach jeder deiner Antworten und Handlungen. Unter git bauen `post-checkout`, `post-merge` und
`post-rewrite` es auch nach einem Checkout oder Wechsel, einem Merge (einschließlich eines Pulls mit Fast-Forward) oder einem
Rebase neu: aus der Kopie der Hooks, mit `--html-only`. Führe `--install-hook` erneut aus, um die von v0.20.0 entfernten
Hooks wieder einzurichten. Das Board sagt, was es gelesen hat und wann. Seine erste Zeile zeigt, was auf dich wartet.
Unter Subversion wird es bei einem Commit über TortoiseSVN oder beim Lauf des Werkzeugs neu gebaut; nach `svn update`
führst du `--html-only` aus.

**Grenze:** git hat keinen Hook nach einem bloßen `git fetch`. Kommt ein Antwort-Branch allein durch Fetch an, bleibt die
Anzeige *unterwegs* auf dem Board wie zuvor, bis zu einem Checkout, einem Merge oder `--html-only`.

Wenn du eine feste Uhrzeit für dein Stand-up willst, setze `standup = "09:00"` in `shoalmark.toml`. Ohne sie hältst du das Stand-up, wann immer es dir passt: siehe [Das Stand-up](standup.md).

Das ist alles. Die Agenten legen die Arbeit an; du beantwortest, was nur du kannst.

*Diese Seiten, gebaut mit `zensical build`, lassen sich direkt aus `site/index.html` öffnen — oder lokal bereitstellen, die Suche braucht das:* `python3 -m http.server -d site 8000`.
