# VLM-Driven Component Extraction Architecture

## The Core Insight

**The VLM is the agent. CV and bbox manipulation are tools the VLM uses.**

```
Traditional Approach (Wrong):
CV detects → VLM analyzes → Human applies changes → Repeat

VLM-Driven Approach (Correct):
VLM sees image → VLM calls CV tool → VLM calls merge tool → VLM calls adjust tool → VLM validates → Done
```

The VLM iteratively refines the regions by USING TOOLS, just like how agents use tools to accomplish tasks.

---

## The Tool Suite

### Tool 1: `cv_detect`
```python
cv_detect(image_path: str, min_area: int = 500) -> {
    "regions": [...],  # Raw detected regions
    "overlay_path": "temp_v1.png"  # Visual for VLM to see
}
```
**Purpose**: Initial detection to give VLM something to start with

### Tool 2: `merge_regions`
```python
merge_regions(region_ids: List[int], new_name: str) -> {
    "new_region_id": int,
    "bbox": {"x": int, "y": int, "width": int, "height": int},
    "overlay_path": "temp_v2.png"
}
```
**Purpose**: VLM decides "regions 5, 6, 7 should be one component" and merges them

### Tool 3: `split_region`
```python
split_region(region_id: int, method: str, params: dict) -> {
    "new_region_ids": [int, int],
    "overlay_path": "temp_v3.png"
}
```
**Purpose**: VLM decides "region 12 is actually two things" and splits it
**Methods**: "vertical", "horizontal", "by_contours"

### Tool 4: `adjust_bbox`
```python
adjust_bbox(region_id: int, new_bbox: dict) -> {
    "updated_region_id": int,
    "bbox": {...},
    "overlay_path": "temp_v4.png"
}
```
**Purpose**: VLM fine-tunes coordinates: "region 8's bottom edge should be y=500, not y=520"

### Tool 5: `get_current_state`
```python
get_current_state() -> {
    "regions": [...],  # Current region list
    "overlay_path": "current_state.png"  # Visual
}
```
**Purpose**: VLM checks current state before deciding next action

### Tool 6: `finalize_component`
```python
finalize_component(region_id: int, component_spec: dict) -> {
    "component": {
        "name": str,
        "bbox": {...},
        "type": str,
        "repeats": bool,
        ...
    }
}
```
**Purpose**: VLM marks a region as "done" and names it semantically

---

## The Agentic Loop

```python
# Initial state
cv_detect(image_path="mockup.png", min_area=1000)

# VLM sees overlay and starts refining
while not satisfied:
    # VLM analyzes current state
    state = get_current_state()
    
    # VLM decides what to do
    if "regions 5-9 should merge":
        merge_regions([5, 6, 7, 8, 9], "ArticleTitle")
    
    if "region 12 is too big":
        split_region(12, method="horizontal")
    
    if "region 15 bbox wrong":
        adjust_bbox(15, {"x": 50, "y": 200, "width": 300, "height": 100})
    
    # VLM checks result
    state = get_current_state()
    
    # VLM decides if satisfied
    satisfied = validate_components(state)

# Finalize
for region in good_regions:
    finalize_component(region.id, component_spec)
```

---

## Conversation Flow

This is how the conversation would actually go:

**Round 1: Initial Detection**
```
User: "Extract components from mockup.png"

VLM (me): Let me start by detecting regions.
[calls cv_detect tool]

VLM: I see 69 regions detected. Looking at the overlay, I notice:
- Regions 0-9 are part of the large hero card but fragmented
- Regions 17-20 look like one article card split into pieces
- Region 64-68 span the entire height - that's clearly wrong

Let me merge the hero card regions first.
[calls merge_regions([0,1,2,3,4,5,6,7,8,9], "HeroArticleCard")]

VLM: Better. Now the hero card is one region. Let me check the overlay...
[calls get_current_state]
```

**Round 2: Refinement**
```
VLM: Looking at the new overlay, I see:
- The merged hero card looks good
- But regions 17-20 still need merging for the article card
- And region 64 (the tall one) needs to be split

Let me merge the article card regions.
[calls merge_regions([17,18,19,20], "ArticleCardSmall")]

Now let me split that problematic tall region.
[calls split_region(64, method="horizontal", params={"split_points": [100, 1200]})]

Let me see the result...
[calls get_current_state]
```

**Round 3: Validation**
```
VLM: Much better. The components now look like:
- HeroArticleCard: x=34, y=215, width=701, height=527 ✓
- ArticleCardSmall: x=57, y=980, width=655, height=197 ✓
- HeaderNav: x=..., y=..., ... ✓

But I need to adjust the HeaderNav bbox slightly - it's including too much whitespace.
[calls adjust_bbox(55, {"y": 800})]  # Adjust top edge

Perfect! Now let me finalize these components.
[calls finalize_component for each]

Done! Here are your components: [shows final JSON with coordinates]
```

---

## Implementation Strategy

### Phase 1: Build the Tools (Python scripts)
Each tool is a standalone script that:
- Takes JSON input (current state)
- Performs the operation
- Outputs JSON (new state) + overlay image
- Returns to VLM

### Phase 2: VLM Uses Tools in Conversation
The VLM (me, in this Amplifier session) calls bash to run the tools:
```bash
.venv/bin/python3 tools/merge_regions.py --regions 5,6,7 --name ArticleTitle
```

After each tool call, the VLM:
1. Sees the new overlay image
2. Reads the updated regions JSON
3. Decides next action
4. Calls another tool or finalizes

### Phase 3: State Management
A single `state.json` file tracks:
```json
{
  "iteration": 3,
  "regions": [...],
  "operations_log": [
    {"action": "merge", "regions": [5,6,7], "result": 70},
    {"action": "split", "region": 64, "result": [71, 72]}
  ],
  "overlay_path": "state_v3.png"
}
```

Each tool:
- Loads state.json
- Modifies it
- Saves state.json
- Generates new overlay

---

## Why This Works

1. **VLM has world knowledge** - Knows what a "card" looks like, what "too much whitespace" means
2. **VLM has visual understanding** - Can see the overlay and judge if bboxes are right
3. **VLM has reasoning** - Can plan multi-step operations ("merge these, then split that")
4. **Tools are deterministic** - CV and bbox math are predictable
5. **Iterative refinement** - VLM can try, see result, adjust, repeat

The VLM becomes a skilled operator wielding CV tools, not a passive analyzer.

---

## Next Steps

1. Build the manipulation tools (merge, split, adjust)
2. Set up state management
3. Run the VLM-driven loop in THIS CONVERSATION
4. Iterate until components are perfect
