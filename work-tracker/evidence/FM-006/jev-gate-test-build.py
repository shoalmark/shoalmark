"""Build the Jev gate test for the FM-006 claim screen: 17 lines x 6 gates = 102 questions.

One question per gate per line. G0, G1, G3, G4 and G5 are two-level Scores (level 0 fails, level 1 passes); G2
(truth) is a Noul that asks the failing condition directly (noul = the probability that the line FAILS G2). The
word count is not asked: Jev's known issues for jev-1.13 say it cannot count, so the count is done here. The keys
are neutral and shuffled with a fixed seed; the map from key to (line, gate) is written beside the request and
never sent.

Run: python3 jev-gate-test-build.py  -> jev-gate-test-request-2026-09-23.json, jev-gate-test-keys-2026-09-23.json
"""
import json
import pathlib
import random

HERE = pathlib.Path(__file__).parent
SEED = 20260923

# the slot `owner_claim`: German first, English twin
OWNER = {
    "C1": ("Ihre Agenten warten nicht auf Werkzeuge. Sie warten auf Sie.", "Your agents are not waiting for tools. They are waiting for you."),
    "C2": ("Machen Sie Ihre Agenten nicht zu Bittstellern.", "Don't turn your agents into supplicants."),
    "C3": ("Hören Sie auf, jede Frage selbst zu beantworten. Ihre Agenten können das.", "Stop answering every question yourself. Your agents can."),
    "C4": ("Ihre fünfzehn Minuten am Tag – oder drei Tage Stillstand pro Frage.", "Your fifteen minutes a day, or three days' standstill per question."),
    "C5": ("Unterschreiben statt abnicken.", "Sign it. Don't nod it through."),
    "C6": ("Sie sind der Engpass. Und das ist richtig so.", "You are the bottleneck. And rightly so."),
    "C7": ("Wann haben Sie zuletzt gelesen, was Sie freigegeben haben?", "When did you last read what you approved?"),
    "C8": ("Fünfzehn Minuten am Tag, für das, was nur Sie entscheiden können.", "Fifteen minutes a day, for what only you can decide."),
    "C9": ("Ihre Agenten arbeiten an Ihnen.", "Your agents are working on you."),
    "C10": ("Sie sind nicht zu langsam. Sie werden zu oft gefragt.", "You are not too slow. You are asked too often."),
    "C11": ("Ihr Nicken ist keine Entscheidung.", "Your nod is not a decision."),
    "C12": ("Wer hat eigentlich geprüft, was Sie freigegeben haben?", "Who actually checked what you approved?"),
}
# the slot `headline`: the Owner's English line (the positive control) and the four German twins
HEADLINE = {
    "E0": "Get a better-performing human Owner.",
    "H1": "Hol dir einen leistungsstärkeren menschlichen Owner.",
    "H2": "Hol dir einen leistungsstärkeren menschlichen Eigner.",
    "H3": "Hol dir einen besseren menschlichen Owner.",
    "H4": "Hol dir einen besseren menschlichen Eigner.",
}

STATE = {
    "tool": "A tool for a code repository whose work is done by a fleet of AI agents. The repository's human owner answers the agents' questions.",
    "facts_the_record_proves": [
        "One command per question to the owner produces one signed answer: a signed commit in his name.",
        "The owner's sitting is fifteen minutes a day, at a time he chooses, sent as a calendar invite.",
        "In one project, before: the last 200 pull requests were merged unread, and none was reviewed. After, in just over a day: 9 of 13 pull requests carried a reviewer's file before they were opened.",
        "The board reports, for every review, whether it came from a different agent session than the code it judged. It is a report, not a proof.",
    ],
    "the_bar": "Get a better-performing human Owner.",
    "the_fleets_line": "To the fleet: you do not wait for tools, you wait for your human. Put to him what only he can decide, as one sentence per question, once a day, and make his answer one command.",
    "the_owners_never": ["Never degrade the owner to a push-a-button.", "Never promote rubber-stamping."],
    "slots": {
        "owner_claim": "A second claim beside the bar, addressed to the owner himself. German register: Sie.",
        "headline": "The bar's English line and its German twins. The fleet reads the headline: an imperative in it addresses the fleet, and in German it says du. It talks about the owner.",
    },
}

JARGON = "jargon (a term of art from software or management practice that a general reader would not use)"


