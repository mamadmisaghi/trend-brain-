# Data Sources, Tool Roles, and Cost Controls

## Source hierarchy

Evidence quality and viral propagation are different concepts. A primary official announcement may be highly credible before it is viral; a viral anonymous post may have low credibility.

Recommended source tiers:

- **Tier A:** official corporate, regulator, government, exchange, issuer, and named high-impact accounts; event-driven where possible.
- **Tier B:** established journalists, researchers, industry leaders, and specialist publications.
- **Tier C:** broad topic/keyword/hashtag discovery.
- **Tier D:** comments and anonymous/community chatter used for propagation evidence, never sole factual confirmation.

## 6551 OpenNews

Use for initial discovery and financial/news coverage. Useful tool families include latest/search/by-source/by-engine/high-score news and real-time subscription. Provider `aiRating` is a feature only; Trend Brain must independently store evidence, calculate its own features, and evaluate outcomes.

The provider advertises news, listing, on-chain, meme, market, and prediction categories. Availability, latency, quotas, and source rights must be measured in shadow mode rather than assumed from marketing documentation.

## 6551 OpenTwitter

Use for:

- priority-account monitoring;
- recent tweets and advanced search;
- tweet-by-ID evidence;
- quote and retweet evidence;
- monitored-account WebSocket events.

Watchlist mutation is an administrative action and should not be exposed to the scheduled analyst.

## 6551 Daily News

Use as a free broad-pulse or degraded-mode fallback. Its category/hot output is not a replacement for raw source evidence, account-level metrics, or the authenticated OpenNews feed.

## Bright Data

Use after a candidate passes deterministic screening:

- known X/TikTok/YouTube/Instagram/Reddit URL enrichment;
- profile/recent-post context where available;
- comments only when discussion quality or manipulation needs inspection;
- web search for independent corroboration;
- page scraping for a known official/public source.

Do not send every raw item to Bright Data. Structured social tools can be billed by returned record; enforce result limits in addition to request limits.

Recommended MCP groups are `social,advanced_scraping`. Do not enable unrelated Crunchbase, ZoomInfo, Google Maps Reviews, Zillow, browser-control, ecommerce, or publishing tools for the analyst.

## OpenTrade

Optional read-only downstream validation:

- market price/volume context;
- token metadata;
- public trades or trend indicators.

Never expose custodial wallet, order, swap, approval, liquidity, or broadcast operations to Trend Brain.

## Twitter-to-Binance Square

Out of scope. It publishes content and therefore belongs in a separate, human-approved communications service if ever adopted.

## Call funnel

An illustrative target funnel, to be recalibrated from real volume:

```text
1,000 raw items
  -> 100 normalized nonduplicates
  -> 20 event clusters worth scoring
  -> 5 candidates worth enrichment
  -> 1-3 Hermes analyses
  -> 0-1 public signals
```

## Runtime budgets

Track at minimum:

- provider and tool;
- request timestamp and duration;
- records requested and returned;
- estimated and invoiced cost when available;
- HTTP/MCP outcome and retry count;
- event/candidate that caused the call;
- daily/monthly budget state.

Default shadow-mode policy:

- Bright Data: 50 returned enrichment records/day;
- Hermes: maximum 5 candidates/run;
- maximum 3 paid snapshots/event unless manually overridden;
- reserve 20% of daily budget for Tier A breaking events;
- at 80% usage, require pre-enrichment Viral Score >= 70;
- at 100%, continue ingestion but stop optional enrichment and mark confidence as degraded.

## Credential policy

- Rotate any credential pasted into chat before deployment.
- Never place a token in an MCP URL committed to Git.
- Keep values in protected server secret storage and use environment substitution.
- Redact query strings and authorization headers from logs, traces, exceptions, and screenshots.

## External references

- [Bright Data MCP tool groups](https://github.com/brightdata/brightdata-mcp)
- [Bright Data social APIs](https://docs.brightdata.com/api-reference/scrapers/social-media-apis/overview)
- [6551 OpenNews](https://github.com/6551Team/opennews-mcp)
- [6551 OpenTwitter](https://github.com/6551Team/opentwitter-mcp)
- [6551 Daily News](https://github.com/6551Team/daily-news)
- [6551 OpenTrade](https://github.com/6551Team/opentrade)
