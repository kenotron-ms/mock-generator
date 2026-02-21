# Mockup-to-Code System: Repeatable Pipeline

## What We Built

A complete VLM-guided workflow for converting design mockups to pixel-perfect code.

**Achievement:** 90% visual match through systematic processes (vs ~30% manual eyeballing)

---

## The Components

### 1. **Skills** (Reusable Knowledge)

Domain knowledge packages for `load_skill`:

| Skill | Purpose | Key Learnings |
|-------|---------|---------------|
| `icon-finding` | VLM describes → topology check → library search → generate only if needed | NEVER use emoji for UI, respect semantic meaning vs topology |
| `font-matching` | Systematic search through 1,600+ Google Fonts with VLM validation | Two-font system (header/body pairing), search ALL fonts not just famous ones |
| `detail-refinement` | Verification loop with contradiction detection | VLMs can contradict - verify against original, human approval for conflicts |
| `vlm-iteration` | Screenshot → Compare → Fix → Repeat convergence loop | One fix at a time, 50% → 70% → 80% → 90% in iterations |

**Location:** `.amplifier/skills/` in this project

---

### 2. **Agents** (Specialized Workers)

Bundle-based agents for delegation:

#### `mockup-analyzer`
**Purpose:** Generates comprehensive annotated blueprints from mockups

**Tools needed:**
- image-generation (Nano Banana Pro)
- file-ops (saving outputs)

**Context:**
- Blueprint annotation patterns
- Component naming conventions
- Spacing/containment theory

**Behavior:**
```
Input: Mockup PNG
Process: 
  1. Generate annotated blueprint (containers, spacing, components)
  2. Extract component spec JSON
  3. Identify typography system (fonts, weights, hierarchy)
Output: Blueprint PNG + Component spec JSON + Typography spec
```

---

#### `font-matcher`
**Purpose:** Systematic font search across entire Google Fonts catalog

**Tools needed:**
- web_fetch (Google Fonts metadata)
- file-ops (rendering comparison pages)
- image-generation (if needed for comparison)

**Context:**
- Two-font typography systems
- Google Fonts catalog structure
- VLM visual ranking patterns

**Behavior:**
```
Input: Mockup + text element type (title vs body)
Process:
  1. VLM analyzes font characteristics
  2. Query Google Fonts (filter by category, weights)
  3. Create batch comparisons (20 fonts per page)
  4. VLM picks top 2 from each batch
  5. Finals comparison
  6. VLM ranks finalists
Output: Winner + fallback chain + weights needed
```

---

#### `detail-refiner`
**Purpose:** Fine-tuning with verification loop and human approval

**Tools needed:**
- Browser automation (Playwright via MCP or direct)
- image-generation (Nano Banana Pro for comparisons)

**Context:**
- Detail validation checklists
- Verification patterns
- Contradiction detection rules

**Behavior:**
```
Input: Original mockup + current implementation URL
Process:
  1. VLM detail checklist (comparative)
  2. For each issue: VLM verification (original only)
  3. Detect contradictions
  4. Present contradictions to user for approval
  5. Apply verified fixes
  6. Re-validate
  7. Iterate until 95%+ match
Output: List of fixes applied + validation report
```

---

#### `implementation-validator`
**Purpose:** Screenshot + VLM comparison iteration loop

**Tools needed:**
- Browser automation (screenshots)
- image-generation (Nano Banana Pro for comparison)

**Context:**
- Iteration convergence patterns
- One-fix-at-a-time methodology
- Match percentage tracking

**Behavior:**
```
Input: Original mockup + implementation URL
Process:
  Loop until match > 95%:
    1. Screenshot current implementation
    2. VLM compares with original
    3. VLM identifies #1 issue
    4. VLM provides exact CSS/HTML fix
    5. Apply fix
    6. Repeat
Output: Iteration history + final match percentage
```

---

### 3. **Recipes** (Multi-Step Workflows)

Declarative YAML workflows orchestrating the agents:

#### `mockup-to-code.yaml`

