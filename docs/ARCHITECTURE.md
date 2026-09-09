# Architecture

## Responsibilities

### Provider collectors

Receive provider data and persist the original identifiers, URLs, author/account, provider timestamps, receipt timestamp, text/hash, and raw payload reference. They do not classify investment direction or call an LLM.

### Normalizer and deduplicator

- canonicalize URLs and account identifiers;
- produce an exact native key `(provider, native_id)`;
- hash normalized text/media references for secondary duplicate detection;
- preserve provider payload provenance;
- make replay idempotent.

### Narrative clusterer

Link multiple posts/articles to one evolving event without deleting source-level evidence. Clustering may use entity overlap, canonical URLs, semantic similarity, time windows, and quoted-source relationships. Every automatic merge and split must be auditable.

### Feature service

Calculate deterministic snapshots. Absolute likes/views are insufficient; compare age-bucketed metrics against the same author's and topic's historical baselines using robust statistics.

### Enrichment worker

Use Bright Data only after deterministic screening. It may retrieve structured post/profile/video/comment data, cross-platform evidence, search results, or the contents of a known page. It must enforce per-event and daily budgets before each call.

### Hermes analyst

Read shortlisted evidence and deterministic features through the Internal MCP. Return a schema-valid semantic analysis. It never owns numeric source metrics, system state, or launch authority.

### Reviewer and delivery

Human reviewers can approve, reject, suppress, or request more evidence. Public APIs expose only approved or policy-eligible signals. A downstream launchpad retains its own wallet, catalog, compliance, and transaction controls.

## Recommended services

```text
trend-brain-api       HTTP API, auth, public/read models, reviewer endpoints
trend-brain-worker    queues, normalization, clustering, scoring, enrichment
trend-brain-streams   OpenNews/OpenTwitter WebSocket connections
trend-brain-mcp       narrow Internal MCP for Hermes
postgres              canonical application state
hermes-gateway        schedules analysis and delivers alerts
```

Redis may be added when queue throughput or distributed locking requires it; do not add it merely for architectural appearance.

## Event lifecycle

```text
RECEIVED
  -> NORMALIZED
  -> CLUSTERED
  -> SCORED
  -> DISCARDED | MONITOR | PENDING_HERMES
  -> ENRICHED
  -> ANALYZED
  -> CATALYST | EMERGING | BREAKOUT | REJECTED | EXPIRED
  -> REVIEWED
  -> PUBLISHED or SUPPRESSED
```

Transitions are append-only audit events. Corrections create a new version; they do not erase the previous decision.

## Minimum Internal MCP surface

| Tool | Mutability | Purpose |
| --- | --- | --- |
| `list_pending_candidates` | read | Return up to the policy maximum due for analysis. |
| `get_event_evidence` | read | Return normalized evidence and provenance. |
| `get_metric_snapshots` | read | Return deterministic feature inputs and changes. |
| `get_enabled_rwa_catalog` | read | Return current downstream-eligible assets. |
| `save_hermes_analysis` | constrained write | Validate schema/version and append one analysis. |
| `mark_candidate_reviewed` | constrained write | Complete the analyst queue lease idempotently. |

No arbitrary SQL, file access, shell, wallet, trade, publish, or provider-administration tool belongs in this surface.

## Reliability

- UTC timestamps and monotonic ingestion sequence.
- Bounded retries with exponential backoff and jitter.
- Dead-letter records with safe replay.
- Per-provider circuit breaker and degraded mode.
- Candidate leases to prevent parallel duplicate analysis.
- Analysis idempotency key `(event_id, evidence_version, model_version, prompt_version)`.
- Graceful shutdown and cursor persistence for stream collectors.
- Health, readiness, queue depth, lag, error-rate, and budget metrics.

## Storage and retention

Store normalized facts and evidence references as the canonical record. Raw third-party content retention must follow provider terms and legal review. Prefer URLs, identifiers, hashes, timestamps, and permitted excerpts over unnecessary full-content replication.
