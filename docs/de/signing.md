# Ihre Antwort ist Ihr Commit — eine Signatur einrichten

*Für den Owner. Zehn Minuten, einmal. Jeder Schritt hier ist das, was die Testsuite des Werkzeugs selbst tut.*

Wenn Sie auf der Tafel eine Frage beantworten, landen drei Zeilen im Arbeitspaket — `answer:`, `answered:`,
`answered-by:` — und **der Commit, der sie trägt, ist der Beleg**. Das Werkzeug liest aus der Versionsverwaltung, wer
committet hat, nie aus der Datei. Unter git reicht das allein nicht: ein git-Autor ist eine Zeichenkette, die jeder
eintippen kann. Deshalb verlangt das Werkzeug **signierte** Commits und lehnt eine Antwort ab, deren Commit sich nicht als
Ihrer verifizieren lässt.

Unter **Subversion** brauchen Sie nichts davon: der Server authentifiziert jeden Commit, und das Werkzeug liest diesen
Autor. Weiter bei *Dem Werkzeug sagen, wer antwortet*.

## Zuerst das Risiko — vor jeder Einstellung lesen

**Eine Signatur beweist, welcher Schlüssel benutzt wurde, nicht welche Hand.** Wenn Sie auf einem Rechner, auf dem
Agenten unter Ihrem Namen laufen, `commit.gpgsign true` setzen, ist *jeder* Commit dieser Agenten mit Ihrem Schlüssel
signiert und gilt als von Ihnen signiert — genau die Fälschung, die diese Seite verhindern soll. Weder das Werkzeug noch git
noch die Forge können das unterscheiden.

Auf einem Rechner, den Agenten benutzen, deshalb:

- **Nie standardmäßig signieren.** `commit.gpgsign` nicht setzen und Antworten **auf Verlangen** signieren:
  `git commit -S`. Ein Agent übergibt nie `-S`.
- Oder den Signierschlüssel dort halten, wo kein Agent hinkommt: ein Hardware-Schlüssel, der eine Berührung braucht,
  oder ein Rechner, auf dem keine Agenten laufen.

## Weg A — mit dem SSH-Schlüssel signieren (git)

Sie haben einen, wenn Sie per SSH zu einer Forge pushen. Derselbe Schlüssel darf signieren; er beweist so oder so
dasselbe, und ein zu schützender privater Schlüssel ist einfacher als zwei.

```
git config gpg.format ssh
git config user.signingkey ~/.ssh/<ihr-schluessel>.pub
```

Das Werkzeug prüft gegen eine **Signierer-Datei** — die öffentlichen Schlüssel, denen das Repository vertraut, eine
Zeile je Schlüssel: die E-Mail, für die der Schlüssel spricht, dann der öffentliche Schlüssel. *Im Repository* halten,
damit jeder Checkout und CI prüfen können:

```
echo "sie@example.org $(cat ~/.ssh/<ihr-schluessel>.pub)" >> docs/work-tracker/allowed_signers
git config gpg.ssh.allowedSignersFile "$PWD/docs/work-tracker/allowed_signers"
```

Ein öffentlicher Schlüssel ist öffentlich; ihn einzuchecken ist in Ordnung. Ein Agent, der diese Datei ändert, ist im Diff zu sehen.

**Auf GitHub** denselben öffentlichen Schlüssel noch einmal eintragen: *Settings → SSH and GPG keys → New SSH key*,
Typ **Signing Key** — dann zeigen Ihre Commits dort *Verified*. GitLab: *Preferences → SSH Keys*, Verwendung *Signing*.

## Weg B — mit einem GPG-Schlüssel signieren (git)

```
gpg --list-secret-keys --keyid-format long      # die Schlüssel-Id finden
git config user.signingkey <KEYID>
```

`gpg.format` nicht setzen. Die Benutzer-Id des Schlüssels muss die E-Mail tragen, mit der Sie committen. Den
öffentlichen Schlüssel exportieren (`gpg --armor --export <KEYID>`) und auf der Forge unter *GPG keys* eintragen.

## Dem Werkzeug sagen, wer antwortet

In `shoalmark.toml`:

```
[seats]
owner = "sie@example.org signed"
```

`sie@example.org` ist die E-Mail, unter der Sie committen (oder Ihr git-Autorname, oder das Subversion-Konto). `signed`
verlangt eine verifizierte Signatur — nur unter Subversion weglassen. Solange Sie keinen Sitz benennen, darf niemand
antworten: Das ist die Voreinstellung, absichtlich. Das ältere `answerers = ["ihrname signed"]` gilt weiter, wo es kein
`[seats]` gibt.

## Prüfen

Einen signierten Commit machen — `git commit -S -m "test"` — und:

```
git log -1 --format='%G? %GS %ae'
```

`G`, dann die E-Mail, für die der Schlüssel spricht, dann Ihre Autor-E-Mail — die letzten beiden müssen übereinstimmen.

**Dann eine Frage beantworten.** Auf der Tafel öffnet *annehmen* oder *ablehnen* einen Dialog mit der Frage, ihren
Möglichkeiten und dem, was sie aufhält; OK gibt Ihnen einen Befehl. Führen Sie ihn in einem Terminal im Repository aus:

```
python3 tools/shoalmark/shoalmark.py --answer AP-007 accept
```

Er legt den Branch `answer/ap-007` an (Branch-Namen klein: `AP-007` ist das Arbeitspaket, `ap-007` der Branch),
schreibt die drei Zeilen, committet sie mit Ihrem Schlüssel signiert (ein Hardware-Schlüssel wartet auf Ihre
Berührung) und pusht; jeden Schritt nennt er, bevor er ihn tut. Scheitert etwas, macht er alles rückgängig, was er
geschrieben hat, und gibt den Befehl aus, mit dem Sie die Antwort erneut geben. `git log -1 --format=%G?
answer/ap-007` gibt `G` aus, und die Frage ist von Ihrer Liste verschwunden.

## Was das Werkzeug ablehnt, und was es sagt

| Sie sehen | Es bedeutet |
|---|---|
| *an answer, but no seat in `[seats]` holds the `answer` right* (oder *`answerers` … names nobody*) | die `[seats]`-Zeile oben schreiben |
| *the answer is not committed yet* | committen — der Commit ist der Beleg |
| *`answered-by: x` but the git author of the answer is `y`* | jemand anderes hat Ihre Antwort committet; sie zählt nicht |
| *the answer's commit does not verify as `x`* | unsigniert, oder mit einem Schlüssel signiert, den die Signierer-Datei nicht an Ihre E-Mail bindet |
| ein *note*, dass der Autor unverifiziert ist | Sie haben unter git `["name"]` ohne `signed` geschrieben — es funktioniert, und beweist nichts |