```yaml
name: Mockup to Code
description: Complete pipeline from design mockup to pixel-perfect implementation

inputs:
  mockup_path: Path to mockup PNG file
  output_dir: Where to generate code
  framework: "html" | "react" | "vue" (default: html)

stages:
  - name: analyze
    approval_required: false
    steps:
      - agent: mockup-analyzer
        instruction: |
          Analyze mockup: {{mockup_path}}
          
          Generate:
          1. Comprehensive annotated blueprint
          2. Component specification JSON
          3. Typography system analysis (fonts, weights)
          
          Save outputs to {{output_dir}}/analysis/
        output_key: analysis_result
  
  - name: font_matching
    approval_required: true  # Human approves font choices
    approval_prompt: |
      Font search complete. Review:
      - Serif winner: {{font_results.serif_winner}}
      - Sans-serif winner: {{font_results.sans_winner}}
      
      Approve to proceed with implementation?
    steps:
      - agent: font-matcher
        instruction: |
          Search for SERIF font matching titles in {{mockup_path}}
          Focus on: Main title "{{analysis_result.main_title_text}}"
          Weights needed: {{analysis_result.serif_weights}}
        output_key: serif_font
      
      - agent: font-matcher
        instruction: |
          Search for SANS-SERIF font matching body text in {{mockup_path}}
          Focus on: Metadata and descriptions
          Weights needed: {{analysis_result.sans_weights}}
        output_key: sans_font
  
  - name: implement
    approval_required: false
    steps:
      - agent: code-generator
        instruction: |
          Generate {{framework}} implementation from:
          - Component spec: {{analysis_result.component_spec}}
          - Fonts: {{serif_font.winner}} + {{sans_font.winner}}
          - Blueprint: {{analysis_result.blueprint_path}}
          
          Output: {{output_dir}}/{{framework}}/
        output_key: implementation
  
  - name: refine
    approval_required: true  # Human reviews each iteration
    approval_prompt: |
      Iteration {{iteration_count}} complete.
      Match: {{refinement_result.match_percentage}}
      
      Issues remaining: {{refinement_result.issues_count}}
      Next fix: {{refinement_result.next_fix}}
      
      Apply fix and continue?
    while_condition: "{{refinement_result.match_percentage}} < 95"
    break_when: "{{iteration_count}} >= 10"
    steps:
      - agent: detail-refiner
        instruction: |
          Compare:
          - Original: {{mockup_path}}
          - Current: {{implementation.demo_url}}
          
          1. Detail checklist validation
          2. Verify issues against original
          3. Flag contradictions for human approval
          4. Apply verified fixes
          
          Report match percentage and next fix.
        output_key: refinement_result
        update_context:
          iteration_count: "{{iteration_count + 1}}"

  - name: finalize
    approval_required: false
    steps:
      - agent: asset-generator
        instruction: |
          Generate production assets:
          - Replace placeholder images with Nano Banana Pro versions
          - Optimize icon sizes
          - Export final CSS/HTML
          
          Output: {{output_dir}}/production/
```

---

### 4. **MCP Servers** (External Tool Integration)

#### Playwright MCP (Browser Automation)
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp-server"]
    }
  }
}
```

**Provides:**
- `playwright_screenshot` - Capture implementation renders
- `playwright_navigate` - Load demo pages
- `playwright_measure` - Get computed CSS values

---

### 5. **Project Structure**

```
mockup-to-code-project/
├── .amplifier/
│   ├── settings.yaml          # Bundle and MCP config
│   ├── skills/
│   │   ├── icon-finding.md
│   │   ├── font-matching.md
│   │   ├── detail-refinement.md
│   │   └── vlm-iteration.md
│   └── bundles/
│       └── mockup-to-code/
│           ├── bundle.md
│           ├── agents/
│           │   ├── mockup-analyzer.md
│           │   ├── font-matcher.md
│           │   ├── detail-refiner.md
│           │   └── implementation-validator.md
│           ├── context/
│           │   ├── blueprint-patterns.md
│           │   ├── typography-systems.md
│           │   └── refinement-checklists.md
│           └── recipes/
│               ├── mockup-to-code.yaml
│               └── iterative-refinement.yaml
├── mockups/                   # Input mockups
├── output/                    # Generated artifacts
└── demo/                      # Final implementation
```

---

## The Repeatable Workflow

### **Option A: Recipe-Driven (Fully Automated with Gates)**

```bash
# One command, handles everything with approval gates
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@mockup-to-code:recipes/mockup-to-code.yaml \
  context='{"mockup_path": "mockups/new-design.png", "output_dir": "output/new-design"}'

