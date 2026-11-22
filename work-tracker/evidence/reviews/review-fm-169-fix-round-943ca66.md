# FM-169: the fix round's critical read, by difference e860f43..943ca66

Verdict: **READY WITH FINDINGS**.

FM-169: READY WITH FINDINGS - the fix round keeps the guard on the state in force

Tier: critical. A read by difference of the fix round, e860f43..943ca66, in one pass. No test
file was run for it: CI's full run and the builder's runs cover the suites.

The checks, each with its result:
1. Each build commit is its patch applied to its parent, by tree, with its message: holds.
2. The guard over the Owner's two sections reads owner and the signers file from the state in
   force at every place it reads them, and a landed unsigned change to either does not move
   it: holds.
3. The three rows whose fixtures changed keep their names and assertions, and each has a
   control row that fails if a plain unsigned change is taken: holds.
4. An Owner identity is printed as before where owner names it alone, and by its place where
   owner names two. No label is chosen by the form of an address: holds.
5. The classification of git starts follows the signature read's new form, with a control
   row: holds.
6. The Git entry differential sets aside nine reads of the default branch's history, at one
   site, with control rows: holds.
7. The facts row pins short hashes at seven characters, with a control at eight: holds.
8. No mutant in a test file looks for text this round took out of the tool: holds.
9. Every address on an added line is a test stand-in: holds.
10. The tracker's record of the round is true, and a plain run changes nothing: holds.
11. The gate's --check exits 0 at 943ca66.

CI: run 45001596894 on 943ca66, success on all five jobs.

Findings:
1. RV-30100: recorded privately

Reviewed: 943ca66017fbd5a4c23bc05d3e0f306c7f6f4bf1
Model: claude-fable-5-2
Effort: xhigh
