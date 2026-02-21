# Mockup-to-Code System Design

## Vision: Idea → Mockup → Code Pipeline

**Goal:** Repeatable, VLM-guided workflow that achieves 90%+ visual match from design mockups.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ SKILLS (Reusable Knowledge)                                 │
│ - icon-finding: VLM + topology + libraries                  │
│ - font-matching: Systematic Google Fonts search             │
│ - detail-refinement: Verification loops + approval          │
│ - vlm-iteration: Screenshot → compare → fix convergence     │
└─────────────────────────────────────────────────────────────┘
                              ↓ Loaded by
┌─────────────────────────────────────────────────────────────┐
│ AGENTS (Specialized Workers)                                │
│                                                              │
│ mockup-analyzer → blueprint-generator → font-matcher →      │
│ → code-generator → iteration-refiner → detail-validator     │
└─────────────────────────────────────────────────────────────┘
                              ↓ Orchestrated by
┌─────────────────────────────────────────────────────────────┐
│ RECIPES (Multi-Step Workflows)                              │
│                                                              │
│ mockup-to-code.yaml:                                        │
│   1. Analyze (blueprint + spec)                             │
│   2. Font search (with approval gate)                       │
│   3. Generate code                                          │
│   4. Iterative refinement (approval per iteration)          │
│   5. Production export                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓ Uses
┌─────────────────────────────────────────────────────────────┐
│ TOOLS & MCP                                                 │
│ - image-generation (Nano Banana Pro)                        │
│ - playwright-mcp (browser automation)                       │
│ - web_fetch (Google Fonts API)                              │
│ - file-ops (read/write)                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Skills Package

**Location:** `.amplifier/skills/mockup-to-code/`

#### `icon-finding.md`
```markdown
---
skill:
  name: icon-finding
  description: VLM-guided icon selection with topology awareness
  version: 1.0.0
  tags: [design, icons, vlm]
---

# Icon Finding Skill

## The Process

1. VLM describes icon visual appearance (not concept)
2. Identify topology (one-to-many vs many-to-many)
3. Check semantic meaning vs app context
4. Search libraries (Heroicons, Feather, Lucide)
5. Generate only if no match found

## Key Rules

- NEVER use emoji for UI elements
- Topology matters (share ≠ network)
- Context-specific meaning > generic conventions
- Prefer <1KB SVG over 500KB generated images

[Full content from ICON_FINDING_SKILL.md]
```

#### `font-matching.md`
```markdown
---
skill:
  name: font-matching
  description: Systematic Google Fonts search with VLM validation
  version: 1.0.0
  tags: [design, typography, vlm, google-fonts]
---

# Font Matching Skill

## Critical: Two-Font Typography Systems

Most designs use header/body pairing:
- Display font (titles, headings)
- Body font (text, metadata, labels)

Search for BOTH, not just one!

## The Systematic Search Process

1. Query Google Fonts API (1,900+ fonts)
2. Filter by category + weights needed
3. Create batch comparisons (20 fonts per page)
4. VLM picks top 2 from each batch
5. Finals comparison
6. VLM ranks finalists → Winner

[Full content from FONT_MATCHING_SKILL.md]
```

#### `detail-refinement.md`
```markdown
---
skill:
  name: detail-refinement
  description: Fine-tuning with verification loops and approval gates
  version: 1.0.0
  tags: [design, refinement, validation, approval]
---

# Detail Refinement Skill

## The Verification Pattern

CRITICAL: VLMs can contradict themselves. Always verify!

### Process:
1. VLM detail checklist (comparative analysis)
2. For each issue: VLM verification (original only)
3. Detect contradictions
4. Human approval for contradictions
5. Apply only verified fixes

## Why This Matters

VLM can say: "Make hero narrower"
But original shows: "Hero is wider than list cards"

→ CONTRADICTION
→ DO NOT apply automatically
→ Present to human for decision

[Full content from DETAIL_REFINEMENT_LESSON.md]
```

