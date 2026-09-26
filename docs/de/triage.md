# Ihr Wort in der TRIAGE.md

*Für den Eigner. Fünf Minuten Lesezeit. Sie schreiben es einmal, in Ihren eigenen Worten, und alles Weitere
übernehmen Ihre Agenten.*

Ihre Agenten bringen eine Aufgabe ohne Rückfrage zu Ende, wenn sie zwei Dinge vorher von Ihnen wissen: wofür die
Arbeit da ist und was zuerst kommt. Beides steht in einer einzigen Datei, die Ihre Agenten für Sie anlegen, der
`TRIAGE.md`. Von Ihnen kommen drei Zeilen und eine kurze nummerierte Liste. Daran messen Ihre Agenten jede Bewertung,
und **ändern kann sie nur Ihr signiertes Wort**. Das hält das Werkzeug, bis zu einer Grenze, deren Stärke Sie selbst
wählen; beides steht weiter unten. Im Chat müssen Sie sich nicht wiederholen, denn die Datei sagt es für Sie.

## Was jede Aussage trägt

Zu jeder Aussage auf dieser Seite steht dabei, was sie hält:

| Kennzeichen | Bedeutung |
|---|---|
| **Das Werkzeug** | shoalmark prüft es selbst: Es gibt den Text aus, oder es lehnt den Commit ab. |
| **Das Review** | Ein Reviewer prüft es vor dem Merge gegen den Beleg. Von selbst lehnt nichts ab. |
| **Nur der Text** | Es ist eine geschriebene Regel. Die Agenten halten sich daran, weil sie dasteht; geprüft wird sie nicht. |

## Was in der Datei steht

Die `TRIAGE.md` liegt im Tracker-Verzeichnis, `docs/work-tracker/`, wenn Sie kein anderes gewählt haben. Sie hat drei
Abschnitte, und zwei davon gehören Ihnen.

- **Die Absicht, *für · damit · niemals*.** Das sind drei Zeilen über das Repository als Ganzes, nie über ein
  einzelnes Feature. Sie sagen, wofür es da ist, was gilt, wenn es funktioniert, und was keine Sichtung und kein
  Agent tun darf, um dorthin zu kommen.
- **Der aktuelle Weg.** Diese nummerierte Liste sagt, was zuerst kommt und nach welchen Regeln gearbeitet wird. An
  ihm misst jede Sichtung, was P1, P2 oder P3 ist.
- **Durchgänge.** Hier steht ein Absatz je Sichtung, geschrieben von dem Agenten, der sie gemacht hat. Dieser
  Abschnitt gehört Ihren Agenten.

In einem deutsch eingerichteten Repository heißen die Überschriften `## Die Absicht`, `## Der aktuelle Weg` und
`## Durchgänge`, so wie `examples/de/shoalmark.toml` sie festlegt. In einem englischen Repository heißen sie
`## The intent`, `## The current path` und `## Passes`.

**Ein erster Entwurf: die Dorfbücherei.** Die deutsche Vorlage `examples/de/TRIAGE.md`, die Ihre Agenten vor `--init`
kopieren ([Einrichtung](setup.md), Schritt 2), bringt ein Beispiel in Kursivschrift mit. Dieses Beispiel ist mit
Absicht ein ganzes Produkt. Der Eigner von shoalmark hat einmal einen ersten Entwurf geschrieben, der nur so groß wie
ein einzelnes Feature war, weil ihm ein Agent zuvor ein Beispiel dieser Größe gezeigt hatte (FM-022). Deshalb lautet
das Beispiel so:

> - **für** — *z. B. die ganze Ausleihe einer Dorfbücherei: Mitglieder, Ausleihen, Rückgaben und das Regal in einem Bestand, dem die Bibliothekarin traut*
> - **damit** — *z. B. ein Mitglied ein Buch und die Bibliothekarin ein Mitglied mit einem Blick findet, und nichts Verliehenes verloren geht*
> - **niemals** — *z. B. verleihen, was der Katalog nicht führt, oder die Akte eines Mitglieds löschen, bevor seine letzte Ausleihe zurück ist*

