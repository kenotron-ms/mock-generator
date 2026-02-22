---
skill:
  name: vlm-iteration
  version: 1.0.0
  description: Screenshot-compare-fix convergence loop for pixel-perfect refinement. Achieves 50% → 90% match through systematic iteration.
  keywords: [iteration, convergence, screenshot, comparison, vlm, refinement]
  author: Ken
  license: MIT
---

# VLM Iteration: Screenshot-Compare-Fix Convergence Loop

## The Iteration Pattern

**Goal:** Achieve >95% visual match through systematic iteration.

**Process:** Screenshot → Compare → Fix ONE thing → Repeat

**Why one fix at a time:**
- Prevents breaking working parts
- Clear cause-effect relationship
- Easier to validate each change
- Faster convergence (no confusion from batch changes)

---

## The Convergence Curve

```
Match %
100% |                              ╱──
     |                          ╱───
 90% |                     ╱────     ← Target
     |                ╱────
 80% |           ╱────
     |      ╱────
 70% | ╱────
     |╱
 50% |─────────────────────────────────→
     0   1   2   3   4   5   6   7  Iterations
```

**Typical progression:**
- Start: 50-60% match (structure correct, details wrong)
- Iteration 1-3: 60-80% (colors, fonts, basic spacing)
- Iteration 4-6: 80-90% (fine-tuning spacing, shadows, borders)
- Iteration 7-10: 90-95% (pixel-perfect details)

---

## The Complete Iteration Loop

### Step 1: Capture Screenshot

**Method 1: Playwright (preferred)**
```python
from playwright.sync_api import sync_playwright

def capture_screenshot(url, output_path, viewport_width=390):
    """Capture screenshot at specific viewport size matching original."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": 844})
        page.goto(url)
        page.screenshot(path=output_path)
        browser.close()
```

**Method 2: Browser DevTools**
```
1. Open implementation in Chrome
2. Open DevTools (Cmd+Option+I)
3. Click device toolbar icon
4. Set dimensions to match original (e.g., 390x844)
5. Cmd+Shift+P → "Capture screenshot"
```

**Critical:** Screenshot must be at SAME viewport size as original mockup.

---

### Step 2: Generate Annotated Comparison with Nano Banana Pro

**Use Nano Banana Pro IMAGE GENERATION to create a visual comparison with annotations:**

```python
# Use Nano Banana Pro (image generation capability)
prompt = """
Create a visual comparison analysis of these two UI screenshots.

LEFT: Original mockup (the target design)
RIGHT: Current implementation (what was built)

Place them side-by-side and ADD VISUAL ANNOTATIONS:
- RED circles/arrows pointing to DIFFERENCES (with labels)
- GREEN checkmarks on elements that MATCH
- Percentage overlay showing match quality in each region
- Text callouts describing discrepancies (e.g., "Wrong width", "Missing shadow", "Color mismatch")
- Heatmap-style color coding: green=match, yellow=close, red=significant difference

Make the discrepancies OBVIOUS and VISUAL so they can be easily read.
"""

# Nano Banana Pro generates the annotated comparison image
comparison_annotated = nano_banana_generator.generate(
    prompt=prompt,
    params={
        "reference_image": [original_mockup, current_screenshot],  # Both images
        "aspect_ratio": "16:9",  # Wide format for side-by-side
        "resolution": "2K",
        "use_thinking": True,
    }
)
# Output: Single annotated image with visual markup
# Saved as: comparison-annotated.png
```

**What Nano Banana Pro does:**
- Takes both images as input
- Generates a NEW image with side-by-side layout
- Adds visual annotations (arrows, circles, text labels, color coding)
- Highlights differences in RED
- Marks matches in GREEN
- Creates a single comprehensive comparison image

**Key distinction:** This is IMAGE GENERATION, not image analysis. Nano Banana Pro creates a visual artifact with markup.

---

### Step 3: VLM Analysis of Annotated Image

**Use Nano Banana Pro VLM (text/vision model) to READ the annotated comparison:**

