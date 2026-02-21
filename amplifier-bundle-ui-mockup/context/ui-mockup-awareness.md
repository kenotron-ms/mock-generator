# UI Mockup to Code System

You have access to a professional mockup-to-code pipeline that achieves 90% visual match.

## When to Use

Use this system when:
- User provides design mockups (Figma, screenshots, images)
- Task involves converting designs to implementation
- Pixel-perfect accuracy is required
- Typography and iconography must match precisely

## Available Specialist Agents

**ALWAYS delegate to these experts rather than attempting mockup conversion yourself:**

- **ui-mockup:mockup-analyzer** - Blueprint generation and semantic analysis
- **ui-mockup:font-matcher** - Systematic font identification across 1,600+ families
- **ui-mockup:detail-refiner** - Refinement with contradiction detection
- **ui-mockup:implementation-validator** - Screenshot comparison and validation

## The 9-Step Pipeline

1. **Mockup Analysis** → Semantic blueprint (delegate to mockup-analyzer)
2. **Constraint Extraction** → Layout relationships (VLM)
3. **Design Token Extraction** → Colors/typography/spacing (VLM)
4. **Visual Asset Extraction** → Icons/images (Nano Banana Pro)
5. **Implementation** → Apply tokens + assets
6. **Screenshot Capture** → Visual validation
7. **Visual Diff Analysis** → Pixel-perfect comparison with heatmap
8. **Refinement Iteration** → VLM-guided fixes until >95% match
9. **Final Validation** → Pixel-perfect achieved

## Critical Success Factors

- **Never use emoji as icons** - always find proper SVG icons
- **Multi-pass extraction** - structure → containers → spacing → tokens
- **Verification before building** - validate extracted tokens
- **Contradiction detection** - VLMs can contradict themselves, verify against original

## Available Skills

Load on-demand when needed:
- `icon-finding` - Topology-aware icon selection (NEVER use emoji)
- `font-matching` - Systematic Google Fonts search process
- `detail-refinement` - Verification loops with contradiction detection
- `vlm-iteration` - Screenshot-compare-fix convergence

## Recipe Available

For the complete automated workflow with approval gates:
```bash
amplifier tool invoke recipes \
  operation=execute \
  recipe_path=@ui-mockup:recipes/mockup-to-code.yaml \
  context='{"mockup_path": "path/to/mockup.png", "output_dir": "output/"}'
```

For documentation: see `ui-mockup:docs/PIPELINE_GUIDE.md`
