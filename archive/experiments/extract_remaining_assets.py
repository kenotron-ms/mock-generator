#!/usr/bin/env python3
"""
Continue extracting the remaining visual assets (thumbnails 2-5 and icons).
"""

import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator


async def extract_remaining_thumbnails():
    """Generate the remaining article thumbnails."""
    
    generator = ImageGenerator()
    original = Path("mockups/blog-meditations-list-v1.png")
    
    # Thumbnails 2-5 (thumb-1 already exists)
    articles = [
        {
            "title": "Stillness in Motion", 
            "description": "Abstract flowing forms, meditative",
            "filename": "thumb-2.png"
        },
        {
            "title": "Breathing Through Change",
            "description": "Nature or breath-like abstract",
            "filename": "thumb-3.png"
        },
        {
            "title": "The Wisdom of Silence",
            "description": "Minimalist, quiet, contemplative",
            "filename": "thumb-4.png"
        },
        {
            "title": "Cultivating Compassion",
            "description": "Warm, gentle imagery",
            "filename": "thumb-5.png"
        },
    ]
    
    print(f"🖼️  Extracting {len(articles)} remaining thumbnails...")
    
    for i, article in enumerate(articles, 2):  # Start at 2 since thumb-1 exists
        output_path = Path(f"demo/public/{article['filename']}")
        
        if output_path.exists():
            print(f"   [{i}/5] {article['filename']} - Already exists, skipping")
            continue
        
        print(f"   [{i}/5] Generating {article['filename']}...")
        
        result = await generator.generate(
            prompt=f"""
            Meditation blog thumbnail for "{article['title']}" article.
            
            Style: Match the warm, calming aesthetic of this blog.
            Colors: Harmonize with cream (#F3EFE7) and terracotta (#C66E5B).
            Theme: {article['description']}
            Format: Square, simple, elegant, meditative.
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
            print(f"      ✅ ${result.cost:.4f}")
    
    print("\n✅ All thumbnails extracted!")


async def main():
    await extract_remaining_thumbnails()


if __name__ == "__main__":
    asyncio.run(main())
