#!/usr/bin/env python3
"""
Generate a UI Element Blueprint breakdown overlay for blog-meditations-list-v1.png
using Nano Banana Pro's reference image capability.

This generates a structured component analysis following the Paper Layering Theory.
"""

import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator


async def generate_blueprint_overlay():
    """Generate UI blueprint breakdown with semantic component analysis."""
    
    generator = ImageGenerator()
    
    # Input and output paths
    input_image = Path("mockups/blog-meditations-list-v1.png")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "blog-meditations-list-blueprint-semantic.png"
    
    if not input_image.exists():
        print(f"❌ Input image not found: {input_image}")
        return

    print(f"📸 Input: {input_image}")
    print("🎯 Generating semantic UI Element Blueprint overlay...")
    
    result = await generator.generate(
        prompt="""
        IMPORTANT: Take the provided reference image and ADD technical blueprint annotations on top of it.
        DO NOT recreate the UI from scratch. Use the exact image provided as the base layer.
        
        # LAYERING THEORY (Paper Cutout Model)
        
        Think like a child making a paper collage:
        1. **Background layer** - The big piece of paper that fills the space
        2. **Content layers ON TOP** - Text, images, buttons stuck on the background
        3. This is NOT boxes-in-boxes. This is layers-on-layers.
        
        When analyzing components, use the "squinting method":
        - Blur your vision to see major color blocks
        - Background elements FILL SPACE (70%+)
        - Foreground elements SIT ON TOP (text, buttons, icons)
        - Text is ALWAYS a layer on top, never "contained"
        
        # YOUR TASK: Semantic Component Breakdown
        
        Analyze this meditation blog list UI and annotate it with:
        
        ## 1. PATTERN RECOGNITION - Identify Repeated Components
        
        Look for components that repeat (like list items). These should:
        - Share the SAME component name (e.g., "ArticleListItem")
        - Be numbered if there are multiple instances: "ArticleListItem #1", "ArticleListItem #2"
        - Include a note: "⟳ Repeatable component - would be rendered in a loop"
        
        ## 2. SEMANTIC NAMING - Describe WHAT, not just WHAT TYPE
        
        Use meaningful names that describe the component's PURPOSE:
        
        ✓ GOOD: "ArticleListItem", "HeroArticleCard", "NavigationTab", "MetadataRow"
        ✗ BAD: "ListItem", "Card", "Button", "Text"
        
        ✓ GOOD: "AuthorByline", "PublishTimestamp", "ReadingTimeIndicator"
        ✗ BAD: "Label", "Text", "Caption"
        
        ## 3. LAYER DETECTION - Background vs Foreground
        
        For each component, identify its layer type:
        - 🔵 BACKGROUND: Fills the container space (images, gradients, colors)
        - 🟢 CONTENT: Sits on top (text, icons, buttons)
        - 🟣 OVERLAY: Top layer (badges, floating action buttons)
        
        ## 4. STRUCTURAL ANNOTATIONS
        
        Draw clean, professional annotations:
        
        **Component Boxes:**
        - Draw thin colored rectangles around each semantic component
        - Use different colors by layer type:
          * Blue (#3B82F6) - Background/container elements
          * Green (#10B981) - Content elements (text, images)
          * Purple (#8B5CF6) - Interactive elements (buttons, tabs)
          * Orange (#F59E0B) - Repeated/looped components
        
        **Labels:**
        - Add component names next to or inside each box
        - Use format: "ComponentName" or "ComponentName #N" for repeated items
        - For repeated components, add "⟳" symbol
        - Small, clean sans-serif font, high contrast
        
        **Spacing Indicators:**
        - Draw dimension arrows for key spacing (padding, margins)
        - Label with pixel values (e.g., "16px", "24px")
        
        **Nesting Indicators:**
        - Use connecting lines to show parent-child relationships
        - Indent labels slightly to show hierarchy
        
        ## 5. HIERARCHY HINTS for Component Tree
        
        Show which components contain others:
        - Use indented labels or tree-style connectors
        - Mark container components with "↓ Contains:" notes
        - This prepares for JSON/YAML component spec generation
        
        ## EXAMPLE ANNOTATIONS YOU SHOULD CREATE:
        
        ```
        NavigationHeader
        ├─ BlogTab (active)
        ├─ ScreenTitle "Meditations"
        └─ ExploreTab
        
        HeroArticleCard (🔵 Background layer)
        ├─ BackgroundImage (geometric pattern)
        ├─ ArticleTitle 🟢
        ├─ AuthorByline 🟢
        └─ MetricsRow 🟢
            ├─ RatingDisplay
            ├─ ViewCount
            └─ ReadingTime
        
        ArticleListItem #1 ⟳ (Orange box - repeatable)
        ├─ ThumbnailImage 🔵
        ├─ ArticleTitle 🟢
        ├─ ArticleDescription 🟢
        └─ MetadataRow 🟢
            ├─ AuthorName
            ├─ PublishDate
            └─ ReadingTime
        
        ArticleListItem #2 ⟳ (Same structure)
        ArticleListItem #3 ⟳ (Same structure)
        
        BottomNavBar
        ├─ HomeIcon
        ├─ SearchIcon
        ├─ BookmarksIcon
        └─ ProfileIcon
        ```
        
        ## VISUAL STYLE:
        - Semi-transparent overlays (original UI visible underneath)
        - Clean, professional developer handoff documentation style
        - All text must be clearly readable
        - Use a grid or structured layout for annotations
        - Include a small legend in corner showing color meanings
        
        ## OUTPUT REQUIREMENTS:
        - Annotate the EXISTING image, don't recreate it
        - Every visible component should be labeled
        - Repeated components must be identified with ⟳ symbol
        - Show hierarchy through indentation or connecting lines
        - Semantic names that describe purpose, not just type
        - Layer indicators (🔵🟢🟣) for background/content/overlay
        
        This blueprint will be used to generate a component hierarchy spec in JSON/YAML,
        so the annotations should clearly show structure, nesting, and repetition patterns.
        """,
        output_path=output_path,
        preferred_api="nano-banana-pro",
        params={
            "reference_image": input_image,
            "aspect_ratio": "9:16",  # Match the original aspect ratio
            "resolution": "2K",       # High quality for readability
            "use_thinking": True,     # Better UI understanding
            "use_search": False,      # No grounding needed
        },
    )
    
    if result.success:
        print("\n✅ Blueprint generated successfully!")
        print(f"   API: {result.api_used}")
        print(f"   Cost: ${result.cost:.4f}")
        print(f"   Output: {result.local_path}")
    else:
        print(f"\n❌ Generation failed: {result.error}")


async def main():
    """Run the blueprint generation."""
    
    print("=" * 70)
    print("Semantic UI Element Blueprint Generator - Nano Banana Pro")
    print("=" * 70)
    print()
    print("Theory: Paper Layering Model")
    print("Output: Semantic component hierarchy with repetition detection")
    print()
    
    await generate_blueprint_overlay()
    
    print()
    print("=" * 70)
    print("Next step: Generate component spec JSON/YAML from blueprint")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
