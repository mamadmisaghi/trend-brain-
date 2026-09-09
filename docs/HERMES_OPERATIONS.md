# Hermes Installation and Operations

## Principle

Hermes is a semantic analyst over a small, pre-screened candidate queue. A normal backend owns streams, persistence, deduplication, deterministic scores, provider budgets, and retries.

## 1. Verify installed third-party skills and MCPs

The previously discussed `npx skills add` commands install skills/instructions. They do not by themselves prove that Hermes has a working MCP process and credential.

```bash
hermes skills list
hermes mcp test opennews
hermes mcp test opentwitter
hermes mcp test brightdata
```

After MCP configuration changes, run `/reload-mcp` in a new/current Hermes session.

## 2. Install the Trend Brain skill

Copy or symlink:

```text
hermes/skills/trnd-viral-tracker/
```

to:

```text
~/.hermes/skills/trnd/trnd-viral-tracker/
```

Then verify it appears in `hermes skills list` and test it in a fresh session with `/trnd-viral-tracker`.

## 3. Protect secrets

Put real provider values in the VPS secret store or `~/.hermes/.env` with owner-only permissions. Never paste them into the skill, cron prompt, repository, issue, or log. Use `${BRIGHTDATA_TOKEN}` substitution in remote MCP URLs/headers where supported by the installed Hermes version.

## 4. Configure provider MCPs

Start from [`../config/hermes-mcp.example.yaml`](../config/hermes-mcp.example.yaml). Merge only the required entries into `~/.hermes/config.yaml`. Probe the server, verify the exact advertised tool names, and retain the smallest allowlist.

Production recommendation: provider connectors belong behind Trend Brain services. The scheduled analyst should ultimately receive only the narrow `trnd-viral` Internal MCP.

## 5. Install the pre-run gate

Copy:

```text
hermes/scripts/trnd-pending-check.py
```

to:

```text
~/.hermes/scripts/trnd-pending-check.py
```

The script calls `GET /internal/v1/candidates/pending-count`. A zero count emits `{"wakeAgent": false}`, so Hermes skips the model invocation.

## 6. Create a paused canary

Adapt the absolute workdir to the VPS checkout:

```bash
hermes cron create "every 10m" \
  "Lease and analyze up to five pending Trend Brain candidates. Use only stored evidence, return schema-valid output, persist through the Internal MCP, and remain silent when no actionable signal exists." \
  --skill trnd-viral-tracker \
  --workdir /opt/trend-brain \
  --script trnd-pending-check.py \
  --name "trend-brain-analysis" \
  --paused \
  --paused-reason "Awaiting shadow-mode verification"
```

Pin the desired model and reasoning effort explicitly for this job if required. Do not assume changing the interactive chat model will change an existing cron job.

## 7. Verify before resuming

```bash
hermes cron run trend-brain-analysis
hermes cron runs trend-brain-analysis --limit 20
hermes cron doctor
```

Verify:

- no candidate -> no model invocation;
- one fixture -> one schema-valid analysis;
- a second run -> no duplicate analysis;
- provider content cannot inject instructions;
- an API failure becomes a visible failed run;
- no forbidden tool is registered for the job.

Resume only after the canary passes:

```bash
hermes cron resume trend-brain-analysis
```

## 8. Recommended job split

- continuous non-LLM services: provider streams and ingestion;
- every 5 minutes, no-agent: due metric snapshots and health/budget checks;
- every 10 minutes, gated Hermes job: shortlisted semantic analysis;
- every 6 hours: outcome snapshot/evaluation;
- daily: owner digest and usage report;
- weekly: calibration proposal requiring human approval.

## 9. Delivery

During shadow mode, save all outputs locally/database-side. Notify only on:

- `BREAKOUT` candidate;
- Tier A high-impact `CATALYST`;
- provider or cron failure;
- budget threshold;
- required human action.

Do not send a routine message for every unchanged run.

## 10. Operational checks

- `hermes cron doctor`
- `hermes cron incidents`
- `hermes cron runs trend-brain-analysis --limit 20`
- Internal API health/readiness
- queue lag and oldest pending candidate
- provider disconnect/retry count
- daily Bright Data records and model calls
- analysis schema validation failures

Hermes' internal `state.db` is not Trend Brain's database. Use the project's PostgreSQL database and public/internal contracts.

## References

- [Hermes MCP](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md)
- [Hermes Cron](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md)
- [Hermes Skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md)
