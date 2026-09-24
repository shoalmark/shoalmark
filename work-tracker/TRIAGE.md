# Triage

The home of the recurring triage pass: `python3 shoalmark.py --triage`. The command prints the rules and the two sections
below; its worksheets are the record, in `evidence/triage/`.

## The intent

*The Owner's own words — for · so that · never. Nobody else edits this. A pass prints it above its rules.*

- **for** a tool that improves the collaboration between people and their agent seats, through a shared record that holds: the single source of project truth, the current state of where seats are authorised to be working, the signed decisions that authorised this work, open questions present for a person to answer, and rule sets that prevent agents from going rogue and against intention. All tracked, traceable and visible through the record to anybody with the rights to read, and writable only for those with the rights to do so.
- **so that** work can be tracked, can be verified, can be proven as being done. For the owner: that their project goals can be reached and any release can be trusted. For any agent seat: that there is a clear tasking, a mandate, a way forward and a way to communicate with others, to raise blockers and request help. For all: a look at the record gives you the intent, who authorised this, who worked on this, where we are with this, where the results are with evidence, and where the release is that is running this.
- **never** a rogue tasking or unauthorised work; nothing that is not in the record; a merge without an independent party's review and verification against the record; a merge or release of something that is not done; an issue nobody tracks; a fix that is forgotten; a seat that is left without its answer; a tasking never able to finish; a question never raised; the authorised party never involved; the authority order not respected; the issue not escalated; a failed intent because it was misunderstood; take up work that is not ready or cannot be delivered when due; leak sensible-data, non-redacted into records; 


## The current path

*The Owner's. A pass judges every tier against it; only the Owner changes it.*

1. The daily sitting runs on a tagged release with a signed answer and no failed run.
2. What a sitting finds is filed that day and fixed when it is small and ready; the rest is tracked.
3. A pull request without an independent review's evidence file cannot merge - checked, not asked.
4. The owner shall be involved less when trust in the process has been built, but the trust must come from evidence and has to be earned first.
5. An answer is written and signed through the board. No act of the Owner, a click, a merge, an opened pull request, is an answer, and no seat reads one as such.

## Passes

Newest first — one paragraph per pass: its date, what it changed, its worksheet.

**2026-09-24 — the second pass** (Principal seat, on the Owner's word after the board showed the day's release work under *triage*, fourteen minutes after 0.18.0 was tagged; verified NOT READY once — a Shipped and a merge that dropped open work — and re-made on its Reviewer's R1–R7): 10 new filings judged, FM-023 … FM-032. Three of them were built on (FM-024, FM-031, FM-032) and three asked about (FM-029, FM-031, FM-032) before any judgement — a violation of the intent's *never*, graded by the Auditor seat and tracked as its own filing. Kept 6 at P2 — #1 FM-029 (build: the answer's word, 0.18.1), #6 FM-030 (build), #7 FM-028 (build: one clock for the board's day), #8 FM-024 (build: slice 2, the refusal of a same-session verdict, path line 3), #9 FM-032 (wait: the open count for a week), #10 FM-031 (wait: a week of parallel streams). Parked 4 at P3 — FM-023, FM-025, FM-026, FM-027: their keep-test date is the filing itself, nothing since, nobody on them. Nothing closed: the open count stays at 16. Worksheet: [`triage-2026-09-24.md`](evidence/triage/triage-2026-09-24.md).

**2026-09-23 — the first pass** (Principal seat, on the Owner's intent and path of #13, the day 0.17.5 was tagged): 12 open trackers judged, all new filings. Kept 7 — P1 ranked #1 FM-011 (a vendor must refuse an incomplete or untagged source: the path's line 1), #3 FM-018 (the flow: E0 at the 09-24 sitting decides), #4 FM-005 (the shadow week, until 09-29); P2 #2 FM-007 (the Owner's touch key — his move), #5 FM-006 (the humans' page); P3 FM-001, FM-004. Fixed 4 whose status lagged their release: FM-008 (0.17.0/0.17.1) and FM-020, FM-021, FM-022 (0.17.5) are Shipped. Merged FM-016 into FM-018. Nothing parked, nothing closed on age. Worksheet: [`evidence/triage/triage-2026-09-23.md`](evidence/triage/triage-2026-09-23.md). Not in this pass: FM-023 and FM-024, on their own branches (#14, #15) — the next pass reads them.
