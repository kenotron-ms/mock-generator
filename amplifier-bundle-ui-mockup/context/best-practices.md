# UI Mockup Generation Best Practices

Proven patterns from a session that achieved 100% mockup success rate (14/14 usable).

---

## The Golden Rules

### 1. **Specificity Beats Creativity**
- ❌ "Make it modern and clean" → Generic result
- ✅ "Terracotta #d4745f buttons, 16px rounded corners, serif headers" → Distinctive result

**Why:** AI models work better with constraints than with creative freedom.

### 2. **Research Before Generating**
- ❌ Generate first, iterate to fix aesthetics
- ✅ Research aesthetic (5-10 min) → Extract palette → Generate with specifications

**Why:** 10 minutes of research prevents 2 hours of iteration.

### 3. **Iterate Without Defending**
- ❌ "The current design is good because..."
- ✅ [Immediately generate alternative based on feedback]

**Why:** Users know what they want when they see it. Show options, don't argue.

### 4. **Detail Density: 800-1200 Tokens**
- ❌ 100-200 token prompts → Generic mockups
- ✅ 800-1200 token prompts → Professional mockups

**Why:** Nano Banana Pro's Thinking mode leverages detail for better understanding.

### 5. **Example Content is Mandatory**
- ❌ "Show navigation items" → Placeholder text
- ✅ "'Latest Thoughts', 'Categories', 'Archive', 'About'" → Realistic mockup

**Why:** Specific text renders professionally. Placeholders look unfinished.

---

## Prompt Engineering Workflow

### Step 1: Gather Requirements (2-3 min)
Ask:
- What's this for? (real use case)
- Who's using it? (mobile/desktop, demographic)
- What's the vibe? (cozy, minimal, bold, professional)
- Visual or text-focused? (impacts layout ratios)

### Step 2: Choose/Research Aesthetic (5-10 min)
**If user provides aesthetic:**
- "Mid-century modern" → Load guide with proven palette
- "Brutalist" → Load minimal, concrete aesthetic
- "Glassmorphism" → Load frosted, layered style

**If user says "cozy", "professional", "fun":**
- Search Dribbble/design sites for that quality
- Extract color palette (3-5 hex codes)
- Note typography patterns (serif/sans mix)
- Identify shape characteristics (rounded/angular)

### Step 3: Build Detailed Prompt (3-5 min)
Use template structure:
1. Viewport type (9:16 mobile, 16:9 desktop)
2. Aesthetic + emotional quality
3. Color palette (hex codes)
4. Layout structure (measurements)
5. Typography (serif/sans guidance)
6. Example content (actual text)
7. Visual style (corners, shadows, spacing)
8. Vibe description (analogies, references)

**Checklist: 70%+ = good results**

### Step 4: Generate with Optimal Parameters (1 min)
```python
params = {
    "aspect_ratio": "9:16",   # or 16:9
    "resolution": "2K",        # sweet spot
    "use_thinking": True,      # always enable
}
```

### Step 5: Review & Iterate (2-3 min)
- Show mockup immediately
- Get specific feedback
- Don't defend - regenerate with adjustments
- 1-3 iterations to excellence

**Total time: 15-25 minutes to exceptional mockup**

---

## Common Feedback Patterns

### "Too [quality]"
**Pattern:** Emphasize opposite quality
- "Too busy" → Reduce elements, increase whitespace
- "Too minimal" → Add visual interest, decoration
- "Too corporate" → Warm up colors, add personality
- "Too casual" → Tighten up, professional fonts

### "Make it feel [emotion]"
**Pattern:** Research designs that evoke that emotion
- "Cozy" → Mid-century warm colors, soft shapes, reading nook references
- "Professional" → Cooler palette, geometric shapes, business space references
- "Playful" → Bright colors, irregular shapes, toy/game references

### "Focus on [element]"
**Pattern:** Adjust visual weight
- Give element 60%+ of screen real estate
- Increase size, saturation, contrast
- Deemphasize other elements (smaller, lower opacity)

### "Deemphasize background"
**Pattern:** Reduce or remove decoration
- Nearly invisible backgrounds (subtle off-white)
- Remove textures, patterns, decorative elements
- Let content create visual interest

---

## Quality Checklist

Before showing mockup to user, verify:
- [ ] All text is legible (labels, buttons, headings)
- [ ] Colors match specified hex codes
- [ ] Layout is coherent (not broken/nonsensical)
- [ ] Proportions feel professional (not distorted)
- [ ] Spacing is generous (not cramped)
- [ ] Aesthetic is distinctive (not generic)

**If <5 of 6: Regenerate before showing**

---

## Common Pitfalls

### ❌ Under-Specifying Colors
**Problem:** "Use warm tones"
**Result:** Model guesses, often generic
**Solution:** "Terracotta #d4745f, olive #7a9b76, mustard #e8b44f"

