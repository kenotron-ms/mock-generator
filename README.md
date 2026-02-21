# Mockup-to-Code Pipeline Research

**Research project that led to the [amplifier-bundle-ui-mockup](https://github.com/kenotron-ms/amplifier-bundle-ui-mockup) production bundle.**

This repository contains the original mockups and exploration that achieved **90% visual match** in mockup-to-code conversion through systematic VLM-guided processes.

---

## 🎯 Production Bundle

The complete, reusable system is now available as an Amplifier bundle:

**Repository:** https://github.com/kenotron-ms/amplifier-bundle-ui-mockup

**Installation:**
```bash
amplifier run --bundle git+https://github.com/kenotron-ms/amplifier-bundle-ui-mockup@main
```

**What it provides:**
- ✅ VLM-guided blueprint generation
- ✅ Systematic font matching (1,600+ Google Fonts)
- ✅ Topology-aware icon selection
- ✅ Contradiction detection in refinement
- ✅ Complete workflow with approval gates
- ✅ Nano Banana Pro tool (auto-installed)

---

## 📁 What's in This Repo

### Active Components

- **`mockups/`** - 9 original meditation app UI mockups used for research
  - `blog-meditations-list-v1.png` - Primary test case
  - 8 other screens for validation

- **`archive/`** - Experimental iterations and learning artifacts

- **`amplifier-bundle-ui-mockup/`** - The production bundle (also at kenotron-ms/amplifier-bundle-ui-mockup)

- **`amplifier-module-tool-nano-banana/`** - Nano Banana Pro tool integration

---

## 🔬 Research Outcomes

This project documented the complete journey from "eyeballing mockups" (~30% match) to systematic VLM processes (90%+ match).

### Key Discoveries

1. **Multi-pass extraction beats single-pass**
   - Structure → containers → spacing → tokens
   - Each pass validates previous findings

2. **Systematic font search across ALL fonts**
   - Don't assume "it's probably Georgia"
   - Batch comparisons (20 fonts per page)
   - VLM ranking narrows 1,600+ → finalists

3. **Topology vs semantics for icons**
   - VLM describes shapes (topology)
   - Human interprets meaning (semantics)
   - Never use emoji for production UI

4. **Contradiction detection prevents regression**
   - VLMs can contradict when comparing images
   - Always verify against original ONLY
   - Human approval for conflicts

5. **Iteration with visual diff**
   - Screenshot → heatmap → fix ONE thing → repeat
   - 50% → 70% → 80% → 90% → 95% convergence

### Documented Patterns

All learnings are captured as reusable skills in the bundle:
- `icon-finding` - Topology-aware icon selection
- `font-matching` - Systematic Google Fonts search
- `detail-refinement` - Verification with contradiction detection
- `vlm-iteration` - Screenshot-compare-fix convergence

---

## 🚀 Using the Bundle

### Quick Start

```bash
# Interactive session
amplifier run --bundle git+https://github.com/kenotron-ms/amplifier-bundle-ui-mockup@main

# Then:
> "Convert this mockup to React: mockups/design.png"
```

### Recipe (Automated Workflow)

```bash
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@ui-mockup:recipes/mockup-to-code.yaml \
  context='{"mockup_path": "mockups/design.png", "target_framework": "react"}'
```

---

## 📚 Documentation

Full documentation is in the bundle repository:
- [Quick Start Guide](https://github.com/kenotron-ms/amplifier-bundle-ui-mockup#quick-start)
- [Pipeline Guide](https://github.com/kenotron-ms/amplifier-bundle-ui-mockup/blob/main/docs/PIPELINE_GUIDE.md)
- [Nano Banana Learnings](https://github.com/kenotron-ms/amplifier-bundle-ui-mockup/blob/main/docs/NANO_BANANA_LEARNINGS.md)

---

## 🙏 Credits

Built using:
- [Nano Banana Pro](https://github.com/kenotron-ms/amplifier-module-tool-nano-banana) - Gemini 3 Pro Image VLM integration
- [Amplifier Foundation](https://github.com/microsoft/amplifier-foundation) - Agent orchestration framework
- Meditation blog mockups - Test case that drove the research

---

## 📄 License

MIT

---

**This was research. The production system is the bundle.**

→ Install: `amplifier run --bundle git+https://github.com/kenotron-ms/amplifier-bundle-ui-mockup@main`
