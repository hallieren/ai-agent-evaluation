# Lab ch04: From Atlas to Eval Set

Following the Chapter 4 Lab steps:

1. Your input is your Chapter 3 failure mode atlas v1. `python labs/ch04/run.py`: the
   generation pipeline drafts YAML by "failure mode × persona" into `labs/ch04/drafts/`
   (default seven modes × four personas; pass your own mode names via `--modes`,
   control drafts per cell with `--n`).
2. Review every draft by hand: edit until it reads like a real user, or throw it away.
   Watch synthetic distortion in particular. When several angry cases read as the same
   anger, rewrite them yourself, and write different angers.
3. For every sev-1 failure mode, hand-write at least one anchor case, made
   assertion-decidable wherever possible
   (`golden-task-design-protocol.md` in `templates/ch04/`).
4. Land the reviewed cases as `cases/cases-50`, then run `python labs/ch04/coverage.py`:
   which cells are empty? Are the sev-1 rows non-zero? Rule every empty cell "fill" or
   "reasoned empty" and log it in the annotation bar of `templates/ch04/coverage-matrix.md`.
5. Drill one expiry: suppose the refund ceiling rises ($500 → $680, drill only, the
   policy ledger stays unchanged), check the basis register in
   `templates/ch04/label-expiry-policy.md`, and list the affected cases.

Without a model API: `run.py` needs a model (it exits with an error; `MODEL_FAKE=1` is
test-only), but all drafts can be hand-written, the pipeline only saves first-draft effort;
`coverage.py` is fully offline and runs any time.
