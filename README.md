# Trend Brain

Trend Brain is the planned evidence and reasoning layer behind the TRND.fun Viral Tracker. It is deliberately separate from the Robinhood-chain and Solana launchpad repositories.

The system is intended to:

1. ingest permitted public news and social signals;
2. normalize, timestamp, deduplicate, and cluster them into narratives;
3. calculate a measurable, versioned Viral Score;
4. use Hermes only for shortlisted semantic analysis;
5. produce evidence-linked signals and RWA pair recommendations;
6. require explicit human approval and wallet signature for every launch.

This repository currently contains the canonical specification, Hermes package, schemas, configuration examples, operational playbook, and implementation handoff. It does **not** yet contain a production collector, scorer, database service, or deployment.

## Start here

- Persian owner guide: [`docs/OWNER_GUIDE_FA.md`](docs/OWNER_GUIDE_FA.md)
- Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Data sources and cost policy: [`docs/DATA_SOURCES_AND_COSTS.md`](docs/DATA_SOURCES_AND_COSTS.md)
- Scoring and decisions: [`docs/SCORING_AND_DECISIONS.md`](docs/SCORING_AND_DECISIONS.md)
- Hermes installation and operations: [`docs/HERMES_OPERATIONS.md`](docs/HERMES_OPERATIONS.md)
- Testing and evaluation: [`docs/TESTING_AND_EVALUATION.md`](docs/TESTING_AND_EVALUATION.md)
- Developer/Codex handoff: [`CODEX_HANDOFF.md`](CODEX_HANDOFF.md)

## Repository map

```text
config/                         Versioned policy and Hermes MCP examples
docs/                           Architecture, operations, evaluation, owner guide
hermes/scripts/                 Hermes pre-run cost gate
hermes/skills/trnd-viral-tracker/  Installable Trend Brain Hermes skill
schemas/                        Machine-readable event and analysis contracts
tests/                          Tests for the included operational script
```

## Safety boundary

Trend Brain is recommendation-only. It must never hold private keys, sign transactions, launch tokens, trade, swap, approve spend, manage liquidity, or publish content automatically. Provider credentials belong only in protected server-side secret storage.

## Quick verification

```bash
python -m unittest discover -s tests -v
python -m json.tool schemas/raw-event.schema.json >/dev/null
python -m json.tool schemas/hermes-analysis.schema.json >/dev/null
```

## Primary external references

- [Hermes MCP configuration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md)
- [Hermes scheduled tasks](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md)
- [Hermes skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md)
- [Bright Data MCP](https://github.com/brightdata/brightdata-mcp)
- [6551 OpenNews MCP](https://github.com/6551Team/opennews-mcp)
- [6551 OpenTwitter MCP](https://github.com/6551Team/opentwitter-mcp)
- [6551 Daily News](https://github.com/6551Team/daily-news)
- [6551 OpenTrade](https://github.com/6551Team/opentrade)
