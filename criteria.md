# Capstone acceptance criteria — TakeMeter

Written before capstone executions or results. The previous unit's criteria
are preserved in criteria-unit5.md. These targets were drafted by Codex at
the user's request, which differs from the course's unaided-writing rule.
All five must hold in each of three independent trials. One run means one
JSON request in a fresh CLI process unless a batch is explicitly specified.

1. **Standalone inference (extension):** From a fresh checkout with the
   documented environment and exported model prepared, the documented start
   command must classify 10 valid comments and return 10 JSON responses with
   one of the four existing labels and confidence between 0 and 1, exiting 0.
   Why: a batch of ten represents a small thread skim; every comment needs a
   usable response. Environment installation and training are setup steps.

2. **Durable observability (extension):** For a batch containing 8 valid
   requests and 2 malformed JSON requests, the appended log must contain
   exactly 10 parseable records, each with timestamp, input, output, status,
   duration_ms, and cpu_seconds. Both durations must be nonnegative.
   Why: missing failures would prevent diagnosis; this batch checks that
   errors are as visible as successful predictions.

3. **Bad-input isolation (extension):** For each of five inputs (malformed
   JSON, missing text, empty text, numeric text, and a JSON list), followed
   by a valid request in the same process, the runner must return an error
   record then a valid prediction, without a traceback, and exit 1.
   Why: a broken comment must not discard the next comment in a thread;
   nonzero exit status also tells scripts the batch was partially invalid.

4. **Warm latency (extension):** In a single process, after one unmeasured
   warmup request, at least 9 of the next 10 valid requests must complete in
   at most 500 ms each, using duration_ms from the log.
   Why: half a second per comment keeps a ten-comment skim interactive;
   model loading is excluded and reported separately rather than hidden.

5. **Prediction preservation (regression):** On the first 10 held-out
   comments, all 10 CLI labels must equal direct inference from the same
   exported weights using truncation and max_length=256 in evaluation mode.
   Why: this extension packages an existing classifier; it should not
   change predictions. This checks equivalence, not accuracy.
