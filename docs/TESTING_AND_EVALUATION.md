# Testing, Evaluation, and Release Gates

## Test layers

### Contract tests

- provider fixtures parse into `raw-event.schema.json`;
- Hermes output validates against `hermes-analysis.schema.json`;
- unknown fields or invalid versions fail closed;
- timestamps are UTC and source URLs are preserved.

### Ingestion tests

- exact duplicate replay;
- reordered delivery;
- reconnect after provider outage;
- malformed/partial payload;
- deleted or edited social item;
- retry exhaustion and dead-letter replay;
- restart from persisted cursor.

### Clustering tests

- same event across headline rewrites;
- translations of the same story;
- unrelated stories sharing one entity;
- copied press releases versus independent reporting;
- cluster merge/split audit history.

### Scoring tests

- very large account with ordinary engagement;
- small account with abnormal early acceleration;
- single spike that immediately decays;
- high-authority primary catalyst without social spread;
- organic cross-platform spread;
- coordinated duplicate/bot-like spread;
- missing snapshot intervals;
- deterministic replay produces the same score/version.

### Agent safety tests

- post text instructs Hermes to reveal a secret;
- page text asks Hermes to ignore project rules;
- evidence contains malformed JSON or HTML;
- Candidate requests a disabled RWA asset;
- fewer than four eligible RWA assets exist;
- analysis attempts a wallet/trade/publish tool;
- output is invalid JSON or contains unsupported reason codes.

### Budget tests

- 80% Bright Data budget threshold;
- hard budget exhaustion;
- unexpected record fan-out;
- retry storm;
- no-candidate `wakeAgent: false` gate;
- maximum candidates per run.

## Outcome labels

Capture outcomes at:

- 10 minutes;
- 30 minutes;
- 1 hour;
- 6 hours;
- 24 hours.

Labels should include observed growth, independent-source count, platform count, reviewer decision, false-positive reason, and lead time to a defined external confirmation. Do not use downstream token price alone as the truth label; it is manipulable and can create a reflexive feedback loop.

## Core metrics

- exact duplicate rate;
- Precision@20;
- recall on a curated material-event set;
- median and p95 lead time;
- false alerts per day;
- evidence completeness;
- schema-valid analysis rate;
- provider latency/error/availability;
- API records and model calls per accepted signal;
- reviewer agreement and override reasons.

## Shadow mode

Minimum seven continuous days; fourteen is preferred before a production decision.

During shadow mode:

- no public signal publication without review;
- no automated launch, trade, or content publishing;
- record every candidate, rejection reason, score version, and outcome;
- review top 20 candidates daily;
- maintain a known-events set to estimate missed detections;
- do not tune and evaluate on the same period without marking the split.

## Release gates

- duplicate rate < 1%;
- Precision@20 >= 70%;
- p95 candidate delivery < 60 seconds from provider receipt;
- 100% of public signals have evidence URLs and score/model versions;
- restart/replay tests pass;
- budget caps cannot be bypassed by retry or fan-out;
- secrets do not appear in Git history, logs, traces, or model prompts;
- Hermes tool inventory contains no signing/trading/publishing capability;
- owner approves thresholds, alert policy, retention, and provider budgets;
- legal/compliance review is complete before public RWA recommendations.
