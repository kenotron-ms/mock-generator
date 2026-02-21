# VLM-Guided Computer Vision System

## The Problem with Blind CV

**Current approach:**
```
CV: "I'll detect everything in the entire image using edge detection"
Result: 69 fragmented regions, many meaningless
```

**What's missing:** 
- CV doesn't know WHAT to look for
- CV doesn't know WHERE to focus
- CV doesn't understand visual context (shadows, gradients, etc.)

---

## The VLM-Guided Solution

**New approach:**
```
VLM: "I see a card at (34, 215). It has a geometric background image with 
      text overlay. Look for the background image first - it's colorful 
      with high contrast. Adjust edge threshold to 50 because of the 
      gradient. Expected size: ~700x300px."

CV: Runs targeted detection with VLM's parameters
Result: Precise bounding box for background image

VLM: "Good! Now look for text overlays in the bottom-left quadrant of 
      that region. Text will be white on dark gradient. Look for 
      typography clusters."

CV: Runs text-specific detection in focus area
Result: Title text, author text, metadata text precisely located
```

---

## VLM Guidance Parameters

### 1. **Focus Area** (WHERE to look)
```python
{
  "bbox": {"x": 34, "y": 215, "width": 701, "height": 527},
  "description": "Look inside the hero card region only"
}
```

### 2. **Visual Hints** (HOW to detect)
```python
{
  "has_shadow": true,          # Adjust for soft edges
  "has_gradient": true,        # Don't treat gradient as multiple regions
  "background_color": "#F5F5F5", # Expect this color
  "edge_threshold": 50,        # Lower for subtle boundaries
  "min_contrast": 0.3          # Minimum contrast to consider
}
```

### 3. **Expected Pattern** (WHAT to look for)
```python
{
  "element_type": "image",     # Looking for image boundary
  "expected_shape": "rectangle",
  "expected_size": {"min_width": 600, "min_height": 200},
  "expected_aspect_ratio": {"min": 1.5, "max": 3.0}
}
```

### 4. **Content Hints** (Semantic clues)
```python
{
  "contains": ["text_overlay", "geometric_pattern"],
  "foreground_background": "text on image",
  "z_layers": 2  # Expect 2 depth levels
}
```

---

## The Targeted CV Tool

```python
def targeted_cv_detect(
    image_path: str,
    focus_bbox: dict,           # WHERE: Region to analyze
    element_type: str,          # WHAT: "image", "text", "button", etc.
    visual_hints: dict,         # HOW: shadows, gradients, colors
    expected_pattern: dict,     # SHAPE: size, aspect ratio
    parent_component: str = None
) -> dict:
    """
    VLM-guided CV detection within a specific region.
    
    Returns:
        {
            "detected_regions": [
                {
                    "name": "BackgroundImage",  # VLM provides semantic name
                    "bbox": {...},
                    "confidence": 0.95,
                    "reasoning": "Detected colorful rectangular region matching expected pattern"
                }
            ]
        }
    """
```

---

## VLM Conversation Flow

### **Iteration 8: Decompose HeroArticleCard**

**VLM Analysis:**
```
Looking at HeroArticleCard (34, 215, 701x527), I see:
- Large colorful geometric background image (majority of card)
- White text overlay in bottom-left: "On Creative Constraints"
- Small metadata row at bottom: author name, rating, view count
- The background has gradients and geometric shapes - high visual complexity

Strategy: Detect in layers (background → text → metadata)
```

**VLM Tool Call 1: Detect Background Image**
```python
targeted_cv_detect(
    image_path="mockup.png",
    focus_bbox={"x": 34, "y": 215, "width": 701, "height": 527},
    element_type="image",
    visual_hints={
        "has_gradient": true,
        "has_geometric_patterns": true,
        "colorful": true,
        "edge_threshold": 40  # Lower due to gradient
    },
    expected_pattern={
        "shape": "rectangle",
        "fills_parent": 0.8,  # Expects to fill ~80% of parent
        "aspect_ratio": {"min": 1.2, "max": 1.5}
    },
    parent_component="HeroArticleCard"
)
```

**CV Returns:**
```json
{
  "detected_regions": [
    {
      "name": "BackgroundImage",
      "bbox": {"x": 34, "y": 215, "width": 701, "height": 400},
      "confidence": 0.92,
      "reasoning": "Large colorful region with gradients, fills most of parent"
    }
  ]
}
```

