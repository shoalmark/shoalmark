# Your answer is your commit — setting up a signature

*For the owner. A minute to find your tier; ten to set up the one you choose, once.*

When you answer an ask on the board, three lines land in the ask's tracker — `answer:`, `answered:`, `answered-by:` —
and **the commit that carries them is the record**. The tool reads who committed from the version control system,
never from the file. Under git that is not enough by itself: a git author is a string anyone can type, so the tool
asks you to **sign** your commits, and it refuses an answer whose commit does not verify as you.

Under **Subversion** you need none of this: the server authenticates every commit, and the tool reads that author.
Skip to *Telling the tool who answers*.

## First, what a signature proves

**A signature proves the key, not the hand.** Anything that runs as you, on your machine, can use your key the way
you do — your agents included. What it signs verifies as yours. Neither the tool nor git nor the forge can tell the
difference. So what counts is what it takes to use the key. Four tiers, weakest first:

| Tier | The key that signs | Can an agent on your account sign as you? |
|---|---|---|
| **0** | A software key unlocked at login (its passphrase in the Keychain), or one with no passphrase | **Yes, silently.** Every process on your account can sign. The passphrase guards only the key file. |
| **1** | A software key in `ssh-agent` that asks you to confirm each use (`ssh-add -c`) | **Partly.** A reflex click signs. On a Mac it also needs a confirmation helper that macOS does not ship. |
| **2** | A separate key used only to sign, whose passphrase you type at every signature and never store | **Not by accident.** A stray setting or a stray `-S` stops at the passphrase. An agent that means harm can fake the prompt and catch it. |
| **3** | A FIDO2 hardware key with Ed25519, a PIN and a touch, and a second one as a backup — or a key inside a Mac's Secure Enclave, with Touch ID at each signature | **No.** The private key never leaves the device, and every signature needs you there: your touch and your PIN, or your finger. |

**Where you are:** you type nothing when you sign — tier 0. You click to confirm — tier 1. You type a passphrase
every time — tier 2. You touch a security key and type its PIN, or give Touch ID at every signature for a key made
inside the Secure Enclave — tier 3.

**Which to choose.** Tier 2 is the easy route: nothing to buy, ten minutes, and it stops the accidents. Tier 3 is the
strong route: it also stops an agent that means harm, and it needs two security keys, bought once — or a Mac with
Touch ID and nothing to buy. Tier 0 is for trying the tool — your record will say so.

## What your record says

Today the tool says only whether an answer's signature verifies: a software key and a hardware key read the same. A
coming version reads the key type from the signers file and says which one signed:

- *signed with a software key — anything on the owner's account can produce it*
- *signed with a hardware key — needs the owner's touch*

At tiers 0 to 2 a software key signs, and the record cannot tell them apart: tier 2 protects you without showing it.
Tier 3 is the step the record can see. A Secure Enclave key is the exception: its type reads like a software key, so
its tier is declared beside it in the signers file (see tier 3).

## Sign on demand — and what that does not stop

If `commit.gpgsign` is `true`, git signs every commit in the repository, your agents' included. At tier 0 each of
them verifies as yours; at tiers 2 and 3 each of them stops at your passphrase or your touch. So leave it unset, and
sign your answers as you give them: the board's `--answer` command does it for you, and by hand it is
`git commit -S`. If you set it already, `git config --unset commit.gpgsign` undoes it.

**Leaving it unset does not keep an agent out.** An agent can pass `-S` itself. Only tier 2 or 3 stops that: the
signature then waits for a passphrase or a touch that the agent does not have. Tier 2 stops the agent that signs by
mistake; tier 3 also stops the one that means to.

## Route A — a separate signing key (git)

Sign with a key that does nothing else — never the key you push with. The key you push with is usually unlocked for
every push, so anything that can push can also sign.

**Only trying the tool?** The key you push with can sign; that is tier 0. Use its `.pub` in steps 1 to 3 under
*Then, for any tier*. It works, and it proves only that something on your account signed — your record will say so.

### Tier 2, the easy route — a passphrase at every signature

Make the key, with a passphrase you use nowhere else:

```
ssh-keygen -t ed25519 -f ~/.ssh/signing_ed25519 -C "you@example.org"
```

Never store that passphrase. Do not add this key to `ssh-agent` or the Keychain — no `ssh-add` — and `ssh-add -l`
must not list it. Its own file name, as here, keeps ssh from offering it when you push. Go on at *Then, for any tier*.

### Tier 3, the strong route — a hardware key that needs your touch

