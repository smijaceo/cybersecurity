export const meta = {
  name: 'backtest',
  description: 'gapfinder D18: backtest the gap finder on pre-2020 data and calibrate the critic panel on historical startups',
  whenToUse: 'Test whether the method works (config/backtest.yaml, pre-registered). args.part: "gap" | "panel" | "both" (default). args.gap_from: "collect" (default) or "verify" to redo only category checks, matching and the report.',
  phases: [
    { title: 'Collect', detail: 'open discovery before the cutoff, into data/backtest.db' },
    { title: 'Judge', detail: 'relevance-judge per batch' },
    { title: 'Themes', detail: 'BERTopic + theme-namer, rank by demand' },
    { title: 'Verify', detail: 'backtest-verifier per pre-registered category' },
    { title: 'Match', detail: 'blind backtest-matcher' },
    { title: 'Calibrate', detail: 'calibration-builder, then 8 critics per historical concept' },
    { title: 'Report', detail: 'gapfinder backtest report' },
  ],
}

// Deterministic steps are `python -m gapfinder ...`; agents follow .claude/agents/<name>.md.
const part = (args && args.part) || 'both'
const DB = 'data/backtest.db'
const OUT = 'reports/backtest'
const CUTOFF = (args && args.cutoff) || '2020-01-01'   // must match config/backtest.yaml
const CATEGORIES = ['compliance-automation', 'cloud-posture-agentless', 'software-supply-chain',
  'secrets-in-code', 'browser-security', 'data-security-posture', 'non-human-identity',
  'identity-threat-detection', 'zero-trust-mesh-vpn', 'api-security']   // config/backtest.yaml
const CAL_LENSES = ['market-skeptic', 'competitor-analyst', 'security-practitioner',
  'technical-feasibility', 'gtm-pricing', 'legal-ethics', 'economic-buyer', 'defensibility']

const RUN = {
  type: 'object',
  properties: { ok: { type: 'boolean' }, exit_code: { type: 'integer' }, output: { type: 'string' } },
  required: ['ok', 'exit_code', 'output'],
}
async function sh(command, phase, label) {
  const r = await agent(
    `From the repository root (the gapfinder project), run exactly this shell command and nothing else:\n\n${command}\n\n` +
    'Do not modify any files yourself. Report ok=true only if the exit code is 0; output = last ~40 lines.',
    { phase, label: label || command.slice(0, 60), schema: RUN, model: 'haiku', effort: 'low' })
  if (!r || !r.ok) throw new Error(`command failed: ${command}\n${r ? r.output : 'runner died'}`)
  return r.output
}
const use = (name, task) => `Read .claude/agents/${name}.md and follow it exactly. It is your full instruction set.\n\n${task}`

async function gapBacktest() {
  const gapFrom = (args && args.gap_from) || 'collect'
  if (gapFrom === 'verify') {
    await sh(`python -m gapfinder --db ${DB} backtest rank --out-dir ${OUT}`, 'Themes', 'rank by demand')
    return verifyAndMatch()
  }
  phase('Collect')
  await sh(`python -m gapfinder --db ${DB} -v collect --segment open-discovery --before ${CUTOFF} --limit 50 ` +
           `--source github --source hn --source stackexchange --source serverfault --source ted --source jobs ` +
           `&& python -m gapfinder --db ${DB} stats`, 'Collect', `collect before ${CUTOFF}`)

  phase('Judge')
  const BATCHES = { type: 'object', properties: { batches: { type: 'array', items: { type: 'string' } } }, required: ['batches'] }
  const prep = await agent(
    `From the repository root run: python -m gapfinder --db ${DB} judge-prepare --out-dir ${OUT}/judge --batch-size 150\n` +
    'Return the batch file paths it printed (relative paths). Do not modify files yourself.',
    { phase: 'Judge', label: 'judge-prepare', schema: BATCHES, model: 'haiku', effort: 'low' })
  const batches = (prep && prep.batches) || []
  const judged = await pipeline(batches, (b) => {
    const labels = b.replace('batch-', 'labels-').replace(/\.json$/, '.jsonl')
    return agent(use('relevance-judge',
      `INPUT: ${b}\nOUTPUT: ${labels}\nImport when done with: python -m gapfinder --db ${DB} judge-import --batch ${b} --labels ${labels}`),
      { phase: 'Judge', label: `judge ${b.split('/').pop()}` })
  })
  if (judged.some((j) => j === null)) throw new Error('a judge batch failed; resume the run')

  phase('Themes')
  await sh(`python -m gapfinder --db ${DB} themes --out-dir ${OUT}`, 'Themes', 'BERTopic themes')
  const named = await agent(use('theme-namer',
    `Use INPUT ${OUT}/theme-naming-input.json and OUTPUT ${OUT}/theme-names.jsonl. ` +
    `Validate with: python -m gapfinder names-check --out-dir ${OUT}`), { phase: 'Themes', label: 'theme-namer' })
  if (!named) throw new Error('theme namer failed')
  await sh(`python -m gapfinder --db ${DB} backtest rank --out-dir ${OUT}`, 'Themes', 'rank by demand')
  return verifyAndMatch()
}

