#!/usr/bin/env python3
"""
Example: Generate UI mockups using Nano Banana Pro (Gemini 3 Pro Image)

This script demonstrates how to use the amplifier-module-image-generation
library to generate high-quality UI mockups with proper text rendering.
"""

import asyncio
from pathlib import Path
from amplifier_module_image_generation import ImageGenerator


async def generate_single_mockup():
    """Generate a single UI mockup with Nano Banana Pro."""
    
    generator = ImageGenerator()
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("Generating mobile dashboard mockup...")
    
    result = await generator.generate(
        prompt="""
        Create a modern fitness tracking mobile app dashboard in dark mode.
        
        Layout (portrait 9:16):
        - Top: User profile avatar and name
        - Below: Today's stats in 3 cards (Steps, Calories, Distance)
        - Middle: Weekly activity graph with clear labels
        - Bottom: Quick action buttons for workouts
        
        Design: Modern, clean, professional with good contrast
        Colors: Dark background with accent colors for stats
        Text: Clear, legible labels and numbers
        """,
        output_path=output_dir / "fitness-dashboard.png",
        preferred_api="nano-banana-pro",
        params={
            "aspect_ratio": "9:16",  # Mobile portrait
            "resolution": "2K",       # High quality
            "use_thinking": True,     # Enable reasoning for better UI understanding
            "use_search": False,      # No need for web grounding
        }
    )
    
    if result.success:
        print(f"✓ Generated with {result.api_used}")
        print(f"  Cost: ${result.cost:.4f}")
        print(f"  Saved to: {result.local_path}")
        print(f"  Dimensions: {result.width}x{result.height}")
    else:
        print(f"✗ Generation failed: {result.error}")


async def generate_with_iterations():
    """Generate a mockup and iterate on it with conversational edits."""
    
    generator = ImageGenerator()
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("\n=== Multi-turn Conversational Generation ===\n")
    
    # Create a conversation session
    conversation_id = generator.create_conversation(
        preferred_api="nano-banana-pro",
        use_thinking=True,
        use_search=False
    )
    
    # Initial generation
    print("Step 1: Initial dashboard...")
    result1 = await generator.generate(
        prompt="Create a simple e-commerce product card with image, title, price, and buy button",
        output_path=output_dir / "product-card-v1.png",
        preferred_api="nano-banana-pro",
        params={
            "conversation_id": conversation_id,
            "aspect_ratio": "1:1",
            "resolution": "2K",
        }
    )
    
    if result1.success:
        print(f"✓ V1 saved to: {result1.local_path} (${result1.cost:.4f})")
    
    # Iterate: Add more details
    print("\nStep 2: Adding rating stars and reviews count...")
    result2 = await generator.generate(
        prompt="Add 5-star rating display and '(247 reviews)' below the title",
        output_path=output_dir / "product-card-v2.png",
        preferred_api="nano-banana-pro",
        params={
            "conversation_id": conversation_id,
            "aspect_ratio": "1:1",
            "resolution": "2K",
        }
    )
    
    if result2.success:
        print(f"✓ V2 saved to: {result2.local_path} (${result2.cost:.4f})")
    
    # Iterate: Change style
    print("\nStep 3: Changing to premium style...")
    result3 = await generator.generate(
        prompt="Make it look more premium - add subtle shadows, better spacing, and a gradient background",
        output_path=output_dir / "product-card-v3.png",
        preferred_api="nano-banana-pro",
        params={
            "conversation_id": conversation_id,
            "aspect_ratio": "1:1",
            "resolution": "2K",
        }
    )
    
    if result3.success:
        print(f"✓ V3 saved to: {result3.local_path} (${result3.cost:.4f})")
        print(f"\nTotal conversation cost: ${result1.cost + result2.cost + result3.cost:.4f}")


async def main():
    """Run examples."""
    
    print("=" * 60)
    print("Nano Banana Pro UI Mockup Generator")
    print("=" * 60)
    
    # Example 1: Single generation
    await generate_single_mockup()
    
    # Example 2: Iterative refinement
    await generate_with_iterations()
    
    print("\n" + "=" * 60)
    print("✓ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