Überschreiben Sie es mit Ihren eigenen Worten.

- **Das Werkzeug.** Eine Sichtung liest alles, was Sie dort schreiben. Sie lässt nur die Einleitung aus und die
  Beispiele, solange diese unverändert sind. Ein unberührtes Beispiel zählt deshalb als *keine Absicht geschrieben*.

## Was eine Änderung bewirkt

Sobald Ihr Commit drin ist, arbeiten Ihre Agenten ab ihrem nächsten Befehl nach den neuen Worten. Dafür braucht es
weder eine Besprechung noch eine Nachricht.

- **Das Werkzeug.** `--next`, der Befehl am Anfang einer Session, gibt Ihren aktuellen Weg aus, noch vor der
  gereihten Arbeit. `INDEX.md` führt ihn wörtlich weit oben, und Ihre Tafel zeigt ihn unter dem, was auf Sie wartet.
- **Das Werkzeug.** `--triage` gibt Ihre Absicht über seinen Regeln aus, mit dem Satz *„Where the mechanics below
  leave you a choice, this decides it"*: Wo die Mechanik eine Wahl lässt, entscheidet Ihre Absicht. Ihren Weg gibt
  es darunter aus, mit der Anweisung *„judge against it"*. Ist kein Weg geschrieben, fängt die Sichtung gar nicht
  erst an: *„tiers cannot be judged; the Owner writes it first"*.
- **Das Review.** Die nächste Sichtung misst jedes offene Arbeitspaket an Ihren neuen Worten. So verlangen es ihre
  Regeln: *„P1 on the current path · P2 next · P3 someday"*. Die Urteile schreibt das Werkzeug. Ob sie Ihren Worten
  folgen, prüft der Reviewer der Sichtung.
- **Das Werkzeug.** Ein *Einwand* ist eine belegte Zeile, die ein Agent unter ein Arbeitspaket schreibt
  (`## Einwände`). Er kann eine Zeile Ihres Wegs als untergraben nennen, etwa `path 5`. Ist der Einwand jünger als
  die letzte Einstufung und nennt er eine Zeile, die Ihr Weg wirklich hat, kommt das Arbeitspaket zurück auf das
  Arbeitsblatt der Sichtung, markiert als RAISED. Nur an dieser Stelle richtet sich eine Prüfung nach Ihrem Weg, und
  zwar nach der Nummer der Zeile, nicht nach ihrem Inhalt.

### Aus shoalmarks eigenem Beleg

Der Beleg von shoalmark ist englisch geführt. Die Zitate bleiben deshalb im Wortlaut.

**Zeile 3 des Wegs, neu geschrieben.** Am 25. September 2026 um 10:37 Uhr hat der Eigner Zeile 3 in einem eigenen,
signierten Commit neu gefasst (`fe36cc0`, `%G?` G). Im selben Commit hat er die Zeilen 1, 2 und 5 umformuliert und
Zeile 6 hinzugefügt. Vorher stand in Zeile 3:

> 3\. A pull request without an independent review's evidence file cannot merge - checked, not asked.

Nachher steht dort:

> 3\. A pull request merges only with a review's evidence file on its head: a Reviewer from another independent
> session for critical changes (critical = a release, the gate or hooks, signing and rights, TRIAGE.md or AGENTS.md
> rules changed by a seat, anything tagged security or P1); inline Reviewer passes on other code; one Reviewer pass
> for documentation; a review of the Owner's own answers and TRIAGE lines reports and never blocks, until FM-007's
> hardware key signs them. The Owner merges on a ready line, or over any other verdict with a signed reason.

Die neue Zeile verlangt für kritische Änderungen einen Reviewer aus einer anderen, unabhängigen Session. Kritisch
sind ein Release, das Gate oder die Hooks, Signatur und Rechte, Regeln in TRIAGE.md oder AGENTS.md, die ein Agent
geändert hat, und alles, was als security oder P1 markiert ist.