#### `vlm-iteration.md`
```markdown
---
skill:
  name: vlm-iteration
  description: Screenshot-compare-fix convergence loop
  version: 1.0.0
  tags: [design, iteration, vlm, convergence]
---

# VLM Iteration Skill

## The Convergence Loop

```
while match < 95%:
  1. Screenshot implementation
  2. VLM compares with original
  3. VLM identifies #1 issue  
  4. VLM provides exact fix
  5. Apply fix
  6. Match increases
  
Result: 50% → 70% → 80% → 90% in 3-5 iterations
```

## Key Principles

- One fix at a time (faster convergence)
- Fallback colors for debugging
- Test simple first (validate CSS works)
- Screenshot automation (Playwright)

[Full content from WHAT_WE_LEARNED.md]
```

---

### 2. Bundle: `mockup-to-code`

**Location:** `.amplifier/bundles/mockup-to-code/`

#### `bundle.md`
```yaml
---
bundle:
  name: mockup-to-code
  version: 1.0.0
  description: VLM-guided mockup-to-code pipeline

modules:
  tools:
    - module: tool-image-generation
      config:
        default_api: nano-banana-pro
    
  hooks:
    - module: hook-checkpoint
      config:
        checkpoints:
          - font_selection
          - iteration_approval
          - production_export

behaviors:
  - behavior: foundation:behaviors/agents  # Agent delegation
  - behavior: mockup-to-code:behaviors/vlm-pipeline

agents:
  mockup-analyzer: ./agents/mockup-analyzer.md
  font-matcher: ./agents/font-matcher.md
  detail-refiner: ./agents/detail-refiner.md
  implementation-validator: ./agents/implementation-validator.md

includes:
  context:
    - ./context/blueprint-patterns.md
    - ./context/typography-systems.md
    - ./context/refinement-checklists.md
  
  skills:
    - @skills:mockup-to-code/icon-finding.md
    - @skills:mockup-to-code/font-matching.md
    - @skills:mockup-to-code/detail-refinement.md
    - @skills:mockup-to-code/vlm-iteration.md
```

---

#### Agents Structure

**`agents/mockup-analyzer.md`**
```yaml
---
meta:
  name: mockup-analyzer
  description: |
    Generates comprehensive annotated blueprints from mockups using Nano Banana Pro.
    
    WHEN: Starting mockup-to-code pipeline
    WHAT: Creates foundation for implementation
    HOW: VLM annotation + component extraction
    
    Output:
    - Annotated blueprint PNG (containers, spacing, components)
    - Component specification JSON
    - Typography analysis
---

# Mockup Analyzer

You are specialized in analyzing design mockups and generating implementation-ready specifications.

## Your Capabilities

### Blueprint Generation
Use Nano Banana Pro with `reference_image` parameter to create comprehensive annotations:

- Container structure (colored boxes: Cards, Panels, Pills)
- Spacing arrows (RED=padding, BLUE=margin, GREEN=gap)
- Semantic component names (ArticleListItem, not just ListItem)
- Repetition markers (⟳ for looped components)
- Layout patterns (vertical, horizontal, space-between)
- Architecture diagram (fixed vs scrollable)

**Critical:** One comprehensive pass, not multiple separate annotations.

### Component Spec Extraction
Feed blueprint image back to VLM to extract structured data:

```json
{
  "containers": [...],
  "components": [...],
  "layout": {...},
  "spacing_system": {...}
}
```

### Typography Analysis
Identify font system:
- How many fonts? (usually 2: header + body)
- Which text uses which font?
- What weights are needed?

Load skills: `icon-finding`, `typography-systems`

## Process

1. Generate comprehensive blueprint
2. Extract component spec
3. Analyze typography
4. Save all artifacts
5. Report to parent session
```

---

