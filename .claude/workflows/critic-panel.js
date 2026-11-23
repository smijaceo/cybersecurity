export const meta = {
  name: 'critic-panel',
  description: 'gapfinder Phase 4: nine independent critics per concept, one revision, re-critique, go/no-go by code',
  whenToUse: 'Run or re-run the Phase 4 critic panel (docs/ROADMAP.md) over the concepts in ideas/. args.only: one opening id. args.from: "round1" (default), "revise" or "round2" to resume a stage.',
  phases: [
    { title: 'Prepare', detail: 'list concepts and validate them' },
    { title: 'Round 1', detail: '6 critics per concept' },
    { title: 'Revise', detail: 'concept-writer revision mode, re-validated' },
    { title: 'Round 2', detail: '6 critics per revised concept, checking round-1 objections' },
    { title: 'Decide', detail: 'gapfinder panel: go/no-go by code, reports' },
  ],
}

// Deterministic steps are `python -m gapfinder ...`; agents follow .claude/agents/critic.md and
// .claude/agents/concept-writer.md. Each concept moves through its stages independently.
// Lenses come from args.lenses or default to all nine (decision D19).
const LENSES = (args && args.lenses) || ['market-skeptic', 'competitor-analyst',
  'security-practitioner', 'technical-feasibility', 'gtm-pricing', 'legal-ethics',
  'economic-buyer', 'defensibility', 'founder-fit']
const STAGES = ['round1', 'revise', 'round2']
const from = (args && args.from) || 'round1'
if (!STAGES.includes(from)) throw new Error(`args.from must be one of ${STAGES.join(', ')}`)
const runs = (s) => STAGES.indexOf(s) >= STAGES.indexOf(from)

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

const dir = (id) => `ideas/critiques/${id}`
const out = (id, rnd, lens) => `${dir(id)}/r${rnd}-${lens}.json`

function critic(id, rnd, lens, phase) {
  const prior = rnd > 1 ? `\nPRIOR: ${out(id, rnd - 1, lens)}` : ''
  return agent(
    'Read .claude/agents/critic.md and follow it exactly. It is your full instruction set.\n\n' +
    `CONCEPT ID: ${id}\nLENS: ${lens}\nROUND: ${rnd}\nOUTPUT: ${out(id, rnd, lens)}${prior}`,
    { phase, label: `r${rnd} ${lens} · ${id}` })
}

async function panelRound(id, rnd, phase) {
  const res = await parallel(LENSES.map((lens) => () => critic(id, rnd, lens, phase)))
  const failed = LENSES.filter((_, i) => res[i] === null)
  if (failed.length) throw new Error(`${id} round ${rnd}: critics failed: ${failed.join(', ')}`)
  log(`${id}: round ${rnd} critiques done`)
  return res
}

// ------------------------------------------------------------------ Prepare
phase('Prepare')
const IDS = { type: 'object', properties: { ids: { type: 'array', items: { type: 'string' } } }, required: ['ids'] }
const prep = await agent(
  'From the repository root run: python -m gapfinder concept-render\nIt must exit 0 and prints "<id>: ok" per ' +
  'concept. Return the ids in printed order. Do not modify files yourself.',
  { phase: 'Prepare', label: 'concept-render', schema: IDS, model: 'haiku', effort: 'low' })
let ids = (prep && prep.ids) || []
if (args && args.only) ids = ids.filter((i) => i === args.only)
if (!ids.length) throw new Error('no valid concepts found')
log(`panel for ${ids.length} concept(s): ${ids.join(', ')}`)

// ------------------------------------------------------------------ per concept
const results = await pipeline(ids,
  async (id) => { if (runs('round1')) await panelRound(id, 1, 'Round 1'); return id },
  async (id) => {
    if (!runs('revise')) return id
    await sh(`mkdir -p ${dir(id)} && cp ideas/${id}.json ${dir(id)}/concept-r1.json`, 'Revise', `snapshot ${id}`)
    const w = await agent(
      'Read .claude/agents/concept-writer.md and follow it exactly. It is your full instruction set.\n\n' +
      `OPENING ID: ${id}\nREVISION ROUND 1`,
      { phase: 'Revise', label: `revise ${id}` })
    if (!w) throw new Error(`revision failed for ${id}`)
    await sh(`python -m gapfinder concept-render --only ${id}`, 'Revise', `validate ${id}`)
    return id
  },
  async (id) => { if (runs('round2')) await panelRound(id, 2, 'Round 2'); return id },
)
const failed = ids.filter((_, i) => results[i] === null)
if (failed.length) log(`concepts that did not finish: ${failed.join(', ')} — re-run with args.only and args.from`)

// ------------------------------------------------------------------ Decide
phase('Decide')
const decision = await sh('python -m gapfinder panel', 'Decide', 'gapfinder panel')
return { concepts: ids, failed, decision }
