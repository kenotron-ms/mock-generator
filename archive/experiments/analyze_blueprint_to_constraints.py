#!/usr/bin/env python3
"""
Analyze the semantic blueprint using a VLM and generate a constraint-based
component specification that works across different portrait screen sizes.

Instead of exact pixels, we use:
- Semantic spacing scales (xs, sm, md, lg, xl)
- Proportional sizing (%, fill, fit-content)
- Flex weights (how much space relative to siblings)
- Constraints (min/max, aspect ratios)
- Relationships (alignment, distribution)
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
    print("❌ google-genai not available. Install with: pip install google-genai")
    GENAI_AVAILABLE = False


async def analyze_blueprint_with_constraints():
    """Use Nano Banana Pro to analyze the blueprint and generate constraint-based spec."""

    if not GENAI_AVAILABLE:
        print("❌ Google GenAI SDK not installed")
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return

    # Input blueprint image
    blueprint_path = Path("output/blog-meditations-list-blueprint-semantic.png")
    if not blueprint_path.exists():
        print(f"❌ Blueprint not found: {blueprint_path}")
        print("   Run generate_ui_blueprint.py first!")
        return

    print(f"📸 Analyzing blueprint: {blueprint_path}")
    print("🤖 Using Nano Banana Pro for constraint analysis...")

    # Read the image
    with open(blueprint_path, "rb") as f:
        image_data = f.read()

    # Create client
    client = genai.Client(api_key=api_key)

    # Prepare the analysis prompt
    prompt = """
    Analyze this UI blueprint and generate a CONSTRAINT-BASED component specification.
    
    # Key Philosophy: Proportions, Not Pixels
    
    We want a spec that works across different portrait screen sizes (iPhone SE to iPhone Pro Max).
    Focus on RELATIONSHIPS and PROPORTIONS, not exact measurements.
    
    # Constraint System
    
    ## 1. Spacing Scale (Semantic Tokens)
    Instead of "16px" or "24px", use semantic spacing:
    
    - **xs**: Tight spacing (text line height, icon padding)
    - **sm**: Close spacing (related items, form fields)
    - **md**: Standard spacing (between sections, card padding)
    - **lg**: Generous spacing (between major sections)
    - **xl**: Maximum spacing (screen edges, dramatic separation)
    
    ## 2. Sizing Constraints
    Instead of fixed sizes, use:
    
    - **fill**: Takes all available space in parent
    - **fit-content**: Sizes to content (text, image intrinsic size)
    - **proportion**: Relative to parent (e.g., "50%", "1/3")
    - **aspect-ratio**: Maintains ratio (e.g., "16:9", "1:1", "3:4")
    - **min/max**: Constraints (e.g., "min-width: 320", "max-width: 600")
    
    ## 3. Flex Weight (for siblings)
    How much space does a component take relative to its siblings?
    
    - **weight: 1**: Equal space with siblings
    - **weight: 2**: Twice the space of weight-1 siblings
    - **fixed**: Doesn't grow/shrink (intrinsic size)
    
    ## 4. Layout Distribution
    How are children distributed?
    
    - **packed-start**: Packed at start with gaps between
    - **packed-center**: Centered with gaps between
    - **space-between**: Spread evenly, edges touch container
    - **space-around**: Spread evenly with space at edges
    
    ## 5. Alignment
    - **start/end**: Align to start/end of cross-axis
    - **center**: Center on cross-axis
    - **stretch**: Fill cross-axis
    - **baseline**: Align text baselines
    
    # Output Schema
    
    Generate JSON following this structure:
    
    ```json
    {
      "screen": "MeditationsBlogList",
      "description": "Blog list with hero card and article list",
      "constraints": {
        "type": "ScrollView",
        "direction": "vertical",
        "spacing": {
          "edges": "md",
          "between-sections": "lg"
        }
      },
      "components": [
        {
          "name": "NavigationHeader",
          "type": "Container",
          "semantic_role": "Top navigation",
          "layer": "content",
          "constraints": {
            "height": "fit-content",
            "width": "fill",
            "padding": {
              "horizontal": "md",
              "vertical": "sm"
            }
          },
          "layout": {
            "type": "horizontal",
            "distribution": "space-between",
            "alignment": "center",
            "gap": "sm"
          },
          "children": [...]
        },
        {
          "name": "HeroArticleCard",
          "constraints": {
            "width": "fill",
            "height": "proportion:60%",
            "aspect-ratio": "16:9",
            "margin": {
              "bottom": "md"
            }
          },
          "layout": {
            "type": "absolute"
          },
          "children": [
            {
              "name": "BackgroundImage",
              "constraints": {
                "width": "fill",
                "height": "fill"
              }
            },
            {
              "name": "ContentOverlay",
              "constraints": {
                "width": "fill",
                "height": "fit-content",
                "position": "bottom-left",
                "padding": "md"
              },
              "layout": {
                "type": "vertical",
                "gap": "xs"
              },
              "children": [...]
            }
          ]
        },
        {
          "name": "ArticleListItem",
          "repeatable": true,
          "constraints": {
            "width": "fill",
            "height": "fit-content",
            "padding": "md",
            "margin": {
              "bottom": "sm"
            }
          },
          "layout": {
            "type": "horizontal",
            "alignment": "start",
            "gap": "md"
          },
          "children": [
            {
              "name": "ThumbnailImage",
              "constraints": {
                "width": "fixed:80",
                "height": "fixed:80",
                "aspect-ratio": "1:1",
                "flex-weight": "fixed"
              }
            },
            {
              "name": "ArticleContent",
              "constraints": {
                "width": "fill",
                "height": "fit-content",
                "flex-weight": 1
              },
              "layout": {
                "type": "vertical",
                "gap": "xs"
              },
              "children": [
                {
                  "name": "ArticleTitle",
                  "constraints": {
                    "width": "fill",
                    "height": "fit-content",
                    "max-lines": 2
                  }
                },
                {
                  "name": "ArticleDescription",
                  "constraints": {
                    "width": "fill",
                    "height": "fit-content",
                    "max-lines": 3
                  }
                },
                {
                  "name": "MetadataRow",
                  "constraints": {
                    "width": "fill",
                    "height": "fit-content"
                  },
                  "layout": {
                    "type": "horizontal",
                    "gap": "xs"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
    ```
    
    # Analysis Guidelines
    
    1. **Look at proportions, not exact sizes**
       - Hero card takes ~60% of screen height?
       - Thumbnail is square and fixed size?
       - Content area fills remaining space?
    
    2. **Identify spacing patterns**
       - Tight spacing for text line-height → xs
       - Standard card padding → md
       - Space between sections → lg
    
    3. **Determine layout behaviors**
       - Does component fill width? → width: "fill"
       - Does it size to content? → height: "fit-content"
       - Fixed size thumbnail? → width: "fixed:80"
    
    4. **Identify flex relationships**
       - Thumbnail stays fixed, content grows → thumbnail gets flex-weight: "fixed", content gets flex-weight: 1
       - Equal-width columns → both get flex-weight: 1
    
    5. **Mark repeatable components**
       - ArticleListItem repeats → repeatable: true
       - NavIcon repeats → repeatable: true
    
    6. **Describe distribution patterns**
       - Nav items spread evenly? → distribution: "space-between"
       - Cards stacked with gaps? → gap: "md"
    
    # Important: NO PIXEL VALUES
    
    Use semantic spacing (xs/sm/md/lg/xl) and proportional sizing.
    The only exception is "fixed" for truly fixed-size elements like icons or thumbnails.
    
    Your response should be ONLY the JSON, no explanations or markdown code fences.
    """

    # Analyze with Nano Banana Pro
    print("🔍 Analyzing component constraints...")

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
    spec_text = response.text

    # Strip markdown code fences if present
    if spec_text.strip().startswith("```"):
        lines = spec_text.strip().split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        spec_text = "\n".join(lines)

    print("\n" + "=" * 70)
    print("GENERATED CONSTRAINT-BASED SPECIFICATION")
    print("=" * 70)
    print(spec_text)
    print("=" * 70)

    # Try to parse as JSON to validate
    try:
        spec_json = json.loads(spec_text)

        # Save to file
        output_path = Path("output/component-spec-constraints.json")
        with open(output_path, "w") as f:
            json.dump(spec_json, f, indent=2)

        print(f"\n✅ Valid JSON! Saved to: {output_path}")

        # Print summary
        print("\n📊 Component Summary:")
        print(f"   Screen: {spec_json.get('screen', 'Unknown')}")
        print(f"   Layout: {spec_json.get('constraints', {}).get('type', 'Unknown')}")
        print(f"   Top-level components: {len(spec_json.get('components', []))}")

        # Count repeatable components
        def count_repeatable(components):
            count = 0
            for comp in components:
                if comp.get("repeatable"):
                    count += 1
                if comp.get("children"):
                    count += count_repeatable(comp["children"])
            return count

        repeatable = count_repeatable(spec_json.get("components", []))
        if repeatable > 0:
            print(f"   Repeatable components: {repeatable}")

        # Show spacing scale used
        print("\n📏 Spacing Scale:")
        print("   xs = tight (line height, icon padding)")
        print("   sm = close (related items)")
        print("   md = standard (sections, card padding)")
        print("   lg = generous (major sections)")
        print("   xl = maximum (screen edges)")

    except json.JSONDecodeError as e:
        print(f"\n⚠️  Response is not valid JSON: {e}")
        print("   Saving raw response to output/component-spec-constraints-raw.txt")
        raw_path = Path("output/component-spec-constraints-raw.txt")
        with open(raw_path, "w") as f:
            f.write(spec_text)
        print(f"   Saved to: {raw_path}")


async def main():
    """Run the constraint-based blueprint analysis."""

    print("=" * 70)
    print("Blueprint → Constraint-Based Component Spec")
    print("=" * 70)
    print()
    print("Philosophy: Proportions over Pixels")
    print("Using: Nano Banana Pro (VLM)")
    print("Output: Responsive constraint-based specification")
    print()

    await analyze_blueprint_with_constraints()

    print()
    print("=" * 70)
    print("This spec works across different portrait screen sizes!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