### ❌ Vague Layout
**Problem:** "Sidebar on left with navigation"
**Result:** Could be 20% or 50% wide
**Solution:** "Sidebar (240px wide, 20% of viewport)"

### ❌ No Example Content
**Problem:** "Show thought cards"
**Result:** Lorem ipsum or placeholder text
**Solution:** "Card 1: 'On Creative Constraints' (Feb 10, 2026)"

### ❌ Missing Emotional Direction
**Problem:** "A modern app interface"
**Result:** Could be anything
**Solution:** "Like a cozy reading nook meets 1960s design magazine"

### ❌ One-Shot Expectation
**Problem:** Expect perfection on first generation
**Result:** Disappointment, abandoning tool
**Solution:** Plan for 1-3 iterations, see it as conversation

---

## Aesthetic Quick Reference

### Mid-Century Modern Cozy
**When:** Personal tools, creative apps, contemplative interfaces
**Colors:** Terracotta, olive, mustard, cream, charcoal
**Fonts:** Serif headers + sans body
**Vibe:** "Cozy reading nook from 1960s architect's home"

### Brutalist Minimal
**When:** Developer tools, technical apps, serious interfaces
**Colors:** Concrete gray, black, white, one bold accent
**Fonts:** Mono or geometric sans-serif
**Vibe:** "Raw concrete building meets Swiss design"

### Glassmorphism
**When:** Modern apps, iOS-style, depth-focused
**Colors:** Translucent whites, soft pastels, blur effects
**Fonts:** SF Pro, system fonts
**Vibe:** "Frosted glass panels floating in space"

### Neo-Brutalism
**When:** Bold brands, playful apps, energetic interfaces
**Colors:** Black, white, one extremely saturated color
**Fonts:** Bold sans-serif, high contrast
**Vibe:** "90s web meets contemporary brutalism"

---

## Success Metrics

**A mockup generation session is successful when:**
- ✅ User says "this looks professional" (not "AI-generated")
- ✅ Text is readable without zooming
- ✅ Colors create cohesive palette
- ✅ Layout matches mental model
- ✅ Fewer than 5 iterations needed
- ✅ Time from brief to final: <30 minutes

---

## Advanced Techniques

### Generate 4 Variants
Instead of one mockup, generate 4 with slight variations:
- Variant 1: As specified
- Variant 2: Alternative color from palette
- Variant 3: Alternative layout structure
- Variant 4: Alternative typography mix

**Let user choose** instead of guessing which they want.

### Multi-Turn Conversation (Nano Banana Pro)
For complex iterative refinement:
1. Create conversation session
2. Generate initial mockup
3. "Make the header bigger" (continues conversation)
4. "Change colors to blue tones" (maintains context)
5. Close conversation when done

**Better coherence** across iterations.

### Visual Block Patterns
For content-rich mockups (dashboards, feeds):
- Image: 40-60% of card height
- Title: Large, prominent
- Metadata: Small, subtle (dates, tags)
- Summary: 2-3 lines max
- Action: Clear CTA

**Proven ratio** for visual thinkers.

---

## Troubleshooting

### Issue: Text is Blurry/Illegible
**Cause:** Resolution too low or text too small
**Solution:** 
- Use 2K or 4K resolution
- Specify "clear, legible text" in prompt
- Make text elements larger (relative to canvas)

### Issue: Colors Don't Match Hex Codes
**Cause:** Model interpretation variance
**Solution:**
- Regenerate (usually fixes)
- Specify "exactly #d4745f" in prompt
- Verify in Thinking mode enabled

### Issue: Layout is Broken/Nonsensical
**Cause:** Conflicting layout instructions
**Solution:**
- Simplify prompt (remove contradictions)
- Use clearer spatial language (top/bottom/left/right)
- Reference proven layout patterns

### Issue: Generic "AI-Generated" Feeling
**Cause:** Under-specified aesthetic, vague vibe
**Solution:**
- Add specific aesthetic guide (mid-century, brutalist)
- Include emotional/physical space references
- Use exact hex codes, not color names

---

## Time Estimates

**With templates and guides:**
- First mockup: 5-10 minutes (research + generate)
- Iterations: 2-3 minutes each
- Final documentation: 5 minutes
- **Total for mockup set:** 20-30 minutes

**Without (manual exploration):**
- Research: 20-30 minutes
- Trial and error prompting: 15-30 minutes per mockup
- Iteration: 5-10 minutes each
- **Total:** 2-6 hours (like our session)

**The bundle should save 4-10x time.**

---

## Final Checklist

Before delivering mockups:
- [ ] All text is legible
- [ ] Color palette is cohesive
- [ ] Layout matches user's mental model
- [ ] Aesthetic is distinctive (not generic)
- [ ] Example content is realistic (not lorem ipsum)
- [ ] Mockups are organized with descriptive names
- [ ] Iteration history is documented
- [ ] Design principles are captured

---

Generated from session achieving "mockups I've never seen before" quality level.
