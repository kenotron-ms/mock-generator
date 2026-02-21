#!/usr/bin/env python3
"""
Extract visual assets from the original mockup by having Nano Banana Pro
analyze and regenerate each visual element (thumbnails, hero image, etc.).

This ensures the rebuilt app uses assets that match the original aesthetic,
not random placeholder images.
"""

import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator


async def extract_hero_background():
    """Generate the hero card background image based on the original."""
    
    generator = ImageGenerator()
    original = Path("mockups/blog-meditations-list-v1.png")
    output_path = Path("demo/public/hero-bg.png")
    
    print("🎨 Extracting hero card background image...")
    
    result = await generator.generate(
        prompt="""
        Looking at this meditation blog mockup, I can see the hero card at the top has
        a distinctive abstract geometric background image with warm colors (oranges, purples, yellows).
        
        Recreate JUST that background image/pattern that fills the hero card.
        
        Visual characteristics to match:
        - Abstract geometric shapes and patterns
        - Warm color palette (terracotta orange #C66E5B, purples, yellows, warm tones)
        - Modern, artistic, slightly abstract aesthetic
        - Smooth gradients between shapes
        - Calming, meditative feel (this is for a meditation blog)
        
        Output: Just the background pattern/image itself (no text, no overlays).
        This will be used as a background-image in CSS.
        """,
        output_path=output_path,
        preferred_api="nano-banana-pro",
        params={
            "reference_image": original,
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "use_thinking": True,
        }
    )
    
    if result.success:
        print(f"   ✅ Hero background: {result.local_path} (${result.cost:.4f})")
        return str(result.local_path)
    else:
        print(f"   ❌ Failed: {result.error}")
        return None


async def extract_article_thumbnails():
    """Generate article thumbnail images based on the original."""
    
    generator = ImageGenerator()
    original = Path("mockups/blog-meditations-list-v1.png")
    
    thumbnails = []
    
    # Define the articles based on what's visible in the mockup
    articles = [
        {
            "title": "The Practice of Presence",
            "description": "Nature scene, calming, possibly trees or landscape",
            "filename": "thumb-1.png"
        },
        {
            "title": "Stillness in Motion", 
            "description": "Abstract or meditative imagery, flowing forms",
            "filename": "thumb-2.png"
        },
        {
            "title": "Breathing Through Change",
            "description": "Nature or abstract, peaceful aesthetic",
            "filename": "thumb-3.png"
        },
        {
            "title": "The Wisdom of Silence",
            "description": "Minimalist, quiet, contemplative imagery",
            "filename": "thumb-4.png"
        },
        {
            "title": "Cultivating Compassion",
            "description": "Warm, gentle imagery",
            "filename": "thumb-5.png"
        },
    ]
    
    print(f"\n🖼️  Extracting {len(articles)} article thumbnails...")
    
    for i, article in enumerate(articles, 1):
        output_path = Path(f"demo/public/{article['filename']}")
        
        print(f"\n   [{i}/{len(articles)}] {article['title']}...")
        
        result = await generator.generate(
            prompt=f"""
            Looking at this meditation blog mockup, there are article list items with small 
            square thumbnail images on the left side.
            
            Generate a thumbnail image for an article titled "{article['title']}" that would 
            fit the meditation blog aesthetic seen in this mockup.
            
            Visual characteristics to match:
            - Square format (1:1 aspect ratio)
            - Same visual style and color palette as the mockup
            - Warm, calming, meditative aesthetic
            - Could be: nature photography, abstract patterns, or minimalist compositions
            - Colors should harmonize with the cream background (#F3EFE7) and terracotta accent (#C66E5B)
            - {article['description']}
            
            Keep it simple, elegant, and on-brand with the meditation theme.
            """,
            output_path=output_path,
            preferred_api="nano-banana-pro",
            params={
                "reference_image": original,
                "aspect_ratio": "1:1",
                "resolution": "1K",  # Small thumbnails
                "use_thinking": True,
            }
        )
        
        if result.success:
            print(f"      ✅ {result.local_path} (${result.cost:.4f})")
            thumbnails.append(str(result.local_path))
        else:
            print(f"      ❌ Failed: {result.error}")
    
    return thumbnails


async def extract_icons():
    """Generate navigation icons based on the original."""
    
    generator = ImageGenerator()
    original = Path("mockups/blog-meditations-list-v1.png")
    
    icons = []
    
    nav_items = [
        {"name": "explore", "description": "compass or exploration icon"},
        {"name": "meditations", "description": "meditation/mindfulness icon"},
        {"name": "voice", "description": "microphone or voice icon"},
    ]
    
    print(f"\n🎯 Extracting {len(nav_items)} navigation icons...")
    
    for i, item in enumerate(nav_items, 1):
        output_path = Path(f"demo/public/icon-{item['name']}.png")
        
        print(f"\n   [{i}/{len(nav_items)}] {item['name'].title()} icon...")
        
        result = await generator.generate(
            prompt=f"""
            Looking at the bottom navigation bar in this meditation blog mockup, 
            there are simple, minimal icons for navigation.
            
            Generate a clean, minimal icon for "{item['name']}" - a {item['description']}.
            
            Visual characteristics:
            - Simple line icon or minimal solid icon
            - Size: 24x24 pixels
            - Style: Matches the minimal, meditative aesthetic of the mockup
            - Color: Dark gray (#2A2A2A) for inactive state
            - Clean, modern, readable at small size
            
            Just the icon on transparent background.
            """,
            output_path=output_path,
            preferred_api="nano-banana-pro",
            params={
                "reference_image": original,
                "aspect_ratio": "1:1",
                "resolution": "1K",
                "use_thinking": True,
            }
        )
        
        if result.success:
            print(f"      ✅ {result.local_path} (${result.cost:.4f})")
            icons.append(str(result.local_path))
        else:
            print(f"      ❌ Failed: {result.error}")
    
    return icons


async def main():
    """Extract all visual assets from the original mockup."""
    
    print("=" * 70)
    print("Visual Asset Extraction - Nano Banana Pro")
    print("=" * 70)
    print()
    print("Purpose: Generate matching visual assets for pixel-perfect replication")
    print("Method: Analyze original mockup + regenerate each visual element")
    print()
    
    # Extract all assets
    hero_bg = await extract_hero_background()
    thumbnails = await extract_article_thumbnails()
    icons = await extract_icons()
    
    # Summary
    print("\n" + "=" * 70)
    print("ASSET EXTRACTION COMPLETE")
    print("=" * 70)
    
    total_cost = 0.0
    assets_created = 0
    
    if hero_bg:
        assets_created += 1
        total_cost += 0.05  # 2K image
    
    assets_created += len(thumbnails)
    total_cost += len(thumbnails) * 0.035  # 1K images
    
    assets_created += len(icons)
    total_cost += len(icons) * 0.035  # 1K images
    
    print(f"\n📊 Summary:")
    print(f"   Assets created: {assets_created}")
    print(f"   Estimated cost: ${total_cost:.2f}")
    print(f"\n   Hero background: {1 if hero_bg else 0}")
    print(f"   Thumbnails: {len(thumbnails)}")
    print(f"   Icons: {len(icons)}")
    
    print("\n🎯 All assets saved to demo/public/")
    print("   Ready to rebuild the app with exact visual assets!")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
