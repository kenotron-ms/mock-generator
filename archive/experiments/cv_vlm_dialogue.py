#!/usr/bin/env python3
"""
CV-VLM Iterative Dialogue System

Implements intelligent component detection through conversation between:
- CV algorithms (edge detection, contour finding)
- VLM (Claude with vision for semantic understanding)

The system iterates until the VLM approves the component structure.
"""

import base64
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import anthropic

from real_component_detector import (
    UIElementDetector, HierarchyBuilder, DetectedRegion,
    BoundingBox, generate_overlay
)


@dataclass
class ComponentSpec:
    """Semantic component specification"""
    region_ids: List[int]  # Which CV regions this component includes
    name: str
    component_type: str  # "section", "component", "element"
    bbox: Tuple[int, int, int, int]  # Computed from merged regions
    repeats: bool
    instance_count: int
    reasoning: str
    elements: List['ComponentSpec'] = None
    
    def to_dict(self):
        result = asdict(self)
        if self.elements:
            result['elements'] = [e.to_dict() for e in self.elements]
        return result


class CVVLMDialogue:
    """Iterative dialogue between CV and VLM for component detection"""
    
    def __init__(self, image_path: str, output_dir: str = None):
        self.image_path = image_path
        self.output_dir = output_dir or str(Path(image_path).parent)
        self.base_name = Path(image_path).stem
        
        # State
        self.version = 0
        self.regions: List[DetectedRegion] = []
        self.components: List[ComponentSpec] = []
        self.conversation: List[Dict[str, Any]] = []
        
        # Claude client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def run_dialogue(self, max_iterations: int = 5) -> List[ComponentSpec]:
        """
        Run the full CV-VLM dialogue until VLM approves or max iterations reached.
        
        Returns:
            Final component specifications
        """
        print("=" * 60)
        print("CV-VLM ITERATIVE DIALOGUE")
        print("=" * 60)
        print()
        
        # Round 1: CV Detection
        print(f"[Round 1] CV Detection")
        print("-" * 60)
        self._cv_detect()
        self._save_version("CV detection - raw regions")
        
        # Iterative refinement
        for iteration in range(max_iterations):
            print()
            print(f"[Round {iteration + 2}] VLM Analysis")
            print("-" * 60)
            
            # VLM analyzes current state
            vlm_response = self._vlm_analyze()
            self.conversation.append(vlm_response)
            
            # Check if VLM approves
            if vlm_response.get("approved", False):
                print("✓ VLM approved the component structure")
                break
            
            # Apply VLM suggestions
            print(f"Applying {len(vlm_response.get('actions', []))} VLM suggestions...")
            self._apply_vlm_suggestions(vlm_response)
            self._save_version(f"After VLM round {iteration + 1}")
        
        print()
        print("=" * 60)
        print("DIALOGUE COMPLETE")
        print("=" * 60)
        print(f"Final version: v{self.version}")
        print(f"Components identified: {len(self.components)}")
        
        return self.components
    
    def _cv_detect(self):
        """Initial CV detection of regions"""
        detector = UIElementDetector(self.image_path)
        self.regions = detector.detect_regions(min_area=500)
        
        # Build hierarchy
        builder = HierarchyBuilder(self.regions)
        roots = builder.build_hierarchy()
        builder.find_repeated_patterns(roots)
        
        # Flatten for easier processing
        self.regions = self._flatten_regions(roots)
        
        # Assign IDs
        for i, region in enumerate(self.regions):
            region.region_id = i
        
        print(f"   Detected {len(self.regions)} regions")
    
    def _vlm_analyze(self) -> Dict[str, Any]:
        """
        Send current state to VLM for analysis.
        
        VLM sees:
        - The original image
        - Current overlay with numbered regions
        - Current component structure (if any)
        
        VLM responds with:
        - Grouping suggestions (merge, split, etc.)
        - Semantic classifications (names, types)
        - Approval or refinement requests
        """
        # Generate annotated image for VLM
        overlay_path = self._get_overlay_path(temp=True)
        self._generate_current_overlay(overlay_path)
        
        # Encode image
        with open(overlay_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")
        
        # Build prompt based on dialogue state
        if self.version == 0:
            prompt = self._get_initial_prompt()
        else:
            prompt = self._get_refinement_prompt()
        
        # Call Claude
        print(f"   Sending to Claude (image + {len(prompt)} chars of prompt)...")
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            # Parse response
            response_text = response.content[0].text
            print(f"   Received {len(response_text)} chars from Claude")
            
            # Extract JSON from response (may be wrapped in markdown)
            json_str = self._extract_json(response_text)
            vlm_response = json.loads(json_str)
            
            # Save full response for debugging
            self._save_conversation(response_text)
            
            return vlm_response
            
        except Exception as e:
            print(f"   Error calling Claude: {e}")
            raise
    
    def _get_initial_prompt(self) -> str:
        """First prompt: analyze raw CV regions"""
        return f"""I'm analyzing a UI mockup to extract component structure.

I've run edge detection and found {len(self.regions)} regions (numbered in the overlay).

**Your task**: Analyze these regions and suggest how to GROUP them into logical components.

**Consider**:
1. **Text consolidation**: Text lines that should merge into paragraphs/text blocks
2. **Background images**: Large images that are backgrounds vs foreground content
3. **Repeated patterns**: Cards, list items that repeat
4. **Containers**: Groups that form logical containers (cards, sections)
5. **Design patterns**: What "looks like" a button, header, card, etc.

**Output JSON** with this structure:
```json
{{
  "observations": [
    "List your observations about the UI structure"
  ],
  "actions": [
    {{
      "type": "merge",
      "region_ids": [5, 6, 7],
      "new_name": "ArticleTitle",
      "reasoning": "These text lines should be one component"
    }},
    {{
      "type": "group",
      "region_ids": [10, 11, 12, 13],
      "new_name": "MeditationCard",
      "component_type": "component",
      "repeats": true,
      "reasoning": "This is a repeating card pattern"
    }}
  ],
  "approved": false
}}
```

Focus on creating meaningful component groups, not just reporting what you see.
"""
    
    def _get_refinement_prompt(self) -> str:
        """Subsequent prompts: refine component structure"""
        return f"""I've applied your previous suggestions.

**Current state**: {len(self.components)} components identified (v{self.version})

**Your task**: Review and either:
- APPROVE the structure (if it looks correct)
- Suggest REFINEMENTS (merge, split, rename, adjust hierarchy)

**Output JSON**:
```json
{{
  "observations": ["What looks good", "What needs fixing"],
  "actions": [
    {{
      "type": "rename",
      "component_name": "Region 5",
      "new_name": "HeaderTitle",
      "reasoning": "More semantic name"
    }},
    {{
      "type": "adjust_hierarchy",
      "parent": "MeditationCard",
      "children": ["Image", "TextContent", "ActionButton"],
      "reasoning": "Correct parent-child relationships"
    }}
  ],
  "approved": true  // or false if more work needed
}}
```

Be critical - if the structure doesn't match standard UI patterns, suggest fixes.
"""
    
    def _apply_vlm_suggestions(self, vlm_response: Dict[str, Any]):
        """Apply VLM's suggestions to the region/component structure"""
        actions = vlm_response.get("actions", [])
        
        for action in actions:
            action_type = action.get("type")
            
            if action_type == "merge":
                self._action_merge(action)
            elif action_type == "group":
                self._action_group(action)
            elif action_type == "rename":
                self._action_rename(action)
            elif action_type == "split":
                self._action_split(action)
            elif action_type == "adjust_hierarchy":
                self._action_adjust_hierarchy(action)
            else:
                print(f"   Warning: Unknown action type '{action_type}'")
    
    def _action_merge(self, action: Dict[str, Any]):
        """Merge multiple regions into one component"""
        region_ids = action.get("region_ids", [])
        new_name = action.get("new_name", "MergedComponent")
        reasoning = action.get("reasoning", "")
        
        # Find regions
        regions_to_merge = [r for r in self.regions if r.region_id in region_ids]
        if not regions_to_merge:
            return
        
        # Compute merged bounding box
        x1 = min(r.bbox.x1 for r in regions_to_merge)
        y1 = min(r.bbox.y1 for r in regions_to_merge)
        x2 = max(r.bbox.x2 for r in regions_to_merge)
        y2 = max(r.bbox.y2 for r in regions_to_merge)
        
        # Create component
        component = ComponentSpec(
            region_ids=region_ids,
            name=new_name,
            component_type="element",
            bbox=(x1, y1, x2, y2),
            repeats=False,
            instance_count=1,
            reasoning=reasoning
        )
        
        self.components.append(component)
        print(f"   ✓ Merged regions {region_ids} → {new_name}")
    
    def _action_group(self, action: Dict[str, Any]):
        """Group regions into a semantic component"""
        region_ids = action.get("region_ids", [])
        new_name = action.get("new_name", "Component")
        component_type = action.get("component_type", "component")
        repeats = action.get("repeats", False)
        reasoning = action.get("reasoning", "")
        
        # Similar to merge, but marks as reusable component
        regions_to_group = [r for r in self.regions if r.region_id in region_ids]
        if not regions_to_group:
            return
        
        # Compute bounding box
        x1 = min(r.bbox.x1 for r in regions_to_group)
        y1 = min(r.bbox.y1 for r in regions_to_group)
        x2 = max(r.bbox.x2 for r in regions_to_group)
        y2 = max(r.bbox.y2 for r in regions_to_group)
        
        # Count instances if it repeats
        instance_count = 1
        if repeats:
            # TODO: Find similar regions
            instance_count = len([r for r in self.regions if r.is_repeated])
        
        component = ComponentSpec(
            region_ids=region_ids,
            name=new_name,
            component_type=component_type,
            bbox=(x1, y1, x2, y2),
            repeats=repeats,
            instance_count=instance_count,
            reasoning=reasoning
        )
        
        self.components.append(component)
        print(f"   ✓ Grouped regions {region_ids} → {new_name} (repeats: {repeats})")
    
    def _action_rename(self, action: Dict[str, Any]):
        """Rename a component"""
        old_name = action.get("component_name")
        new_name = action.get("new_name")
        
        for component in self.components:
            if component.name == old_name:
                component.name = new_name
                print(f"   ✓ Renamed '{old_name}' → '{new_name}'")
                break
    
    def _action_split(self, action: Dict[str, Any]):
        """Split a component into multiple components"""
        # TODO: Implement if needed
        print(f"   ⚠ Split action not yet implemented")
    
    def _action_adjust_hierarchy(self, action: Dict[str, Any]):
        """Adjust parent-child relationships"""
        # TODO: Implement hierarchy adjustment
        print(f"   ⚠ Hierarchy adjustment not yet implemented")
    
    def _save_version(self, description: str):
        """Save current state as a versioned overlay"""
        self.version += 1
        
        # Save overlay image
        overlay_path = self._get_overlay_path()
        self._generate_current_overlay(overlay_path)
        
        # Save JSON spec
        spec_path = self._get_spec_path()
        spec = {
            "version": self.version,
            "description": description,
            "image": self.image_path,
            "regions_count": len(self.regions),
            "components_count": len(self.components),
            "components": [c.to_dict() for c in self.components]
        }
        
        with open(spec_path, 'w') as f:
            json.dump(spec, f, indent=2)
        
        print(f"   Saved v{self.version}: {overlay_path}")
    
    def _generate_current_overlay(self, output_path: str):
        """Generate overlay showing current regions/components"""
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.open(self.image_path)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 10)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # If we have components, draw those; otherwise draw raw regions
        if self.components:
            # Draw components
            colors = ["#2196F3", "#F44336", "#4CAF50", "#FFC107", "#9C27B0"]
            for i, component in enumerate(self.components):
                color = colors[i % len(colors)]
                x1, y1, x2, y2 = component.bbox
                
                # Draw box
                for j in range(3):
                    draw.rectangle([(x1+j, y1+j), (x2-j, y2-j)], outline=color, width=1)
                
                # Label
                label = component.name
                if component.repeats:
                    label += f" (×{component.instance_count})"
                
                draw.rectangle([(x1, y1-20), (x1+200, y1)], fill=color)
                draw.text((x1+4, y1-18), label, fill="white", font=font)
        else:
            # Draw raw regions with IDs
            for region in self.regions:
                x1, y1, x2, y2 = region.bbox.x1, region.bbox.y1, region.bbox.x2, region.bbox.y2
                
                # Color by depth
                colors = ["#2196F3", "#F44336", "#4CAF50", "#FFC107"]
                color = colors[region.depth % len(colors)]
                
                draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)
                
                # Region ID
                label = f"#{region.region_id}"
                draw.rectangle([(x1, y1), (x1+30, y1+16)], fill=color)
                draw.text((x1+2, y1), label, fill="white", font=font_small)
        
        img.save(output_path, quality=95)
    
    def _get_overlay_path(self, temp: bool = False) -> str:
        """Get path for overlay image"""
        if temp:
            return f"{self.output_dir}/{self.base_name}-TEMP.png"
        return f"{self.output_dir}/{self.base_name}-ANNOTATED-v{self.version}.png"
    
    def _get_spec_path(self) -> str:
        """Get path for JSON spec"""
        return f"{self.output_dir}/{self.base_name}-spec-v{self.version}.json"
    
    def _save_conversation(self, response_text: str):
        """Save VLM response for debugging"""
        conv_path = f"{self.output_dir}/{self.base_name}-conversation-v{self.version}.txt"
        with open(conv_path, 'w') as f:
            f.write(f"=== VLM Response v{self.version} ===\n\n")
            f.write(response_text)
        print(f"   Saved conversation: {conv_path}")
    
    def _flatten_regions(self, roots: List[DetectedRegion]) -> List[DetectedRegion]:
        """Flatten tree to list"""
        result = []
        def traverse(region):
            result.append(region)
            for child in region.children:
                traverse(child)
        for root in roots:
            traverse(root)
        return result
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown-wrapped response"""
        # Look for ```json ... ```
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        
        # Look for { ... }
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return text[start:end]
        
        return text


def main():
    """Run the dialogue on a mockup"""
    image_path = "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1.png"
    
    dialogue = CVVLMDialogue(image_path)
    components = dialogue.run_dialogue(max_iterations=3)
    
    print()
    print("FINAL COMPONENTS:")
    for component in components:
        print(f"  • {component.name} ({component.component_type})")
        if component.repeats:
            print(f"    ↳ Repeats {component.instance_count} times")
        print(f"    ↳ {component.reasoning}")


if __name__ == "__main__":
    main()
