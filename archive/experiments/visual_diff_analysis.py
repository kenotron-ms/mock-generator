#!/usr/bin/env python3
"""
Use Nano Banana Pro as a VLM to compare the original mockup with a screenshot
of the current implementation and identify ALL visual differences.
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


async def compare_images_with_vlm():
    """Use Nano Banana Pro to pixel-peep the differences."""

    if not GENAI_AVAILABLE:
        print("❌ Google GenAI SDK not installed")
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return

    # Check if we have a screenshot
    screenshot_path = Path("output/current-app-screenshot.png")
    if not screenshot_path.exists():
        print(f"❌ Screenshot not found: {screenshot_path}")
        print()
        print("PLEASE CAPTURE SCREENSHOT:")
        print("1. Open http://localhost:5173 in Chrome")
        print("2. DevTools → Device Mode → iPhone 14 Pro (390x844)")
        print("3. Cmd+Shift+P → 'Capture screenshot'")
        print("4. Save as: output/current-app-screenshot.png")
        print()
        print("OR just take any screenshot of the app and save it there!")
        return

    original_path = Path("mockups/blog-meditations-list-v1.png")

    print(f"📸 Original: {original_path}")
    print(f"📸 Current:  {screenshot_path}")
    print()
    print("🔍 Using Nano Banana Pro to analyze pixel-by-pixel differences...")

    # Read both images
    with open(original_path, "rb") as f:
        original_data = f.read()

    with open(screenshot_path, "rb") as f:
        current_data = f.read()

    # Create client
    client = genai.Client(api_key=api_key)

    # Prepare the comparison prompt
    prompt = """
    You are a meticulous visual QA specialist doing pixel-perfect design comparison.
    
    # Your Task: Compare These Two Images
    
    IMAGE 1: Original mockup (the design target)
    IMAGE 2: Current implementation (what we built)
    
    # Analysis Method: Systematic Component-by-Component Comparison
    
    Go through EVERY visible component and identify differences:
    
    ## 1. COLORS
    Compare each color in the implementation vs original:
    - Background colors (screen, cards, navigation)
    - Text colors (titles, descriptions, metadata)
    - Accent colors (active tabs, buttons, highlights)
    - Tag/badge colors
    - Are the colors EXACTLY matching or slightly off?
    
    ## 2. TYPOGRAPHY
    - Font family (serif vs sans-serif vs monospace?)
    - Font sizes (measure visually - is text larger/smaller?)
    - Font weights (bolder/lighter?)
    - Line heights (tighter/looser spacing between lines?)
    - Letter spacing
    - Text alignment
    
    ## 3. SPACING
    - Padding inside components (is there more/less space?)
    - Margins between components (gaps too large/small?)
    - Screen edge padding (content too close/far from edges?)
    - Gaps between elements (title to description, thumbnail to text, etc.)
    
    ## 4. SIZING
    - Component heights (hero card, list items, nav bar)
    - Component widths
    - Thumbnail sizes (are they the right size?)
    - Icon sizes
    - Aspect ratios (is hero card the right proportions?)
    
    ## 5. BORDERS & EFFECTS
    - Border radius (rounded corners - more/less rounded?)
    - Shadows (are shadows visible? Right depth?)
    - Borders (any borders present/missing?)
    - Opacity/transparency effects
    
    ## 6. LAYOUT & ALIGNMENT
    - Component positions (too high/low?)
    - Alignment (centered vs left-aligned vs right-aligned?)
    - Distribution (spacing between nav icons, etc.)
    - Vertical rhythm (does spacing feel consistent?)
    
    ## 7. VISUAL HIERARCHY
    - Prominence (what draws the eye first?)
    - Contrast ratios
    - Visual weight
    
    ## 8. MISSING/EXTRA ELEMENTS
    - Are there elements in original that are missing in implementation?
    - Are there elements in implementation that shouldn't be there?
    
    # Output Format: Detailed Diff Report (JSON)
    
    ```json
    {
      "overall_assessment": "65% match - close but significant differences remain",
      "critical_issues": [
        "Font family is wrong - should be serif, currently sans-serif",
        "Background color is off - should be #F3EFE7 (warm beige), currently gray"
      ],
      "differences_by_component": {
        "ScreenHeader": {
          "colors": {
            "background": {
              "original": "#FFFFFF",
              "current": "#F5F5F5",
              "severity": "minor",
              "fix": "Change to exact white #FFFFFF"
            }
          },
          "typography": {
            "title_size": {
              "original": "32px",
              "current": "~28px",
              "severity": "major",
              "fix": "Increase font-size to 32px"
            }
          },
          "spacing": {
            "gap_title_to_tabs": {
              "original": "~24px",
              "current": "~16px", 
              "severity": "medium",
              "fix": "Increase gap to 24px (gap-lg)"
            }
          }
        },
        "HeroArticleCard": {
          "colors": {
            "gradient_overlay": {
              "original": "rgba(0,0,0,0.4) bottom to top",
              "current": "rgba(0,0,0,0.5) bottom to top",
              "severity": "minor",
              "fix": "Reduce opacity from 0.5 to 0.4"
            }
          },
          "borders": {
            "border_radius": {
              "original": "16px",
              "current": "8px",
              "severity": "medium",
              "fix": "Increase border-radius to 16px"
            }
          }
        },
        "ArticleListItem": {
          "spacing": {
            "padding": {
              "original": "16px all sides",
              "current": "12px all sides",
              "severity": "medium",
              "fix": "Increase padding to 16px"
            },
            "gap_between_items": {
              "original": "16px",
              "current": "24px",
              "severity": "medium",
              "fix": "Reduce margin-bottom to 16px"
            }
          },
          "colors": {
            "metadata_tag": {
              "original": "Varies - green and red tags visible",
              "current": "All green",
              "severity": "minor",
              "fix": "Alternate tag colors or assign based on category"
            }
          }
        },
        "BottomNavBar": {
          "sizing": {
            "height": {
              "original": "~60px",
              "current": "~50px",
              "severity": "medium",
              "fix": "Increase height to 60px"
            }
          },
          "effects": {
            "border_radius": {
              "original": "30px (pill shape)",
              "current": "0px (square)",
              "severity": "major",
              "fix": "Add rounded-nav (30px) class"
            },
            "shadow": {
              "original": "Subtle upward shadow",
              "current": "Border line",
              "severity": "medium",
              "fix": "Replace border with shadow-nav"
            }
          }
        }
      },
      "missing_elements": [
        "Navigation icons are emoji placeholders - need actual minimal icon images",
        "Some thumbnails missing (only 2/5 generated)",
        "Article list items might be missing visual separators or subtle backgrounds"
      ],
      "priority_fixes": [
        "1. Fix font family to serif (CRITICAL for feel)",
        "2. Fix background color to #F3EFE7 warm beige (CRITICAL for feel)",
        "3. Fix BottomNavBar border-radius to 30px pill shape",
        "4. Adjust all spacing to match exact values from tokens",
        "5. Generate remaining thumbnails and icons"
      ]
    }
    ```
    
    # Instructions:
    
    - Be brutally honest - identify EVERY difference you can see
    - Measure visually (e.g., "component appears 20% larger")
    - Prioritize by severity: critical (changes feel), major (noticeable), medium (subtle), minor (trivial)
    - Provide specific fixes for each issue
    - Think like a pixel-perfect designer reviewing a developer's implementation
    
    Your response should be ONLY the JSON diff report.
    """

    # Analyze with Nano Banana Pro
    print("📊 Analyzing differences...")
    print()

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",  # Nano Banana Pro for precise vision
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": original_data,
                }
            },
            "IMAGE 1 above is the ORIGINAL (design target)",
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": current_data,
                }
            },
            "IMAGE 2 above is the CURRENT IMPLEMENTATION (what we built)",
        ],
    )

    # Extract the response
    diff_text = response.text

    # Strip markdown code fences
    if diff_text.strip().startswith("```"):
        lines = diff_text.strip().split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        diff_text = "\n".join(lines)

    print("=" * 70)
    print("VISUAL DIFF ANALYSIS")
    print("=" * 70)
    print(diff_text)
    print("=" * 70)

    # Parse and save
    try:
        diff_json = json.loads(diff_text)

        output_path = Path("output/visual-diff-report.json")
        with open(output_path, "w") as f:
            json.dump(diff_json, f, indent=2)

        print(f"\n✅ Saved to: {output_path}")

        # Print summary
        print("\n📊 Diff Summary:")
        print(f"   Overall: {diff_json.get('overall_assessment', 'N/A')}")
        print(f"   Critical issues: {len(diff_json.get('critical_issues', []))}")
        print(
            f"   Components analyzed: {len(diff_json.get('differences_by_component', {}))}"
        )
        print(f"   Priority fixes: {len(diff_json.get('priority_fixes', []))}")

        if diff_json.get("critical_issues"):
            print("\n🚨 Critical Issues:")
            for issue in diff_json["critical_issues"]:
                print(f"   - {issue}")

        if diff_json.get("priority_fixes"):
            print("\n🎯 Top Priority Fixes:")
            for i, fix in enumerate(diff_json["priority_fixes"][:5], 1):
                print(f"   {i}. {fix}")

    except json.JSONDecodeError as e:
        print(f"\n⚠️  Not valid JSON: {e}")
        raw_path = Path("output/visual-diff-raw.txt")
        with open(raw_path, "w") as f:
            f.write(diff_text)
        print(f"   Saved raw to: {raw_path}")


async def main():
    print("=" * 70)
    print("PIXEL-BY-PIXEL VISUAL COMPARISON")
    print("=" * 70)
    print()
    print("Method: Nano Banana Pro VLM analysis of both images")
    print("Goal: Identify ALL differences for pixel-perfect matching")
    print()

    await compare_images_with_vlm()

    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