**`agents/font-matcher.md`**
```yaml
---
meta:
  name: font-matcher
  description: |
    Systematic Google Fonts search using VLM visual ranking.
    
    WHEN: After mockup analysis identifies font needs
    WHAT: Finds best Google Fonts match from 1,600+ options
    HOW: Batch comparison + VLM ranking
    
    Can search serif (187 fonts) or sans-serif (362 fonts).
    Returns winner + fallback chain + weights.
---

# Font Matcher

You systematically search Google Fonts to find the best visual match.

## Your Capabilities

### Systematic Search
- Query Google Fonts metadata API
- Filter by category (serif/sans-serif) and weights
- Create batch comparison pages (20 fonts each)
- VLM visual ranking

### VLM-Guided Selection
- Screenshot comparison sheets
- VLM picks top 2 from each batch
- Finals comparison with semifinalists
- VLM final ranking

Load skill: `font-matching`

## Process

1. Identify font type needed (serif or sans-serif)
2. Query Google Fonts catalog
3. Create batch comparisons (187 serif OR 362 sans-serif)
4. VLM progressive elimination
5. Return: Winner + runner-up + third place + weights

## Output Format

```json
{
  "winner": "Playfair Display",
  "fallback_chain": ["David Libre", "Ibarra Real Nova", "Georgia"],
  "weights_needed": [400, 600, 700],
  "search_stats": {
    "fonts_evaluated": 187,
    "batches_processed": 10,
    "semifinalists": 20
  }
}
```
```

---

**`agents/detail-refiner.md`**
```yaml
---
meta:
  name: detail-refiner
  description: |
    Fine-tuning with verification loop and contradiction detection.
    
    MUST: Use verification pattern to prevent going backwards
    CRITICAL: Human approval required for contradictions
    
    WHEN: Implementation is 80-90% match, needs fine-tuning
    WHAT: Identifies and fixes spacing, sizing, positioning details
    HOW: Checklist → Verification → Approval → Apply
---

# Detail Refiner

You refine implementations to pixel-perfection using a verification loop.

## The Verification Pattern

**CRITICAL:** VLMs can contradict themselves. You MUST verify!

### Process:

1. **Detail Checklist (Comparative)**
   - Compare original vs current
   - Flag potential issues
   
2. **Verification (Original Only)**
   - For EACH flagged issue
   - Look at original mockup ONLY
   - Get ground truth measurements
   
3. **Contradiction Detection**
   - If checklist ≠ verification → CONTRADICTION
   - DO NOT apply automatically
   - Present to user for approval
   
4. **Apply Only Verified Fixes**
   - No contradictions → Apply
   - Contradictions → Wait for user

Load skill: `detail-refinement`

## Approval Template

When contradiction detected:

```
⚠️ CONTRADICTION DETECTED

Issue: {item_name}

Checklist suggests: {checklist_recommendation}
Original shows: {verification_observation}
Current state: {current_implementation}

Options:
A) Apply checklist suggestion
B) Keep current (matches verification)
C) Different approach

Which should I use?
```

## Example Contradiction

**Checklist:** "Make hero card narrower than list cards"
**Verification:** "Hero has 20px margins, list has 30px → Hero is WIDER"
**Action:** Present to user, don't apply automatically

This prevents going backwards!
```

---

**`agents/implementation-validator.md`**
```yaml
---
meta:
  name: implementation-validator
  description: |
    Screenshot → Compare → Fix iteration loop for convergence.
    
    WHEN: Implementation generated, needs refinement
    WHAT: Iteratively improves match percentage
    HOW: Automated screenshot + VLM comparison + one fix at a time
---

# Implementation Validator

You run the iteration convergence loop to reach 90%+ match.

## The Iteration Loop

```python
iteration = 0
while match_percentage < 95 and iteration < 10:
    1. Screenshot implementation
    2. VLM compares with original
    3. VLM identifies #1 issue + provides exact fix
    4. Apply fix
    5. iteration += 1
    6. Report progress
