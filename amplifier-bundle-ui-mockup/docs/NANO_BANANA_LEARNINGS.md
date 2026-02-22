# Nano Banana Pro: Mockup-to-Code Pipeline Learnings

## What We've Successfully Done

### ✅ Working Process: Semantic Blueprint Generation

**Input:** Original mockup (`mockups/blog-meditations-list-v1.png`)

**Tool:** `generate_ui_blueprint.py` - Uses Nano Banana Pro with reference image

**Method:**
```python
generator.generate(
    prompt="""
    IMPORTANT: Take the provided reference image and ADD annotations.
    DO NOT recreate - use the exact image as base layer.
    
    Annotate with:
    - Semantic component names (ArticleListItem not ListItem)
    - Repetition detection (⟳ symbol for looped components)
    - Layer indicators (🔵 background, 🟢 content, 🟣 overlay)
    - Hierarchy structure (parent-child relationships)
    - Paper layering theory (backgrounds FILL, content SITS ON TOP)
    """,
    params={
        "reference_image": original_mockup,
        "aspect_ratio": "9:16",
        "resolution": "2K",
        "use_thinking": True,
    }
)
```

**Output:** Semantic blueprint with visual annotations

**Success Rate:** ✅ Works reliably - gives structural understanding

---

### ✅ Working Process: Design Token Extraction

**Input:** Original mockup (not the blueprint - the actual mockup)

**Tool:** `extract_design_tokens.py` - Uses Nano Banana Pro VLM analysis

**Method:**
```python
prompt = """
You are a meticulous design token extraction specialist.

Extract EXACT values:
- Colors (hex codes for every background, text, accent)
- Typography (font-family, sizes in px, weights, line-heights)
- Spacing (padding, margin, gaps in px)
- Effects (shadows, border-radius, opacity)

MEASURE, don't guess.
Output: Pure JSON.
"""
```

**Output:** `output/design-tokens.json`

**Key Findings:**
- Background: `#F3EFE7` (warm cream, not gray)
- Font: Serif (not sans-serif!)
- Accent: `#C66E5B` (terracotta, not blue)
- Screen title: 32px (not 17px)

**Success Rate:** ✅ Colors and typography extraction work well

