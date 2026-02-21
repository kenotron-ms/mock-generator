# The Optimal Prompt (Synthesis)

Combining:
- Your insight: Paper layering (child's collage)
- Gemini's insight: Draw first (visual blueprint)
- Designer thinking: Grid systems, constraints, self-review

---

## THE PROMPT

```
You are creating a technical blueprint for implementing this UI.

Think like:
- A CHILD making a paper collage (simple layering)
- A DESIGNER with a ruler (precision, grids, constraints)
- A DEVELOPER (layout strategies for code)

---

STEP 1: SQUINT & SEE LAYERS

Close your eyes halfway. What are the BIG PIECES OF PAPER?

For each major component (card, section):
- What's the BACKGROUND layer? (the big paper filling space)
- What's GLUED ON TOP? (text, images, buttons)
- Don't overthink it - what would a 5-year-old see?

---

STEP 2: DRAW BOUNDING BOXES

Using your image tools, draw boxes ON THE IMAGE:
- Different colors for different z-layers:
  - GRAY for backgrounds (z=0)
  - BLUE for content layers (z=1)  
  - ORANGE for interactive elements (z=2)
- Label each box with semantic PascalCase names
- Make lines thick and high-contrast (easy to see)

This forces you to PAY ATTENTION to actual pixel regions.

---

STEP 3: MEASURE WITH DESIGNER PRECISION

For each layer, measure coordinates BUT think like a designer:

✓ **Grid System**: Snap ALL coordinates to 8px grid
  - x, y, width, height should be multiples of 8
  - Why: Designers use systematic grids, not arbitrary pixels

✓ **Standard Spacing**: Use conventional margins
  - 16px, 24px, or 32px (not 27px or 43px)
  - Why: Design systems have spacing tokens

✓ **Full Text Enclosure**: Text boxes must FULLY contain text
  - Account for line-height (1.4-1.5× font size)
  - If title is 2 lines at 36px font → height = 2 × 36 × 1.4 = ~100px
  - Round UP to grid: 104px
  - Why: Text spillover breaks layouts

✓ **Standard Sizes**: Use powers of 2 or multiples of 8
  - Thumbnails: 128px, 144px, 160px (not 171px)
  - Touch targets: 44px, 48px, 56px minimum
  - Why: These are accessibility and design standards

---

STEP 4: DESCRIBE LAYOUT STRATEGY

For each component, identify the layout pattern:

- **Stack/Absolute**: Layers on top of each other (z-index)
- **Row/Horizontal**: Elements side-by-side (flexbox row)
- **Column/Vertical**: Elements stacked (flexbox column)
- **Grid**: Equal-sized cells

Example:
```
HeroCard: Stack (background image + text overlays)
ArticleCard: Row (thumbnail on left, text column on right)
TextColumn: Column (title, description, metadata stacked)
```

This maps DIRECTLY to UI framework code.

---

STEP 5: SELF-REVIEW (CRITICAL)

Before outputting, CHECK YOUR WORK:

□ Did I miss any elements? (icons, buttons, tabs, etc.)
□ Is every text box FULLY enclosing its text? (no spillover?)
□ Are all coordinates grid-snapped? (all % 8 == 0?)
□ Are margins consistent and standard? (16, 24, 32px?)
□ Would a professional designer approve these values?
□ Does the layout strategy make sense for implementation?

If NO to any → FIX IT before outputting.

---

STEP 6: OUTPUT STRUCTURED JSON

```json
{
  "components": [
    {
      "name": "HeroArticleCard",
      "type": "Card",
      "layout": "Stack",
      "bbox": {"x": 32, "y": 216, "width": 704, "height": 528},
      "props": {
        "borderRadius": "16px",
        "elevation": "2",
        "padding": "0"
      },
      "layers": [
        {
          "z": 0,
          "name": "BackgroundImage",
          "type": "Image",
          "bbox": {"x": 32, "y": 216, "width": 704, "height": 528},
          "props": {
            "source": "geometric-pattern.jpg",
            "resizeMode": "cover",
            "position": "absolute"
          },
          "fills_parent": true
        },
        {
          "z": 1,
          "name": "TitleText",
          "type": "Text",
          "layout": "Absolute",
          "bbox": {"x": 80, "y": 600, "width": 640, "height": 104},
          "props": {
            "text": "On Creative Constraints",
            "fontSize": 36,
            "lineHeight": 1.4,
            "color": "#FFFFFF",
            "fontWeight": "bold",
            "position": "absolute"
          }
        }
      ]
    },
    {
      "name": "ArticleCard",
      "type": "Card",
      "layout": "Row",
      "bbox": {"x": 56, "y": 760, "width": 656, "height": 200},
      "repeats": true,
      "children": [
        {
          "name": "ThumbnailImage",
          "type": "Image",
          "bbox": {"x": 72, "y": 776, "width": 160, "height": 160},
          "props": {"borderRadius": "8px"}
        },
        {
          "name": "TextColumn",
          "type": "Container",
          "layout": "Column",
          "bbox": {"x": 256, "y": 776, "width": 440, "height": 168},
          "children": [
            {
              "name": "TitleText",
              "type": "Text",
              "bbox": {"x": 256, "y": 792, "width": 440, "height": 48}
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Key Differences from My Original Approach

| My Approach | Optimal Synthesis |
|-------------|-------------------|
| 29 iterations | 1 prompt |
| CV detection first | VLM draws first |
| Geometric containment | Paper layering |
| Region merging | Semantic naming from start |
| 9 specialized tools | VLM vision + design rules |
| No layout strategy | Row/Column/Stack specified |
| No visual props | Colors, shadows, border-radius included |
| Declared done early | Self-review checklist |

---

## Why This Works

1. **"Draw first"** → Forces visual attention → Accurate coordinates
2. **Paper layering** → Simple z-index model → Matches real UI
3. **Designer constraints** → Grid + spacing → Professional quality
4. **Layout strategy** → Row/Column/Stack → Directly maps to code
5. **Self-review** → Catches errors → Higher accuracy
6. **Props included** → Visual specs → Ready for implementation

---

## Testing This Now

Let me try this synthesized prompt on the meditation mockup and compare:
- My 29-iteration result
- This 1-prompt result

Should be vastly simpler and equally (or more) accurate.
```
