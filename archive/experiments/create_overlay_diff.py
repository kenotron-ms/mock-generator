#!/usr/bin/env python3
"""
Create a visual overlay comparison so we can SEE the differences directly.

Method:
1. Align both images to same size
2. Create side-by-side comparison
3. Create overlay (50% opacity blend)
4. Create pixel difference heatmap
5. Then ask Nano Banana Pro to analyze THESE diff images
"""

from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np


def create_side_by_side(original_path, current_path, output_path):
    """Create side-by-side comparison."""
    original = Image.open(original_path)
    current = Image.open(current_path)
    
    # Resize current to match original dimensions if needed
    if original.size != current.size:
        print(f"   Resizing current from {current.size} to {original.size}")
        current = current.resize(original.size, Image.Resampling.LANCZOS)
    
    # Create side-by-side canvas
    width, height = original.size
    canvas = Image.new('RGB', (width * 2 + 20, height), 'white')
    
    # Paste images
    canvas.paste(original, (0, 0))
    canvas.paste(current, (width + 20, 0))
    
    # Add labels
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 10), "ORIGINAL", fill='red', font=font)
    draw.text((width + 30, 10), "CURRENT", fill='blue', font=font)
    
    canvas.save(output_path)
    print(f"✓ Side-by-side: {output_path}")
    return output_path


def create_overlay(original_path, current_path, output_path):
    """Create 50/50 overlay blend to see differences."""
    original = Image.open(original_path).convert('RGBA')
    current = Image.open(current_path).convert('RGBA')
    
    # Resize if needed
    if original.size != current.size:
        current = current.resize(original.size, Image.Resampling.LANCZOS)
    
    # Blend 50/50
    blended = Image.blend(original, current, alpha=0.5)
    blended.save(output_path)
    print(f"✓ Overlay blend: {output_path}")
    return output_path


def create_difference_heatmap(original_path, current_path, output_path):
    """Create heatmap showing pixel differences."""
    original = Image.open(original_path).convert('RGB')
    current = Image.open(current_path).convert('RGB')
    
    # Resize if needed
    if original.size != current.size:
        current = current.resize(original.size, Image.Resampling.LANCZOS)
    
    # Calculate absolute difference
    diff = ImageChops.difference(original, current)
    
    # Convert to numpy for heatmap generation
    diff_array = np.array(diff)
    
    # Calculate magnitude of difference (RGB distance)
    magnitude = np.sqrt(np.sum(diff_array**2, axis=2))
    
    # Normalize to 0-255
    if magnitude.max() > 0:
        magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)
    else:
        magnitude = magnitude.astype(np.uint8)
    
    # Create heatmap (green=match, yellow=close, red=different)
    heatmap = Image.new('RGB', original.size)
    pixels = heatmap.load()
    
    for y in range(original.size[1]):
        for x in range(original.size[0]):
            diff_value = magnitude[y, x]
            if diff_value < 10:  # Very close match
                color = (0, 255, 0)  # Green
            elif diff_value < 50:  # Close
                color = (255, 255, 0)  # Yellow
            elif diff_value < 100:  # Noticeable
                color = (255, 165, 0)  # Orange
            else:  # Significant difference
                color = (255, 0, 0)  # Red
            
            pixels[x, y] = color
    
    heatmap.save(output_path)
    print(f"✓ Difference heatmap: {output_path}")
    
    # Calculate stats
    total_pixels = magnitude.size
    matched_pixels = np.sum(magnitude < 10)
    close_pixels = np.sum((magnitude >= 10) & (magnitude < 50))
    different_pixels = np.sum(magnitude >= 50)
    
    match_percentage = (matched_pixels / total_pixels) * 100
    
    print(f"\n   Pixel Match Analysis:")
    print(f"   - Exact match (<10 diff):  {match_percentage:.1f}%")
    print(f"   - Close match (<50 diff):  {(close_pixels/total_pixels)*100:.1f}%")
    print(f"   - Different (>=50 diff):   {(different_pixels/total_pixels)*100:.1f}%")
    
    return output_path


def main():
    print("="*70)
    print("VISUAL DIFF TOOL - Creating Comparison Images")
    print("="*70)
    print()
    
    original = Path("mockups/blog-meditations-list-v1.png")
    current = Path("output/current-app-screenshot.png")
    
    if not original.exists():
        print(f"❌ Original not found: {original}")
        return
    
    if not current.exists():
        print(f"❌ Screenshot not found: {current}")
        print("   Run: cd demo && node capture.js")
        return
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📸 Original: {original}")
    print(f"📸 Current:  {current}")
    print()
    
    # Create comparison images
    print("🎨 Creating comparison visualizations...")
    print()
    
    side_by_side = create_side_by_side(
        original, 
        current,
        output_dir / "comparison-side-by-side.png"
    )
    
    overlay = create_overlay(
        original,
        current, 
        output_dir / "comparison-overlay.png"
    )
    
    heatmap = create_difference_heatmap(
        original,
        current,
        output_dir / "comparison-heatmap.png"
    )
    
    print()
    print("="*70)
    print("✅ COMPARISON IMAGES CREATED")
    print("="*70)
    print()
    print("Visual diff tools generated:")
    print(f"  1. Side-by-side:  {side_by_side}")
    print(f"  2. Overlay blend: {overlay}")
    print(f"  3. Heatmap:       {heatmap}")
    print()
    print("Next step: Ask Nano Banana Pro to analyze the heatmap and identify")
    print("          specific differences to fix!")
    print()
    print("="*70)


if __name__ == "__main__":
    main()
