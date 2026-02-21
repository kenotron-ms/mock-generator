# Quick Start Guide

Get started with the UI Mockup bundle in 5 minutes.

## Installation

The bundle auto-installs when you use it. No manual setup required.

```bash
# Test the bundle is available
amplifier run --bundle ui-mockup
```

## Option 1: Interactive Session (Recommended for Learning)

```bash
amplifier run --bundle ui-mockup
```

Then in the session:

```
> "I have a mockup at mockups/app-design.png - convert it to React"

# The assistant will:
# 1. Delegate to mockup-analyzer for blueprint
# 2. Delegate to font-matcher for fonts
# 3. Use modular-builder for implementation
# 4. Delegate to implementation-validator for refinement
# 5. Ask for approval at key decision points
```

## Option 2: Recipe (Recommended for Repeatable Workflows)

```bash
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@ui-mockup:recipes/mockup-to-code.yaml \
  context='{
    "mockup_path": "mockups/design.png",
    "target_framework": "react",
    "output_dir": "./output"
  }'
```

The recipe will pause at approval gates:
1. **After blueprint** - Review semantic structure
2. **After font matching** - Approve font choices
3. **After implementation** - Review generated code
4. **Each refinement iteration** - Approve next fix

## Your First Mockup Conversion

### Step 1: Prepare Your Mockup

```bash
# Create mockups directory
mkdir mockups

# Add your design mockup (PNG, JPG, or Figma screenshot)
# Recommended: Mobile viewport (390x844 or similar)
cp ~/Downloads/design.png mockups/app-design.png
```

### Step 2: Run Analysis

```bash
amplifier run --bundle ui-mockup

# In session:
> "Analyze mockup: mockups/app-design.png"
```

**Output:**
- `output/analysis/blueprint.png` - Annotated blueprint
- `output/analysis/component-spec.json` - Component specifications
- `output/analysis/design-tokens.json` - Colors, typography, spacing

### Step 3: Font Matching

```
> "Search Google Fonts for this mockup"
```

**Output:**
- `output/fonts/batch-comparisons/` - HTML comparison pages
- `output/fonts/finalists.json` - Top font matches
- Font recommendations with confidence scores

### Step 4: Implementation

```
> "Generate React implementation with the matched fonts"
```

**Output:**
- `output/react/` - Full React project
- Components built from spec
- Design tokens applied
- Google Fonts imported

### Step 5: Validation & Refinement

```
> "Start refinement loop until 95% match"
```

**Output:**
- `output/screenshots/` - Implementation screenshots
- `output/comparisons/` - Visual diff heatmaps
- Iteration history with match percentages
- Final production-ready code

## Common Tasks

### Just Extract Design Tokens

```
> "Extract design tokens from mockups/design.png"
```

Gets colors, typography, spacing without full implementation.

### Font Matching Only

```
> "Find Google Fonts that match mockups/design.png"
```

Useful when you already have implementation but wrong fonts.

### Refinement Only

```
> "Refine my implementation at localhost:3000 to match mockups/design.png"
```

Use when implementation exists but needs fine-tuning.

## Tips for Best Results

### 1. Mockup Preparation
- **Clear, high-resolution** - 2x or 3x device resolution
- **Consistent viewport** - All screenshots at same size
- **Complete screens** - Show full UI, not cropped portions
- **Representative content** - Real text, not lorem ipsum

### 2. Font Matching
- **Patience** - Systematic search takes 15-30 minutes
- **Review finalists** - VLM provides top 3, you choose
- **Check weights** - Ensure winner has all needed weights

### 3. Implementation
- **One framework** - Stick to React, Vue, or HTML
- **Incremental build** - Validate each component before next
- **Trust the tokens** - Use extracted values, don't guess

### 4. Refinement
- **One fix at a time** - Systematic iteration works better
- **Verify each fix** - Check compiled CSS after each change
- **Stop at 95%** - Perfect is enemy of good

## Troubleshooting

### "Fonts don't match"
- Load skill: `load_skill('font-matching')`
- Review batch comparison methodology
- Try broader search (serif → display category)

### "Icons are emoji"
- Load skill: `load_skill('icon-finding')`
- Always search Lucide → Heroicons → Feather first
- Generate with Nano Banana only if no library match

### "VLM suggests contradictory changes"
- Load skill: `load_skill('detail-refinement')`
- Use verification against original ONLY
- Get human approval for contradictions

### "Match percentage stuck at 80%"
- Switch from implementation-validator to detail-refiner
- Use verification loops with contradiction detection
- Check compiled CSS (fixes might not be applying)

## Next Steps

- Read `PIPELINE_GUIDE.md` for complete process
- Review `NANO_BANANA_LEARNINGS.md` for insights
- Try the full recipe with approval gates
- Experiment with your own mockups

## Support

- Bundle repo: `amplifier-bundle-ui-mockup`
- Nano Banana Pro: https://github.com/kenotron-ms/amplifier-module-tool-nano-banana
- Amplifier docs: https://github.com/microsoft/amplifier
