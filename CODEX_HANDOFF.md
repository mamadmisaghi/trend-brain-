# Trend Brain — Canonical Codex and Developer Handoff

Last updated: 2026-09-11

## 1. Purpose

Trend Brain is the chain-neutral intelligence service for TRND.fun. It detects early public narratives across news and social sources, stores verifiable evidence, measures growth, asks Hermes to analyze only shortlisted candidates, and produces human-reviewed RWA pair recommendations.

It is not a launchpad, wallet, trading bot, content publisher, or autonomous financial agent.

## 2. Repository isolation

This repository is `mamadmisaghi/trend-brain-`. It was intentionally created separately. Do not push Trend Brain work into:

- the TRND.fun Robinhood-chain repository;
- the TRND Solana/Raydium repository;
- either website preview repository.

Those products may later consume Trend Brain through typed APIs. They are not source directories for this repository.

## 3. What has been completed here

- Canonical architecture and trust boundaries.
- Plain-language Persian owner guide.
- Provider-role and cost-control policy for Bright Data and 6551.
- Version 1 Viral Score and decision-state specification.
- Version 1 Coinability policy with hard-reject, promotion, review-only, feed-priority, and strict RWA gates.
- Version 2 low-cost discovery/watchlist policy.
- JSON schemas for normalized raw events and Hermes analysis.
- Backward-compatible v1 Hermes schema plus the new v2 semantic-analysis schema.
- Example source, Viral Score, Coinability, discovery, and Hermes MCP configurations.
- Installable `trnd-viral-tracker` Hermes skill v2 with a dedicated Coinability reference.
- Persian Coinability strategy and copy-ready Hermes master instruction.
- Hermes pre-run script that can skip the LLM when no candidates exist.
- Unit tests for that pre-run script.
- Shadow-mode evaluation and release gates.

## 4. What is not implemented

- PostgreSQL migrations and production data access layer.
- Always-on OpenNews/OpenTwitter WebSocket collector.
- Polling fallbacks, queues, retry/backoff, and dead-letter worker.
- Entity extraction and narrative clustering service.
- Deterministic feature and Viral Score service.
- Trend Brain Internal MCP/API.
- Bright Data enrichment worker and provider budget ledger.
- Hermes deployment on the owner's VPS.
- Reviewer/admin application.
- TRND.fun UI/API integration.
- Training data, calibrated thresholds, or production-quality evaluation evidence.

No document in this repository should be interpreted as evidence that those services are live.

## 5. Approved architecture

```text
6551 WebSockets / permitted polling
              -> raw event store
              -> normalization + exact dedupe
              -> narrative/entity clustering
              -> deterministic feature snapshots and Viral Score
              -> candidate queue
              -> selective Bright Data enrichment
              -> Hermes semantic analysis
              -> reviewer decision
              -> public Signal API
              -> downstream human-approved RWA launch flow
```

Hermes is the semantic analyst. It is not the always-on collector or system of record.

## 6. Provider allocation

- **6551 OpenNews:** primary news discovery, high-impact financial/official sources, WebSocket feed, provider AI rating as one feature.
- **6551 OpenTwitter:** priority-account watch, X search, tweet/quote/retweet evidence, WebSocket events.
- **6551 Daily News:** free broad pulse and fallback, not canonical truth.
- **Bright Data:** selective enrichment of a small candidate set across X, TikTok, YouTube, Instagram, Reddit, search, and page scraping.
- **OpenTrade:** optional read-only market validation. Never expose wallet/trade/swap/broadcast tools to the analyst.
- **Twitter-to-Binance Square:** out of scope for the intelligence engine; potential later human-approved publishing integration.

## 7. Decision model

Event stages:

- `CATALYST`: credible material event; social propagation not yet demonstrated.
- `EMERGING`: abnormal early velocity/acceleration with incomplete corroboration.
- `BREAKOUT`: sustained, quality-adjusted, cross-source or cross-platform spread.
- `REJECTED`: duplicate, false, stale, manipulated, irrelevant, or insufficient.
- `EXPIRED`: monitoring window ended without sufficient evidence.

Do not claim an event is viral merely because a high-authority source published it. Use `CATALYST` until propagation evidence appears.

Launch-oriented content is also classified into two independent lanes:

- `COINABLE_RADAR`: safe cultural moments with a compact identity and remix/community potential;
- `RWA_CATALYST`: material economic intelligence that may be valuable but is not automatically Coinable.

Hard news involving war, death, serious injury, disaster, emergency, victimization, serious illness/private grief, exploitation, explicit/hateful content, public-safety alerts, or existing-token promotion never enters the launch-oriented feed. Political/election and public-figure/brand-rights risks require human review. Routine official promotion is not Coinable without independently observed organic derivative evidence.

## 8. Scoring contract

The version 1 weighted components are:

- velocity: 25;
- acceleration: 15;
- baseline anomaly: 15;
- cross-platform spread: 15;
- quality-adjusted reach: 10;
- source authority: 10;
- novelty: 5;
- persistence: 5;
- manipulation penalty: separate 0–30 deduction.

Numeric feature calculation belongs in deterministic code. Hermes receives the feature vector, evidence, and candidate state; it returns semantic classification, reason codes, risk notes, entity mapping, and RWA relevance.

