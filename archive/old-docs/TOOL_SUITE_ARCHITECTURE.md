# Complete Tool Suite for Mockup → Component Hierarchy Extraction

## The Discovery: This is a Multi-Modal Reasoning Problem

We've discovered that extracting component hierarchies from mockups requires:

1. **Visual Understanding** (VLM) - "What am I looking at?"
2. **Spatial Reasoning** (VLM) - "Where approximately should this text be?"
3. **Computer Vision** (CV) - "Validate/refine those coordinates"
4. **Pattern Matching** (VLM) - "These three things are the same component"
5. **Hierarchy Construction** (VLM + Logic) - "This contains that"
6. **Semantic Naming** (VLM) - "Call this 'ArticleCard', not 'Region 5'"
7. **Completeness Validation** (VLM + Rules) - "Did I name everything?"

---

## Complete Tool Inventory

### **Phase 1: Initial Detection**

#### Tool 1: `cv_detect.py` ✅ (Built)
**Purpose**: Blind CV detection to get raw regions
**Input**: Image path
**Output**: 69 regions with coordinates, hierarchy, repetition info

---

### **Phase 2: VLM-Driven Refinement**

#### Tool 2: `vlm_propose_bbox.py` 🔨 (Need to Build)
**Purpose**: VLM estimates bounding box from visual analysis
**Why**: VLM can SEE "the title text is in the upper-left of this card" and propose coordinates
**Input**: 
```json
{
  "image_path": "mockup.png",
  "parent_bbox": {"x": 34, "y": 215, "width": 701, "height": 527},
  "element_description": "Large white title text 'On Creative Constraints', positioned in bottom-left quadrant, approximately 2-3 lines tall",
  "element_type": "text",
  "semantic_name": "TitleText"
}
```
**Output**:
```json
{
  "proposed_bbox": {"x": 50, "y": 520, "width": 400, "height": 80},
  "confidence": 0.85,
  "reasoning": "Based on visual analysis, text appears to start ~30px from left edge, ~60% down the card, spans ~400px width for 2-line title"
}
```

#### Tool 3: `cv_validate_bbox.py` 🔨 (Need to Build)
**Purpose**: CV confirms/refines VLM's proposed bbox
**Input**: VLM's proposed bbox + visual hints
**Output**: Refined bbox with actual edge detection
```json
{
  "validated_bbox": {"x": 51, "y": 521, "width": 397, "height": 77},
  "adjustments_made": {"y": "+1px", "width": "-3px", "height": "-3px"},
  "confidence": 0.92,
  "method": "MSER text detection + edge refinement"
}
```

#### Tool 4: `deduplicate_regions.py` 🔨 (Need to Build)  
**Purpose**: Merge overlapping CV detections (fix the 28 duplicate author boxes)
**Input**: List of regions with IoU threshold
**Output**: Deduplicated list (28 boxes → 1 box)

---

### **Phase 3: Hierarchy Construction**

#### Tool 5: `add_subcomponent.py` 🔨 (Need to Build)
**Purpose**: Add a child component to a parent component
**Input**:
```json
{
  "parent_id": 69,
  "child": {
    "name": "BackgroundImage",
    "bbox": {"x": 34, "y": 215, "width": 701, "height": 400},
    "type": "image"
  }
}
```
**Output**: Updated state with hierarchical relationship

#### Tool 6: `build_component_tree.py` 🔨 (Need to Build)
**Purpose**: Construct nested tree from flat region list
**Output**: Nested JSON structure representing full hierarchy

---

### **Phase 4: Validation & Export**

#### Tool 7: `validate_completeness.py` 🔨 (Need to Build)
**Purpose**: Check for unnamed regions, missing hierarchy
**Output**:
```json
{
  "is_complete": false,
  "issues": [
    "64 regions without semantic names",
    "HeroArticleCard has no children (should have 4)",
    "BottomNavBar children not named"
  ],
  "completeness_score": 7.5
}
```

#### Tool 8: `export_clean_spec.py` 🔨 (Need to Build)
**Purpose**: Export ONLY named components, remove all CV artifacts
**Output**: Clean JSON with nested hierarchy, no "Region" labels

#### Tool 9: `visualize_hierarchy.py` 🔨 (Need to Build)
**Purpose**: Generate overlay showing parent-child relationships (with lines/indents)

---

## The Workflow

```
Step 1: cv_detect(image)
  → 69 raw regions

Step 2: VLM analyzes visually → identifies 5 top-level components
  → merge_regions → 5 named components

Step 3: For each component, VLM proposes sub-components:
  → vlm_propose_bbox("I see a title text at...")
  → cv_validate_bbox(VLM's guess)
  → add_subcomponent(parent, validated_child)

Step 4: validate_completeness()
  → If incomplete: loop back to Step 3
  → If complete: export_clean_spec()

Step 5: visualize_hierarchy()
  → Generate final overlay with tree structure

Step 6: layout_architect validation
  → Must be 10/10
```

---

## The Critical Insight: VLM Visual Coordinate Estimation

**The missing piece**: VLM should be able to LOOK at an image and say:

> "I see a large text block that says 'On Creative Constraints'. Based on the card dimensions (701x527) and the visual positioning, I estimate:
> - Starts ~30-40px from left edge (allowing for padding)
> - Positioned ~60% down the card (visual balance)
> - Text is ~2 lines, roughly 24-30pt font
> - Width: ~350-400px (text length estimation)
> - Height: ~60-80px (2 lines with line-height)
> 
> **Proposed bbox**: x=50, y=520, width=400, height=80"

Then CV validates and refines to actual: x=51, y=521, width=397, height=77

**This is vision + spatial reasoning + design knowledge working together.**

---

## Building the Tools Now

Let me build these tools systematically so we have the complete pipeline.
