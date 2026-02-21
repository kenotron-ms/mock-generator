# CV-VLM Iterative Dialogue Architecture

## The Problem

**CV Algorithm alone**: Finds 69 fragmented regions (every text line, every edge)
- Over-segments text runs into individual lines
- Can't distinguish background images from foreground content
- No understanding of design patterns or semantic grouping

**What we need**: Intelligent grouping based on:
- Text rendering behavior (lines → paragraphs → text blocks)
- Container relationships (card → image + text content)
- Visual hierarchy (title vs body vs metadata)
- Design patterns (what "looks like" a button, card, etc.)

## The Solution: Iterative Dialogue

```
Round 1: CV Detection
├─ Input: Raw image
├─ Process: Edge detection, contour finding
└─ Output: 69 raw regions (fragmented)

Round 2: VLM Initial Grouping
├─ Input: Image + CV regions overlay
├─ Process: VLM analyzes and suggests groupings
│  "Regions 5-9 are text lines that should be one TextBlock"
│  "Regions 12-18 are a background image with overlay content"
│  "Regions 20-25 form a repeated card pattern"
└─ Output: Grouping instructions

Round 3: CV Refinement
├─ Input: VLM grouping instructions
├─ Process: Merge regions per VLM guidance
└─ Output: ~15 grouped regions

Round 4: VLM Semantic Classification
├─ Input: Image + grouped regions overlay
├─ Process: Name components meaningfully
│  "This is a MeditationCard"
│  "This is a Header with navigation"
└─ Output: Named components with reasoning

Round 5: VLM Hierarchy Validation
├─ Input: Component tree structure
├─ Process: Validate logical hierarchy
│  "The PlayButton should be a child of MeditationCard, not sibling"
└─ Output: Corrected hierarchy

Final: Approved Component Specification
├─ Semantic component names
├─ Logical hierarchy
├─ Accurate bounding boxes
└─ Ready for code generation
```

## Dialogue Flow Design

### Conversation 1: "What do you SEE?"

**CV**: "I detected 69 regions. Here's the overlay."

**VLM**: Looking at this UI:
```json
{
  "observations": [
    "There are 3 large rectangular areas with similar structure - likely cards",
    "Each card has a large image at top (~200px) with text overlay",
    "Below the image are 3 text lines: bold title, lighter body, metadata",
    "The text lines are currently separate regions but should be one TextGroup",
    "Top area has 3 separate elements (back, title, menu) - should stay separate",
    "High contrast background images are confusing the edge detector"
  ],
  "grouping_suggestions": [
    {
      "action": "merge",
      "regions": [5, 6, 7],
      "reason": "These are text lines in the same paragraph - normal text wrapping",
      "new_name": "ArticleTitle"
    },
    {
      "action": "merge",
      "regions": [12, 13, 14, 15, 16, 17, 18],
      "reason": "These are all part of the background image with gradient overlay",
      "new_name": "FeaturedImage"
    }
  ]
}
```

### Conversation 2: "Does this GROUPING make sense?"

**CV**: "I merged regions per your suggestions. Here's v2."

**VLM**: Better! But I notice:
```json
{
  "refinements": [
    "The FeaturedImage should CONTAIN the text overlay, not be siblings",
    "Each card (regions 20, 25, 30) are instances of same component - group as pattern",
    "The metadata row (author, date, time) should be one component with 3 sub-elements"
  ]
}
```

### Conversation 3: "Name these COMPONENTS"

**VLM**: Based on design patterns and context:
```json
{
  "components": [
    {
      "region_id": 1,
      "name": "Header",
      "type": "navigation",
      "reasoning": "Top bar with back button, title, action button - standard mobile header"
    },
    {
      "region_id": 20,
      "name": "MeditationArticleCard",
      "type": "card_component",
      "repeats": true,
      "instances": [20, 25, 30],
      "reasoning": "Large hero image + title + excerpt + metadata - blog card pattern"
    }
  ]
}
```

## Implementation Strategy

### Phase 1: CV Detection (Done ✓)
- Detect all visual regions
- Build geometric containment tree
- Find repeated patterns by similarity

