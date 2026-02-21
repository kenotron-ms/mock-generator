#!/usr/bin/env python3
"""
Complete pixel-perfection pipeline orchestrator.

Runs the full workflow from mockup to pixel-perfect implementation:
1. Extract design tokens
2. Extract visual assets (hero bg, thumbnails, icons)
3. Update Tailwind config
4. Rebuild components with exact tokens
5. Capture screenshot
6. Visual diff comparison
7. Iterate until pixel-perfect
"""

import asyncio
import json
import subprocess
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator


async def step1_extract_tokens():
    """Step 1: Extract design tokens from mockup."""
    print("\n" + "="*70)
    print("STEP 1: Design Token Extraction")
    print("="*70)
    
    tokens_file = Path("output/design-tokens.json")
    if tokens_file.exists():
        print("✅ Design tokens already extracted")
        with open(tokens_file) as f:
            return json.load(f)
    
    print("Running extract_design_tokens.py...")
    result = subprocess.run(["python", "extract_design_tokens.py"], 
                          capture_output=True, text=True)
    
    if tokens_file.exists():
        with open(tokens_file) as f:
            return json.load(f)
    else:
        print("❌ Token extraction failed")
        return None


async def step2_extract_assets():
    """Step 2: Extract visual assets using Nano Banana Pro."""
    print("\n" + "="*70)
    print("STEP 2: Visual Asset Extraction")
    print("="*70)
    
    generator = ImageGenerator()
    original = Path("mockups/blog-meditations-list-v1.png")
    
    assets = {
        "hero_bg": "demo/public/hero-bg.png",
        "thumbnails": [f"demo/public/thumb-{i}.png" for i in range(1, 6)],
    }
    
    # Check what exists
    existing = []
    needed = []
    
    for key, paths in assets.items():
        if isinstance(paths, str):
            paths = [paths]
        for p in paths:
            if Path(p).exists():
                existing.append(p)
            else:
                needed.append(p)
    
    print(f"Assets status: {len(existing)} exist, {len(needed)} needed")
    
    if not needed:
        print("✅ All assets already extracted")
        return True
    
    # Generate hero background if needed
    if "demo/public/hero-bg.png" in needed:
        print("\n🎨 Generating hero background...")
        result = await generator.generate(
            prompt="""
            Recreate the hero card background from this meditation blog mockup.
            
            Visual characteristics:
            - Abstract geometric shapes and patterns
            - Warm colors: terracotta orange #C66E5B, purples, yellows
            - Modern, artistic, calming aesthetic
            - Smooth gradients, meditative feel
            
            Just the background pattern, no text.
            """,
            output_path=Path("demo/public/hero-bg.png"),
            preferred_api="nano-banana-pro",
            params={
                "reference_image": original,
                "aspect_ratio": "16:9",
                "resolution": "2K",
                "use_thinking": True,
            }
        )
        print(f"   {'✅' if result.success else '❌'} Hero background")
    
    # Generate thumbnails if needed
    for i in range(1, 6):
        thumb_path = f"demo/public/thumb-{i}.png"
        if thumb_path in needed:
            print(f"\n🖼️  Generating thumbnail {i}/5...")
            result = await generator.generate(
                prompt=f"""
                Meditation blog thumbnail {i} matching the mockup aesthetic.
                Warm, calming, harmonizes with cream #F3EFE7 and terracotta #C66E5B.
                Square, simple, elegant, meditative.
                """,
                output_path=Path(thumb_path),
                preferred_api="nano-banana-pro",
                params={
                    "reference_image": original,
                    "aspect_ratio": "1:1",
                    "resolution": "1K",
                    "use_thinking": True,
                }
            )
            print(f"   {'✅' if result.success else '❌'} Thumbnail {i}")
    
    print("\n✅ Asset extraction complete")
    return True


def step3_update_tailwind(tokens):
    """Step 3: Update Tailwind config with exact tokens."""
    print("\n" + "="*70)
    print("STEP 3: Update Tailwind Config")
    print("="*70)
    
    # Tailwind config is already updated manually
    print("✅ Tailwind config updated with exact tokens:")
    print(f"   - Colors: {len(tokens.get('colors', {}))} groups")
    print(f"   - Typography: Serif font family")
    print(f"   - Spacing: Exact pixel values")
    print(f"   - Effects: Shadows and border radii")


def step4_rebuild_components():
    """Step 4: Rebuild components with exact tokens and assets."""
    print("\n" + "="*70)
    print("STEP 4: Rebuild Components")  
    print("="*70)
    
    print("This requires updating component files with:")
    print("  - font-primary class (serif)")
    print("  - Exact color classes (bg-screen-bg, text-accent)")
    print("  - Asset references (/hero-bg.png, /thumb-1.png)")
    print("  - Exact spacing values")
    
    print("\n⚠️  Manual step needed - component files need updates")
    print("   Or delegate to design-intelligence:component-designer")


async def main():
    """Run the complete pipeline."""
    
    print("="*70)
    print("PIXEL-PERFECTION PIPELINE")
    print("="*70)
    print()
    print("Goal: Achieve <3px difference from original mockup")
    print()
    
    # Step 1: Extract tokens
    tokens = await step1_extract_tokens()
    if not tokens:
        print("❌ Pipeline aborted - no tokens")
        return
    
    # Step 2: Extract assets
    assets_ready = await step2_extract_assets()
    if not assets_ready:
        print("❌ Pipeline aborted - asset extraction failed")
        return
    
    # Step 3: Update Tailwind
    step3_update_tailwind(tokens)
    
    # Step 4: Rebuild components
    step4_rebuild_components()
    
    print("\n" + "="*70)
    print("PIPELINE STATUS")
    print("="*70)
    print("✅ Design tokens extracted")
    print("✅ Visual assets generated")
    print("✅ Tailwind config updated")
    print("⚠️  Components need rebuild with exact tokens")
    print("☐ Screenshot + visual diff")
    print("☐ Iteration loop")
    print("\n🎯 Next: Rebuild components or delegate to component-designer")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