**Problems Found:**
- Spacing extraction is approximate (VLM can't measure pixels precisely)
- Container structure detection is weak (doesn't distinguish padding vs margin)
- Bottom nav described wrong (missed the floating pill container)

---

### ✅ Working Process: Visual Asset Generation

**Input:** Original mockup + component description

**Tool:** `extract_visual_assets.py` - Uses Nano Banana Pro image generation

**Method:**
```python
# For hero background
generator.generate(
    prompt="""
    Recreate the hero card background from this mockup.
    Abstract geometric shapes, warm colors (terracotta, purple, yellow).
    Just the background pattern, no text.
    """,
    params={
        "reference_image": original_mockup,
        "aspect_ratio": "16:9",
        "resolution": "2K",
    }
)

# For thumbnails
generator.generate(
    prompt=f"""
    Thumbnail for article '{title}' matching the meditation blog aesthetic.
    Harmonize with cream #F3EFE7 and terracotta #C66E5B.
    """,
    params={
        "reference_image": original_mockup,
        "aspect_ratio": "1:1",
        "resolution": "1K",
    }
)
```

**Output:** Aesthetically-matched assets in `demo/public/`

**Success Rate:** ✅ Generates matching aesthetic (warm, meditative feel)

**Problems:** Slow (takes time), costs add up ($0.04-0.05 per image)

---

### ✅ Working Process: Visual Diff Analysis (Enhanced with Nano Banana Annotation)

**Input:** Original mockup + current implementation screenshot

**Tool:** Nano Banana Pro (image generation) → Nano Banana Pro (VLM analysis)

**Method (Two-Stage Process):**

**Stage 1: Generate Annotated Comparison**
```python
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

comparison = generator.generate(
    prompt=prompt,
    params={
        "reference_image": [original_mockup, current_screenshot],
        "aspect_ratio": "16:9",
        "resolution": "2K",
        "use_thinking": True,
    }
)
```

**Stage 2: VLM Reads the Annotated Comparison**
```python
vlm_analysis = vlm.analyze(
    image=comparison_annotated,
    prompt="Based on the visual annotations, identify the #1 MOST SIGNIFICANT difference..."
)
```

**Why This Works Better:**
- Nano Banana's image generation creates visual markup (arrows, circles, text labels)
- VLM reads the already-annotated comparison instead of doing raw pixel comparison
- Combines Nano Banana's visual generation strength with VLM's text analysis strength
- More reliable than asking VLM to compare two separate images

**Output:** 
- Single annotated comparison image with visual discrepancy markup
- `output/visual-diff-report.json` with prioritized fixes

**Success Rate:** ✅ More reliable than VLM-only comparison - annotations make differences explicit

---

## ❌ What Didn't Work

### Failed: Single-Pass Full Extraction

**What we tried:** Ask VLM one big question "extract all tokens and structure"

**Why it failed:**
- VLM missed container structures (pill-shaped bottom nav)
- Couldn't distinguish padding vs margin
- Approximate spacing values (16px vs 20px confusion)
- Missed nuanced layout details

### Failed: Trusting Code Without Verification

**What we tried:** 
- Update Tailwind config with tokens
- Change components to use new classes
- Build → assume it worked

**Why it failed:**
- Custom Tailwind classes weren't verified in compiled CSS
- Never inspected browser DevTools to see computed styles
- Build succeeded but changes didn't actually render
- Result: 0.3% match despite "applying" all the tokens

---

## 🎯 What We're About To Try Next

### Hypothesis: Multi-Pass Extraction for Higher Accuracy

**The Problem:**
VLM sees visuals but doesn't understand the CSS box model:
- Doesn't automatically know: "rounded white area" = container with bg-color + border-radius + padding
- Doesn't distinguish: padding (inside) vs margin (outside) vs gap (between)

**The Solution - Structured Multi-Pass Prompting:**

### **Pass 1: Container Structure Detection**
```
Prompt: "Identify all CONTAINERS (cards, pills, panels).

For each container:
- Does it have a background color/image? (if yes → it's a real container)
- Does it have rounded corners? (border-radius value)
- Does it have a shadow? (shadow value)
- Does it have space INSIDE? (padding value)
- Does it have space OUTSIDE from other components? (margin value)
- Is it full-width or constrained? (width value)
- Is it floating/centered or edge-to-edge? (positioning)

Output: Container inventory with exact properties."
```

### **Pass 2: Spacing Annotation Pass**
```
Prompt: "Create a spacing annotation overlay.

Draw arrows:
- RED arrows = PADDING (space inside containers)
- BLUE arrows = MARGIN (space outside containers)  
- GREEN arrows = GAP (space between sibling children)

Label each arrow with pixel measurement.

Output: Annotated image showing every spacing relationship."
```

Then extract spacing values from the annotated image!

### **Pass 3: Component-by-Component Deep Dive**
```
Instead of analyzing whole screen:

1. Crop BottomNavBar region
2. Ask VLM: "Describe ONLY this component's structure"
   - What's the outer container? (pill shape, shadow, centered)
   - What's inside? (3 buttons)
   - How are children arranged? (space-between)
   - What's the padding inside?
   - What's the margin outside?

More focused = more accurate.
```

### **Pass 4: Token Validation Showcase**
```
Before implementation:

1. Generate a "token showcase" page using extracted tokens
2. Shows color swatches, font samples, spacing examples
3. VLM compares showcase vs original
4. If showcase matches → tokens are correct
5. If not → identify wrong tokens and re-extract

Don't build the real app until tokens are validated!
```

### **Pass 5: Incremental Implementation with Verification**
```
For EACH component:
  1. Apply tokens to component
  2. npm run build
  3. Verify: cat dist/assets/*.css | grep "the-custom-class"
  4. If class exists → check value is correct
  5. If not → debug Tailwind config
  6. Open browser → inspect element → check computed styles
  7. Screenshot JUST that component
  8. VLM compares component vs original component
  9. If match → next component
  10. If not → fix before proceeding

NEVER batch changes without verification checkpoints.
```

### **Pass 6: Visual Diff-Guided Iteration**
```
Loop:
  1. Build full app
  2. Screenshot
  3. Create comparison images (heatmap is key!)
  4. Feed heatmap TO Nano Banana: "Look at this heatmap, top 3 red areas?"
  5. VLM: "Fix the bottom nav pill shape, fix the card backgrounds, fix the serif font"
  6. Apply ONLY those 3 fixes
  7. Rebuild → Screenshot → New heatmap
  8. Repeat until heatmap is >95% green
```

---

## 🧠 Key Insights

### 1. **VLM Needs Structure, Not Freedom**
- ❌ "Extract all the things" → misses details
- ✅ "Extract containers. Then spacing. Then colors." → accurate

### 2. **Container Detection is Critical**
The difference between:
```css
/* What we built (wrong) */
.bottom-nav { width: 100%; }

/* What the mockup has (right) */
.bottom-nav-container { 
  width: 320px; 
  margin: 0 auto;
  border-radius: 30px;
  background: white;
  padding: 12px 32px;
}
```

Comes down to: **Did the VLM detect this is a CONTAINER with properties?**

### 3. **Spacing Needs Visual Annotation**
VLM can't reliably measure spacing from a static image.

**Solution:** Have VLM create spacing annotation first, THEN extract from that.

### 4. **Verification Beats Assumption**
Never trust that code changes worked - verify in:
- Compiled CSS
- Browser DevTools
- Visual screenshot
- Pixel diff heatmap

### 5. **Iteration Needs VLM Guidance**
The heatmap shows WHERE differences are.
Feed it back to VLM: "Look at the red areas - what's wrong?"
VLM guides the fixes with visual evidence.

---

## 📋 The Improved Pipeline (To Try)

```
1. Semantic Blueprint (✅ works)
2. Container Structure Detection (new - multi-pass)
3. Spacing Annotation Image (new - visual measurement)
4. Design Token Extraction (✅ works, but needs refinement)
5. Token Validation Showcase (new - verify before building)
6. Asset Generation (✅ works)
7. Incremental Component Implementation (new - one at a time)
8. Build Verification (new - check compiled CSS)
9. Screenshot + Heatmap
10. VLM-Guided Iteration (new - feed heatmap back to VLM)
11. Repeat 7-10 until >95% match
```

The key additions: **Multi-pass extraction, validation showcase, incremental builds with verification, VLM-guided iteration.**

---

Ready to clean up and start fresh with this improved process? 🧹
