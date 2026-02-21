# Component Hierarchy Theory

## The Multi-Dimensional Problem

When we decompose UI into components, we're dealing with several overlapping concepts:

### 1. **Physical Containment** (Geometric)
- What bounding box contains what other bounding box?
- Pure spatial relationship: if bbox A ⊂ bbox B, then A *might* be child of B
- **Problem**: Doesn't distinguish between true containment vs. overlap vs. adjacency

### 2. **Logical Hierarchy** (Component Tree)
- Parent-child relationships in the actual component structure
- A `<Card>` contains `<Image>` and `<Text>` as children
- This is what we actually want to generate code from
- **Problem**: Not always 1:1 with geometric containment (margins, absolute positioning)

### 3. **Visual Grouping** (Gestalt Principles)
- Things that "feel" grouped together even if not geometrically contained
- Proximity, similarity, continuity, closure
- Example: Icon + text that form a "button" concept
- **Problem**: Subjective, context-dependent

### 4. **Z-Order / Layering** (Depth)
- What appears "on top of" what
- Overlays, modals, floating action buttons, shadows
- Important for understanding interaction affordances
- **Problem**: Can't be determined from a static 2D image alone (need color/shadow analysis)

### 5. **Semantic Grouping** (Functional)
- Things that serve a common purpose
- "Form group", "navigation bar", "product card"
- Requires understanding intent, not just visual structure
- **Problem**: Requires domain knowledge and context

### 6. **Prominence Hierarchy** (Visual Weight)
- Some components are more "important" than others
- Headers > Cards > Body Text > Captions
- Affects traversal order and naming
- **Problem**: Subjective, varies by design system

## The Tree Representation Challenge

```
Visual Reality (Pixel Space):
┌─────────────────────────┐
│ [Header Area]           │  ← Region
│  [←] [Title] [≡]       │  ← Three regions with gaps
├─────────────────────────┤
│ ┌───────────────────┐   │
│ │ [Image]           │   │  ← Nested region
│ │                   │   │
│ ├───────────────────┤   │  ← Visual boundary (not geometric)
│ │ Title Text        │   │
│ │ Subtitle Text     │   │
│ │ [Button]          │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │  ← Repeated pattern
│ │ [Image] ...       │   │
└─────────────────────────┘

Desired Tree Structure:
Screen
├─ Header (group, no actual visual boundary)
│  ├─ BackButton
│  ├─ Title
│  └─ MenuButton
├─ ScrollView (container)
│  └─ CardList
│     ├─ Card (reusable component)
│     │  ├─ Image
│     │  ├─ ContentArea (logical group)
│     │  │  ├─ Title
│     │  │  └─ Subtitle
│     │  └─ ActionButton
│     └─ Card (same type)
```

**The Key Insight**: The tree structure is NOT just geometric containment. It requires:
- **Semantic understanding** (this is a "card", not just a rectangle)
- **Pattern recognition** (these 3 things are instances of the same component)
- **Abstraction** (ContentArea doesn't have a visual boundary, but logically groups text)

## Detection Strategy

To build an accurate hierarchy, we need a **multi-stage pipeline**:

### Stage 1: Region Detection (Computer Vision)
**Goal**: Get precise bounding boxes for ALL visible regions

**Methods**:
- **Segment Anything Model (SAM)**: State-of-the-art segmentation
- **UIED (UI Element Detection)**: Trained specifically on UI screenshots
- **Edge detection + contour finding**: OpenCV traditional methods
- **VLM-based detection**: Ask GPT-4V/Claude to identify regions

**Output**: List of rectangles with coordinates, no hierarchy yet

### Stage 2: Containment Analysis (Geometric)
**Goal**: Build initial parent-child relationships based on spatial containment

**Algorithm**:
```python
def build_containment_tree(regions):
    for region in regions:
        # Find all regions that contain this one
        potential_parents = [r for r in regions if contains(r, region)]
        
        # Choose the smallest containing region (immediate parent)
        if potential_parents:
            region.parent = min(potential_parents, key=lambda r: area(r))
        else:
            region.parent = None  # Root element
    
    return build_tree_from_parents(regions)
```

**Challenges**:
- Margins/padding create ambiguity
- Overlapping elements (modals, floating buttons)
- Elements at same visual level but different depth

### Stage 3: Pattern Recognition (Similarity)
**Goal**: Identify repeated components (list items, cards)

**Methods**:
- **Visual similarity**: Compare region sizes, aspect ratios, internal structure
- **Layout similarity**: Vertical/horizontal repetition patterns
- **Feature matching**: Similar sub-elements (all have image + text)

**Output**: Grouped regions marked as "instances of same component"

### Stage 4: Semantic Classification (VLM)
**Goal**: Name components meaningfully ("Button", not "Rectangle")

**Method**: Show VLM each region and ask:
- "What type of UI component is this?"
- "Why do you classify it this way?" (reasoning)
- "What would a developer call this?" (naming)

**Output**: Semantic labels for each region

### Stage 5: Hierarchy Refinement (Logical Grouping)
**Goal**: Add logical containers that don't have visual boundaries

**Example**: 
- Icon + Text geometrically separate → Logically grouped as "IconButton"
- Title + Subtitle visually stacked → Grouped as "TextGroup"

**Method**: Apply heuristics + VLM reasoning:
- Proximity rules (Gestalt)
- Semantic relationships (icon + text commonly grouped)
- VLM validation ("Do these form a single conceptual unit?")

### Stage 6: Prominence Assignment
**Goal**: Determine visual hierarchy for traversal order

**Factors**:
- Size (larger = more prominent)
- Position (top/center = more prominent)
- Semantic role (headers > content > metadata)
- Visual styling (bold, color, elevation)

**Output**: Weighted tree where important nodes are marked

## What We Actually Need to Implement

For a working prototype:

1. ✅ **Component tree data structure** (already have this)
2. ❌ **ACTUAL region detection** (need to implement)
3. ❌ **Containment algorithm** (need to implement)
4. ❌ **Pattern recognition** (need to implement)
5. ❌ **VLM semantic labeling** (can use Claude with vision!)
6. ✅ **Overlay visualization** (already have this)

The critical missing piece: **Step 2 - ACTUAL region detection with real coordinates**
