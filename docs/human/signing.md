# Your answer is your commit — setting up a signature

*For the Owner. Ten minutes, once. Every step here is what the tool's own test suite does.*

When you answer an ask on the board, three lines land in the ask's tracker — `answer:`, `answered:`, `answered-by:` —
and **the commit that carries them is the record**. The tool reads who committed from the version control system,
never from the file. Under git that is not enough by itself: a git author is a string anyone can type, so the tool
asks you to **sign** your commits, and it refuses an answer whose commit does not verify as you.

Under **Subversion** you need none of this: the server authenticates every commit, and the tool reads that author.
Skip to *Telling the tool who answers*.

## Route A — sign with your SSH key (git)

You already have one if you push to a forge over SSH. The same key may sign; it proves the same thing either way,
and one private key to protect is simpler than two.

```
git config gpg.format ssh
git config user.signingkey ~/.ssh/<your-key>.pub
git config commit.gpgsign true
```

The tool verifies against a **signers file** — the public keys the repository trusts, one line each: the email the
key speaks for, then the public key. Keep it *in the repository*, so every checkout and CI can verify:

```
echo "you@example.org $(cat ~/.ssh/<your-key>.pub)" >> docs/work-tracker/allowed_signers
git config gpg.ssh.allowedSignersFile "$PWD/docs/work-tracker/allowed_signers"
```

A public key is public; committing it is fine. A seat that edits this file shows in the diff.

**On GitHub**, add the same public key once more under *Settings → SSH and GPG keys → New SSH key*, key type
**Signing Key** — then your commits show *Verified* there too. GitLab: *Preferences → SSH Keys*, usage type *Signing*.

## Route B — sign with a GPG key (git)

```
gpg --list-secret-keys --keyid-format long      # find your key id
git config user.signingkey <KEYID>
git config commit.gpgsign true
```

Leave `gpg.format` unset. The key's user id must carry the email you commit with. Export the public key
(`gpg --armor --export <KEYID>`) and add it on the forge under *GPG keys*.

## Telling the tool who answers

In `shoalmark.toml`:

```
answerers = ["yourname signed"]
```

`yourname` is the git author name (`git config user.name`) or the Subversion account. `signed` asks for a verified
signature — drop it only under Subversion. Empty, nobody may answer: that is the default, on purpose.

## Check it

Make any commit and run:

```
git log -1 --format='%G? %GS %ae'
```

`G`, then the email the key is trusted for, then your author email — the last two must agree. Then answer an ask on
the board: click, paste the three lines, commit. `python3 tools/shoalmark/shoalmark.py --check` is green, and the ask
has left your queue.

## What the tool refuses, and what it says

| You see | It means |
|---|---|
| *an answer, but `answerers` names nobody* | write the line above |
| *the answer is not committed yet* | commit it — the commit is the record |
| *`answered-by: x` but the git author of the answer is `y`* | someone else committed your answer; it does not count |
| *the answer's commit does not verify as `x`* | unsigned, or signed by a key the signers file does not tie to your email |
| a *note* that the author is unverified | you wrote `["name"]` without `signed` under git — it works, and it proves nothing |
