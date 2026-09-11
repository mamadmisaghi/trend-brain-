# Scoring and Decision Specification

## Separate outputs

Never compress the entire decision into one opaque value. Persist at least:

- `viral_score` (0–100): measured propagation potential/state;
- `coinability_score` (0–100): deterministic result derived from fixed Hermes semantic factor enums;
- `confidence` (0–1): completeness and consistency of evidence;
- `manipulation_risk` (0–100): likely coordinated, synthetic, spam, or misleading behavior;
- `rwa_relevance` (0–100): relationship to the runtime enabled RWA catalog.

Viral Score does not prove Coinability. Coinability does not prove RWA relevance. A high-authority or famous author changes discovery priority, not these conclusions.

## Coinability policy

The canonical policy is [`../config/coinability.v1.json`](../config/coinability.v1.json). Hermes returns only `NONE`, `WEAK`, `MEDIUM`, or `STRONG` for each semantic factor. Deterministic backend code maps those labels to points, applies the versioned weights and gates, and owns the final numeric score and feed decision.

Apply hard-reject and human-review gates before calculating or using Coinability. Routine official promotion is not Coinable unless independent organic derivative evidence exists. Preserve non-coinable financial news in the separate `RWA_CATALYST` lane rather than placing it in the launch-oriented feed.

## Viral Score v1

```text
base_score =
  0.25 * velocity
  + 0.15 * acceleration
  + 0.15 * baseline_anomaly
  + 0.15 * cross_platform
  + 0.10 * quality_reach
  + 0.10 * source_authority
  + 0.05 * novelty
  + 0.05 * persistence

viral_score = clamp(round(base_score - manipulation_penalty), 0, 100)
```

Each component is normalized to 0–100. `manipulation_penalty` is 0–30.

## Feature guidance

### Velocity

Use age-adjusted change, not total engagement. A possible raw measure is the robust z-score of `log1p(weighted_engagement_per_minute)` within the same author and post-age bucket.

### Acceleration

Measure the change in velocity across successive snapshots. Require at least two intervals for a high value.

### Baseline anomaly

Compare an item with historical behavior for the author, topic, language, platform, post format, and time bucket. Prefer median and median absolute deviation over mean/standard deviation when distributions are heavy-tailed.

### Cross-platform

Reward independent platforms and independent sources. Multiple copies of one press release are not independent confirmation.

### Quality-adjusted reach

Use unique accounts, authority, account age/history when permitted, and diversity. Do not let raw follower count dominate.

### Authority

Source credibility affects confidence/materiality, not proof of virality. An official filing can immediately produce a `CATALYST`, but it needs propagation evidence to become `BREAKOUT`.

### Novelty

Compare with recent narrative clusters. Penalize old articles, recycled media, translated copies, and renamed duplicates.

### Persistence

Require continued growth across multiple snapshots rather than a single transient spike.

### Manipulation

Signals include repetitive text, synchronized posting, low account diversity, abnormal engagement composition, suspicious referral patterns, copied media, and rapid decay after an isolated burst.

## Initial thresholds

| Viral Score | Candidate policy |
| --- | --- |
| 80–100 | Eligible for `BREAKOUT` if confidence >= 0.85 and manipulation risk < 25. |
| 65–79 | `HOT_WATCH`; enrich and resnapshot. |
| 45–64 | `MONITOR`; no public signal. |
| 0–44 | Discard or retain as negative training/evaluation data. |

Thresholds are hypotheses until validated. Never tune them only to maximize historical price performance.

## Event states

- `CATALYST`: credible/material evidence with limited propagation.
- `EMERGING`: abnormal early propagation; corroboration incomplete.
- `BREAKOUT`: sustained and sufficiently independent propagation.
- `REJECTED`: false, duplicate, manipulated, irrelevant, or unsupported.
- `EXPIRED`: monitoring window ended without meeting a state threshold.

## RWA matching

RWA matching happens after event analysis and never changes Viral Score. Calculate each enabled asset independently from:

- direct entity/security match;
- economic exposure;
- event materiality;
- geography/sector fit;
- timing;
- evidence confidence;
- compliance and availability gates.

For launch-oriented recommendations, require an evidence-backed `DIRECT_ENTITY` or `VERIFIED_ECONOMIC_EXPOSURE` relation and the policy minimum relevance score. Topic similarity, public-figure association, or a desire to fill the UI is insufficient.

Return four ranked matches only when the downstream product requires four and four eligible assets exist. Otherwise return `NO_SAFE_RECOMMENDATION`; never fill a slot with an invented or disabled asset.

## Versioning

Persist:

- feature version;
- scoring-policy version;
- evidence version;
- prompt version;
- model/provider version;
- RWA catalog version;
- recommendation-policy version.

Reprocessing produces a new versioned analysis. Do not overwrite the record that caused an earlier public decision.
