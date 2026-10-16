# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts **Hacker News comments** by what the comment is offering the
reader and what it's standing on. Each comment gets one of four labels:
`experience` (backed by something the writer did or saw), `argument` (backed
by a fact, number, source or mechanism a reader could check),
`assertion` (a position with nothing behind it), or `chatter` (no claim about
the topic at all: thanks, jabs, questions). On HN, regulars skim for the
first two and skip the last two. This classifier tries to make that skim
explicit. Notes from the first reading pass are in
[`community_notes.md`](community_notes.md).

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Four labels. The question every label answers is the same one: **what is
this comment offering the reader, and what is it standing on?**

### `experience`

**Definition:** Supports its point mainly with something the writer personally
did, built, used, measured or saw happen.

**Example 1:**
> I have also been using 5.6 Sol instead of 6. I found 6 to burn through my usage incredibly quick, making it somewhat unusable because I wouldn't be able to get anything done.
>
> My results with 5.6 Sol were quite similar to 6, although I haven't tested it that much.

**Example 2:**
> That's the very reason I vibed my own daemon. I don't want the Logitech binary blob on my system. It needs too many permissions, it's huge, hogs memory and telemetry built in.
>
> My vibe coded daemon is just a few hundred LOC of go code I can inspect, modify and trust.

### `argument`

**Definition:** Supports a claim about the topic with at least one reason a
reader could check or dispute on its own — a fact, a number, a mechanism, a
source, an outside example — rather than the writer's own experience.

**Example 1:**
> Yes, that's how the trick works. Profit is revenue minus expenses. By increasing expenses, you decrease profit, and therefore tax. But it only works if you had a profit before, because the government doesn't pay you back tax when you lose money.

**Example 2:**
> And in 2018 the Pixel 2 was the Android flagship with 3 years of updates promised, with a Snapdragon 835 that was half the single thread speed of the corresponding A11 and slower in multicore with two extra cores.

### `assertion`

**Definition:** Takes a position on the topic — a verdict, a prediction, an
opinion, a sarcastic jab at the subject — and offers nothing to support it
beyond the claim itself.

**Example 1:**
> It's called growing up. And ultimately it's liberaing.
>
> Many people don't achieve that level of understanding before their death.

**Example 2:**
> Stock prices always include the expected future profits, that's the market rates a stock

### `chatter`

**Definition:** Makes no claim about the topic at all: thanks, praise or jabs
aimed at a person or their project, clarifying questions, concessions, bare
link drops, and talk about the thread itself.

**Example 1:**
> Hey. Thats looks really cool. Thanks!

**Example 2:**
> No! Surely not? Where did you read that?

### The hardest boundary

**Which two labels:** `argument` vs `assertion`. Hacker News commenters almost
always attach *something* to an opinion — a "because", an analogy, a "look at
X". Whether that something counts as support is where I kept stalling.

The post that sat right on it:

> The real farce is that you don't get paid for recycling. Really demonstrates that it's a complete charade.
>
> If there was any value in recycling you'd pay some fee for the packaging, and you'd get it right back when you recycle it.
>
> Outside of aluminum cans and bottle it certainly looks like recycling ends up being 'send it to the landfill, but with some extra steps and fees.'

**The decision rule I used every time:**

> **Delete the conclusion and look at what's left.** If what's left is a reason
> a reader could check or argue with *separately* — a fact, a number, a
> mechanism ("if it had value, you'd be paid for it"), a named example, a
> source — it's `argument`, even if the tone is a rant and even if the reason
> is wrong. If what's left is the conclusion said again more forcefully, an
> "everyone knows", a bare link, or nothing, it's `assertion`.

Under that rule the recycling post is `argument`: the deposit-refund mechanism
and the aluminum-can exception are reasons you can dispute on their own.
Being *wrong* doesn't move a post out of `argument`; having *no reason* does.

**The two other boundaries, and their rules:**

- **`experience` vs `argument` — the deletion test again.** Delete every
  first-person sentence ("I tried", "at my job", "we measured"). If the
  support collapses, it's `experience`. If outside facts or reasoning still
  carry the claim, it's `argument`, and the anecdote was colour.