Two ways lead there: two FIDO2 security keys, or, with nothing to buy, the Secure Enclave of a Mac with Touch ID. A
passkey on your phone is not one of them today: OpenSSH signs through libfido2 over USB or NFC, and it cannot reach a
phone's passkey. If it could, it would still rank below tier 3, because a synced passkey lives on every device of your
account, not on one.

#### With two security keys

1. **Buy two security keys** sold as FIDO2 (CTAP2) with Ed25519 (EdDSA). The second is the backup: if you lose the
   first, the backup still signs. Set a PIN on each, with its maker's tool.

2. **On a Mac, install an OpenSSH that can talk to them.** Apple's bundled OpenSSH cannot enrol a security key:
   `ssh-keygen -t ed25519-sk` answers *No FIDO SecurityKeyProvider specified*. The *invalid format* on the next line
   does not mean your key lacks Ed25519. Homebrew's openssh is built with libfido2:

    ```
    brew install openssh
    git config gpg.ssh.program "$(brew --prefix)/bin/ssh-keygen"
    ```

    The second line makes git sign, and check signatures, with it. Open a new terminal: `which ssh-keygen` should
    now name Homebrew's. Homebrew's `ssh` comes first now too; if your `~/.ssh/config` says `UseKeychain`, put
    `IgnoreUnknown UseKeychain` above that line, or your pushes stop. On Linux or Windows, skip this step: any
    OpenSSH from 8.4 on, built with FIDO support, will do.

