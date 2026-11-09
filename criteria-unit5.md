# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.55 on the held-out test split, on all three seeds

**Why this target:** With four labels, a uniform guesser gets 0.25. My counts
are roughly even, so always guessing the biggest label should get about 0.30.
0.55 is close to double that. At 0.55 the classifier is worth running as a
first pass over a thread. Any lower and you'd have to re-read everything it
sorted. I didn't go higher because the test split is only about 33 posts, so
one seed with an unlucky draw costs about 3 points per wrong answer.

---

## 2. Macro F1 is at least 0.50 on all three seeds

**Why this target:** Accuracy can hide one label being thrown away. Macro F1
weights all four labels equally, so it can't. It sits 0.05 below the accuracy
target because macro F1 is always pulled down by the weakest label, and with
about 8 test posts per label, the weakest one will be noisy.

---

## 3. Every label has an F1 of at least 0.35 on every seed — no label is abandoned

**Why this target:** This is a floor, not a goal. `experience` is likely to be
my thinnest label (it was about a fifth of the first 130 posts I read), so it
will have only 6–8 posts in test. A label at 0.35 F1 is still being predicted
and getting some right. A label at 0.00 means the model has stopped using it.
Across three seeds, every label has 12 chances to fall below this line, so
it's stricter than it looks.

---

## 4. The most-confident third of test predictions is at least 0.15 more accurate than the least-confident third, on all three seeds

(`results.json → confidence.accuracy_most_confident_third` minus
`accuracy_least_confident_third`.)

**Why this target:** The useful version of this tool is "trust the confident
calls, read the unsure ones yourself". That only works if confidence actually
separates right from wrong. A gap of 0.15 on thirds of about 11 posts each
means roughly two more correct answers in the confident third. Anything
smaller is within the noise of a split that size. I expect the confident third
to be dominated by `chatter` ("Thanks!", "Is that for a month or a year?"),
and the unsure third by argument/assertion posts. If the gap doesn't show up,
my hardest boundary isn't the model's hardest boundary, which would itself be
worth knowing.

---

## 5. I agree with the staff labels on at least 23 of the 30 staff posts (≥ 0.75), using `agreement.py`

**Why this target:** This is the only check on whether I label consistently
that doesn't come from me. The staff notes say a rate in the 70s is normal,
and I've set mine at the top of that band on purpose. The staff
`analysis`/`hot_take` rule ("is the fact load-bearing?") is the same test as
my own `argument`/`assertion` rule ("delete the conclusion, is a reason
left?"), and I'll have applied it about 200 times by then. If I can't clear
the normal range on a boundary I designed my whole taxonomy around, that tells
me my 200 labels are less consistent than I think.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