**VLM Tool Call 2: Detect Title Text**
```python
targeted_cv_detect(
    image_path="mockup.png",
    focus_bbox={"x": 34, "y": 500, "width": 400, "height": 150},  # Bottom-left quadrant
    element_type="text",
    visual_hints={
        "text_color": "white",
        "text_on_dark_background": true,
        "font_size": "large",  # Title is prominent
        "multiline": false
    },
    expected_pattern={
        "shape": "text_block",
        "horizontal_alignment": "left",
        "max_lines": 2
    },
    parent_component="HeroArticleCard"
)
```

**CV Returns:**
```json
{
  "detected_regions": [
    {
      "name": "TitleText",
      "bbox": {"x": 50, "y": 520, "width": 350, "height": 50},
      "confidence": 0.88,
      "reasoning": "Large white text block in expected location"
    }
  ]
}
```

**VLM Tool Call 3: Detect Metadata Row**
```python
targeted_cv_detect(
    image_path="mockup.png",
    focus_bbox={"x": 34, "y": 670, "width": 701, "height": 72},  # Bottom of card
    element_type="metadata_row",
    visual_hints={
        "contains_icons": true,
        "contains_small_text": true,
        "horizontal_layout": true,
        "spaced_elements": true  # Author, rating, views are separated
    },
    expected_pattern={
        "shape": "horizontal_group",
        "element_count": {"min": 3, "max": 5},
        "spacing": "even"
    },
    parent_component="HeroArticleCard"
)
```

---

## VLM Reasoning Examples

### **Example 1: Card with Shadow**
```
VLM: "This card has a drop shadow (visible darker edge). When detecting 
      the card boundary, use edge_threshold=30 and ignore_shadow_edges=true, 
      otherwise you'll detect the shadow as a separate region."
```

### **Example 2: Text on Gradient**
```
VLM: "The title text is white on a blue-to-purple gradient background. 
      Use text_detection_mode=true and increase contrast_boost=1.5 so 
      the text edges are clear despite the changing background."
```

### **Example 3: Icon + Text Button**
```
VLM: "This looks like a button with an icon (clock) on the left and text 
      on the right. Look for two adjacent regions that should be grouped. 
      Use proximity_threshold=10px to detect they belong together."
```

### **Example 4: Repeated Pattern**
```
VLM: "I see this is the second ArticleCard. It should have the same 
      internal structure as the first one. Use the same detection parameters 
      we used for ArticleCard #1 but apply them to this bbox."
```

---

## Implementation Strategy

### **Tool: targeted_cv_detect.py**

```python
def targeted_cv_detect(
    image_path: str,
    focus_bbox: dict,
    element_type: str,
    visual_hints: dict,
    expected_pattern: dict,
    parent_component: str = None
) -> dict:
    """
    VLM-guided CV detection.
    """
    # Load image
    img = cv2.imread(image_path)
    
    # Crop to focus area
    x, y, w, h = focus_bbox["x"], focus_bbox["y"], focus_bbox["width"], focus_bbox["height"]
    roi = img[y:y+h, x:x+w]
    
    # Apply VLM hints
    if visual_hints.get("has_gradient"):
        # Use different edge detection for gradients
        edges = cv2.Canny(roi, 30, 100)  # Lower thresholds
    elif visual_hints.get("has_shadow"):
        # Morphological operations to remove shadow edges
        kernel = np.ones((5,5), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Element-specific detection
    if element_type == "text":
        regions = detect_text_regions(roi, visual_hints)
    elif element_type == "image":
        regions = detect_image_regions(roi, visual_hints)
    elif element_type == "button":
        regions = detect_button_regions(roi, visual_hints)
    
    # Validate against expected pattern
    validated = []
    for region in regions:
        if matches_expected_pattern(region, expected_pattern):
            validated.append(region)
    
    # Convert back to absolute coordinates
    for region in validated:
        region["bbox"]["x"] += x
        region["bbox"]["y"] += y
    
    return {"detected_regions": validated}
```

---

## Benefits of VLM-Guided CV

1. **Precision**: Focus on relevant areas, ignore noise
2. **Context-aware**: Adjust for shadows, gradients, overlays
3. **Semantic**: VLM names components during detection
4. **Efficient**: Don't process entire image every time
5. **Hierarchical**: Decompose parent → children naturally
6. **Validated**: VLM checks if detection matches expectations

---

## Next: Implement and Test

1. Build `tools/targeted_cv_detect.py`
2. VLM decomposes HeroArticleCard using targeted detection
3. VLM decomposes ArticleCard (reusable pattern)
4. VLM extracts header sub-components
5. VLM extracts nav sub-components
6. Clean up unnamed regions
7. Final validation → 10/10