- **Das Review.** Noch am selben Tag haben sich die Agenten nach der neuen Zeile gerichtet. Die Sichtung, die
  den CI-Fix aufnahm, schrieb *„the Owner's line 3 names a release critical, so its fix's review is the cold
  session's"* (`42f4eca`), also: Das Review des Fixes gehört der kalten Session. FM-037, der weiter unten beschriebene
  Schutz, wurde vor dem Merge in zwei anderen Sessions geprüft, und `--check` führt beide Urteile als *independent*.
- **Das Werkzeug.** `--check` zeigt an, wie unabhängig die Reviews der Woche waren. Am 26. September 2026 hat es
  bei `88c7b0c` `reviews this week · 104 verdict(s) · independent 10 · same session 89 · untraced 5`
  ausgegeben. Das ist eine Meldung, keine Sperre. Die meisten Urteile dieser Woche kamen aus derselben Session wie die
  Arbeit, und ein solches Urteil wird bisher nicht abgelehnt, weil der zweite Abschnitt von FM-024 noch nicht gebaut
  ist. Die Zeile zeigt Ihnen, was Sie mergen.

**Drei Wörter, eine andere Einstufung.** Am 25. September 2026 war die CI auf dem Release-Tag `v0.18.3` rot. Die erste
Sichtung (`42f4eca`, 12:15 Uhr) hat FM-035 als P1 eingestuft, denn ein rotes Release-Tag sei *„a failed command on the
current path, line 1"*. Ihr Reviewer hat bemerkt, dass das Zitat gekürzt war. Vollständig lautet Zeile 1: *„The daily
sitting runs on a tagged release with a signed answer and no failed command in the sitting."* Die Sichtung wurde neu
gemacht (`c8939e3`, 12:30 Uhr) und kam auf P2: *„the sitting's commands ran green here, so a red CI is not that
command"*. Die Befehle des Standups selbst waren grün gelaufen.

- **Das Review.** Die drei Wörter *in the sitting* haben die Einstufung verschoben. Keine Prüfung richtet sich nach
  dem, was Ihre Worte sagen, und deshalb achtet der Reviewer darauf, dass die Sichtung sich an sie hält. Soll ein
  rotes Release-Tag für Sie P1 sein, schreiben Sie es in Ihren Weg. Es ist Ihre Zeile.

**Ein Einwand, der Ihren Weg nennt.** Am 24. September 2026 hat der Auditor-Sitz zu FM-007 einen Einwand erhoben,
mit einer belegten Zeile. Darin stand, dass der Schlüssel, der die Antworten des Eigners signiert, ein
Software-Schlüssel im gemeinsamen ssh-agent war, den jeder Push eines Agenten ohne Nachfrage benutzte. Die Zeile
endete mit *„undermines: TRIAGE.md path 5"*. Am selben Abend hat eine Sichtung FM-007 neu eingestuft (`29466fc`).
Nach den Befunden ihres Reviewers wurde sie neu gemacht (`c5696c5`) und setzte P1: *„on the current path, line 5: an
answer is written and signed, and the raise shows the signature proves the account, not the hand"*. Die Signatur
beweist also das Konto, nicht die Hand.

- **Nur der Text.** Dass neu eingestuft wird, noch am selben Tag, ist Ihre Regel, Ihre signierte Antwort zu
  FM-033. Eine Sichtung hält sie ein, indem sie an diesem Tag noch läuft.
- **Das Werkzeug**, seit 0.18.3: Ein Einwand, der eine Zeile nennt, die Ihr Weg hat, stellt das Arbeitspaket unter
  *triage*, bis eine Sichtung es neu eingestuft hat. Am 24. September konnte das Werkzeug ein solches Arbeitspaket
  noch nicht auflisten. Der Agent hat die Zeile im Arbeitsblatt deshalb von Hand geschrieben.
- **Das Review.** Die Begründung der neuen Einstufung stammt vom Agenten, und sein Reviewer prüft sie gegen Ihre
  Zeile.

## Nur Sie ändern sie

