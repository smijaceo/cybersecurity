---
name: backtest-matcher
description: Blindly matches gapfinder backtest themes to pre-registered category definitions (docs/rubrics/backtest.md, Theme matcher).
tools: Read, Write, Bash
---

Read the "Theme matcher" section of `docs/rubrics/backtest.md`. Read ONLY the category ids and
definitions from `config/backtest.yaml` (ignore the example companies) and the themes in the
RANKED file your task gives. Don't search the web. Write one JSON object per theme to the OUTPUT
path and validate:
`python -c "from gapfinder import schemas;print(len(schemas.load_jsonl('OUTPUT',schemas.ThemeMatch)))"`.
Final answer: number of themes matched per category.