3. **Enrol both keys**, one at a time. Plug in the first:

    ```
    ssh-keygen -t ed25519-sk -O verify-required -f ~/.ssh/signing_sk -C "you@example.org"
    ```

    It asks for the key's PIN and a touch. `-O verify-required` is what makes every signature ask for the PIN, not
    only the touch. Then it offers a passphrase for the file it writes: you may leave it empty, because that file is
    only a handle, useless without the device. Plug in the backup and run it again with
    `-f ~/.ssh/signing_sk_backup`. [OpenSSH's manual](https://man.openbsd.org/ssh-keygen.1) has the details under
    *FIDO authenticator*.

4. **Keep the backup away from your desk**, and go on below with `~/.ssh/signing_sk.pub` — and the backup's `.pub`
   wherever a step says *both*.

#### Without buying — a Mac's Secure Enclave

On a Mac with Touch ID (Apple silicon, or an Intel Mac with a T2 chip), the signing key can be made inside the Secure
Enclave. An open-source SSH agent app such as [Secretive](https://github.com/maxgoedjen/secretive) makes it there and
can ask for Touch ID at each signature. The key cannot be exported, each signature needs your finger, and the app
announces every use. Its limits:

- It makes P-256 ECDSA keys only. The forge accepts them.
- The key is bound to this one Mac. Register a second signer too — a key on another Mac, or a FIDO2 key — or losing
  the Mac locks you out of answering.
- By its type, the tool cannot tell it from a software ECDSA key. So declare the tier beside the key in the signers
  file: a comment line above it, such as `# tier 3: Secure Enclave, Touch ID at each signature`.
- Check that no approval is cached between signatures: sign twice in a row, and both must ask for your finger.

Set the key to ask for Touch ID at every use, point `SSH_AUTH_SOCK` at the app's agent as its setup shows, and save
the key's public half as `~/.ssh/signing_se.pub`. Go on below with that file — and the second signer's wherever a
step says *both*.

### Then, for any tier

1. **Tell git which key signs**, in the repository:

    ```
    git config gpg.format ssh
    git config user.signingkey ~/.ssh/signing_ed25519.pub     # tier 3: signing_sk.pub or signing_se.pub
    ```

2. **Add it to the signers file** — the public keys the repository trusts, one line each: the email the key speaks
   for, then the key. Keep it *in the repository*, so every checkout and CI can verify:

    ```
    echo "you@example.org $(cat ~/.ssh/signing_ed25519.pub)" >> docs/work-tracker/allowed_signers
    git config gpg.ssh.allowedSignersFile "$PWD/docs/work-tracker/allowed_signers"
    ```

    Tier 3: both signers, one line each. A security key's line reads `you@example.org sk-ssh-ed25519@openssh.com AAAA…`
    — the `sk-` marks a hardware key for anyone who reads the file. A Secure Enclave key's reads
    `ecdsa-sha2-nistp256`, with its comment line above it. A public key is public; committing it is fine. Only your
    signed commit changes this file: the gate refuses a seat's change to it, and it checks every signature against the
    default branch's copy, never a branch's own. So commit its first version on the default branch yourself, signed — a
    branch cannot prove a key the default branch does not hold.

3. **Add it on the forge, as a signing key.** On GitHub: *Settings → SSH and GPG keys → New SSH key*, key type
   **Signing Key** ([GitHub's steps](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)).
   On GitLab: *Preferences → SSH Keys*, usage type *Signing*. Your commits then show *Verified* there too. Tier 3:
   both signers. As a signing key only — this key never pushes.

4. **Retire the old key**, if another key signed before — the one you push with, say. Until you do, anything that
   can use it still signs, and what it signs still verifies. Retire it once none of the answers it signed is still
   open: an open answer signed by the old key would read unverified once its line leaves the signers file. Then take
   its line out of the signers file, and delete it under *Signing keys* on the forge. It stays under
   *Authentication keys*, and keeps pushing.

## Route B — sign with a GPG key (git)

```
gpg --list-secret-keys --keyid-format long      # find your key id
git config user.signingkey <KEYID>
```

Leave `gpg.format` unset. The key's user id must carry the email you commit with. Export the public key
(`gpg --armor --export <KEYID>`) and add it on the forge under *GPG keys*.

The tiers hold here too. A key whose passphrase `gpg-agent` or the Keychain keeps signs for anything on your account
— tier 0. A key on a token that needs your touch at every signature is the strong route.

## Telling the tool who answers

In `shoalmark.toml`:

```
[seats]
owner = "you@example.org signed"
```

`you@example.org` is the email you commit with (or your git author name, or the Subversion account). `signed` asks
for a verified signature — drop it only under Subversion. No seat holds the answer right unless you name it: nobody
may answer by default, on purpose. The older `answerers = ["yourname signed"]` still works where there is no `[seats]`.

## Check it

```
git commit --allow-empty -S -m "signature test"
git log -1 --format='%G? %GS %ae'
git reset --soft HEAD~1
```

The first line asks for your passphrase at tier 2, for your PIN and a touch or for Touch ID at tier 3 — and for
nothing at tier 0. The second prints `G`, then the email the key is trusted for, then your author email; the last two
must agree. The third drops the test commit.

**Then answer an ask.** On the board, *accept* or *reject* opens a dialog with the question, its choices and what it
holds up; OK gives you one command. Run it in a terminal, in the repository:

```
python3 tools/shoalmark/shoalmark.py --answer AP-007 accept
```

It cuts the branch `answer/ap-007` (shoalmark lower-cases the branch it creates; git keeps the case it is given),
writes the three lines, commits them signed with your key (tier 2 asks for your passphrase, tier 3 for your touch),
and pushes, naming each step as it starts. If anything fails it undoes everything it wrote and prints the
command to give the answer again. `git log -1 --format=%G? answer/ap-007` prints `G`, and the ask leaves your queue.

## Your intent and your current path — only your signed commit changes them

The two sections of `TRIAGE.md` that are yours — *The intent* and *The current path* — change only in a commit you
sign. On a branch, `--check` refuses any other commit that changes their text (a word, a line, a blank line: whitespace
counts), renames or removes their headings, deletes `TRIAGE.md` or moves it away from the tracker directory, or points
`tracker_dir` somewhere else; the commit hook refuses a seat's such commit before it is made, and `--queue` reads its
pull request *wait: TRIAGE.md changed unsigned*. Your commit passes when `git log -1 --format='%G? %GS %ae'` prints `G`
and your email twice — the check under *Check it*. A seat that wants either section changed asks you, with an `ask:`;
you make the change yourself, signed. `## Passes` stays open to the seats that record a pass. The signers file is
guarded the same way, and a signature is checked against the default branch's copy of it: a branch that adds its own
key under your email proves nothing.

**What it cannot tell.** A commit signed with your key passes; at tier 0 any process on your account holds that key
(FM-007) — the tiers above are what make the key yours alone. Where your seat in `[seats]` is not marked `signed`, the
tool proves the author only, a string anyone can type, and says so: mark it `signed` to prove the key. Under Subversion
this guard is out of scope: its working copy carries no signature.

## What the tool refuses, and what it says

| You see | It means |
|---|---|
| *an answer, but no seat in `[seats]` holds the `answer` right* (or *`answerers` … names nobody*) | write the `[seats]` line above |
| *the answer is not committed yet* | commit it — the commit is the record |
| *`answered-by: x` but the git author of the answer is `y`* | someone else committed your answer; it does not count |
| *the answer's commit does not verify as `x`* | unsigned, or signed by a key the signers file does not tie to your email |
| a *note* that the author is unverified | you wrote `["name"]` without `signed` under git — it works, and it proves nothing |
| *refused: commit … changes the text under `## The intent`* (or `## The current path`) | a commit on that branch that is not yours, signed, changed your two sections — it does not merge |
| *… the Owner's email, unsigned* | a commit carries your email and no signature: you forgot `-S`, or someone typed your email |