- **Das Werkzeug.** Auf einem Branch lehnt `--check` jeden Commit ab, der den Text unter *Die Absicht* oder *Der
  aktuelle Weg* ändert, sei es ein Wort, eine Zeile oder nur eine Leerzeile, denn auch Leerraum zählt. Ebenso lehnt
  es einen Commit ab, der diese Überschriften umbenennt oder entfernt, die `TRIAGE.md` löscht oder verschiebt oder
  das Tracker-Verzeichnis woandershin zeigen lässt. Durch kommt nur Ihr signierter Commit: `%G?` G, Ihre E-Mail als
  Signierer, und als Autor der Sitz, der in den `[seats]` des Standard-Branchs das Recht `answer` hält. Bei einem
  Merge zählt nur ein Text, den keiner seiner Eltern hatte.
- **Das Werkzeug.** Der Commit-Hook lehnt einen solchen Commit eines Agenten schon ab, bevor er entsteht, und
  `--queue` liest seinen Pull Request als `wait: TRIAGE.md changed unsigned`.
- **Das Werkzeug.** Auch die Schlüssel, gegen die Ihre Signatur geprüft wird, sind so geschützt. Sie kommen aus der
  Signierer-Datei des Standard-Branchs, nie aus der Kopie eines Branchs. Ein Branch, der seinen eigenen Schlüssel
  unter Ihrer E-Mail einträgt, beweist deshalb nichts.
- **Das Werkzeug.** Die *Durchgänge* bleiben offen für die Agenten, die eine Sichtung festhalten.