```
You are analyzing a mockup implementation comparison that has been visually annotated.

Input: [comparison-annotated.png] - Shows original (left) and implementation (right) with visual annotations

The image already has RED markers showing differences and GREEN markers showing matches.

Task: Based on the visual annotations in the image, identify the #1 MOST SIGNIFICANT difference that reduces visual match.

Output format:
{
  "match_percentage": 75,
  "most_significant_issue": {
    "component": "Hero card",
    "problem": "Text not visible",
    "original_state": "White text visible on dark image",
    "current_state": "No text showing",
    "fix_needed": "Ensure hero-content has z-index:10 and white color"
  },
  "other_issues_found": ["Minor spacing difference in nav", "Shadow slightly darker"],
  "progress": "Good progress on layout, colors, and nav. Focus on hero card visibility."
}

Pick ONE issue to fix. After fixing, we'll re-screenshot and compare again.
```

**Key distinction:** This is TEXT ANALYSIS reading a visual image. The VLM reads the annotations that Nano Banana Pro generated.

**Why this two-stage approach works better:**
1. **Stage 1 (Nano Banana Pro generation):** Creates visual markup making differences explicit
2. **Stage 2 (VLM analysis):** Reads the marked-up comparison and prioritizes fixes

**Key principle:** ONE issue at a time, most significant first.

---

### Step 4: Apply Fix

**Based on VLM guidance, apply the fix:**

```javascript
// Example fix from VLM
// Issue: Hero text not visible
// Fix: Ensure proper z-index and white color

// In hero-card.css
.hero-content {
  position: absolute;
  bottom: 24px;
  left: 24px;
  right: 24px;
  z-index: 10;        /* ← Added */
  color: #FFFFFF;     /* ← Verified */
}

.hero-title {
  color: inherit;     /* ← Ensure inherits white */
}
```

**Verify fix was applied:**
```bash
# Build
npm run build

# Check compiled CSS
grep "hero-content" dist/assets/*.css

# Should see z-index: 10 and color: #FFFFFF
```

---

### Step 5: Re-Validate

**Capture new screenshot and compare:**

```python
# Capture updated implementation
capture_screenshot("http://localhost:5173", "screenshots/iteration-2.png")

# Create new comparisons
create_side_by_side("mockup.png", "screenshots/iteration-2.png", "compare-iter2.png")
create_heatmap("mockup.png", "screenshots/iteration-2.png", "heatmap-iter2.png")

# VLM re-analysis
# Did the fix work? What's the new match percentage?
```

**Expected progression:**
- Iteration 1: 60% → Fixed nav → 70%
- Iteration 2: 70% → Fixed colors → 80%
- Iteration 3: 80% → Fixed hero text → 85%
- Iteration 4: 85% → Fixed spacing → 90%

---

### Step 6: Convergence Check

**When to stop:**

```python
def should_continue_iteration(match_percentage, iteration_count):
    if match_percentage >= 95:
        return False  # Success! ✓
    
    if iteration_count >= 10:
        return False  # Diminishing returns
    
    return True  # Keep iterating
```

**Stopping criteria:**
- ✓ Match percentage >95%
- ✓ User satisfied with result
- ✓ Only minor differences remaining (<5px, subtle shadows)
- ✗ Iteration count >10 (might indicate deeper problem)

---

## Critical Success Factors

### 1. **Same Viewport Size**
```
Original mockup: 390x844 (iPhone 13)
Screenshot MUST be: 390x844

Wrong viewport = invalid comparison!
```

### 2. **One Fix Per Iteration**
```
❌ Fix hero text + nav spacing + colors all at once
   → Can't tell which change helped/hurt

✓ Fix hero text ONLY
   → Clear cause-effect
   → Easy to validate
   → Can revert if needed
```

### 3. **VLM Picks Priority**
```
Don't fix issues in order found.
Let VLM identify MOST SIGNIFICANT difference.

Example:
- 1px shadow difference (low priority)
- Hero card completely missing (HIGH priority)

Fix high priority first!
```

### 4. **Verify Each Fix**
```
After applying fix:
1. Build project
2. Check compiled CSS
3. Open in browser
4. Inspect element
5. Confirm fix is active

Don't assume it worked!
```

---

## Handling Common Issues

### Issue: Match percentage not improving

**Possible causes:**
1. Fixes not actually being applied (check compiled CSS)
2. Fixing wrong things (VLM misidentifying issues)
3. Breaking previously-working parts (avoid batch changes)

**Solution:**
- Verify each fix in browser DevTools
- Use VLM verification (from detail-refinement skill)
- Revert if match percentage goes DOWN

