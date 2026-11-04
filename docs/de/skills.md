# Die Drift-Skills — find-drift und prune-drift

*Zwei Agenten-Skills aus shoalmark, in einem eigenen Repository, [shoalmark/skills](https://github.com/shoalmark/skills),
als ein Plugin für Claude Code und Codex gepackt.*

## Was sie tun

- **find-drift** liest das Repository und findet, wo ein Agent vom Kurs abkommen könnte: Regeln, die nur als Prosa
  festgehalten sind, Quellen, die einander widersprechen, und veralteter Text, der sich noch wie gültig liest. Er ordnet,
  was zu einer Prüfung werden kann. Er schreibt einen Bericht und dessen Prüfsumme und committet nichts.
- **prune-drift** arbeitet auf einem neuen Branch, ausgehend vom Bericht von find-drift. Er entfernt festgehaltenen
  Verlauf aus Kommentaren und ungelesenen Docstrings in Code, den git verfolgt, mit einem Beweis, dass der Code derselbe
  bleibt, und hält fehlende Begründungen zuerst fest. Der Beweis deckt Python ab; eine Datei, die er nicht abdecken
  kann, bleibt unverändert und wird genannt.

## Was sie brauchen

Ein beliebiges git-Repository, ohne lokale Änderungen, frühere Berichte ausgenommen. shoalmark brauchst du nicht: Keiner
der beiden Skills führt es aus. Hat das Repository eine `shoalmark.toml`, nutzen beide sie, und die Berichte landen in
`evidence/drift/` im Tracker-Ordner; ohne sie fragt find-drift, wohin er schreiben soll. Keiner der beiden nutzt das
Netz oder führt deine Tests aus.

## Installieren

Jede Installation ist auf einen Release-Tag von shoalmark/skills festgelegt.

**Claude Code:**

```text
/plugin marketplace add shoalmark/skills@SKILLS-TAG-PENDING
/plugin install shoalmark@shoalmark
```

**Codex:**

```text
codex plugin marketplace add shoalmark/skills@SKILLS-TAG-PENDING
```

Starte dann die ChatGPT-Desktop-App neu, öffne das Plugins Directory, wähle den Marketplace shoalmark und installiere
daraus shoalmark.

## Benutzen

In Claude Code heißen die Skills des Plugins `/shoalmark:find-drift` und `/shoalmark:prune-drift`. In Codex erwähnst du
einen Skill mit `$`: `$find-drift` und `$prune-drift`.

### find-drift

**Frag** vor einem Release oder bevor du Prosa kürzt: `/shoalmark:find-drift`, in Codex `$find-drift`. Hat sich eine
Regel oder eine Entscheidung geändert, bitte um einen begrenzten Lauf über die Quellen, die sie berührt.

**Zurück kommt** ein Bericht, `<tracker folder>/evidence/drift/<date>-<short sha>.md`, daneben seine SHA-256 in
`<file>.sha256`: die gefundenen Regeln, jede danach eingestuft, wie sie durchgesetzt wird, die zehn, die zuerst stärker
durchgesetzt werden sollten, die Widersprüche und der veraltete Text. Seine letzte Nachricht nennt jeden Widerspruch und
jeden veralteten Text in einer Zeile, fragt, ob sie als Fragen erfasst werden sollen, und nennt den nächsten Schritt:
prune-drift.

### prune-drift

**Frag** nach find-drift oder wenn du Prosa kürzen willst: `/shoalmark:prune-drift`, in Codex `$prune-drift`. Er braucht
einen Bericht, dessen Quellen sich seither nicht geändert haben; ist keiner aktuell, lässt er zuerst find-drift laufen.

**Zurück kommt** ein neuer Branch, nie dein Standard-Branch: zuerst die fehlenden Begründungen, festgehalten in einem
eigenen Commit; ein Commit, der den abgestimmten Verlauf löscht, mit der Ausgabe des Beweises in seiner Nachricht;
veralteter Text, korrigiert in eigenen Commits, nur wo eine spätere Quelle ihn klärt. Sein Bericht,
`<date>-<short sha>-prune.md`, und dessen SHA-256 landen im selben Ordner. Seine letzte Nachricht listet auf, was deine
Entscheidung braucht, fragt, ob es als Fragen erfasst werden soll, und fragt, ob die Tests und die CI deines Repositorys
laufen sollen: Er selbst führt keine davon aus.

## Die Sprache des Berichts

Die Prosa des Berichts und das Gespräch folgen deiner Sprache: der Sprache des Boards, `lang` in der
`<tracker dir>/brand/labels.yaml` des Repositorys, wo diese Datei sie setzt, sonst der Sprache, in der du schreibst. Ein
`lang`, das die eigene Prüfung von shoalmark nicht besteht, gilt als nicht gesetzt. Die Abschnittsschlüssel des Berichts
und seine Dateinamen bleiben, wie sie sind, damit prune-drift liest, was find-drift geschrieben hat. **Grenze:** Das
Board liest `labels.yaml` an drei Orten, und der spätere gewinnt: im `brand/` der festgeschriebenen Kopie, in
`<tracker dir>/brand/` des Repositorys und in deinem `~/.config/shoalmark/`. Ein Skill liest nur die Datei des
Repositorys; wo das Board `lang` aus der Datei der festgeschriebenen Kopie oder aus deiner nimmt, kann die Sprache des
Berichts von der des Boards abweichen.

## Der Weg zu shoalmark

Die Skills stammen aus shoalmark, einem Arbeits-Tracker, der in dem Repository lebt, das er verfolgt, und zuerst zeigt,
was auf dich wartet.

- [Warum shoalmark?](warum-shoalmark.md)
- [In zehn Minuten eingerichtet](setup.md)
- [Das Rückmeldeformular](https://shoalmark.tools/feedback), für das, was die Skills gefunden haben oder was im Weg
  stand. Was du dort absendest, ist öffentlich, unter deinem GitHub-Namen.
