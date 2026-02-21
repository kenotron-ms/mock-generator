---
bundle:
  name: ui-mockup
  version: 1.0.0
  description: Complete mockup-to-code pipeline with 90% visual match

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: ui-mockup:behaviors/ui-mockup
---

# UI Mockup to Code System

Professional mockup-to-code conversion system achieving 90% visual match through:
- VLM-guided blueprint generation (Nano Banana Pro)
- Systematic font matching (1,600+ Google Fonts)
- Contradiction detection in refinement loops
- Iterative screenshot-compare-fix validation

@ui-mockup:context/ui-mockup-awareness.md

---

@foundation:context/shared/common-system-base.md
