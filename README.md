# gapfinder

Find unmet needs in the cybersecurity tools market, turn them into product concepts, and
stress-test each concept against a panel of critic agents.

- **Plan and status:** [docs/ROADMAP.md](docs/ROADMAP.md)
- **Decisions:** [docs/DECISIONS.md](docs/DECISIONS.md)

## Quick start

```bash
pip install -e '.[dev]'
pip install --no-deps bertopic==0.17.4   # see decision D9 (avoids PyTorch)
python -m pytest

python -m gapfinder -v collect --segment appsec-supply-chain   # or omit --segment for all
python -m gapfinder stats
python -m gapfinder export --segment appsec-supply-chain --out data/appsec.jsonl

# quality review (decision D8): sample → relevance judge (Claude Code subagent) → evaluate
python -m gapfinder sample --out reports/phase1/roundN-sample.json
python -m gapfinder evaluate --sample reports/phase1/roundN-sample.json \
    --labels reports/phase1/roundN-labels.jsonl --report reports/phase1/roundN-review.md
```

Phase 2 gap analysis runs end to end with the saved Claude Code workflow
`.claude/workflows/gap-analysis.js` (ask Claude Code to "run the gap-analysis workflow from
<stage>"). The individual steps, if you need them:

```bash
python -m gapfinder judge-prepare --out-dir reports/phase2/judge   # then: relevance judge per batch
python -m gapfinder judge-import --batch <batch.json> --labels <labels.jsonl>
python -m gapfinder themes            # then: theme namer -> reports/phase2/theme-names.jsonl
python -m gapfinder threat-prepare    # then: threat mapper -> reports/phase2/threat-mapping.jsonl
python -m gapfinder market-prepare    # then: market-researcher per theme -> reports/phase2/market-research-parts/
python -m gapfinder market-merge
python -m gapfinder gaps              # -> reports/gaps-<date>.md
```

`collect --fresh` clears a segment before re-collecting (use it after changing its search terms).

Segments and search terms live in [`config/segments.yaml`](config/segments.yaml). Signals are
stored in `data/signals.db` (SQLite, not committed).

Sources: Hacker News (Algolia API), GitHub issue search (set `GITHUB_TOKEN` for higher rate
limits), Stack Exchange (security.stackexchange.com, ~300 requests/day without a key).
