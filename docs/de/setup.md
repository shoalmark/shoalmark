# In zehn Minuten eingerichtet

*Für die Person, der das Repository gehört. Python 3.9 oder neuer ist die einzige Voraussetzung.*

## 1. Das Werkzeug ins Repository legen

```
git clone --branch v0.19.0 https://github.com/shoalmark/shoalmark ~/shoalmark   # ein Release: das, mit dem diese Seite erscheint, sauber geklont
cd <Ihr Repository>
python3 ~/shoalmark/shoalmark.py --vendor tools/shoalmark
```

`tools/shoalmark/` ist jetzt eine festgeschriebene Kopie: acht Dateien und ein `PIN` mit ihren Prüfsummen. Seine
erste Zeile sagt, aus welchem Release die Kopie stammt. `--vendor` übernimmt nur ein Release, das ganze Werkzeug genau
auf seinem Git-Tag und ohne lokale Änderungen, und lehnt alles andere ab, ohne eine Datei zu schreiben. Die Kopie
aktualisiert sich nie selbst: Sie holen einen neueren Git-Tag und rufen `--vendor` erneut auf, und es zeigt Ihnen, was
sich geändert hat. Unter Windows heißt der Befehl `python`, nicht `python3`.

## 2. Auf Deutsch umstellen, dann einrichten

Zuerst die vier Dateien aus `examples/de/` kopieren — `shoalmark.toml` (die Abschnittsnamen auf Deutsch), `TEMPLATE.md`,
`TRIAGE.md`, `brand/labels.yaml` —, den Namen und den Schlüssel in `shoalmark.toml` anpassen, dann:

```
python3 tools/shoalmark/shoalmark.py --init --key AP
```

`AP` ist Ihr Id-Präfix — Arbeitspakete heißen `AP-001`, `AP-002` … Kurz, und nach dem Projekt benannt, nicht nach einer
Art von Arbeit. Der Befehl schreibt `TRIAGE.md`, den Vertrag für Agenten in `AGENTS.md` und einen `CLAUDE.md`-Verweis.
Nichts wird überschrieben.

## 3. Das Gate verdrahten

```
python3 tools/shoalmark/shoalmark.py --install-hook
```

- **git:** einfache Hooks — der Index wird bei jedem Commit erzeugt und geprüft; ein Arbeitspaket, das sich widerspricht, wird abgelehnt.
- **Subversion:** die TortoiseSVN-Hook-Eigenschaften und `svn:ignore` für die Tafel. Die Subversion-Kommandozeile
  kennt keinen Client-Hook — der Vertrag sagt den Agenten, das Werkzeug vor jedem `svn commit` laufen zu lassen.
  `--check` nach dem Commit ist das Gate.

## 4. Sagen, wer antwortet — und wer die Agenten sind

In `shoalmark.toml`:

```
owner = "sie@example.org signed"          # Sie, der Eigner — kein Sitz: Ihre Antworten sind signierte Commits, siehe „Ihre Antwort ist Ihr Commit“

[seats]
planner     = "planner@seat"              # die Sitze der Agenten, jeder mit eigener Identität
builder     = "builder@seat"
reviewer    = "reviewer@seat"
```

`owner` steht oben in der Datei, vor jeder Tabelle: Eine Zeile unter einer Tabellen-Kopfzeile gehört zu dieser Tabelle, und das
Werkzeug lehnt sie in jeder Tabelle außer `[seats]` ab, wo `owner` als alte Schreibweise weiter gilt. Unter Subversion steht für den Eigner (`owner`) Ihr Server-Konto, ohne `signed`: Der Server kennt Sie schon. Jeder Sitz committet unter
seiner eigenen Identität, einmal in seinem eigenen Worktree eingestellt
(`git config --worktree user.email builder@seat`), und hat nur seine eigenen Rechte: Der Eigner (`owner`) antwortet, der
Planner fragt, schließt und sichtet, der Reviewer sichtet, der Builder baut. Die Sitze heißen `planner` und `builder`; `principal` und `implementer`, ihre früheren Namen, gelten weiter und haben dieselben Rechte. Das ältere
`answerers = ["ihrname"]` gilt weiter, wo es weder `owner` noch `[seats]` gibt. Eine Identität mit `signed` ist eine
E-Mail-Adresse und wird über SSH geprüft (siehe „Ihre Antwort ist Ihr Commit“); jede andere lehnt das Werkzeug schon beim
Lesen der Konfiguration ab.

**Sessions.** Neben seinem Sitz trägt jeder Worktree eines Agenten `seat.session`, also den Lauf, zu dem er gehört,
und der Hook von `--install-hook` hängt ihn an jeden Commit an: `Session: <id>`, daneben den Worktree. Das Gate lehnt
den Commit eines Sitzes ohne eine Session seines eigenen Sitzes ab; `--sessions` liest allein aus diesen Zeilen ab, wer
was wann und wo gemacht hat, und die Tafel zeigt, wer am letzten Tag gearbeitet hat. Das erledigen Ihre Agenten.
Ihre eigenen Commits tragen keine Session: Ihre Signatur ist Ihr Ausweis.

## 5. Zwei Dinge schreiben, die nur Sie können

`docs/work-tracker/TRIAGE.md` öffnen. **Die Absicht** — *für · damit · niemals*, in Ihren Worten — und **der aktuelle
Weg**: was zuerst kommt. Agenten lesen beides vor jeder Bewertung. Alles andere überlassen Sie ihnen.

## 6. Die Tafel öffnen

`docs/work-tracker/index.html` — sie ist git-ignoriert und wird bei jedem Commit neu gebaut, mit git auch bei jedem Checkout und
Merge; unter Subversion bei einem Commit über TortoiseSVN oder wenn das Werkzeug läuft. Ihre erste Zeile zeigt, was auf Sie wartet. `standup = "09:00"` in `shoalmark.toml`, und `--standup kalender.ics` schreibt die Einladung.

Das ist alles. Die Agenten legen die Arbeit an; Sie beantworten, was nur Sie können.

*Diese Seiten, gebaut mit `zensical build`, lassen sich direkt aus `site/index.html` öffnen — oder lokal bereitstellen, die Suche braucht das:* `python3 -m http.server -d site 8000`.
