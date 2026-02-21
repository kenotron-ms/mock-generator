#!/usr/bin/env python3
"""
Analyze the semantic blueprint image using a VLM (Gemini Pro Vision)
and generate a structured component specification in JSON/YAML format.
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


async def analyze_blueprint_with_vlm():
    """Use Gemini Pro Vision to analyze the blueprint and generate component spec."""

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
    print("🤖 Using Gemini Pro Vision for analysis...")

    # Read the image
    with open(blueprint_path, "rb") as f:
        image_data = f.read()

    # Create client
    client = genai.Client(api_key=api_key)

    # Prepare the analysis prompt
    prompt = """
    Analyze this UI blueprint image and generate a structured component specification.
    
    # Your Task
    
    Study the annotated blueprint and extract:
    1. Every labeled component with its semantic name
    2. The hierarchy/nesting structure (parent-child relationships)
    3. Components marked as repeatable/looped (⟳ symbol)
    4. Layer types (background 🔵, content 🟢, overlay 🟣)
    5. **Spacing information** (look for dimension arrows and pixel values like "16px", "24px")
    6. **Layout information** (how children are arranged - vertical stack, horizontal row, grid)
    
    # Output Format: JSON Component Tree
    
    Generate a JSON structure following this schema:
    
    ```json
    {
      "screen": "MeditationBlogList",
      "description": "Blog list view with hero card and article list items",
      "layout": {
        "type": "ScrollView",
        "direction": "vertical"
      },
      "spacing": {
        "screenPadding": "16px",
        "componentGap": "24px"
      },
      "components": [
        {
          "name": "ComponentName",
          "type": "Container|Text|Image|Button|List|etc",
          "semantic_role": "What this component does",
          "layer": "background|content|overlay",
          "repeatable": false,
          "layout": {
            "type": "horizontal|vertical|absolute|grid",
            "alignment": "start|center|end|stretch",
            "gap": "16px"
          },
          "spacing": {
            "padding": "16px",
            "margin": "8px"
          },
          "children": [
            {
              "name": "ChildComponent",
              "type": "...",
              "semantic_role": "...",
              "layer": "...",
              "repeatable": false,
              "layout": {...},
              "spacing": {...},
              "children": []
            }
          ]
        }
      ]
    }
    ```
    
    # Important Rules:
    
    1. **Use the exact semantic names from the blueprint**
       - If it says "ArticleListItem", use that, not "ListItem"
       - If it says "AuthorByline", use that, not "Text"
    
    2. **Preserve hierarchy from the blueprint**
       - If component A contains component B, B should be in A's children array
       - Match the tree structure shown in the annotations
    
    3. **Mark repeatable components**
       - If a component has ⟳ symbol or #1, #2, #3 numbering, set "repeatable": true
       - Include ONE instance with all its structure (not multiple copies)
    
    4. **Include layer information**
       - "background" for components that fill space (🔵)
       - "content" for components sitting on top (🟢)
       - "overlay" for top-layer elements (🟣)
    
    5. **Add semantic_role descriptions**
       - Brief description of what the component does
       - Example: "Displays article title and metadata"
    
    6. **Extract spacing information from dimension arrows**
       - Look for pixel values shown in the blueprint (e.g., "16px", "24px", "32px")
       - Add to "spacing" object with padding/margin hints
       - If no specific values visible, estimate based on visual proportions
    
    7. **Determine layout/containment patterns**
       - **Vertical stack**: Children arranged top to bottom (common for lists, forms)
       - **Horizontal row**: Children arranged left to right (common for nav bars, button groups)
       - **Grid**: Children in rows and columns (common for image galleries, card grids)
       - **Absolute**: Children positioned absolutely (common for overlays, floating elements)
    
    8. **Add overarching container information**
       - Is the whole screen a ScrollView?
       - Are there fixed headers/footers?
       - What's the overall layout pattern?
    
    # Example Output Structure:
    
    ```json
    {
      "screen": "MeditationBlogList",
      "layout": {
        "type": "ScrollView",
        "direction": "vertical"
      },
      "spacing": {
        "screenPadding": "16px",
        "componentGap": "24px"
      },
      "components": [
        {
          "name": "NavigationHeader",
          "type": "Container",
          "semantic_role": "Top navigation bar with tabs",
          "layer": "content",
          "layout": {
            "type": "horizontal",
            "alignment": "center",
            "gap": "8px"
          },
          "spacing": {
            "padding": "16px",
            "margin": "0px"
          },
          "children": [
            {
              "name": "BlogTab",
              "type": "Button",
              "semantic_role": "Navigate to blog section",
              "layer": "content",
              "state": "active"
            },
            {
              "name": "ScreenTitle",
              "type": "Text",
              "semantic_role": "Display current screen name",
              "layer": "content",
              "text": "Meditations"
            },
            {
              "name": "ExploreTab",
              "type": "Button",
              "semantic_role": "Navigate to explore section",
              "layer": "content"
            }
          ]
        },
        {
          "name": "HeroArticleCard",
          "type": "Container",
          "semantic_role": "Featured article with large visual",
          "layer": "background",
          "children": [
            {
              "name": "BackgroundImage",
              "type": "Image",
              "semantic_role": "Decorative background pattern",
              "layer": "background"
            },
            {
              "name": "ArticleTitle",
              "type": "Text",
              "semantic_role": "Main article title",
              "layer": "content"
            },
            {
              "name": "AuthorByline",
              "type": "Text",
              "semantic_role": "Author attribution",
              "layer": "content"
            },
            {
              "name": "MetricsRow",
              "type": "Container",
              "semantic_role": "Article engagement metrics",
              "layer": "content",
              "children": [
                {
                  "name": "RatingDisplay",
                  "type": "Component",
                  "semantic_role": "Star rating"
                },
                {
                  "name": "ViewCount",
                  "type": "Component",
                  "semantic_role": "Number of views"
                },
                {
                  "name": "ReadingTime",
                  "type": "Component",
                  "semantic_role": "Estimated reading time"
                }
              ]
            }
          ]
        },
        {
          "name": "ArticleListItem",
          "type": "Container",
          "semantic_role": "Individual article in scrollable list",
          "layer": "content",
          "repeatable": true,
          "note": "This component repeats for each article in the list",
          "children": [
            {
              "name": "ThumbnailImage",
              "type": "Image",
              "semantic_role": "Article preview image",
              "layer": "background"
            },
            {
              "name": "ArticleTitle",
              "type": "Text",
              "semantic_role": "Article title",
              "layer": "content"
            },
            {
              "name": "ArticleDescription",
              "type": "Text",
              "semantic_role": "Brief article summary",
              "layer": "content"
            },
            {
              "name": "MetadataRow",
              "type": "Container",
              "semantic_role": "Article metadata",
              "layer": "content",
              "children": [
                {
                  "name": "AuthorName",
                  "type": "Text",
                  "semantic_role": "Article author"
                },
                {
                  "name": "PublishDate",
                  "type": "Text",
                  "semantic_role": "Publication date"
                },
                {
                  "name": "ReadingTime",
                  "type": "Text",
                  "semantic_role": "Estimated reading time"
                }
              ]
            }
          ]
        },
        {
          "name": "BottomNavBar",
          "type": "Container",
          "semantic_role": "Bottom navigation bar",
          "layer": "overlay",
          "children": [
            {
              "name": "HomeIcon",
              "type": "Button",
              "semantic_role": "Navigate to home"
            },
            {
              "name": "SearchIcon",
              "type": "Button",
              "semantic_role": "Navigate to search"
            },
            {
              "name": "BookmarksIcon",
              "type": "Button",
              "semantic_role": "Navigate to bookmarks"
            },
            {
              "name": "ProfileIcon",
              "type": "Button",
              "semantic_role": "Navigate to profile"
            }
          ]
        }
      ]
    }
    ```
    
    # Your Response:
    
    Provide ONLY the JSON output. No explanations, no markdown code fences, just the raw JSON.
    Study the blueprint carefully and extract the exact structure shown.
    """

    # Analyze with Gemini Pro Vision
    print("🔍 Analyzing component structure...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",  # Nano Banana Pro - best vision model
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
        # Remove ```json or ``` at start and ``` at end
        lines = spec_text.strip().split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]  # Remove first line
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # Remove last line
        spec_text = "\n".join(lines)

    print("\n" + "=" * 70)
    print("GENERATED COMPONENT SPECIFICATION")
    print("=" * 70)
    print(spec_text)
    print("=" * 70)

    # Try to parse as JSON to validate
    try:
        spec_json = json.loads(spec_text)

        # Save to file
        output_path = Path("output/component-spec.json")
        with open(output_path, "w") as f:
            json.dump(spec_json, f, indent=2)

        print(f"\n✅ Valid JSON! Saved to: {output_path}")

        # Also save as YAML if pyyaml is available
        try:
            import yaml

            yaml_path = Path("output/component-spec.yaml")
            with open(yaml_path, "w") as f:
                yaml.dump(spec_json, f, default_flow_style=False, sort_keys=False)
            print(f"✅ Also saved as YAML: {yaml_path}")
        except ImportError:
            print("ℹ️  Install pyyaml for YAML output: pip install pyyaml")

        # Print summary
        print("\n📊 Component Summary:")
        print(f"   Screen: {spec_json.get('screen', 'Unknown')}")
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

    except json.JSONDecodeError as e:
        print(f"\n⚠️  Response is not valid JSON: {e}")
        print("   Saving raw response to output/component-spec-raw.txt")
        raw_path = Path("output/component-spec-raw.txt")
        with open(raw_path, "w") as f:
            f.write(spec_text)
        print(f"   Saved to: {raw_path}")


async def main():
    """Run the blueprint analysis."""

    print("=" * 70)
    print("Blueprint → Component Spec Generator")
    print("=" * 70)
    print()
    print("Using: Gemini Pro Vision (VLM)")
    print("Input: Semantic blueprint PNG with annotations")
    print("Output: Structured JSON/YAML component specification")
    print()

    await analyze_blueprint_with_vlm()

    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
