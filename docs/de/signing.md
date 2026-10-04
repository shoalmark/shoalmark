# Ihre Antwort ist Ihr Commit — eine Signatur einrichten

*Für den Eigner. Eine Minute, um Ihre Stufe zu finden; zehn, um die gewählte einzurichten, einmal.*

Wenn Sie auf der Tafel eine Frage beantworten, landen drei Zeilen im Arbeitspaket — `answer:`, `answered:`,
`answered-by:` — und **der Commit, der sie trägt, ist der Beleg**. Das Werkzeug liest aus der Versionsverwaltung, wer
committet hat, nie aus der Datei. Unter git reicht das allein nicht: ein git-Autor ist eine Zeichenkette, die jeder
eintippen kann. Deshalb verlangt das Werkzeug **signierte** Commits und lehnt eine Antwort ab, deren Commit sich nicht als
Ihrer verifizieren lässt.

Unter **Subversion** brauchen Sie nichts davon: der Server authentifiziert jeden Commit, und das Werkzeug liest diesen
Autor. Weiter bei *Dem Werkzeug sagen, wer antwortet*.

## Zuerst: was eine Signatur beweist

**Eine Signatur beweist den Schlüssel, nicht die Hand.** Alles, was unter Ihrem Konto auf Ihrem Rechner läuft, kann
Ihren Schlüssel benutzen wie Sie — auch Ihre Agenten. Was es signiert, gilt als von Ihnen signiert. Weder das Werkzeug
noch git noch die Forge können das unterscheiden. Es zählt also, was es braucht, den Schlüssel zu benutzen. Vier
Stufen, die schwächste zuerst:

| Stufe | Der Schlüssel, der signiert | Kann ein Agent unter Ihrem Konto als Sie signieren? |
|---|---|---|
| **0** | Ein Software-Schlüssel, der beim Anmelden entsperrt wird (die Passphrase im Schlüsselbund), oder einer ohne Passphrase | **Ja, lautlos.** Jeder Prozess unter Ihrem Konto kann signieren. Die Passphrase schützt nur die Schlüsseldatei. |
| **1** | Ein Software-Schlüssel im `ssh-agent`, der jede Verwendung bestätigen lässt (`ssh-add -c`) | **Teilweise.** Ein Klick aus Reflex signiert. Auf dem Mac braucht es außerdem ein Bestätigungsprogramm, das macOS nicht mitliefert. |
| **2** | Ein eigener Schlüssel nur zum Signieren, dessen Passphrase Sie bei jeder Signatur eintippen und nirgends speichern | **Nicht aus Versehen.** Eine verirrte Einstellung oder ein verirrtes `-S` bleibt an der Passphrase hängen. Ein Agent, der Schaden will, kann die Abfrage fälschen und die Passphrase mitlesen. |
| **3** | Ein FIDO2-Hardware-Schlüssel mit Ed25519, PIN und Berührung, dazu ein zweiter als Reserve — oder ein Schlüssel in der Secure Enclave eines Macs, mit Touch ID bei jeder Signatur | **Nein.** Der private Schlüssel verlässt das Gerät nie, und jede Signatur braucht Sie selbst: Berührung und PIN, oder Ihren Finger. |

**Wo Sie stehen:** Sie tippen nichts, wenn Sie signieren — Stufe 0. Sie klicken zur Bestätigung — Stufe 1. Sie
tippen jedes Mal eine Passphrase — Stufe 2. Sie berühren einen Sicherheitsschlüssel und geben seine PIN ein, oder Sie
geben bei jeder Signatur Touch ID für einen Schlüssel aus der Secure Enclave — Stufe 3.

**Welche Stufe?** Stufe 2 ist der einfache Weg: nichts zu kaufen, zehn Minuten, und er hält die Versehen auf.
Stufe 3 ist der starke Weg: Er hält auch einen Agenten auf, der Schaden will, und braucht zwei Sicherheitsschlüssel,
einmal gekauft — oder einen Mac mit Touch ID, ohne Kauf. Stufe 0 ist zum Ausprobieren des Werkzeugs — Ihr Beleg wird
es sagen.

