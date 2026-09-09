# Trend Brain — Canonical Codex and Developer Handoff

Last updated: 2026-09-09

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
- JSON schemas for normalized raw events and Hermes analysis.
- Example source, scoring, and Hermes MCP configurations.
- Installable `trnd-viral-tracker` Hermes skill.
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

## 9. Cost model

- Prefer provider WebSockets for discovery instead of LLM polling.
- Run a cheap pre-check before every Hermes cron invocation.
- Wake Hermes only when new shortlisted candidates exist.
- Default maximum: 5 candidates per Hermes run.
- Default Bright Data enrichment budget: 50 returned records per day until real billing is measured.
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
7. Add selective Bright Data enrichment with a daily record budget.
8. Implement the constrained Internal MCP tools.
9. Deploy the Hermes skill and paused canary cron on the VPS.
10. Run the evaluation fixtures, then seven-day minimum shadow mode.
11. Build reviewer endpoints/UI.
12. Connect TRND.fun surfaces only after evidence and evaluation gates pass.

## 13. Required acceptance targets

- Exact duplicate rate below 1%.
- `Precision@20 >= 70%` on the labeled evaluation set.
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
- Initial topic/entity dictionaries and languages.
- Runtime enabled RWA asset catalog API/schema.
- Alert destination and severity policy.
- Confirmed daily/monthly provider and model budgets.

## 15. First command for the next developer/Codex

Read `AGENTS.md`, this file, and every file in `docs/`. Validate the included schemas and tests. Do not integrate a provider until secrets, budgets, retention, and terms are confirmed. Begin with the database and Internal API; do not begin with a large agent prompt or UI changes.
