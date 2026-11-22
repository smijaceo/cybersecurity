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
```

Segments and search terms live in [`config/segments.yaml`](config/segments.yaml). Signals are
stored in `data/signals.db` (SQLite, not committed).

Sources: Hacker News (Algolia API), GitHub issue search (set `GITHUB_TOKEN` for higher rate
limits), Stack Exchange (security.stackexchange.com, ~300 requests/day without a key).