## Die dokumentierte Signaturstufe dieses Projekts

Laut Stand vom 25. September 2026 verwendet der Owner von shoalmark **Stufe 0**, einen
Software-Schlüssel. Der geplante Wechsel zum Hardware-Schlüssel ist noch nicht als abgeschlossen
dokumentiert. Eine verifizierte Antwort belegt bis dahin die Nutzung des vertrauten Schlüssels,
nicht die persönliche Anwesenheit des Owners. Das ist der dokumentierte Projektstand, keine
Prüfung Ihres Rechners. Siehe [FM-007](https://github.com/shoalmark/shoalmark/blob/main/work-tracker/FM-007-a-signature-proves-the-key-not-the-hand-an-agent-running-as.md).

## Was Ihr Beleg sagt

Heute sagt das Werkzeug nur, ob sich die Signatur einer Antwort verifizieren lässt: ein Software-Schlüssel und ein
Hardware-Schlüssel sehen gleich aus. Eine kommende Version liest die Schlüsselart aus der Signierer-Datei und sagt,
welcher signiert hat:

- *mit einem Software-Schlüssel signiert — alles, was unter dem Konto des Eigners läuft, kann das erzeugen*
- *mit einem Hardware-Schlüssel signiert — braucht die Berührung des Eigners*

Auf den Stufen 0 bis 2 signiert ein Software-Schlüssel, und der Beleg kann sie nicht unterscheiden: Stufe 2 schützt
Sie, ohne es zu zeigen. Stufe 3 ist der Schritt, den der Beleg sehen kann. Ein Schlüssel aus der Secure Enclave ist die
Ausnahme: Seine Art liest sich wie die eines Software-Schlüssels, deshalb wird seine Stufe neben ihm in der
Signierer-Datei angegeben (siehe Stufe 3).

## Auf Verlangen signieren — und was das nicht aufhält

Steht `commit.gpgsign` auf `true`, signiert git jeden Commit im Repository, auch die Ihrer Agenten. Auf Stufe 0 gilt
jeder davon als von Ihnen signiert; auf Stufe 2 und 3 bleibt jeder an Ihrer Passphrase oder Ihrer Berührung hängen.
Lassen Sie es also ungesetzt, und signieren Sie Ihre Antworten, wenn Sie sie geben: Der Befehl `--answer` von der Tafel
tut das für Sie, von Hand ist es `git commit -S`. Haben Sie es schon gesetzt, macht `git config --unset commit.gpgsign`
es rückgängig.

**Ein ungesetztes `commit.gpgsign` hält keinen Agenten fern.** Ein Agent kann `-S` selbst übergeben. Nur Stufe 2
oder 3 hält das auf: Die Signatur wartet dann auf eine Passphrase oder eine Berührung, die der Agent nicht hat.
Stufe 2 hält den Agenten auf, der aus Versehen signiert; Stufe 3 auch den, der es absichtlich tut.

## Weg A — ein eigener Signierschlüssel (git)

Signieren Sie mit einem Schlüssel, der nichts anderes tut — nie mit dem, mit dem Sie pushen. Der Schlüssel, mit dem
Sie pushen, ist meist für jeden Push entsperrt; was pushen kann, kann also auch signieren.

**Nur zum Ausprobieren?** Der Schlüssel, mit dem Sie pushen, kann signieren; das ist Stufe 0. Nehmen Sie seine `.pub`
in den Schritten 1 bis 3 unter *Danach, für jede Stufe*. Es funktioniert, und es beweist nur, dass etwas unter Ihrem
Konto signiert hat — Ihr Beleg wird es sagen.

### Stufe 2, der einfache Weg — eine Passphrase bei jeder Signatur

Den Schlüssel erzeugen, mit einer Passphrase, die Sie sonst nirgends verwenden:

```
ssh-keygen -t ed25519 -f ~/.ssh/signing_ed25519 -C "sie@example.org"
```

Diese Passphrase nie speichern. Den Schlüssel weder dem `ssh-agent` noch dem Schlüsselbund geben — kein `ssh-add` —,
und `ssh-add -l` darf ihn nicht auflisten. Sein eigener Dateiname, wie hier, verhindert, dass ssh ihn beim Pushen
anbietet. Weiter bei *Danach, für jede Stufe*.

### Stufe 3, der starke Weg — ein Hardware-Schlüssel, der Ihre Berührung braucht

Zwei Wege führen dorthin: zwei FIDO2-Sicherheitsschlüssel, oder, ohne Kauf, die Secure Enclave eines Macs mit
Touch ID. Ein Passkey auf Ihrem Telefon gehört heute nicht dazu: OpenSSH signiert über libfido2 per USB oder NFC und
erreicht den Passkey eines Telefons nicht. Könnte es das, stünde er trotzdem unter Stufe 3, denn ein synchronisierter
Passkey liegt auf jedem Gerät Ihres Kontos, nicht auf einem.

#### Mit zwei Sicherheitsschlüsseln

1. **Zwei Sicherheitsschlüssel kaufen**, die als FIDO2 (CTAP2) mit Ed25519 (EdDSA) verkauft werden. Der zweite ist
   die Reserve: Verlieren Sie den ersten, signiert die Reserve weiter. Auf jedem mit dem Programm seines Herstellers
   eine PIN setzen.

2. **Auf dem Mac ein OpenSSH installieren, das mit ihnen sprechen kann.** Das von Apple mitgelieferte OpenSSH kann
   keinen Sicherheitsschlüssel einrichten: `ssh-keygen -t ed25519-sk` antwortet *No FIDO SecurityKeyProvider
   specified*. Das *invalid format* in der Zeile danach heißt nicht, dass Ihrem Schlüssel Ed25519 fehlt. Das openssh
   von Homebrew ist mit libfido2 gebaut:

    ```
    brew install openssh
    git config gpg.ssh.program "$(brew --prefix)/bin/ssh-keygen"
    ```

    Die zweite Zeile lässt git damit signieren und Signaturen prüfen. Ein neues Terminal öffnen: `which ssh-keygen`
    sollte jetzt das von Homebrew nennen. Auch das `ssh` von Homebrew kommt jetzt zuerst; steht in Ihrer
    `~/.ssh/config` `UseKeychain`, setzen Sie `IgnoreUnknown UseKeychain` über diese Zeile, sonst scheitern Ihre
    Pushes. Unter Linux oder Windows diesen Schritt überspringen: Jedes OpenSSH ab 8.4 mit FIDO-Unterstützung genügt.

3. **Beide Schlüssel einrichten**, einen nach dem anderen. Den ersten einstecken:

    ```
    ssh-keygen -t ed25519-sk -O verify-required -f ~/.ssh/signing_sk -C "sie@example.org"
    ```

    Der Befehl fragt nach der PIN des Schlüssels und einer Berührung. `-O verify-required` sorgt dafür, dass jede
    Signatur nach der PIN fragt, nicht nur nach der Berührung. Dann bietet er eine Passphrase für die Datei an, die er
    schreibt: Sie dürfen sie leer lassen, denn diese Datei ist nur ein Verweis, ohne das Gerät nutzlos. Die Reserve
    einstecken und dasselbe mit `-f ~/.ssh/signing_sk_backup` noch einmal. Einzelheiten stehen im
    [Handbuch von OpenSSH](https://man.openbsd.org/ssh-keygen.1) (englisch) unter *FIDO authenticator*.

4. **Die Reserve nicht am Schreibtisch aufbewahren**, und unten mit `~/.ssh/signing_sk.pub` weitermachen — und mit
   der `.pub` der Reserve, wo ein Schritt *beide* sagt.

#### Ohne Kauf — die Secure Enclave eines Macs

Auf einem Mac mit Touch ID (Apple Silicon, oder ein Intel-Mac mit T2-Chip) lässt sich der Signierschlüssel in der
Secure Enclave erzeugen. Eine quelloffene SSH-Agent-App wie [Secretive](https://github.com/maxgoedjen/secretive)
(englisch) erzeugt ihn dort und kann bei jeder Signatur nach Touch ID fragen. Der Schlüssel lässt sich nicht
exportieren, jede Signatur braucht Ihren Finger, und die App meldet jede Verwendung. Die Grenzen:

- Die App erzeugt nur P-256-ECDSA-Schlüssel. Die Forge nimmt sie an.
- Der Schlüssel ist an diesen einen Mac gebunden. Tragen Sie auch einen zweiten Signierer ein — einen Schlüssel auf
  einem anderen Mac oder einen FIDO2-Schlüssel —, sonst sperrt Sie der Verlust des Macs vom Antworten aus.
- An seiner Art kann das Werkzeug ihn nicht von einem Software-ECDSA-Schlüssel unterscheiden. Geben Sie die Stufe
  deshalb neben dem Schlüssel in der Signierer-Datei an: eine Kommentarzeile darüber, etwa
  `# tier 3: Secure Enclave, Touch ID at each signature`.
- Prüfen Sie, dass zwischen zwei Signaturen keine Freigabe zwischengespeichert wird: zweimal hintereinander
  signieren — beide Male muss Touch ID nach Ihrem Finger fragen.

Den Schlüssel so einstellen, dass er bei jeder Verwendung nach Touch ID fragt, `SSH_AUTH_SOCK` auf den Agenten der
App richten, wie ihre Einrichtung es zeigt, und den öffentlichen Teil des Schlüssels als `~/.ssh/signing_se.pub`
speichern. Unten mit dieser Datei weitermachen — und mit der des zweiten Signierers, wo ein Schritt *beide* sagt.

### Danach, für jede Stufe

1. **git sagen, welcher Schlüssel signiert**, im Repository:

    ```
    git config gpg.format ssh
    git config user.signingkey ~/.ssh/signing_ed25519.pub     # Stufe 3: signing_sk.pub oder signing_se.pub
    ```

2. **Ihn in die Signierer-Datei eintragen** — die öffentlichen Schlüssel, denen das Repository vertraut, eine Zeile
   je Schlüssel: die E-Mail, für die der Schlüssel spricht, dann der Schlüssel. *Im Repository* halten, damit jeder
   Checkout und CI prüfen können:

    ```
    echo "sie@example.org $(cat ~/.ssh/signing_ed25519.pub)" >> docs/work-tracker/allowed_signers
    git config gpg.ssh.allowedSignersFile "$PWD/docs/work-tracker/allowed_signers"
    ```

    Stufe 3: beide Signierer, je eine Zeile. Die Zeile eines Sicherheitsschlüssels lautet
    `sie@example.org sk-ssh-ed25519@openssh.com AAAA…` — das `sk-` zeigt jedem, der die Datei liest, einen
    Hardware-Schlüssel an. Die eines Secure-Enclave-Schlüssels lautet `ecdsa-sha2-nistp256`, mit ihrer Kommentarzeile
    darüber. Ein öffentlicher Schlüssel ist öffentlich; ihn einzuchecken ist in Ordnung. Nur Ihr signierter Commit
    ändert diese Datei: Das Werkzeug lehnt die Änderung eines Agenten ab und prüft jede Signatur gegen die Fassung auf
    dem Standard-Branch, nie gegen die eines Branches. Committen Sie ihre erste Fassung darum selbst auf dem
    Standard-Branch, signiert — ein Branch kann keinen Schlüssel beweisen, den der Standard-Branch nicht führt, und bis
    die Datei dort liegt, wird keine Signatur verifiziert. Ein neuer Schlüssel zählt, sobald er dort gemergt ist: `--answer`
    prüft das, bevor es pusht.

3. **Ihn auf der Forge als Signierschlüssel eintragen.** Auf GitHub: *Settings → SSH and GPG keys → New SSH key*,
   Typ **Signing Key** ([die Schritte bei GitHub](https://docs.github.com/de/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)).
   Auf GitLab: *Preferences → SSH Keys*, Verwendung *Signing*. Dann zeigen Ihre Commits dort *Verified*. Stufe 3:
   beide Signierer. Nur als Signierschlüssel — dieser Schlüssel pusht nie.

4. **Den alten Schlüssel stilllegen**, falls vorher ein anderer signiert hat — etwa der, mit dem Sie pushen. Bis
   dahin signiert alles, was ihn benutzen kann, weiter, und was er signiert, lässt sich weiter verifizieren. Legen
   Sie ihn still, sobald keine der Antworten, die er signiert hat, mehr offen ist: Eine offene Antwort, die der alte
   Schlüssel signiert hat, gälte als unverifiziert, sobald seine Zeile die Signierer-Datei verlässt. Dann seine Zeile
   aus der Signierer-Datei nehmen und ihn auf der Forge unter *Signing keys* löschen. Unter *Authentication keys*
   bleibt er stehen und pusht weiter.

**Eine signierte Zeile wird nur über SSH geprüft.** Eine GPG-Signatur darauf lehnt das Werkzeug ab: `sign with SSH; GPG returns with a fingerprint binding`.

## Dem Werkzeug sagen, wer antwortet

In `shoalmark.toml`:

```
owner = "sie@example.org signed"
```

Oben in der Datei, vor jeder Tabelle. `sie@example.org` ist die E-Mail, die die Signierer-Datei für Ihren Schlüssel nennt: Eine Identität mit `signed`
ist eine E-Mail-Adresse, jede andere lehnt das Werkzeug schon beim Lesen der Konfiguration ab (Exit 1). `signed` verlangt
eine SSH-Signatur, deren Prinzipal genau diese E-Mail ist — nur unter Subversion weglassen, wo Ihr Server-Konto die
Identität ist. Solange Sie niemanden benennen, darf niemand antworten: Das ist die Voreinstellung, absichtlich.
`[seats] owner` ist die alte Schreibweise und gilt weiter; das ältere `answerers = ["ihrname"]` gilt weiter, wo es weder
`owner` noch `[seats]` gibt — für eine signierte Antwort schreiben Sie die `owner`-Zeile.

## Prüfen

```
git commit --allow-empty -S -m "Signaturtest"
git log -1 --format='%G? %GS %ae'
git reset --soft HEAD~1
```

Die erste Zeile fragt auf Stufe 2 nach Ihrer Passphrase, auf Stufe 3 nach PIN und Berührung oder nach Touch ID — und
auf Stufe 0 nach nichts. Die zweite gibt `G` aus, dann die E-Mail, für die der Schlüssel spricht — sie muss genau
Ihre `owner`-E-Mail sein —, dann Ihre Autor-E-Mail. Die dritte nimmt den Test-Commit wieder weg.

**Dann eine Frage beantworten.** Auf der Tafel öffnet *annehmen* oder *ablehnen* einen Dialog mit der Frage, ihren
Möglichkeiten und dem, was sie aufhält; OK gibt Ihnen einen Befehl. Führen Sie ihn in einem Terminal im Repository aus:

```
python3 tools/shoalmark/shoalmark.py --answer AP-007 accept
```

Er legt den Branch `answer/ap-007` an (Branch-Namen klein: `AP-007` ist das Arbeitspaket, `ap-007` der Branch),
schreibt die drei Zeilen, committet sie mit Ihrem Schlüssel signiert (Stufe 2 fragt nach Ihrer Passphrase, Stufe 3
nach Ihrer Berührung) und pusht; jeden Schritt nennt er, bevor er ihn tut. Scheitert etwas, macht er alles rückgängig,
was er geschrieben hat, und gibt den Befehl aus, mit dem Sie die Antwort erneut geben. `git log -1 --format=%G?
answer/ap-007` gibt `G` aus, und die Frage ist von Ihrer Liste verschwunden.

## Ihre Absicht und Ihr aktueller Weg — nur Ihr signierter Commit ändert sie

Die beiden Abschnitte der `TRIAGE.md`, die Ihnen gehören — *Die Absicht* und *Der aktuelle Weg* —, ändern sich nur in
einem Commit, den Sie signieren. Auf einem Branch lehnt `--check` jeden anderen Commit ab, der ihren Text ändert (ein
Wort, eine Zeile, eine Leerzeile: Leerraum zählt), ihre Überschriften umbenennt oder entfernt, die `TRIAGE.md` löscht
oder aus dem Tracker-Verzeichnis verschiebt oder `tracker_dir` woandershin zeigen lässt; der Commit-Hook lehnt einen
solchen Commit eines Agenten ab, bevor er entsteht, und `--queue` liest seinen Pull Request als *wait: TRIAGE.md changed
unsigned*. Ihr Commit geht durch, wenn `git log -1 --format='%G? %GS %ae'` `G` und zweimal Ihre E-Mail ausgibt — die
Probe unter *Prüfen*. Ein Agent, der einen der beiden Abschnitte geändert haben will, fragt Sie mit einem `ask:`; die
Änderung machen Sie selbst, signiert. Der Abschnitt der Durchgänge (`## Passes`) bleibt offen für die Agenten, die eine
Sichtung festhalten. Die Signierer-Datei ist ebenso geschützt, und eine Signatur wird gegen deren Fassung auf dem
Standard-Branch geprüft: Ein Branch, der seinen eigenen Schlüssel unter Ihrer E-Mail einträgt, beweist nichts.

**Was es nicht unterscheiden kann.** Ein Commit, der mit Ihrem Schlüssel signiert ist, geht durch; auf Stufe 0 hat jeder
Prozess unter Ihrem Konto diesen Schlüssel (FM-007) — erst die Stufen oben machen ihn allein zu Ihrem. Wo Ihr `owner`
oder ein Sitz mit `answer` nicht `signed` ist, beweist das Werkzeug nur den Autor, eine Zeichenkette, die jeder tippen
kann, und sagt es: Markieren Sie ihn `signed`, um den Schlüssel zu beweisen. Unter Subversion liegt dieser Schutz
außerhalb des Umfangs: seine Arbeitskopie trägt keine Signatur.

## Was das Werkzeug ablehnt, und was es sagt

| Sie sehen | Es bedeutet |
|---|---|
| *an answer, but no seat in `[seats]` holds the `answer` right* (oder *`answerers` … names nobody*) | die `owner`-Zeile oben schreiben |
| *the answer is not committed yet* | committen — der Commit ist der Beleg |
| *`answered-by: x` but the git author of the answer is `y`* | jemand anderes hat Ihre Antwort committet; sie zählt nicht |
| *the answer's commit does not verify as `x`* | unsigniert, oder mit einem Schlüssel signiert, den die Signierer-Datei auf dem Standard-Branch nicht an genau Ihre E-Mail bindet — ein neuer Schlüssel zählt, sobald er dort gemergt ist |
| *sign with SSH; GPG returns with a fingerprint binding* | die Antwort ist mit einem GPG-Schlüssel signiert: signieren Sie sie mit Ihrem SSH-Schlüssel (Weg A) |
| *`owner` names `x` as signed, and a signed identity is an email address* | die E-Mail eintragen, die die Signierer-Datei für Ihren Schlüssel nennt |
| ein *note*, dass der Autor unverifiziert ist | Sie haben unter git `["name"]` ohne `signed` geschrieben — es funktioniert, und beweist nichts |
| *refused: commit … changes the text under `## The intent`* (oder `## The current path`) | ein Commit auf diesem Branch, der nicht Ihrer ist, signiert, hat Ihre beiden Abschnitte geändert — er wird nicht gemergt |
| *… the Owner's email, unsigned* | ein Commit trägt Ihre E-Mail und keine Signatur: Sie haben `-S` vergessen, oder jemand hat Ihre E-Mail getippt |