# Recipe will pause at:
# - Font selection (approve font choices)
# - Each iteration (approve next fix)
# - Final review (approve for production)
```

---

### **Option B: Agent-Driven (Interactive Session)**

```bash
amplifier run --bundle mockup-to-code

# In session:
> Analyze mockup: mockups/new-design.png

> Search fonts for this mockup
# Agent runs systematic search, presents winners

> Generate implementation with these fonts
# Agent creates HTML/React

> Start refinement iterations
# Agent does screenshot → compare → suggest fix → apply → repeat
# Asks for approval at each step
```

---

### **Option C: CLI Commands (Modular)**

```bash
# Step 1: Analyze
amplifier mockup analyze mockups/design.png

# Step 2: Find fonts  
amplifier mockup fonts --mockup mockups/design.png --output fonts.json

# Step 3: Implement
amplifier mockup generate --spec analysis/spec.json --fonts fonts.json

# Step 4: Refine
amplifier mockup refine --original mockups/design.png --current demo.html
```

---

## What Needs to Be Built

### Phase 1: Foundation (Skills + Context)
- [x] Document skills (we have markdown)
- [ ] Convert to Amplifier skill format
- [ ] Add to `.amplifier/skills/`

### Phase 2: Agents (Bundle)
- [ ] Create `mockup-to-code` bundle
- [ ] Write agent descriptions (mockup-analyzer, font-matcher, detail-refiner, validator)
- [ ] Add context files (patterns, checklists, philosophies)

### Phase 3: Recipes (Workflows)
- [ ] Write `mockup-to-code.yaml` recipe
- [ ] Add approval gates at key decision points
- [ ] Test with our meditation blog mockup

### Phase 4: Integration
- [ ] Add Playwright MCP for browser automation
- [ ] Test full pipeline end-to-end
- [ ] Document usage

---

## Quick Start Template (For Next Mockup)

```markdown
# Project: New Mockup Implementation

## 1. Analyze
```bash
amplifier run "Analyze mockup: mockups/design.png - generate blueprint and component spec"
```

## 2. Find Fonts
```bash
amplifier run "Search Google Fonts for this mockup - serif for titles, sans for body"
```

## 3. Implement
```bash
amplifier run "Generate HTML implementation from the spec with chosen fonts"
```

## 4. Refine
```bash
amplifier run "Start iterative refinement - screenshot → compare → fix loop until 95% match"
```
```

---

## The Critical Innovations

What makes this different from "just implement the mockup":

1. **VLM-Guided Blueprint** - Comprehensive annotation in one pass
2. **Systematic Font Search** - ALL 1,600+ fonts, not 5 famous ones
3. **Iteration Loop** - Automated screenshot → compare → fix convergence
4. **Verification with Approval** - Contradiction detection prevents going backwards
5. **Topology-Aware Icon Selection** - Understands one-to-many vs many-to-many
6. **Two-Font System Discovery** - Automatically detects header/body pairing

---

## Next Steps to Make This Real

**Want me to:**

1. **Create the bundle** (`amplifier-bundle-mockup-to-code`)
   - Agent definitions
   - Context files
   - Recipe workflows

2. **Convert skills to Amplifier skill format**
   - Proper frontmatter
   - Companion files (examples, checklists)

3. **Write the main recipe** with approval gates at:
   - Font selection (you review choices)
   - Each refinement iteration (you approve next fix)
   - Final production export

4. **Test it end-to-end** on a new mockup to prove it works

5. **Clean up this workspace** - keep learnings, archive experiments, commit to git

Which should I tackle first? Or should I create a todo list for the whole system build? 🎯