```

Load skill: `vlm-iteration`

## One Fix at a Time

**Why:** Single fixes converge faster than batch changes
- 50% → 70% → 80% → 90% in 3-5 iterations
- Each iteration validates previous fix worked

## Progress Reporting

After each iteration:
```
Iteration {n}: {match_percentage}%
Applied: {fix_description}
Next issue: {next_fix}
Continue? (yes/no)
```

Pause for user approval between iterations.
```

---

### 3. Recipe: `mockup-to-code.yaml`

**Location:** `@mockup-to-code:recipes/mockup-to-code.yaml`

```yaml
name: Mockup to Pixel-Perfect Code
description: |
  Complete VLM-guided pipeline from design mockup to production code.
  
  Phases:
  1. Analysis (blueprint + component spec)
  2. Font matching (systematic search with approval)
  3. Implementation (generate code)
  4. Refinement (iteration with approval per fix)
  5. Production (finalize assets)

inputs:
  mockup_path:
    type: string
    description: Path to mockup PNG file
    required: true
  
  output_dir:
    type: string
    description: Where to save generated files
    default: "./output"
  
  framework:
    type: string
    description: Target framework
    enum: [html, react, vue, svelte]
    default: html
  
  match_target:
    type: number
    description: Target match percentage
    default: 95

stages:
  # STAGE 1: ANALYSIS (No approval needed - just data gathering)
  - name: analysis
    approval_required: false
    steps:
      - agent: mockup-analyzer
        instruction: |
          Analyze mockup: {{mockup_path}}
          
          Tasks:
          1. Generate comprehensive annotated blueprint
             - Containers, spacing, components, layout
          2. Extract component specification JSON
          3. Analyze typography system
             - How many fonts? (header/body pairing)
             - Identify font characteristics
             - List weights needed
          
          Save to: {{output_dir}}/analysis/
        output_key: analysis
      
      - collect_analysis_data:
          blueprint_path: "{{analysis.blueprint_path}}"
          component_spec: "{{analysis.component_spec}}"
          typography: "{{analysis.typography_analysis}}"

  # STAGE 2: FONT MATCHING (Approval gate - user reviews font choices)
  - name: font_search
    approval_required: true
    approval_prompt: |
      📚 Font Search Complete
      
      Serif (for titles):
        🥇 Winner: {{serif_result.winner}}
        🥈 Runner-up: {{serif_result.runner_up}}
        📊 Evaluated: {{serif_result.fonts_evaluated}} fonts
      
      Sans-serif (for body):
        🥇 Winner: {{sans_result.winner}}
        🥈 Runner-up: {{sans_result.runner_up}}
        📊 Evaluated: {{sans_result.fonts_evaluated}} fonts
      
      Typography system:
        Titles: {{serif_result.winner}} (weights: {{serif_result.weights}})
        Body: {{sans_result.winner}} (weights: {{sans_result.weights}})
      
      Approve these font choices to proceed with implementation?
    
    steps:
      # Search serif for titles
      - agent: font-matcher
        instruction: |
          Search for SERIF font matching mockup titles.
          
          Mockup: {{mockup_path}}
          Target text: "{{analysis.typography.main_title_text}}"
          Characteristics: {{analysis.typography.serif_characteristics}}
          Weights needed: {{analysis.typography.serif_weights}}
          
          Process:
          1. Query Google Fonts (category=serif)
          2. Create batches (20 fonts each)
          3. VLM picks top 2 per batch
          4. Finals ranking
          
          Return: Winner + fallbacks + weights
        output_key: serif_result
      
      # Search sans-serif for body
      - agent: font-matcher
        instruction: |
          Search for SANS-SERIF font matching mockup body text.
          
          Mockup: {{mockup_path}}
          Target text: Metadata and descriptions
          Characteristics: {{analysis.typography.sans_characteristics}}
          Weights needed: {{analysis.typography.sans_weights}}
          
          Focus on top 40 most popular (covers 95% of usage).
          
          Return: Winner + fallbacks + weights
        output_key: sans_result

  # STAGE 3: ICON SELECTION (Approval gate - user reviews icon choices)
  - name: icon_selection
    approval_required: true
    approval_prompt: |
      🎨 Icons Identified
      
      {{icons.count}} icons needed:
      {{#each icons.list}}
      - {{this.name}}: {{this.description}}
        Library match: {{this.library_icon}} ({{this.source}})
        {{#if this.requires_generation}}⚠️ No library match - will generate{{/if}}
      {{/each}}
      
      Approve icon selections?
    
    steps:
      - agent: icon-finder
        instruction: |
          Identify and source icons for mockup: {{mockup_path}}
          
          Process:
          1. VLM describes each icon visually
          2. Check topology (hub-spoke vs mesh)
          3. Search libraries (Heroicons, Feather, Lucide)
          4. Flag any that need generation
          
          Return: Icon specs with sources
        output_key: icons

  # STAGE 4: IMPLEMENTATION (No approval - just execute spec)
  - name: implementation
    approval_required: false
    steps:
      - agent: code-generator
        instruction: |
          Generate {{framework}} implementation.
          
          From:
          - Component spec: {{analysis.component_spec}}
          - Fonts: {{serif_result.winner}} + {{sans_result.winner}}
          - Icons: {{icons.list}}
          - Blueprint: {{analysis.blueprint_path}}
          
          Output: {{output_dir}}/{{framework}}/demo.html
          
          Include:
          - Google Fonts imports
          - SVG icons inline
          - Fallback colors for debugging
          - Responsive viewport
        output_key: implementation

  # STAGE 5: REFINEMENT (Approval per iteration - loop until 95%)
  - name: refinement
    approval_required: true
    approval_prompt: |
      🔄 Iteration {{context.iteration}} Complete
      
      Match: {{refinement.match_percentage}}% (target: {{match_target}}%)
      
      Issue identified: {{refinement.issue_description}}
      Suggested fix: {{refinement.suggested_fix}}
      
      {{#if refinement.contradiction_detected}}
      ⚠️ CONTRADICTION DETECTED
      Checklist says: {{refinement.checklist_says}}
      Original shows: {{refinement.original_shows}}
      
      Which should I apply?
      A) Checklist suggestion
      B) Keep current (matches original)
      C) Skip this fix
      {{/if}}
      
      Continue refinement?
    
    while_condition: "{{refinement.match_percentage}} < {{match_target}}"
    break_when: "{{context.iteration}} >= 10"
    
    update_context:
      iteration: "{{context.iteration + 1}}"
      match_history: "{{append match_history refinement.match_percentage}}"
    
    steps:
      - agent: detail-refiner
        instruction: |
          Refinement iteration {{context.iteration}}.
          
          Compare:
          - Original: {{mockup_path}}
          - Current: {{implementation.demo_url}}
          
          Process:
          1. VLM detail checklist
          2. Verify each issue against original
          3. Detect contradictions
          4. If contradiction: FLAG for human approval (don't apply)
          5. If verified: Apply fix
          
          Return: Match %, issue, fix, contradiction status
        output_key: refinement

  # STAGE 6: PRODUCTION (Final approval before export)
  - name: production
    approval_required: true
    approval_prompt: |
      ✅ Refinement Complete - {{refinement.match_percentage}}% match
      
      Ready for production export:
      - Generate final assets with Nano Banana Pro
      - Replace placeholders
      - Optimize and minify
      - Export clean code
      
      Proceed with production build?
    
    steps:
      - agent: asset-generator
        instruction: |
          Generate production-ready assets:
          
          1. Nano Banana Pro: Generate actual images
             - Hero backgrounds
             - Article thumbnails
             - Replace all placeholders
          
          2. Optimize:
             - Minify CSS
             - Inline critical CSS
             - Lazy-load images
          
          3. Export:
             - Clean HTML/CSS (remove debug comments)
             - Package with assets
             - Generate README with font/asset credits
          
          Output: {{output_dir}}/production/
        output_key: production_build

summary: |
  Mockup-to-Code Pipeline Complete! 🎉
  
  Analysis: {{analysis.component_count}} components identified
  Fonts: {{serif_result.winner}} + {{sans_result.winner}}
  Icons: {{icons.count}} sourced
  Iterations: {{context.iteration}}
  Final match: {{refinement.match_percentage}}%
  
  Location: {{output_dir}}/production/
```

