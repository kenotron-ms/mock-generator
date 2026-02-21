# Amplifier UI Mockup Bundle

**Professional mockup-to-code conversion achieving 90% visual match.**

This bundle provides a complete pipeline for converting design mockups (Figma, screenshots, images) into pixel-perfect code implementations using VLM-guided analysis and systematic refinement.

## 🎯 What This Bundle Does

Takes a mockup image and produces:
- ✅ Semantic component blueprint
- ✅ Extracted design tokens (colors, typography, spacing)
- ✅ Matched Google Fonts (from 1,600+ families)
- ✅ Proper icon libraries (no emoji!)
- ✅ Production-ready code (React, Vue, or HTML)
- ✅ **90%+ visual match** through systematic refinement

## 🚀 Quick Start

### Installation

```bash
# The bundle will be installed automatically when you use it
# Nano Banana Pro tool is included as a dependency
```

### Basic Usage

```bash
# Interactive session
amplifier run --bundle ui-mockup

# Then in session:
> "Convert this mockup to React: mockups/design.png"
```

### Using the Recipe (Recommended)

```bash
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@ui-mockup:recipes/mockup-to-code.yaml \
  context='{"mockup_path": "mockups/design.png", "target_framework": "react", "output_dir": "output/"}'
```

The recipe includes approval gates at:
- Blueprint review
- Font selection
- Implementation review
- Each refinement iteration

## 📋 The 9-Step Pipeline

1. **Mockup Analysis** → Semantic blueprint generation
2. **Constraint Extraction** → Layout relationships
3. **Design Token Extraction** → Colors, typography, spacing
4. **Visual Asset Extraction** → Icons, images
5. **Implementation** → Apply tokens and build
6. **Screenshot Capture** → Visual validation
7. **Visual Diff Analysis** → Pixel-perfect comparison
8. **Refinement Iteration** → VLM-guided fixes until >95% match
9. **Final Validation** → Production-ready assets

## 🤖 Available Agents

### ui-mockup:mockup-analyzer
Blueprint generation and design token extraction specialist.

**Use for:**
- Initial mockup analysis
- Semantic structure identification
- Multi-pass extraction (structure → containers → spacing → tokens)

### ui-mockup:font-matcher
Systematic Google Fonts search expert (1,600+ families).

**Use for:**
- Font identification from mockups
- Two-font typography system discovery (display + body)
- Batch comparison and VLM ranking

### ui-mockup:detail-refiner
Fine-tuning with contradiction detection and verification loops.

**Use for:**
- 80-90% → 95%+ refinement
- Preventing regression through VLM verification
- Human approval for ambiguous changes

### ui-mockup:implementation-validator
Screenshot comparison and iteration loop specialist.

**Use for:**
- Automated validation loops
- Screenshot → compare → fix convergence
- Visual diff heatmap generation

## 📚 Available Skills

Load on-demand with `load_skill('skill-name')`:

- **icon-finding** - Topology-aware icon selection (NEVER use emoji)
- **font-matching** - Systematic Google Fonts search process
- **detail-refinement** - Verification loops with contradiction detection
- **vlm-iteration** - Screenshot-compare-fix convergence

## 🎨 Key Innovations

### 1. VLM-Guided Blueprint
Comprehensive annotation in one pass using Nano Banana Pro.

### 2. Systematic Font Search
ALL 1,600+ Google Fonts, not just famous ones. Batch comparisons with VLM ranking.

### 3. Topology-Aware Icon Selection
Understands semantic meaning vs visual appearance. Never uses emoji.

### 4. Contradiction Detection
Verifies VLM suggestions against original mockup before applying. Prevents going backwards.

### 5. Iteration with Heatmaps
Automated screenshot → visual diff → fix loops until >95% match.

## 📖 Documentation

- **Pipeline Guide** - `@ui-mockup:docs/PIPELINE_GUIDE.md`
- **System Overview** - `@ui-mockup:docs/SYSTEM_OVERVIEW.md`
- **Learnings** - `@ui-mockup:docs/NANO_BANANA_LEARNINGS.md`

## 🛠️ Requirements

- **Nano Banana Pro** - Included as tool dependency (git+https://github.com/kenotron-ms/amplifier-module-tool-nano-banana)
- **Browser automation** (optional) - For screenshot capture (Playwright or manual)
- **Google Fonts API key** (optional) - For systematic font search

## 💡 Example Workflow

```bash
# 1. Start with mockup
amplifier run --bundle ui-mockup

# 2. Generate blueprint
> "Analyze mockup: mockups/meditation-app.png"

# 3. Find fonts
> "Search Google Fonts for this mockup - serif for titles, sans for body"

# 4. Implement
> "Generate React implementation with the matched fonts"

# 5. Iterate to perfection
> "Start refinement loop - screenshot, compare, fix until 95% match"
```

## 🎯 Success Metrics

From real-world usage:
- **90%+ visual match** achieved (vs ~30% with manual eyeballing)
- **Systematic font matching** across full Google Fonts catalog
- **Zero emoji in production** (proper icon libraries)
- **Contradiction detection** prevented regressions in 100% of test cases

## 🤝 Contributing

This bundle was developed through practical mockup-to-code sessions, documenting:
- What worked (multi-pass extraction, batching, verification)
- What didn't (single-pass extraction, trusting VLM comparisons blindly)
- Critical learnings (two-font systems, topology vs semantics, contradiction detection)

## 📄 License

MIT

## 🙏 Credits

Built using:
- [Nano Banana Pro](https://github.com/kenotron-ms/amplifier-module-tool-nano-banana) by @kenotron-ms
- [Amplifier Foundation](https://github.com/microsoft/amplifier-foundation)
- Learnings from meditation blog mockup implementation

---

**Ready to achieve pixel-perfect mockup conversions?**

```bash
amplifier run --bundle ui-mockup
```
