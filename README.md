# gapfinder

Find unmet needs in the cybersecurity tools market, turn them into product concepts, and
stress-test each concept against a panel of critic agents.

- **Plan and status:** [docs/ROADMAP.md](docs/ROADMAP.md)
- **Decisions:** [docs/DECISIONS.md](docs/DECISIONS.md)

## Quick start

```bash
pip install -e '.[dev]'
python -m pytest

python -m gapfinder -v collect --segment appsec-supply-chain   # or omit --segment for all
python -m gapfinder stats
python -m gapfinder export --segment appsec-supply-chain --out data/appsec.jsonl

# quality review (decision D8): sample → relevance judge (Claude Code subagent) → evaluate
python -m gapfinder sample --out reports/phase1/roundN-sample.json
python -m gapfinder evaluate --sample reports/phase1/roundN-sample.json \
    --labels reports/phase1/roundN-labels.jsonl --report reports/phase1/roundN-review.md
```

`collect --fresh` clears a segment before re-collecting (use it after changing its search terms).

Segments and search terms live in [`config/segments.yaml`](config/segments.yaml). Signals are
stored in `data/signals.db` (SQLite, not committed).

Sources: Hacker News (Algolia API), GitHub issue search (set `GITHUB_TOKEN` for higher rate
limits), Stack Exchange (security.stackexchange.com, ~300 requests/day without a key).