Coinability is separate from Viral Score. Hermes returns fixed semantic factor enums; deterministic backend code maps them to the numeric Coinability Score using `config/coinability.v1.json` and owns final feed eligibility. A famous author changes discovery priority only.

## 9. Cost model

- Prefer provider WebSockets for discovery instead of LLM polling.
- Run a cheap pre-check before every Hermes cron invocation.
- Wake Hermes only when new shortlisted candidates exist.
- Default maximum: 5 candidates per Hermes run.
- Default X rotating search: one query pack every 20 minutes with at most 25 results.
- Default Bright Data enrichment budget: 50 returned records per day until real billing is measured.
- Default Bright Data fan-out: at most two platforms and 20 records per event, only after Coinability pre-screening.
- Store provider/tool/result-count/latency/cost metadata for every call.
- Reserve at least 20% of daily budget for high-authority breaking events.
- At 80% daily usage, enrich only candidates with Viral Score >= 70.
- At 100%, stop nonessential enrichment and continue ingestion with explicit degraded-state flags.

## 10. Security decisions

- The Bright Data credential previously pasted into conversation must be rotated before deployment.
- No real secret is present in this repository.
- Provider MCP access must use allowlists.
- The Internal MCP is read-heavy and exposes one constrained analysis write operation.
- Every outbound provider call has a deadline, retry cap, and usage ledger entry.
- Scraped content is untrusted and must not be inserted into system/developer instructions.
- All downstream launches require a human decision and wallet signature outside Trend Brain.

## 11. Hermes deployment contract

Install the repository skill into `~/.hermes/skills/trnd/trnd-viral-tracker/`. Run Hermes scheduled work with the absolute repository `workdir` so `AGENTS.md` is loaded. Create the analysis cron paused, test it manually, inspect its execution history, then resume it.

Use `docs/HERMES_COINABILITY_STRATEGY_FA.md` as the canonical copy-ready instruction. The v2 cron must output `schemas/hermes-analysis-v2.schema.json`, not silently mix v1 and v2 records.

The pre-run gate calls `GET /internal/v1/candidates/pending-count`. Expected response:

```json
{"pending_count": 3}
```

It emits `{"wakeAgent": false}` when the count is zero, preventing an unnecessary model call.

## 12. Initial implementation order

1. Add PostgreSQL migrations for sources, raw items, metric snapshots, events, event links, features, scores, analyses, recommendations, reviews, outcomes, provider usage, jobs, and dead letters.
2. Implement the Internal API and health endpoints first, including the pending-count endpoint required by the included Hermes script.
3. Implement exact-post idempotent ingestion and replay fixtures.
4. Add OpenNews and OpenTwitter WebSocket collectors with reconnect and polling fallback.
5. Add entity extraction, canonical URL normalization, and narrative clustering.
6. Implement deterministic scoring from `config/scoring.v1.yaml`.
7. Implement deterministic Coinability scoring and final decision gates from `config/coinability.v1.json`.
8. Add the two-lane Coinable Radar / RWA Catalyst routing and v1-to-v2 analysis migration.
9. Add selective Bright Data enrichment with per-event and daily record budgets.
10. Implement the constrained Internal MCP tools.
11. Deploy the Hermes skill v2 and paused canary cron on the VPS.
12. Replay at least 1,000 stored candidates, then run seven-day minimum shadow mode; fourteen days is preferred.
13. Build reviewer endpoints/UI.
14. Connect the v2 public signal feed to TRND.fun only after evidence and evaluation gates pass.

## 13. Required acceptance targets

- Exact duplicate rate below 1%.
- `Precision@20 >= 70%` on the labeled evaluation set.
- `Coinable Precision@20 >= 70%` on a separately labeled evaluation set.
- Zero hard-reject leakage into the launch-oriented feed.
- Zero unsupported RWA matches.
- p95 internal candidate delivery below 60 seconds after provider receipt.
- Every public signal has at least one stored evidence record and source URL.
- Every score and analysis exposes its version.
- Zero unauthorized provider-budget overruns in shadow mode.
- Restart/replay does not duplicate raw events or public signals.
- No wallet, signing, launch, trading, swap, or publishing capability is reachable from Hermes.

## 14. Inputs still required from the owner

- Rotated Bright Data token, stored directly on the VPS rather than in chat or GitHub.
- 6551 token, stored directly on the VPS.
- Hermes version and `HERMES_HOME` path.
- VPS access/deployment workflow.
- PostgreSQL location or approval to provision it.
- Initial Tier A/Tier B account watchlists.
- Owner review of political-content and public-figure/brand-rights policy before public activation.
- Initial topic/entity dictionaries and languages.
- Runtime enabled RWA asset catalog API/schema.
- Alert destination and severity policy.
- Confirmed daily/monthly provider and model budgets.

## 15. First command for the next developer/Codex

Read `AGENTS.md`, this file, and every file in `docs/`. Validate the included schemas and tests. Do not integrate a provider until secrets, budgets, retention, and terms are confirmed. Begin with the database and Internal API; do not begin with a large agent prompt or UI changes.