---

## Usage Examples

### Quick Start (Recipe)

```bash
# Complete pipeline with approval gates
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@mockup-to-code:recipes/mockup-to-code.yaml \
  context='{
    "mockup_path": "mockups/meditation-blog.png",
    "output_dir": "output/meditation-app",
    "framework": "html",
    "match_target": 95
  }'

# Recipe will pause at:
# 1. Font selection approval
# 2. Icon selection approval  
# 3. Each refinement iteration
# 4. Final production export
```

---

### Interactive (Agent Delegation)

```bash
amplifier run --bundle mockup-to-code

# In session:
> Analyze this mockup: mockups/new-design.png

> Search fonts for the typography system
# Agent: "Found Playfair Display (serif) + Roboto (sans). Approve?"

> Generate implementation with approved fonts

> Start iterative refinement
# Agent: "Iteration 1: 70% match. Issue: Tab underline positioning. Fix: ... Apply?"
# Agent: "Iteration 2: 82% match. Issue: Hero card width. **CONTRADICTION DETECTED** ..."
```

---

### Modular (Individual Agents)

```bash
# Just analyze
amplifier run "Delegate to mockup-analyzer: analyze mockups/design.png"

# Just find fonts
amplifier run "Delegate to font-matcher: find serif font for this mockup's titles"

# Just refine
amplifier run "Delegate to detail-refiner: compare mockups/design.png with demo.html"
```