- **`assertion` vs `chatter` — topic or people?** A claim about the subject of
  the thread is `assertion`, even as a joke or one-word verdict. Thanks,
  praise for the poster's own project, jabs at another commenter, "what did you
  mean?", and "you're right, my mistake" are `chatter`. A question that is
  really a claim ("So when will LLVM be rewritten in Rust?") is judged as the
  claim — here `assertion`.
- **A claim beats chatter.** If a post thanks someone *and* takes a position
  on the topic ("Great writeup, thanks — though I think you're wrong about
  compile times"), the claim decides the label, judged by its support.
- **Vague first person isn't `experience`.** "In my experience it's always
  worse" or "every benchmark I've seen says otherwise" names nothing the
  writer actually did. `experience` has to say what was done, used or seen.
  Otherwise it's judged as a bare claim.

**Added while labelling (posts the rules above didn't settle):**

- **Fact-only posts.** A one-line correction with nothing behind it
  ("Mozilla is not a company though", "They do have Fields medal winners
  among their staff") is `assertion` — the fact *is* the claim and nothing
  supports it. It becomes `argument` only when a specific detail does the
  work: a number, a date, a quote, a source, or an example with specifics
  (the Pixel 2 post above). A fact passed along with no position attached
  ("it starts at $2999 in Canada!") is `chatter`.
- **Recommendations are opinions.** "Try Librera if you haven't" and "Use
  Muse Glimmer. It's good." are `assertion` — a position on the topic with no
  support.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
cases. -->

**Where the posts came from:** Public Hacker News comments, pulled through
HN's public search API (`hn.algolia.com`, no login or key), from 188
front-page threads with 120+ comments posted in the 75 days before
2026-10-09. To stop the busiest AI-release threads from dominating, I took at
most 4 comments per thread, shuffled, and kept only comments of 25–900
characters, with no `[flagged]`/`[dead]` comments. Threads about wars,
deaths and US politics were filtered out by title. I also dropped 13 comments
by hand that got past the filter: a few on the same topics, plus some
fragments that made no sense without their parent comment. Posts are
whole and untrimmed. The HN link for every row is in
[`data/labels_sources.csv`](data/labels_sources.csv).

**How I labelled them:** All 248 rows were pre-labelled by Claude, an AI
assistant, working from the definitions and decision rules above. I'm
disclosing that plainly, and every row's `note` says so. The
pass went in two sweeps: the first 250 comments of the pool in order (237
kept), then a targeted pass for the thinnest label, which added 10
`experience` posts and 1 `assertion`. Posts that needed a rule to decide are
marked `hard:` in the `note` column with the two candidate labels. The
20-row cold pass is described under *Pre-labelling disclosure* below.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `argument` | 70 | 28% |
| `assertion` | 68 | 27% |
| `chatter` | 62 | 25% |
| `experience` | 48 | 19% |
| **Total** | 248 | 100% |

No label is near the 70% cap. `experience` is the thin one. It started at
38 (16%), which is why I went back for more. Even at 48 it lands only 7 posts
in the test split.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "it starts at $2999 in Canada!"
>
> *Could have been:* `assertion` or `chatter`
>
> *I chose, because:* `chatter`. It's a checkable fact about the topic, so my
> first instinct was `assertion`. But `assertion` is defined as *taking a
> position*, and this takes none — it reports a price with an exclamation
> mark. This post is where the "a fact passed along with no position is
> `chatter`" rule came from.

**2.**
> *The post:* "My experience has been that security is mostly treated as some contractual obligation that has little benefit and just costs money so the minimum amount of effort that prevents charges of gross negligence is put in. But I'm glad to hear that apparently there are places that take it more seriously."
>
> *Could have been:* `experience` or `assertion`
>
> *I chose, because:* `assertion`. It literally opens with "my experience",
> but it never says what the writer did, where, or what they saw. Under the
> vague-first-person rule that came out of the stress test, "my experience
> has been that X" with no specifics is a bare claim about X.

**3.**
> *The post:* "Did you even read my comment? Specifically this part: > There's 1000 chatgpt clones but everyone still uses chatgpt. There might be 1000 jev clones soon enough but people won't switch unless there's something significantly better about it. The fact that Jev will be cloned is exactly why brand and distribution matter even more. When 1,000 products do the same thing, you'll use the one you know."
>
> *Could have been:* `chatter` or `argument`
>
> *I chose, because:* `argument`. The opening line is a pure jab at the other
> commenter, and posts that open this way usually are `chatter`. But "a claim
> beats chatter", and the claim (brand matters more once a product is cloned)
> rests on an outside example you can check: ChatGPT clones exist and people
> still use ChatGPT. Delete the conclusion and that example is still there.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, the notebook default.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on **`mps` (Apple Silicon GPU), torch 2.14.1**, also
recorded in `results.json`. The whole of section 4 took well under a minute.

**Anything I changed from the defaults, and why:** Nothing. I wanted the
first run to be the plain recipe, so that next unit's improvement is the
only thing that moves.

One thing I checked rather than changed: the median post is 53 tokens, but
32 of 248 posts (13%) are longer than 128 tokens and get truncated. Those are
almost all `argument` and `experience` (23% of each, against 3–5% of
`assertion` and `chatter`). That's because supported posts are longer —
median 326 and 338 characters, against 131 for `assertion` and 89 for
`chatter`. So the model sees *less* of exactly the posts whose support often
comes at the end. I left `MAX_LENGTH` at 128 for this run and flagged it as a
candidate for unit 6.

**Split sizes:** train 172 · val 38 · test 38 (stratified 70/15/15, seed 42).

| Label | train | val | test |
|---|---|---|---|
| `experience` | 34 | 7 | **7** |
| `argument` | 48 | 11 | 11 |
| `assertion` | 47 | 11 | 10 |
| `chatter` | 43 | 9 | 10 |

`experience` has **7** examples in test, under the notebook's threshold of 8.
One post more or less changes its F1 by a lot, so expect it to be the
jumpiest number across next unit's three seeds.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: stress-testing the taxonomy before labelling**

- *What I asked for:* Eight posts sitting on the boundaries between my four
  labels, to classify using only the written definitions.
- *What came back:* Eight variations on one claim ("Rust compile times are a
  dealbreaker"): backed by our CI times, by monomorphization, by nothing; a
  "thanks, but you're wrong"; a Phoronix benchmark plus "matches my laptop";
  "Source? Every benchmark I've seen says the opposite"; a sarcastic price
  jab; and a bare link. Six sorted cleanly. Two didn't. "Thanks, but you're
  wrong" was both `chatter` and `assertion`. "Every benchmark I've seen" read
  as `experience` but named nothing.
- *What I changed:* Added two rules before labelling a single real post:
  **a claim beats chatter**, and **vague first person isn't `experience`**.
  The second one decided hard case 2 above.

**Moment 2: pre-labelling, and the gap it exposed**

- *What I asked for:* A first-pass label on each of the 250 collected posts,
  under the definitions and rules in this README, with any post that needed a
  rule to decide flagged in the `note` column.
- *What came back:* Labels for every post, but also a real inconsistency.
  "Mozilla is not a company though" (my original `assertion` example) and the
  Pixel 2 chip-speed post (my `argument` example) are *both* bare facts
  offered as a rebuttal, and nothing in my rules said why they differed.
- *What I changed:* Wrote the **fact-only** rule (a one-line correction with no
  detail behind it is `assertion`; a number, date, quote, source or specific
  example makes it `argument`; a fact with no position is `chatter`). I also
  swapped the Mozilla post out as the `assertion` example for one that isn't
  borderline. The flagged rows are the `hard:` notes in `labels.csv`.

**Pre-labelling disclosure:** All 248 labels in `labels.csv` were
pre-labelled by Claude (an AI assistant, run through Claude Code) and are
marked `pre-labelled (Claude)` in the `note` column. Claude also wrote the
collection script for the HN search API. **The 20-row cold pass has not been
done yet.** Those 20 rows have to be labelled by a person with no help, so
they can't be produced the same way. When it's done, those rows will be
marked `cold`, and how often the cold labels agree with the pre-labels will
be reported here.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.289 | 0.526 | +0.237 |
| Macro F1 | 0.112 | 0.453 | +0.340 |
| F1 — `argument` | 0.449 | 0.556 | +0.107 |
| F1 — `assertion` | 0.000 | 0.588 | +0.588 |
| F1 — `chatter` | 0.000 | 0.667 | +0.667 |
| F1 — `experience` | 0.000 | 0.000 | +0.000 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

Before running the zero-shot baseline, I expect it to score around 0.35–0.45
accuracy and below the seed-42 trained model's 0.526 accuracy. The four
definitions include subtle support and first-person rules that a general
entailment model may not apply consistently. This prediction was recorded after
the trained numbers were already known, so it is only a prediction about the
baseline, not a claim that I forecast the full comparison beforehand.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

On the same 38 held-out posts, fine-tuning added 0.237 accuracy and 0.340
macro F1 in the seed-42 run. The zero-shot model predicted `argument` for
all 38 posts, so learning the local taxonomy helped especially for
`assertion` and `chatter`. Neither method recognized `experience` in this
split. This is a comparison with the seed-42 trained run; the three-seed
results below show that its advantage is unstable. The baseline used the
definitions in `label_definitions.txt` and `facebook/bart-large-mnli`.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.55, all seeds | 0.526 | 0.289 | 0.368 | MISSED |
| 2. Macro F1 | ≥ 0.50, all seeds | 0.453 | 0.122 | 0.216 | MISSED |
| 3. Lowest per-label F1 | ≥ 0.35, every label, every seed | 0.000 (`experience`) | 0.000 (`experience`, `assertion`, `chatter`) | 0.000 (`experience`, `chatter`) | MISSED |
| 4. Confident third minus unsure third (accuracy) | ≥ 0.15, all seeds | 0.667 − 0.417 = 0.250 | 0.750 − 0.000 = 0.750 | 0.750 − 0.250 = 0.500 | MET |
| 5. Agreement with staff set | ≥ 23 / 30 | 30 / 30 | same check | same check | MET |

Per label, from section 6 (n_test = 38 on every seed; `mps`, torch 2.14.1):

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.526 | 0.289 | 0.368 | 0.237 |
| Macro F1 | 0.453 | 0.122 | 0.216 | 0.330 |
| F1 — `experience` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `argument` | 0.556 | 0.489 | 0.564 | 0.075 |
| F1 — `assertion` | 0.588 | 0.000 | 0.300 | 0.588 |
| F1 — `chatter` | 0.667 | 0.000 | 0.000 | 0.667 |

Accuracy moved 0.237 across seeds, more than the notebook's 10-point line for
a stable measure. Seed 42, the unit 5 run, was the friendly draw.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42 (the same run as `results.json`):

| true \ predicted | experience | argument | assertion | chatter |
|---|---|---|---|---|
| **experience** | 0 | 6 | 1 | 0 |
| **argument** | 0 | 10 | 1 | 0 |
| **assertion** | 1 | 4 | 5 | 0 |
| **chatter** | 0 | 5 | 0 | 5 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

Six real `experience` posts were predicted as `argument`, and none of the
11 real `argument` posts were predicted as `experience`. The model kept the
supported-claim cue but failed to use *whose evidence* supplied the support.
The other seed runs sent all seven `experience` posts to `argument` (seed 7)
or five to `argument` and two to `assertion` (seed 2024), so this is a repeated
boundary failure rather than one unlucky split.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.55 on all seeds | MISSED | 0.526, 0.289, 0.368; none clears 0.55. |
| 2 | Macro F1 | ≥ 0.50 on all seeds | MISSED | 0.453, 0.122, 0.216. |
| 3 | Every label F1 | ≥ 0.35 on every seed | MISSED | `experience` scores 0 on all three; `chatter` scores 0 on two. |
| 4 | Confidence gap | ≥ 0.15 on all seeds | MET | The gaps are 0.250, 0.750, 0.500. |
| 5 | Staff agreement | ≥ 23/30 | MET | The AI-assisted staff set labels match 30/30. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

Criteria 1–3 fail mainly because the model collapses toward `argument`.
At seed 7 it predicts `argument` for 34 of 38 test posts, including every
`experience` and `assertion` post; the near-perfect `argument` recall is
therefore misleading. `experience` has only 34 training examples and seven
test examples, and it is never predicted correctly on any seed. This looks
like a small-data and feature problem: the model sees generic support, but
does not reliably distinguish personal evidence from outside evidence.

The agreement check offers limited reassurance about rule application. The
30 staff posts use a different three-label taxonomy, and the categories in
this set are unusually cleanly grouped. Matching 30/30 shows the written
staff rules can be applied consistently here; it does not validate the
248 AI-prelabelled Hacker News rows or prove my own four-way boundaries are
consistent. In particular, no staff category tests `experience` against
`argument`, the model's largest confusion. `chatter` failing in two seeds
despite 62 examples, and seed accuracy ranging from 0.289 to 0.526, also
point to unstable learning from this small corpus rather than a single
incorrect staff-rule decision.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

`my_staff_labels.csv` was filled with AI assistance from the published staff
taxonomy, before running `agreement.py`; it was not a human cold pass. The
staff key was already in the repo. The earlier staff-vs-staff tooling check
confirmed the script's matching, but the figure below comes from the newly
filled file.

**Agreement rate:** 30 / 30 = 100%.

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

There are no disagreements to adjudicate. The borderline cases still matter:
`sp_014` includes a 3% figure, but uses it as decoration on an unsupported
claim, so it is `hot_take` under rule 1. `sp_028` gives a count of DNFs, but
draws no argument from it and reports the writer's current feeling, so it is
`reaction` under rules 2 and 3.

**What the pattern in my disagreements tells me:**

There is no disagreement pattern in this set. Its three categories are also
ordered in contiguous blocks, which makes 100% a weak test of whether I could
reliably label a mixed, unseen staff sample. It provides no evidence for
changing the Hacker News labels to force agreement.



---

## The Improvement

**What I changed:**

Raised the notebook's `MAX_LENGTH` from 128 to 256 tokens for the three-seed
rerun, leaving the data, split seeds, model, optimizer, and other settings
unchanged. The earlier audit found 32 of 248 posts longer than 128 tokens;
`argument` and `experience` were disproportionately affected.

**Which diagnosis pointed at it:**

The repeated `experience` → `argument` confusion suggested that the evidence
distinguishing a personal account might occur after the old cutoff. This
change tests that specific explanation; it may still fail if the problem is
too few examples or an inconsistent distinction in the prelabels.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.55, all seeds | 0.553 | 0.289 | 0.368 | MISSED |
| 2. Macro F1 | ≥ 0.50, all seeds | 0.508 | 0.120 | 0.216 | MISSED |
| 3. Lowest per-label F1 | ≥ 0.35, every label, every seed | 0.222 (`experience`) | 0.000 (`experience`, `assertion`, `chatter`) | 0.000 (`experience`, `chatter`) | MISSED |
| 4. Confident third minus unsure third (accuracy) | ≥ 0.15, all seeds | 0.667 − 0.500 = 0.167 | 0.667 − 0.000 = 0.667 | 0.667 − 0.167 = 0.500 | MET |
| 5. Agreement with staff set | ≥ 23 / 30 | 30 / 30 | same check | same check | MET |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

Only partly. Seed 42 gained one correct test post (0.526 → 0.553), macro F1
rose from 0.453 to 0.508, and `experience` F1 rose from 0 to 0.222.
Seeds 7 and 2024 did not improve in accuracy; their macro F1 stayed at
about 0.12 and 0.216. The longer input rescued one `experience` example
on the friendly seed but did not make the distinction reliable. Criteria
1–3 still miss across the three seeds; criteria 4–5 remain met. Both runs
used the same stratified split seeds and Apple MPS device, so the change
being tested is the 128-to-256 token limit.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

Accuracy, macro F1, and the per-label floor still fail. The seed-7 model
still sends all seven `experience` and all ten `assertion` test posts to
`argument`; seed 2024 also never predicts `experience` correctly. More
input text is therefore insufficient. The next experiment would audit a
blinded, human-labelled sample of the 248 Hacker News rows, especially
`experience`/`argument` and `chatter`/`argument`, then add or correct training
examples using the written rules. I stopped after the single controlled
improvement asked for here so that its effect is visible rather than mixed
with a simultaneous relabelling intervention. The 20-row human cold pass
from unit 5 is still blank and should be completed by a person before using
it to make any claim about prelabel accuracy.



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

The taxonomy distinguishes personal evidence from independently checkable
support, but the seed-42 model called six of seven personal-evidence posts
`argument` before the change and five of seven after it. In two seeds it also
missed every `chatter` post, so the model mostly learned a broad
supported-comment signal rather than the four intended functions.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
