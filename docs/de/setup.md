# In zehn Minuten eingerichtet

*Für die Person, der das Repository gehört. Python 3.9 oder neuer ist die einzige Voraussetzung.*

## 1. Das Werkzeug ins Repository legen

```
git clone https://github.com/holgo99/shoalmark ~/shoalmark      # einmal, irgendwo
cd <Ihr Repository>
python3 ~/shoalmark/shoalmark.py --vendor tools/shoalmark
```

`tools/shoalmark/` ist jetzt eine festgehaltene Kopie: acht Dateien und ein `PIN` mit ihren Prüfsummen. Sie aktualisiert
sich nie selbst; `--vendor` erneut ausführen holt eine neuere und druckt, was sich geändert hat. Unter Windows heißt der
Befehl `python`, nicht `python3`.

## 2. Deutsch, dann einrichten

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
  kennt keinen Client-Hook — der Vertrag sagt den Agenten, das Werkzeug vor jedem `svn commit` laufen zu lassen. Für ein
  Gate, das niemand umgehen kann: `--check` aus dem `pre-commit`-Hook Ihres Servers.

## 4. Sagen, wer antwortet

In `shoalmark.toml`:

```
answerers = ["ihrname signed"]     # git — siehe „Ihre Antwort ist Ihr Commit“
answerers = ["ihrname"]            # Subversion — der Server kennt Sie schon
```

## 5. Zwei Dinge schreiben, die nur Sie können

`docs/work-tracker/TRIAGE.md` öffnen. **Die Absicht** — *für · damit · niemals*, in Ihren Worten — und **der aktuelle
Weg**: was zuerst kommt. Agenten lesen beides vor jeder Bewertung. Alles andere überlassen Sie ihnen.

## 6. Die Tafel öffnen

`docs/work-tracker/index.html` — sie ist git-ignoriert und wird bei jedem Commit und Checkout neu gebaut. Ihre erste
Zeile ist, was Sie braucht. `standup = "09:00"` in `shoalmark.toml`, und `--standup kalender.ics` schreibt die Einladung.

Das ist alles. Die Agenten legen die Arbeit an; Sie beantworten, was nur Sie können.