### Phase 2: VLM Grouping (Next)
Create prompts for:
1. **Text consolidation**: "Which regions are text that should be merged?"
2. **Background/foreground separation**: "What's a background image vs content?"
3. **Pattern recognition**: "What components repeat?"
4. **Semantic naming**: "What would you call this component?"

### Phase 3: Iterative Refinement
- Apply VLM suggestions
- Regenerate overlay (v1, v2, v3...)
- Show VLM the result
- Iterate until VLM says "This looks correct"

### Phase 4: Human Validation
- Show final overlay to human
- Human can:
  - Approve ✓
  - Provide feedback → Loop back to VLM
  - Manual adjustments → Regenerate

## Technical Architecture

```python
class CVVLMDialogue:
    def __init__(self, image_path):
        self.image_path = image_path
        self.version = 0
        self.regions = []
        self.conversation_history = []
    
    def run_dialogue(self):
        # Round 1: CV detection
        self.regions = cv_detect(self.image_path)
        self.save_overlay(self.regions, version=self.version)
        
        # Round 2: VLM initial analysis
        vlm_response = vlm_analyze(
            self.image_path,
            self.regions,
            prompt="What do you see? How should these regions be grouped?"
        )
        self.conversation_history.append(vlm_response)
        
        # Round 3: Apply VLM groupings
        self.regions = apply_groupings(self.regions, vlm_response)
        self.version += 1
        self.save_overlay(self.regions, version=self.version)
        
        # Round 4: VLM semantic classification
        vlm_response = vlm_analyze(
            self.image_path,
            self.regions,
            prompt="Name these components and explain the hierarchy"
        )
        self.conversation_history.append(vlm_response)
        
        # Apply semantic labels
        self.regions = apply_semantics(self.regions, vlm_response)
        self.version += 1
        self.save_overlay(self.regions, version=self.version)
        
        # Round 5: VLM validation
        vlm_response = vlm_analyze(
            self.image_path,
            self.regions,
            prompt="Is this component structure correct? Any refinements?"
        )
        
        if vlm_response.needs_refinement:
            # Iterate again
            return self.run_dialogue()
        else:
            # Done!
            return self.regions
```

## VLM Prompts

### Prompt 1: Initial Grouping
```
I've detected 69 regions in this UI mockup using edge detection.

The regions are numbered and overlaid on the image (see attached).

Your task:
1. Identify which regions should be MERGED (e.g., text lines → paragraph)
2. Identify which regions are BACKGROUND vs FOREGROUND
3. Identify REPEATED PATTERNS (e.g., cards in a list)
4. Suggest logical GROUPINGS

Consider:
- Normal text rendering (lines wrap, form paragraphs)
- Background images with overlays
- Container relationships (cards contain content)
- Design patterns (headers, cards, buttons)

Output JSON with merge/group instructions.
```

### Prompt 2: Semantic Classification
```
I've grouped the regions based on your suggestions.

Here's the updated overlay (v2).

Your task:
1. NAME each component (think React component names)
2. Classify TYPE (section, component, element)
3. Identify if components REPEAT
4. Explain your REASONING

Use design pattern knowledge:
- What "looks like" a card, button, header?
- What suggests hierarchy?
- What indicates reusability?

Output JSON with component specifications.
```

### Prompt 3: Validation
```
Here's the final component structure (v3).

Your task:
1. Validate hierarchy makes sense
2. Check for missing elements
3. Verify component names are appropriate
4. Suggest any final refinements

Output: "APPROVED" or list of refinements needed.
```

## Output Versioning

Each iteration produces a versioned overlay:
- `mockup-ANNOTATED-v1.png` - Raw CV detection (69 regions)
- `mockup-ANNOTATED-v2.png` - After VLM grouping (~15 components)
- `mockup-ANNOTATED-v3.png` - After semantic naming
- `mockup-ANNOTATED-v4.png` - After hierarchy refinement
- `mockup-ANNOTATED-FINAL.png` - Human-approved

Plus JSON specs:
- `mockup-spec-v1.json`
- `mockup-spec-v2.json`
- ...
- `mockup-spec-FINAL.json`

This allows reviewing the progression and understanding how the system reasoned.
