# Your answer is your commit — setting up a signature

*For the Owner. Ten minutes, once. Every step here is what the tool's own test suite does.*

When you answer an ask on the board, three lines land in the ask's tracker — `answer:`, `answered:`, `answered-by:` —
and **the commit that carries them is the record**. The tool reads who committed from the version control system,
never from the file. Under git that is not enough by itself: a git author is a string anyone can type, so the tool
asks you to **sign** your commits, and it refuses an answer whose commit does not verify as you.

Under **Subversion** you need none of this: the server authenticates every commit, and the tool reads that author.
Skip to *Telling the tool who answers*.

## First, the risk — read this before you set anything

**A signature proves which key was used, not which hand.** If you set `commit.gpgsign true` on a machine where agents
run as you, *every* commit they make is signed with your key and verifies as you — the exact forgery this page exists to
refuse. The tool cannot tell the difference, and neither can git or the forge.

So, on a machine agents use:

- **Never sign by default.** Leave `commit.gpgsign` unset (or `false`) and sign your answers **on demand**:
  `git commit -S`. An agent never passes `-S`.
- Or keep the signing key where no agent can reach it: a hardware key that needs a touch, or a machine agents do not
  run on.

The steps below set the key up; they do **not** turn signing on by default. If you already did, `git config --unset
commit.gpgsign` undoes it.

## Route A — sign with your SSH key (git)

You already have one if you push to a forge over SSH. The same key may sign; it proves the same thing either way,
and one private key to protect is simpler than two.

```
git config gpg.format ssh
git config user.signingkey ~/.ssh/<your-key>.pub
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
```

Leave `gpg.format` unset. The key's user id must carry the email you commit with. Export the public key
(`gpg --armor --export <KEYID>`) and add it on the forge under *GPG keys*.

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

Make a signed commit — `git commit -S -m "test"` — and run:

```
git log -1 --format='%G? %GS %ae'
```

`G`, then the email the key is trusted for, then your author email — the last two must agree.

**Then answer an ask.** On the board, *accept* or *reject* opens a dialog with the question, its choices and what it
holds up; OK gives you one command. Run it in a terminal, in the repository:

```
python3 tools/shoalmark/shoalmark.py --answer AP-007 accept
```

It cuts the branch `answer/ap-007` (git refs are lower-case; `AP-007` is the tracker, `ap-007` the branch), writes the three lines, commits them signed with your key (a hardware key waits for
your touch), and pushes, naming each step as it starts. If anything fails it undoes everything it wrote and prints the
command to give the answer again. `git log -1 --format=%G? answer/ap-007` prints `G`, and the ask leaves your queue.

## What the tool refuses, and what it says

| You see | It means |
|---|---|
| *an answer, but no seat in `[seats]` holds the `answer` right* (or *`answerers` … names nobody*) | write the `[seats]` line above |
| *the answer is not committed yet* | commit it — the commit is the record |
| *`answered-by: x` but the git author of the answer is `y`* | someone else committed your answer; it does not count |
| *the answer's commit does not verify as `x`* | unsigned, or signed by a key the signers file does not tie to your email |
| a *note* that the author is unverified | you wrote `["name"]` without `signed` under git — it works, and it proves nothing |
