# Mock Generator Project

**Pixel-first UI mockup generation using Nano Banana Pro**

This project proves that AI image generation (specifically Nano Banana Pro / Gemini 3 Pro Image) can create exceptional UI mockups that escape component library constraints and enable true creative exploration.

---

## What's Here

### 1. **Nano Banana Pro Integration** (Contribution)
**Location:** `amplifier-module-image-generation/`

**Status:** ✅ PR submitted to @robotdad: https://github.com/robotdad/amplifier-module-image-generation/pull/1

**What it adds:**
- Nano Banana Pro (Gemini 3 Pro Image) provider
- Multi-turn conversational editing
- Thinking mode for complex UI instructions
- Google Search grounding
- Professional text rendering
- Multiple aspect ratios and resolutions

### 2. **UI Mockup Bundle** (Reusable Tool)
**Location:** `amplifier-bundle-ui-mockup/`

**Status:** 🚧 Foundation complete, ready for implementation

**What it provides:**
- Hyper-detailed prompt templates (proven 800-1200 token structure)
- Pre-researched aesthetic guides (mid-century modern, brutalist, etc.)
- Best practices from 14 successful mockup generations
- Reusable patterns for mobile apps, dashboards, visual networks

**Goal:** Help others generate mockups at the quality that made someone say "I've never seen mockups like this before."

### 3. **Session Analysis**
**Location:** `SESSION_ANALYSIS.md`

**Comprehensive breakdown of:**
- What made 14 mockups exceptionally successful
- Prompt engineering patterns that worked
- Iteration workflow (feedback → regenerate)
- Design research methodology
- Nano Banana Pro optimal configuration
- Replicable vs human elements

---

## Key Findings

### The Proven Formula
```
Exceptional Mockup = 
    Nano Banana Pro
    + Hyper-Detailed Prompts (800-1200 tokens)
    + Design Research (aesthetic → palette → specs)
    + Iterative Refinement (1-3 feedback cycles)
    + Real Use Case (genuine constraints)
```

**Success rate:** 14/14 mockups usable (100%)
- All text legible
- All colors accurate
- All layouts coherent
- Zero generic "AI-generated" feeling

### Why This Worked

1. **Specificity beats creativity** - Exact hex codes > "warm colors"
2. **Research grounds aesthetics** - 10 min Dribbble search > hours of iteration
3. **Detail density matters** - 800-1200 token prompts > 100-200 token prompts
4. **Iteration is expected** - 1-3 cycles is normal, not failure
5. **Nano Banana Pro excels at UI** - Text rendering + Thinking mode + aspect ratios

### What Can Be Codified

✅ **Prompt templates** - Fill-in-the-blank structures  
✅ **Aesthetic guides** - Pre-researched palettes and design languages  
✅ **Iteration patterns** - Feedback → regenerate workflows  
✅ **Organization** - Auto-naming, cataloging, documentation  
✅ **Parameters** - Optimal Nano Banana Pro configuration  

❌ **Design taste** - Knowing "soulless" vs "exceptional" requires human judgment  
❌ **Authentic constraints** - Real use cases create genuine decisions  
❌ **Engagement** - 6.5 hours of patient refinement can't be automated  

---

## Example Projects

### Meditation App (Spun Off)
**Location:** `/Users/ken/workspace/meditation-app/`

**What it is:** Mobile-first personal knowledge system for organizing and sharing thoughts

**Mockups generated:** 13 high-fidelity screens showing:
- Voice-first thought navigation
- Spatial (pan/zoom) + linear (swipe) navigation
- Mid-century modern cozy aesthetic
- Personal mode (99%) + sharing mode (1%)
- Visitor experience and engagement mechanics

**Why it proves the concept:** Complete app design from concept to mockups in one session using only Nano Banana Pro.

---

## Quick Start

### Use the Image Generation Module (Now)
```bash
# Clone the enhanced module (or use robotdad's once PR is merged)
cd /Users/ken/workspace/mock-generator
cd amplifier-module-image-generation

# Set up Google API key
export GOOGLE_API_KEY="your-key-here"

# Generate a mockup
uv run python << 'EOF'
import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator

async def generate():
    generator = ImageGenerator()
    
    result = await generator.generate(
        prompt="""Your detailed prompt here...""",
        output_path=Path("output/mockup.png"),
        preferred_api="nano-banana-pro",
        params={"aspect_ratio": "9:16", "resolution": "2K"}
    )
    
    print(f"Generated: {result.local_path}")

asyncio.run(generate())
EOF
```