---

### Issue: Hitting plateau at 85%

**Possible causes:**
1. Remaining differences are subjective (font rendering, anti-aliasing)
2. Structural issues need bigger refactor
3. Original mockup has details impossible to match exactly

**Solution:**
- Get user feedback (is 85% good enough?)
- Consider if perfect match worth additional effort
- Document known differences

---

### Issue: VLM reports contradictory findings

**Example:**
- Iteration 2: "Hero too wide"
- Iteration 4: "Hero too narrow"

**Solution:**
- Use verification from detail-refinement skill
- Check against original ONLY (not comparative)
- Get human confirmation

---

## Iteration History Tracking

**Track each iteration:**

```json
{
  "iterations": [
    {
      "number": 1,
      "screenshot": "screenshots/iter-1.png",
      "match_percentage": 60,
      "issue_fixed": "Bottom nav pill shape",
      "fix_applied": "border-radius: 40px, width: 320px, margin: auto",
      "result": "Nav now matches, match improved to 70%"
    },
    {
      "number": 2,
      "screenshot": "screenshots/iter-2.png",
      "match_percentage": 70,
      "issue_fixed": "Background color",
      "fix_applied": "Changed from #FFFFFF to #F3EFE7",
      "result": "Warm aesthetic restored, match improved to 78%"
    }
  ]
}
```

**Benefits:**
- Can revert to any iteration
- Clear history of what was tried
- Learn what fixes worked best

---

## Success Metrics

### Per Iteration:
- ✓ Match percentage improved (even 5% is good)
- ✓ Specific issue was resolved
- ✓ No previously-working parts broke
- ✓ VLM confirms fix worked

### Final Result:
- ✓ Match percentage >95%
- ✓ All major components match
- ✓ Typography correct
- ✓ Colors accurate
- ✓ Spacing within 2-3px
- ✓ User confirms satisfaction

---

## Integration with Other Skills

**Combine with:**
- **detail-refinement** - When VLM gives contradictory suggestions
- **icon-finding** - If icons need replacing during iteration
- **font-matching** - If fonts need adjustment

**Workflow:**
```
1. Initial implementation (50-70% match)
2. VLM iteration (70-85% match) ← This skill
3. Detail refinement with verification (85-95% match)
4. Final validation (>95% match)
```

---

## Implementation Code

### Complete iteration script:

```python
def iteration_loop(original_mockup, implementation_url, max_iterations=10):
    """Complete VLM-guided iteration loop."""
    
    for i in range(1, max_iterations + 1):
        print(f"\n=== Iteration {i} ===")
        
        # 1. Capture screenshot
        screenshot_path = f"screenshots/iter-{i}.png"
        capture_screenshot(implementation_url, screenshot_path)
        
        # 2. Create comparisons
        side_by_side = f"compare/side-by-side-{i}.png"
        heatmap = f"compare/heatmap-{i}.png"
        create_side_by_side(original_mockup, screenshot_path, side_by_side)
        create_heatmap(original_mockup, screenshot_path, heatmap)
        
        # 3. VLM analysis
        analysis = vlm_compare(original_mockup, screenshot_path, heatmap)
        print(f"Match: {analysis['match_percentage']}%")
        print(f"Issue: {analysis['most_significant_issue']['component']}")
        
        # 4. Check convergence
        if analysis['match_percentage'] >= 95:
            print("✓ Success! >95% match achieved")
            break
        
        # 5. Get fix from VLM
        fix = analysis['most_significant_issue']['fix_needed']
        print(f"Fix: {fix}")
        
        # 6. Apply fix (human or automated)
        input(f"Apply fix and rebuild. Press Enter when ready...")
        
        # 7. Continue to next iteration
    
    return analysis
```

---

## Summary

**The Pattern:**
1. Screenshot current implementation
2. Compare to original (side-by-side, overlay, heatmap)
3. VLM identifies #1 most significant issue
4. Apply ONE fix
5. Re-screenshot and validate
6. Repeat until >95% match

**Key Principles:**
- One fix at a time
- Most significant issue first
- Verify each fix worked
- Track iteration history
- Stop at 95% or 10 iterations

**Critical Insight:** Iteration is a convergence process. Each fix should improve match percentage. If match percentage goes down, revert and try different approach. Systematic iteration beats guesswork.
