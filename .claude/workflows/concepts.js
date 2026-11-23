export const meta = {
  name: 'concepts',
  description: 'gapfinder Phase 3: write one validated startup concept per shortlisted opening',
  whenToUse: 'Generate or regenerate Phase 3 concepts (docs/ROADMAP.md) after the shortlist in config/shortlist.yaml or the Phase 2 data changes. args.only: an opening id to (re)write just that one.',
  phases: [
    { title: 'Prepare', detail: 'gapfinder concept-prepare' },
    { title: 'Write', detail: 'concept-writer per opening, self-validated' },
    { title: 'Render', detail: 'gapfinder concept-render: schema + grounding, ideas/<slug>.md' },
  ],
}

// Deterministic steps are `python -m gapfinder ...`; the writer follows .claude/agents/concept-writer.md.
const RUN = {
  type: 'object',
  properties: { ok: { type: 'boolean' }, exit_code: { type: 'integer' }, output: { type: 'string' } },
  required: ['ok', 'exit_code', 'output'],
}
async function sh(command, phase) {
  const r = await agent(
    `From the repository root (the gapfinder project), run exactly this shell command and nothing else:\n\n${command}\n\n` +
    'Do not modify any files yourself. Report ok=true only if the exit code is 0; output = last ~40 lines.',
    { phase, label: command.slice(0, 60), schema: RUN, model: 'haiku', effort: 'low' })
  if (!r || !r.ok) throw new Error(`command failed: ${command}\n${r ? r.output : 'runner died'}`)
  return r.output
}

phase('Prepare')
const IDS = {
  type: 'object',
  properties: { opening_ids: { type: 'array', items: { type: 'string' } } },
  required: ['opening_ids'],
}
const prep = await agent(
  'From the repository root run: python -m gapfinder concept-prepare\nIt must exit 0. It prints one path per ' +
  'opening like ideas/<id>.input.json. Return the <id> parts, in printed order. Do not modify files yourself.',
  { phase: 'Prepare', label: 'concept-prepare', schema: IDS, model: 'haiku', effort: 'low' })
let ids = (prep && prep.opening_ids) || []
if (args && args.only) ids = ids.filter((i) => i === args.only)
if (!ids.length) throw new Error('no openings to write')
log(`writing ${ids.length} concept(s): ${ids.join(', ')}`)

phase('Write')
const written = await pipeline(ids, (id) => agent(
  `Read .claude/agents/concept-writer.md and follow it exactly. It is your full instruction set.\n\nOPENING ID: ${id}`,
  { phase: 'Write', label: `concept-writer ${id}` }))
const failed = ids.filter((_, i) => written[i] === null)
if (failed.length) throw new Error(`concept writers failed: ${failed.join(', ')}; re-run with args.only`)

phase('Render')
const out = await sh(args && args.only ? `python -m gapfinder concept-render --only ${args.only}`
                                       : 'python -m gapfinder concept-render', 'Render')
return { concepts: ids, render: out, writers: written }