### Use the Bundle (Future)
```bash
# Once the bundle is complete
amplifier bundle add /path/to/amplifier-bundle-ui-mockup
amplifier bundle use ui-mockup
amplifier

# Then in session
> Create a mobile app mockup for a fitness tracker
> Make it feel mid-century cozy
> Generate 4 color palette variants
```

---

## Repository Structure

```
mock-generator/
├── amplifier-module-image-generation/  # Enhanced with Nano Banana Pro
│   ├── src/amplifier_module_image_generation/
│   │   ├── nano_banana_client.py      # NEW: Nano Banana Pro provider
│   │   ├── generator.py                # ENHANCED: Conversation support
│   │   └── models.py                   # UPDATED: New provider type
│   └── NANO_BANANA_PRO.md              # NEW: Documentation
│
├── amplifier-bundle-ui-mockup/         # Reusable mockup generation bundle
│   ├── bundle.md                       # Bundle configuration
│   ├── context/
│   │   ├── prompt-patterns/
│   │   │   ├── mobile-app.md           # Mobile UI templates
│   │   │   ├── desktop-dashboard.md    # Desktop templates
│   │   │   └── visual-network.md       # Graph/spatial templates
│   │   ├── aesthetic-guides/
│   │   │   └── mid-century-modern.md   # Proven palette + guidance
│   │   └── best-practices.md           # Golden rules
│   ├── agents/                         # Future: Specialized agents
│   ├── recipes/                        # Future: Workflow recipes
│   └── examples/                       # Future: Reference mockups
│
└── SESSION_ANALYSIS.md                 # What made this successful
```

---

## Contributions

### To robotdad/amplifier-module-image-generation
**PR #1:** Nano Banana Pro support
**Status:** Awaiting review
**Impact:** Adds conversational image editing to the Amplifier ecosystem

### To Amplifier Ecosystem (Planned)
**Bundle:** `amplifier-bundle-ui-mockup`
**Status:** Foundation complete, agents/recipes pending
**Impact:** Makes mockup generation accessible to everyone

---

## Next Steps

### Short Term (Week 1)
- [ ] Wait for PR review/merge
- [ ] Complete bundle agents (mockup-generator, design-researcher)
- [ ] Add remaining aesthetic guides (brutalist, glassmorphism)
- [ ] Create iteration recipes

### Medium Term (Week 2-3)
- [ ] Add mockup-refiner agent (conversation management)
- [ ] Add mockup-documenter agent (auto-cataloging)
- [ ] Create batch-variants recipe
- [ ] Test bundle with real users

### Long Term (Month 1-2)
- [ ] Clickable prototype generation from mockups
- [ ] Design token extraction from mockups
- [ ] Mockup versioning and history
- [ ] Collaboration features

---

## Lessons Learned

### What Worked
1. **Real use case** - Meditation app design created authentic constraints
2. **Patient iteration** - 14 mockups, 9 feedback cycles, no rushing
3. **Design research** - Dribbble/palette lookups before generating
4. **Hyper-detailed prompts** - 800-1200 tokens with exact specifications
5. **Nano Banana Pro** - Perfect for UI mockups (text rendering + thinking)

### What to Build Into Tools
- Prompt templates (codify the 800-1200 token structure)
- Aesthetic guides (pre-researched palettes like mid-century)
- Iteration recipes (guide feedback → regenerate pattern)
- Design research automation (Dribbble, color extraction)
- Mockup organization (descriptive naming, auto-cataloging)

### What Requires Human
- Design taste and aesthetic judgment
- Concept evolution through conversation
- Philosophical grounding ("99% personal")
- Real constraints from genuine use cases

---

## Credits

**Image Generation Module:** @robotdad (original), enhanced with Nano Banana Pro support
**Meditation App Design:** Ken (concept and vision)
**Mockup Generation:** Nano Banana Pro (Gemini 3 Pro Image)
**Analysis & Tooling:** Amplifier session analysis

---

🎨 **Generated with [Amplifier](https://github.com/microsoft/amplifier) and Nano Banana Pro**
