# Designer Thinking: Constraints, Grids, and Intent

## What I Missed (Self-Criticism)

### 1. **I Didn't Check My Own Work**
- Said "done" without verifying coordinates against the actual image
- Missed the "Meditations" title in the header entirely
- Didn't see "Blog" and "Explore" tabs
- Text bboxes too small (spillover)

### 2. **I Forgot About Grid Systems**
Designers don't use arbitrary values like:
- ❌ x=85, y=605 (random)
- ✓ x=88, y=608 (snapped to 8px grid)

Standard grids:
- **8px base grid** (most common in mobile)
- **4px for fine-tuning**
- **16px, 24px, 32px for spacing**

### 3. **I Forgot About Standard Spacing**
Designers use consistent spacing values:
- ❌ width=400 (arbitrary)
- ✓ width=608 (768 - 32px margin on each side, snapped to 8px)

Common spacing:
- Card margins: 16px, 24px, 32px
- Text padding: 16px, 24px
- Element spacing: 8px, 16px, 24px

### 4. **I Didn't Think About Optical Alignment**
Text needs space around it:
- Title text height=60 is too tight for 2 lines
- Should be: height=72 or height=80 (more breathing room)
- Designers account for line-height, not just font size

### 5. **I Didn't Verify Full Enclosure**
Text bboxes must FULLY contain all text:
- If title is 2 lines at 24pt font
- Line height is ~1.4-1.5 × font size
- Total height = 2 lines × 24pt × 1.4 = ~67px
- Should round UP to 72 or 80 for safety

---

## Design Constraints to Apply

### Mobile Design Standards (iOS/Android)

**Screen margins:**
- Standard edge margin: 16px or 24px
- Cards usually have 16-24px from screen edge

**Typography spacing:**
- Title to subtitle: 8px, 12px, or 16px
- Paragraph spacing: 16px or 24px
- Metadata spacing: 8px from content

**Component sizing:**
- Headers: 56px, 64px, or 72px height
- Bottom nav: 56px, 64px, or 72px height
- Thumbnails: Powers of 2 (128px, 144px, 160px) or multiples of 8

**Grid snapping:**
- ALL coordinates should align to 8px grid
- x, y, width, height should be multiples of 8 (or 4 for fine-tuning)

---

## Self-Review Questions

Before declaring coordinates "done", ask:

1. **Is this on the grid?** (x % 8 == 0?)
2. **Is this standard spacing?** (16px, 24px, 32px margin?)
3. **Does text have room to breathe?** (line-height considered?)
4. **Would a designer pick this value?** (or would they use a standard?)
5. **Is everything fully enclosed?** (no spillover?)
6. **Did I check my work against the actual image?** (not just guess?)

---

## What a Designer Would Think

Looking at the hero card:

**My guess:** x=85, y=605, width=400, height=60
**Designer thinks:**
- "85 is not on the grid... should be 88 (11 × 8)"
- "605 is weird... should be 608 (76 × 8)"
- "400 width? That's random... what's the card width? 701. With 32px margin on each side, text width should be 701-64=637. Round to grid: 640."
- "60 height for 2-line title? Too tight. Line-height 1.4 × 2 lines = need ~72-80px"

**Corrected:** x=88, y=608, width=640, height=72

---

## The Process for Accurate Extraction

1. **Visual analysis** (VLM sees layers)
2. **Grid snapping** (round to 8px grid)
3. **Design constraints** (apply standard spacing)
4. **Enclosure check** (ensure full coverage)
5. **Self-review** (check against image)
6. **Second review** (would a designer approve?)
7. **Third review** (did I miss anything?)

Only THEN declare done.

---

## I Need to Redo This With Care

My current spec has issues:
- Missing header elements
- Text spillover
- Arbitrary coordinates
- Not grid-snapped

Let me fix it properly.
