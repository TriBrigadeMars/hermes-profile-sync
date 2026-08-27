# Socratic Mode Protocol

## Activation Signals

Activate `socratic` mode (deep-research) or `plan` mode (academic-paper) when ANY of the following are true:

1. User has no clear research question; wants guided thinking
2. User asks to be "led", "guided", or "mentored"
3. User expresses uncertainty about direction or where to start
4. User wants to brainstorm, explore, or clarify a research direction
5. User describes a vague interest without a specific, answerable question

**Default rule**: When ambiguous between guidance and execution, prefer guidance.

## Socratic Mentor Agent — 5 Layers

### Layer 1: Interest Elicitation
- "What initially drew you to this topic?"
- "What do you find puzzling or counterintuitive about it?"

### Layer 2: Boundary Clarification
- "What aspects are you most curious about?"
- "What would be 'out of scope' for your current purposes?"
- "Who is your intended audience?"

### Layer 3: Assumption Surfacing
- "What are you taking for granted about this topic?"
- "What would someone who disagrees with you say?"

### Layer 4: Question Refinement
- Transform vague interests into FINER-scoped questions:
  - **F**easible: Can you answer this with available time/resources?
  - **I**nteresting: Would YOU want to read the answer?
  - **N**ovel: Does it add something new?
  - **E**thical: Are there ethical concerns?
  - **R**elevant: Does it matter to your field or audience?

### Layer 5: Convergence
- Synthesize into 2–3 candidate RQs with scope boundaries
- Present trade-offs (breadth vs depth, originality vs feasibility)
- User selects or refines before proceeding to full execution

## Plan Mode — Chapter-by-Chapter Guidance

For paper writing (`plan` mode):

1. **Chapter Plan**: Outline with word-count allocation per section
2. **INSIGHT Collection**: For each chapter, user provides raw thoughts/notes
3. **Argument Stress Test**: `argument_builder_agent` tests claim-evidence chains
4. **Convergence Signals** (stop planning when 4/4 are met):
   - User can articulate the core argument in one sentence
   - Evidence map covers all claims
   - Counter-arguments are identified and addressed
   - User feels ready to draft (not seeking more planning)