**Vorgeführt.** Wir haben das in einem Scratch-Repository ausprobiert, mit dem Werkzeug aus shoalmarks `main`
(`88c7b0c`). Es war deutsch eingerichtet wie in Schritt 2 der Einrichtung, hatte die Dorfbücherei als Absicht und zwei
Zeilen Weg, dazu einen erfundenen Eigner mit Schlüssel und einen Agenten. Nichts davon hat das Scratch-Verzeichnis
verlassen. Auf seinem Branch hat der Agent Zeile 2 des Wegs geändert, von *„Ein Pull Request wird nur gemergt, wenn
auf seinem Kopf die Belegdatei eines Reviews liegt."* zu *„Ein Pull Request wird gemergt, wenn seine Tests grün
sind."* `--check` hat auf diesem Branch mit Exit-Code 4 geendet. Das sind die Zeilen der Ablehnung, so wie das
Werkzeug sie ausgibt. Wie alle seine Meldungen sind sie englisch, nennen aber Ihre deutsche Überschrift. Das Skript
und seine vollständige Ausgabe liegen in den
[Belegen zu FM-006](https://github.com/holgo99/shoalmark/tree/main/work-tracker/evidence/FM-006/triage-page).

```text
  lint: refused: commit aee039e "AP-001: Zeile 2 des Wegs, kürzer" changes the text under `## Der aktuelle Weg` in docs/work-tracker/TRIAGE.md — its author `implementer@seat` is not the Owner (`du@example.org`): not the Owner's signed commit — only the Owner changes his intent and his current path (FM-037). The way through: the Owner commits it signed; a seat proposes the change as an ask — `ask:` in its tracker, one sentence he can answer, with `ask-kind: ruling`, `ask-since:` and `next: owner`
  the limit: a commit signed with the Owner's key passes; at tier 0 any process on his account holds that key (FM-007)
FAILED: 1 ledger-integrity violation(s) — fix the tracker; regenerating will not clear these.
```

Mit installierten Hooks (`--install-hook`) ist die Änderung eines Agenten an der Absicht gar nicht erst entstanden.
Der Hook hat dieselbe Ablehnung für *this commit* ausgegeben und vor der Grenze einen Satz ergänzt: *„the hook proves
the author only: git signs a commit after its hooks have run — `--check` on the branch is the gate, and it judges the
signature"*. Der Hook beweist also nur den Autor, und die Signatur prüft `--check` auf dem Branch.

**Der Weg führt über Sie.** Ein Agent, der eine Zeile geändert haben will, fragt Sie in der Form, die die Ablehnung
nennt (*das Werkzeug*): mit einem `ask:` in seinem Arbeitspaket und `ask-kind: ruling`. Sie antworten auf Ihrer Tafel.
Sind Sie einverstanden, ändern Sie die Zeile selbst: Datei bearbeiten, `git commit -S`, pushen. Danach gibt
`git log -1 --format='%G? %GS %ae'` ein `G` und zweimal Ihre E-Mail aus. Das ist die Probe auf der
[Signaturseite](signing.md).

**Die Grenze** steht in den Worten, mit denen FM-006 sie erfasst hat: *a commit signed with the Owner's key passes,
and at tier 0 any process on his account holds that key.* Ein Commit, der mit dem Schlüssel des Eigners signiert ist,
geht also durch, und auf Stufe 0 hat jeder Prozess unter seinem Konto diesen Schlüssel. Das Werkzeug gibt diesen Satz
nach jeder Ablehnung aus.

- **Das Werkzeug** kann den Unterschied nicht erkennen. Auf Stufe 0 heißt *nur Sie* in Wahrheit *nur Ihr Konto*. Im
  Scratch-Repository ging ein Commit, der mit dem Schlüssel des Eigners ohne Passphrase signiert war, genauso durch
  `--check` wie sein eigener. Erst eine Passphrase bei jeder Signatur (Stufe 2) oder ein Hardware-Schlüssel
  (Stufe 3) macht den Schlüssel allein zu Ihrem. Die vier Stufen stehen auf der [Signaturseite](signing.md).
- **Das Werkzeug.** Ist Ihr Sitz in `[seats]` nicht als `signed` markiert, beweist der Schutz nur den Autor, eine
  Zeichenkette, die jeder tippen kann, und das Werkzeug sagt das auch.
- **Das Werkzeug.** Unter Subversion liegt der Schutz außerhalb seines Umfangs, und das Werkzeug sagt es in einer
  Zeile: Eine Arbeitskopie trägt keine Signatur.

## Was eine Änderung nicht bewirkt

- **Sie ändert keine Prüfung.** Die Ablehnungen des Gates, die Art, wie `--queue` einen Pull Request liest, der
  Aufnahmestopp für neue Arbeitspakete und die Rechte der Sitze stehen im Code des Werkzeugs und in `shoalmark.toml`.
  Zeile 3 verlangt die Belegdatei eines Reviews, und `--queue` verlangt ein Urteil auf dem Kopf, weil sein Code es so
  vorsieht. Streichen Sie Zeile 3, bleibt das so. *Das Werkzeug:* Keine Prüfung richtet sich nach dem Inhalt Ihrer
  Zeilen, nur eine nach ihren Nummern (der Einwand, siehe oben).
- **Sie verschiebt weder Einstufung noch Rang.** Die ändern sich erst bei der nächsten Sichtung, wenn ihr Befehl das
  Arbeitsblatt anwendet. *Das Werkzeug* schreibt sie und lehnt einen Agenten ohne das Recht `triage` ab. Dass kein
  Agent sie von Hand ändert, trägt *nur der Text*. Bis dahin zeigt Ihre Tafel das alte Urteil.
- **Sie beantwortet keine Frage.** Eine Frage auf Ihrer Tafel beantworten Sie mit `--answer`, signiert (*das
  Werkzeug*). Eine Änderung an der `TRIAGE.md` beantwortet nichts, und ein Merge oder ein Klick ebenso wenig. Dass
  kein Agent so etwas als Ihre Antwort nimmt, steht in einer Zeile des Wegs, bei shoalmark selbst in Zeile 5, und das
  trägt *nur der Text*: Das Werkzeug kann nicht verhindern, dass ein Agent einen Klick als Ihr Wort liest.
- **Sie erreicht keinen älteren Branch.** *Das Werkzeug* liest die Datei in dem Checkout, in dem es läuft. Ein Agent
  auf einem Branch von vorher liest Ihre alten Zeilen, bis sein Branch Ihren Commit aufnimmt.
- **Sie schreibt keine frühere Sichtung um.** Jede Sichtung wurde an den Worten ihres Tages gemessen. *Das Werkzeug*
  schreibt jede neue Sichtung in ein Arbeitsblatt ihres eigenen Tages, sodass ein früheres bleibt, wie es war, und
  git behält Ihren alten Text.