async function verifyAndMatch() {
  phase('Verify')
  const checks = await parallel(CATEGORIES.map((c) => () => agent(use('backtest-verifier',
    `CATEGORY ID: ${c}\nOUTPUT: ${OUT}/category-checks/${c}.jsonl`), { phase: 'Verify', label: `verify ${c}` })))
  if (checks.some((c) => c === null)) throw new Error('a category check failed; resume the run')
  await sh(`cat ${OUT}/category-checks/*.jsonl > ${OUT}/category-checks.jsonl`, 'Verify', 'merge checks')

  phase('Match')
  const m = await agent(use('backtest-matcher', `RANKED: ${OUT}/ranked.json\nOUTPUT: ${OUT}/matches.jsonl`),
    { phase: 'Match', label: 'blind matcher' })
  if (!m) throw new Error('matcher failed')
}

async function panelCalibration() {
  phase('Calibrate')
  const built = await agent(use('calibration-builder', 'Build the calibration set described in the rubric.'),
    { phase: 'Calibrate', label: 'calibration-builder' })
  if (!built) throw new Error('calibration builder failed')
  const IDS = { type: 'object', properties: { ids: { type: 'array', items: { type: 'string' } } }, required: ['ids'] }
  const listed = await agent('From the repository root list the files backtest/calibration/cal-*.input.json and return ' +
    'their ids (e.g. cal-01). Do not read the labels file. Do not modify files.',
    { phase: 'Calibrate', label: 'list calibration ids', schema: IDS, model: 'haiku', effort: 'low' })
  const ids = (listed && listed.ids) || []
  if (!ids.length) throw new Error('no calibration concepts')
  const jobs = ids.flatMap((id) => CAL_LENSES.map((lens) => [id, lens]))
  const res = await parallel(jobs.map(([id, lens]) => () => agent(use('critic',
    `CONCEPT ID: ${id}\nLENS: ${lens}\nROUND: 1\nOUTPUT: backtest/calibration/critiques/${id}/r1-${lens}.json\n` +
    `The concept is backtest/calibration/${id}.json and its input backtest/calibration/${id}.input.json ` +
    '(use these paths instead of ideas/). This is a calibration run: judge the idea as of its founding, from the ' +
    'concept text alone. Do NOT try to identify the real company, and do NOT read backtest/calibration-labels.jsonl.'),
    { phase: 'Calibrate', label: `${id} ${lens}` })))
  const failed = res.filter((r) => r === null).length
  if (failed) throw new Error(`${failed} calibration critiques failed; resume the run`)
}

const tasks = []
if (part === 'gap' || part === 'both') tasks.push(() => gapBacktest())
if (part === 'panel' || part === 'both') tasks.push(() => panelCalibration())
await parallel(tasks)

phase('Report')
const report = await sh(`python -m gapfinder --db ${DB} backtest report --out-dir ${OUT}`, 'Report', 'backtest report')
return { part, report }