---

## What Makes This System Repeatable

### 1. **Skill-Based Knowledge**
- Load `font-matching` skill → Get systematic search process
- Load `icon-finding` skill → Get topology awareness
- Load `detail-refinement` skill → Get verification pattern
- Reusable across projects

### 2. **Agent Specialization**
- Each agent has ONE job
- Agents compose skills + context
- Agents are context sinks (heavy docs in their context, not main session)

### 3. **Recipe Orchestration**
- Declarative workflow
- Approval gates at decision points
- Resumable (interruption → resume)
- State tracking (match percentage, iteration count)

### 4. **Verification & Approval**
- Contradiction detection prevents going backwards
- Human-in-loop for key decisions
- VLM validates, human approves

---

## Build Order

To make this real:

**Phase 1: Skills (1-2 hours)**
- [ ] Convert 4 markdown files to Amplifier skill format
- [ ] Add frontmatter, structure properly
- [ ] Test with `load_skill`

**Phase 2: Bundle (2-3 hours)**
- [ ] Create bundle.md with composition
- [ ] Write 4 agent descriptions
- [ ] Add context files
- [ ] Test bundle loads

**Phase 3: Recipe (2-3 hours)**
- [ ] Write mockup-to-code.yaml
- [ ] Add approval gates
- [ ] Test with meditation blog mockup
- [ ] Validate approval flow works

**Phase 4: Documentation & Testing (1-2 hours)**
- [ ] Usage guide
- [ ] Example walkthrough
- [ ] Test on NEW mockup (prove repeatability)

**Total: ~8-10 hours to productionize**

---

## Immediate Next Steps

**Want me to:**

1. **Create the bundle skeleton** (directory structure, bundle.md draft)?
2. **Convert one skill as example** (show you the format)?
3. **Write the recipe** (show the orchestration)?
4. **Clean up this workspace** and commit what we've learned?
5. **All of the above in order?**

We have all the pieces - now it's about packaging them properly in Amplifier's bundle/skill/recipe system! 🎯
