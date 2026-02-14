# Mobile App Mockup Prompt Template

## Template Structure

```
A [APP_PURPOSE] mobile app interface (9:16 portrait, phone screen). 
[AESTHETIC_STYLE] aesthetic with [EMOTIONAL_QUALITY] atmosphere.

COLOR PALETTE:
- [Color 1 name]: #[hex]
- [Color 2 name]: #[hex]
- [Color 3 name]: #[hex]
- [Background name]: #[hex]
- [Text name]: #[hex]

TOP SECTION ([X]% of screen):
- [Element name]: [description, position, styling]
- [Element name]: [description]

MAIN CONTENT ([X]% of screen):
- [Primary component]: [layout, content, styling]
  * [Sub-element A]: [details]
  * [Sub-element B]: [details]
  * [Sub-element C]: [details]

BOTTOM NAVIGATION/ACTION ([X]% of screen):
- [Element]: [description, interaction hints]

TYPOGRAPHY:
- Headers: [serif/sans-serif], [relative size like "large", "medium"]
- Body: [serif/sans-serif], [relative size]
- Labels: [serif/sans-serif], [relative size]

EXAMPLE TEXT TO RENDER:
- [Label 1]: "[exact text]"
- [Label 2]: "[exact text]"
- [Label 3]: "[exact text]"

VISUAL STYLE:
- Corners: [radius in px]
- Shadows: [soft/hard, color]
- Spacing: [generous/tight, measurements]

OVERALL VIBE:
"[Sensory description - how should it FEEL? Reference physical spaces, eras, materials, emotions. Be specific about analogies.]"
```

---

## Proven Example: Voice-First Thought Navigator

**Prompt used (generated exceptional result):**

```
A warm, cozy mobile app interface for visual thought exploration (9:16 portrait, phone screen). Mid-century modern aesthetic with organic shapes and inviting atmosphere.

COLOR PALETTE - Cozy mid-century:
- Warm terracotta #d4745f
- Soft olive green #7a9b76
- Mustard yellow #e8b44f
- Cream background #f9f6f0
- Warm charcoal text #3a3633

TOP SECTION - Status and context (minimal):
- Time "2:14 PM" (small, top left, warm charcoal)
- Date "Thursday, Feb 13" (small, below time)
- Thought count: "47 thoughts" in soft olive circle badge

MAIN VISUAL AREA (70% of screen) - Network graph of connected thoughts:
- Interactive node-link diagram showing thought connections
- Nodes are organic rounded shapes (not perfect circles - slightly irregular)
- 8-10 nodes visible, varying sizes based on importance
- Largest node (center): "Creative Constraints" (terracotta, glowing/active)
- Connected nodes: "Minimalism", "Building in Public", "Design Systems"
- Connecting lines: warm, soft, curved (not straight/rigid)
- Some nodes have date labels "Feb 10", "Feb 8"

SUMMARY BAR (just below graph, minimal):
- Single line: "5 related thoughts about creative constraints"
- Small serif font, warm charcoal

BOTTOM SECTION - Voice-first input:
- Large circular voice button (terracotta, 80px diameter, centered)
- Microphone icon (cream colored) inside
- Soft glow/shadow around button
- Small text below: "Ask or speak your thought..." (serif, gray)
- Tiny keyboard icon (bottom right corner, secondary)

TYPOGRAPHY:
- Headers: Serif (Georgia-style), warm charcoal
- Body: Sans-serif, medium gray
- Labels: Small serif, warm tones

OVERALL VIBE:
"Cozy reading corner meets visual knowledge explorer. Mid-century organic shapes (kidney shapes, rounded rectangles). Warm, inviting color palette. Like looking at a beautiful hand-drawn mind map on warm paper. Think 1960s design meets contemporary app."
```

**Result:** High-quality, distinctive mockup with all text legible, colors accurate, layout coherent.

---

## Fill-in-the-Blank Checklist

Before generating, ensure you have:
- [ ] Aspect ratio specified (9:16)
- [ ] 3-5 colors with hex codes
- [ ] Layout percentages or measurements
- [ ] Typography guidance (serif/sans)
- [ ] Example content (actual labels/text)
- [ ] Emotional/aesthetic direction (vibe reference)
- [ ] Visual style notes (corners, shadows, spacing)

**70%+ filled = good results**
**<50% filled = generic output**

---

## Common Mobile Patterns

### Login/Onboarding Screen
- Hero section (50-60%): Image or illustration
- Form/action (30-40%): Inputs, buttons
- Bottom links (10%): Terms, help

### Dashboard/Home
- Header (15%): Logo, profile, notifications
- Main content (70%): Cards, charts, feed
- Bottom nav (15%): Tab bar with 3-5 icons

### List/Feed View
- Top bar (10%): Title, filters, search
- Scrollable content (80%): Cards or list items
- Floating action (10%): Primary CTA button

### Detail/Reading View
- Hero/header (40%): Image, title, metadata
- Content (50%): Text, embedded media
- Actions (10%): Share, save, related items

---

## Aspect Ratio Guide

| Ratio | Use Case |
|-------|----------|
| 9:16 | Phone portrait (default mobile) |
| 16:9 | Phone landscape, tablet |
| 3:4 | Tablet portrait |

---

## Resolution Strategy

- **Iteration phase:** 1K (faster)
- **Final mockup:** 2K (sweet spot)
- **Presentation:** 4K (client deliverables)

---

## Parameters

Always use:
```python
params = {
    "aspect_ratio": "9:16",
    "resolution": "2K",
    "use_thinking": True,  # Always enable for better UI understanding
    "use_search": False    # Rarely needed for mockups
}
```

---

Generated from proven session achieving 100% mockup success rate (14/14 usable).
