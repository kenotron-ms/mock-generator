#!/usr/bin/env python3
"""
Use Nano Banana Pro as a VLM to extract precise design tokens from the original mockup.

This extracts:
- Colors (hex values for backgrounds, text, accents)
- Typography (font sizes, weights, line-heights, families)
- Spacing (exact pixel values for padding, margins, gaps)
- Shadows (depth, blur, color)
- Borders (width, color, radius)
- Other visual properties
"""

import asyncio
import json
import os
from pathlib import Path

try:
    from google import genai  # type: ignore[import-untyped]

    GENAI_AVAILABLE = True
except ImportError:
    genai = None  # type: ignore[assignment]
    print("❌ google-genai not available")
    GENAI_AVAILABLE = False


async def extract_design_tokens():
    """Use Nano Banana Pro to extract precise design tokens from mockup."""

    if not GENAI_AVAILABLE:
        print("❌ Google GenAI SDK not installed")
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return

    # Original mockup image
    mockup_path = Path("mockups/blog-meditations-list-v1.png")
    if not mockup_path.exists():
        print(f"❌ Mockup not found: {mockup_path}")
        return

    print(f"📸 Analyzing mockup: {mockup_path}")
    print("🎨 Using Nano Banana Pro to extract design tokens...")

    # Read the image
    with open(mockup_path, "rb") as f:
        image_data = f.read()

    # Create client
    client = genai.Client(api_key=api_key)

    # Prepare the extraction prompt
    prompt = """
    You are a meticulous design token extraction specialist. Analyze this UI mockup with extreme precision.
    
    # Your Mission: Extract EXACT Design Tokens
    
    Study this meditation blog list UI and measure/extract every visual property with precision.
    
    ## 1. COLOR PALETTE (Hex Values)
    
    Identify and extract:
    
    **Backgrounds:**
    - Screen background color (the overall page background)
    - Card backgrounds (if different from screen)
    - Navigation bar backgrounds
    - Button backgrounds (default, active, hover states)
    
    **Text Colors:**
    - Primary text (headlines, titles) - exact hex
    - Secondary text (descriptions, metadata) - exact hex
    - Tertiary text (captions, timestamps) - exact hex
    - Ensure you note the contrast ratio for accessibility
    
    **Accent Colors:**
    - Active tab indicator color
    - Active navigation item color
    - Link colors
    - Any brand accent colors
    
    **Overlays/Gradients:**
    - Hero card gradient overlay (start color, end color, direction, opacity)
    - Any other overlays or semi-transparent layers
    
    ## 2. TYPOGRAPHY SYSTEM (Exact Values)
    
    For EACH text element, measure:
    
    **Font Sizes:**
    - Screen title ("Meditations") - exact px size
    - Hero card title ("On Creative Constraints") - exact px size
    - Article list title - exact px size
    - Article description - exact px size
    - Metadata text (dates, reading time) - exact px size
    - Navigation labels - exact px size
    
    **Font Weights:**
    - Which text uses: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)?
    
    **Line Heights:**
    - Tight (1.2), normal (1.5), relaxed (1.6), loose (1.8)?
    - Measure for headlines vs body text
    
    **Letter Spacing:**
    - Tight (-0.02em), normal (0), wide (0.05em)?
    
    **Font Family:**
    - What font does this appear to use? (San Francisco, Inter, System UI, etc.)
    - Is it a system font or custom?
    
    ## 3. SPACING SYSTEM (Exact Pixel Values)
    
    Measure every gap, padding, and margin:
    
    **Screen-Level Spacing:**
    - Edge padding (left/right screen edges to content)
    - Top safe area padding
    - Bottom safe area padding
    - Gap between header and hero card
    - Gap between hero card and article list
    - Gap between article list items
    
    **Component-Level Spacing:**
    - Navigation header padding (horizontal and vertical)
    - Hero card content padding
    - Article list item padding
    - Bottom nav bar padding
    - Gap between nav icons
    
    **Internal Component Spacing:**
    - Gap between title and metadata in hero card
    - Gap between article title and description
    - Gap between description and metadata tag
    - Gap inside metadata row (icon to text)
    - Gap between thumbnail and content in list items
    
    ## 4. SIZING VALUES
    
    **Fixed Sizes:**
    - Navigation header height
    - Tab indicator height/width
    - Thumbnail dimensions (width x height)
    - Bottom nav bar height
    - Navigation icon sizes
    
    **Aspect Ratios:**
    - Hero card aspect ratio (measure width:height ratio)
    - Thumbnail aspect ratio
    
    ## 5. VISUAL EFFECTS
    
    **Shadows:**
    - Card shadows (x-offset, y-offset, blur, spread, color, opacity)
    - Bottom nav shadow
    - Any elevation effects
    
    **Borders:**
    - Border widths (if any)
    - Border colors
    - Border radius (corner rounding) for:
      * Hero card
      * Thumbnails
      * Buttons/tabs
      * Article list items
      * Metadata tags
    
    **Opacity/Transparency:**
    - Hero card overlay opacity
    - Any semi-transparent elements
    
    ## 6. COMPONENT-SPECIFIC TOKENS
    
    **Active States:**
    - Active tab: What visual changes? (color, underline, background?)
    - Active nav item: What indicates selection? (color, icon, background?)
    
    **Interactive States:**
    - Hover effects (if visible or can be inferred)
    - Focus states
    - Pressed states
    
    # Output Format: JSON Design Tokens
    
    ```json
    {
      "colors": {
        "background": {
          "screen": "#FAFAFA",
          "card": "#FFFFFF",
          "navigation": "#FFFFFF"
        },
        "text": {
          "primary": "#1A1A1A",
          "secondary": "#666666",
          "tertiary": "#999999"
        },
        "accent": {
          "active": "#6366F1",
          "link": "#6366F1"
        },
        "overlay": {
          "hero-gradient": {
            "start": "rgba(0, 0, 0, 0.0)",
            "end": "rgba(0, 0, 0, 0.6)",
            "direction": "to-top"
          }
        }
      },
      "typography": {
        "fontFamily": {
          "primary": "system-ui, -apple-system, sans-serif"
        },
        "fontSize": {
          "screen-title": "17px",
          "hero-title": "32px",
          "article-title": "18px",
          "article-description": "14px",
          "metadata": "12px",
          "nav-label": "10px"
        },
        "fontWeight": {
          "screen-title": "600",
          "hero-title": "700",
          "article-title": "600",
          "article-description": "400",
          "metadata": "400",
          "nav-label": "500"
        },
        "lineHeight": {
          "tight": "1.2",
          "normal": "1.5",
          "relaxed": "1.6"
        },
        "letterSpacing": {
          "tight": "-0.02em",
          "normal": "0",
          "wide": "0.02em"
        }
      },
      "spacing": {
        "screen": {
          "horizontal": "16px",
          "top": "8px",
          "bottom": "0px"
        },
        "component-gaps": {
          "header-to-hero": "0px",
          "hero-to-list": "16px",
          "list-items": "0px"
        },
        "padding": {
          "navigation-header": {
            "horizontal": "16px",
            "vertical": "8px"
          },
          "hero-content": "16px",
          "article-list-item": "16px",
          "bottom-nav": {
            "horizontal": "24px",
            "vertical": "8px"
          }
        },
        "gaps": {
          "hero-title-to-metadata": "4px",
          "article-title-to-description": "4px",
          "description-to-metadata": "8px",
          "thumbnail-to-content": "12px",
          "nav-icons": "0px"
        }
      },
      "sizing": {
        "navigation-header": {
          "height": "52px"
        },
        "hero-card": {
          "aspect-ratio": "16:9"
        },
        "thumbnail": {
          "width": "80px",
          "height": "80px"
        },
        "bottom-nav": {
          "height": "60px"
        },
        "nav-icon": {
          "size": "24px"
        }
      },
      "effects": {
        "shadows": {
          "card": "0 1px 3px rgba(0, 0, 0, 0.1)",
          "bottom-nav": "0 -1px 3px rgba(0, 0, 0, 0.05)"
        },
        "borderRadius": {
          "hero-card": "0px",
          "thumbnail": "8px",
          "tab-indicator": "3px",
          "metadata-tag": "12px"
        },
        "opacity": {
          "hero-overlay": "0.6",
          "inactive-nav": "0.5"
        }
      }
    }
    ```
    
    # Instructions for Precision:
    
    1. **MEASURE, don't guess** - Look at the actual pixel values in the image
    2. **Be specific** - "17px" not "16-18px"
    3. **Include reasoning** - Why do you think the hero title is 32px vs 28px?
    4. **Cross-check consistency** - Do all article titles use the same size?
    5. **Note variations** - If spacing isn't perfectly consistent, document the pattern
    
    # Important:
    
    - Output ONLY the JSON, no explanations
    - Use exact hex colors (e.g., "#1A1A1A", not "dark gray")
    - Use exact pixel values (e.g., "16px", not "medium")
    - Include ALL components you can identify
    - If you can't measure precisely, give your best estimate with a note
    
    Your response should be pure JSON that can be saved directly to a file.
    """

    # Analyze with Nano Banana Pro
    print("🔍 Extracting design tokens with precision...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",  # Nano Banana Pro
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_data,
                }
            },
        ],
    )

    # Extract the response text
    tokens_text = response.text

    # Strip markdown code fences if present
    if tokens_text.strip().startswith("```"):
        lines = tokens_text.strip().split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        tokens_text = "\n".join(lines)

    print("\n" + "=" * 70)
    print("EXTRACTED DESIGN TOKENS")
    print("=" * 70)
    print(tokens_text)
    print("=" * 70)

    # Try to parse as JSON to validate
    try:
        tokens_json = json.loads(tokens_text)

        # Save to file
        output_path = Path("output/design-tokens.json")
        with open(output_path, "w") as f:
            json.dump(tokens_json, f, indent=2)

        print(f"\n✅ Valid JSON! Saved to: {output_path}")

        # Print summary
        print("\n🎨 Design Token Summary:")

        if "colors" in tokens_json:
            color_count = sum(
                len(v) if isinstance(v, dict) else 1
                for v in tokens_json["colors"].values()
            )
            print(f"   Colors: {color_count} tokens extracted")

        if "typography" in tokens_json:
            typo = tokens_json["typography"]
            font_sizes = len(typo.get("fontSize", {}))
            print(f"   Typography: {font_sizes} font sizes")

        if "spacing" in tokens_json:
            print("   Spacing: ✓ Extracted")

        if "effects" in tokens_json:
            effects = tokens_json["effects"]
            shadows = len(effects.get("shadows", {}))
            radii = len(effects.get("borderRadius", {}))
            print(f"   Effects: {shadows} shadows, {radii} border radii")

    except json.JSONDecodeError as e:
        print(f"\n⚠️  Response is not valid JSON: {e}")
        print("   Saving raw response to output/design-tokens-raw.txt")
        raw_path = Path("output/design-tokens-raw.txt")
        with open(raw_path, "w") as f:
            f.write(tokens_text)
        print(f"   Saved to: {raw_path}")


async def main():
    """Run design token extraction."""

    print("=" * 70)
    print("Design Token Extraction - Nano Banana Pro VLM Analysis")
    print("=" * 70)
    print()
    print("Purpose: Extract EXACT design tokens for pixel-perfect replication")
    print("Method: Visual analysis of original mockup")
    print()

    await extract_design_tokens()

    print()
    print("=" * 70)
    print("Use these tokens to rebuild the app with exact styling!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
