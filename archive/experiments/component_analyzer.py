"""
Component Analyzer - Extract component hierarchy from UI mockups
"""
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json


@dataclass
class ComponentElement:
    """A primitive element within a component"""
    name: str
    element_type: str  # Image, Text, Button, View, etc.
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    reasoning: str


@dataclass
class Component:
    """A UI component (can be reusable)"""
    name: str
    component_type: str  # section, component, element
    bbox: Tuple[int, int, int, int]
    repeats: bool
    instance_count: int
    elements: List[ComponentElement]
    reasoning: str
    color: str  # for visualization


class ComponentOverlay:
    """Draws component boundaries and labels on mockup images"""
    
    # Color scheme
    COLORS = {
        "section": "#2196F3",      # Blue
        "component": "#F44336",    # Red
        "element": "#FFC107",      # Yellow
        "repeated": "#4CAF50",     # Green
    }
    
    def __init__(self, image_path: str):
        self.image = Image.open(image_path).convert("RGB")
        self.draw = ImageDraw.Draw(self.image)
        
        # Try to load a font, fallback to default
        try:
            self.font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
            self.font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        except:
            self.font = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    def draw_component(self, component: Component, draw_elements: bool = True):
        """Draw a component boundary and its elements"""
        x1, y1, x2, y2 = component.bbox
        color = self.COLORS.get(component.component_type, "#FFFFFF")
        
        # Draw main component box
        thickness = 4 if component.component_type == "section" else 3
        for i in range(thickness):
            self.draw.rectangle(
                [(x1+i, y1+i), (x2-i, y2-i)],
                outline=color,
                width=1
            )
        
        # Draw label background
        label = component.name
        if component.repeats:
            label += f" (×{component.instance_count})"
        
        # Get text size
        bbox = self.draw.textbbox((0, 0), label, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw label background (semi-transparent effect with solid color)
        label_bg = [(x1, y1 - text_height - 8), (x1 + text_width + 12, y1)]
        self.draw.rectangle(label_bg, fill=color)
        
        # Draw label text
        self.draw.text((x1 + 6, y1 - text_height - 4), label, fill="white", font=self.font)
        
        # Draw child elements
        if draw_elements:
            for element in component.elements:
                self.draw_element(element)
    
    def draw_element(self, element: ComponentElement):
        """Draw an element boundary with thin lines"""
        x1, y1, x2, y2 = element.bbox
        color = self.COLORS["element"]
        
        # Thin dashed-style box
        self.draw.rectangle(
            [(x1, y1), (x2, y2)],
            outline=color,
            width=2
        )
        
        # Small label
        label = f"{element.name} ({element.element_type})"
        bbox = self.draw.textbbox((0, 0), label, font=self.font_small)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Only draw label if element is big enough
        if (x2 - x1) > text_width + 8 and (y2 - y1) > text_height + 8:
            self.draw.rectangle(
                [(x1, y1), (x1 + text_width + 8, y1 + text_height + 4)],
                fill=color
            )
            self.draw.text((x1 + 4, y1 + 2), label, fill="black", font=self.font_small)
    
    def draw_legend(self):
        """Draw a legend explaining the color scheme"""
        legend_items = [
            ("Sections", self.COLORS["section"]),
            ("Reusable Components", self.COLORS["component"]),
            ("Elements", self.COLORS["element"]),
        ]
        
        x, y = 20, self.image.height - 100
        
        for label, color in legend_items:
            # Draw color box
            self.draw.rectangle([(x, y), (x + 20, y + 20)], fill=color, outline="white", width=1)
            # Draw label
            self.draw.text((x + 30, y + 2), label, fill="white", font=self.font)
            y += 30
    
    def save(self, output_path: str):
        """Save the annotated image"""
        self.image.save(output_path, quality=95)
        print(f"Saved annotated image to: {output_path}")


def analyze_mockup(image_path: str, output_path: str, components: List[Component]):
    """
    Analyze a mockup and generate an annotated overlay.
    
    Args:
        image_path: Path to the mockup image
        output_path: Where to save the annotated image
        components: List of identified components
    """
    overlay = ComponentOverlay(image_path)
    
    # Draw all components
    for component in components:
        overlay.draw_component(component)
    
    # Draw legend
    overlay.draw_legend()
    
    # Save
    overlay.save(output_path)


def export_component_spec(components: List[Component], output_path: str):
    """Export component specification as JSON"""
    spec = {
        "components": [
            {
                "name": c.name,
                "type": c.component_type,
                "bbox": c.bbox,
                "repeats": c.repeats,
                "instance_count": c.instance_count,
                "reasoning": c.reasoning,
                "elements": [
                    {
                        "name": e.name,
                        "type": e.element_type,
                        "bbox": e.bbox,
                        "reasoning": e.reasoning
                    }
                    for e in c.elements
                ]
            }
            for c in components
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"Saved component spec to: {output_path}")


if __name__ == "__main__":
    # Example usage
    print("Component Analyzer - Ready to process mockups")