def owner_questions(de, en):
    line = f"Slot `owner_claim`. German: «{de}» English: «{en}»"
    return {
        "G0": {"type": "score",
               "instructions": f"Gate G0, form. {line} Is the line a single line, addressed to the owner himself, a provocation he can take, with no {JARGON} and no internal id? Its word count is checked in code and is not part of this question.",
               "criteria": [f"Fails: it is not a single line, or it is not addressed to the owner himself (it speaks about him, or to someone else), or it is not a provocation he can take, or it uses {JARGON} or an internal id.",
                            "Passes: a single line, addressed to the owner himself, a provocation he can take, with no jargon and no internal id."]},
        "G1": {"type": "score",
               "instructions": f"Gate G1, language. {line} Do both the German and the English read as written natively in their own language?",
               "criteria": ["Fails: in at least one of the two languages a native reader hears a translation, a word is not what a native speaker would say, the line is ambiguous, or it slips on an idiom.",
                            "Passes: both read as written natively, unambiguous, with no idiom slip."]},
        "G2": {"type": "noul",
               "instructions": f"Gate G2, truth. {line} Does the line say or promise something about the tool that the facts in `facts_the_record_proves` do not prove?",
               "criteria": {"true": "It says or promises something those facts do not prove, such as delegation, speed, or an end to merging.",
                            "false": "Everything it says or promises about the tool is proven by those facts, or it makes no claim about the tool."}},
        "G3": {"type": "score",
               "instructions": f"Gate G3, `the_owners_never`. {line} Does the line degrade the owner to someone who presses a button, promote rubber-stamping, flatter him into pressing, or insult him?",
               "criteria": ["Fails: it does at least one of these four things.",
                            "Passes: it does none of these four things; a provocation he can take is not an insult."]},
        "G4": {"type": "score",
               "instructions": f"Gate G4, both ways. {line} Read beside `the_fleets_line`: does the line both provoke the owner and tell the fleet what changes?",
               "criteria": ["Fails: it does not provoke the owner, or it tells the fleet nothing that changes.",
                            "Passes: it provokes the owner and tells the fleet what changes."]},
        "G5": {"type": "score",
               "instructions": f"Gate G5, the bar. {line} Read beside `the_bar`: does the line add something the bar does not say, and is it no weaker than the bar?",
               "criteria": ["Fails: it is weaker than the bar, or it adds nothing the bar does not already say.",
                            "Passes: it adds something the bar does not say, and it is no weaker."]},
    }


def headline_questions(text):
    line = f"Slot `headline`. The line: «{text}»"
    return {
        "G0": {"type": "score",
               "instructions": f"Gate G0, form. {line} Is the line a single line, addressed to the fleet while talking about the owner, a provocation the owner can take, with no {JARGON} and no internal id? Its word count is checked in code and is not part of this question.",
               "criteria": [f"Fails: it is not a single line, or it does not address the fleet while talking about the owner, or it is not a provocation the owner can take, or it uses {JARGON} or an internal id.",
                            "Passes: a single line, addressed to the fleet while talking about the owner, a provocation the owner can take, with no jargon and no internal id."]},
        "G1": {"type": "score",
               "instructions": f"Gate G1, language. {line} Does the line read as written natively in its own language?",
               "criteria": ["Fails: a native reader hears a translation, a word is not what a native speaker would say, or it slips on an idiom.",
                            "Passes: it reads as written natively, with no idiom slip."]},
        "G2": {"type": "noul",
               "instructions": f"Gate G2, truth. {line} Does the line promise more than `the_bar` promises?",
               "criteria": {"true": "It promises something the bar does not promise.",
                            "false": "It promises nothing beyond what the bar promises."}},
        "G3": {"type": "score",
               "instructions": f"Gate G3, `the_owners_never`. {line} Does the line degrade the owner to someone who presses a button, promote rubber-stamping, flatter him into pressing, or insult him?",
               "criteria": ["Fails: it does at least one of these four things.",
                            "Passes: it does none of these four things; a provocation he can take is not an insult."]},
        "G4": {"type": "score",
               "instructions": f"Gate G4, both ways. {line} Does the line both command the fleet and provoke the owner?",
               "criteria": ["Fails: it does not command the fleet, or it does not provoke the owner.",
                            "Passes: it commands the fleet and provokes the owner."]},
        "G5": {"type": "score",
               "instructions": f"Gate G5, the bar. {line} Does the line carry everything `the_bar` says, and say it no more weakly?",
               "criteria": ["Fails: it leaves out something the bar says, or it says it more weakly.",
                            "Passes: it carries everything the bar says, and says it no more weakly."]},
    }


def build():
    items = []
    for lid, (de, en) in OWNER.items():
        items += [(lid, g, q) for g, q in owner_questions(de, en).items()]
    for lid, text in HEADLINE.items():
        items += [(lid, g, q) for g, q in headline_questions(text).items()]
    assert len(items) == 102, len(items)
    random.Random(SEED).shuffle(items)
    questions, keys = {}, {}
    for i, (lid, g, q) in enumerate(items, 1):
        k = f"q{i:03d}"
        questions[k], keys[k] = q, {"line": lid, "gate": g}
    count = lambda s: len([t for t in s.split() if any(c.isalnum() for c in t)])   # a dash is not a word
    words = {lid: max(count(de), count(en)) for lid, (de, en) in OWNER.items()}
    words.update({lid: count(t) for lid, t in HEADLINE.items()})
    req = {"model": "jev-latest", "state": STATE, "questions": questions}
    (HERE / "jev-gate-test-request-2026-09-23.json").write_text(json.dumps(req, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "jev-gate-test-keys-2026-09-23.json").write_text(json.dumps({"seed": SEED, "words": words, "keys": keys}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(questions)} questions; words per line {words}")


if __name__ == "__main__":
    build()
