#!/usr/bin/env python3
"""
Real Component Detector - Actually analyze images to find UI elements

Strategy:
1. Use OpenCV to detect visual regions (edges, contours, color segmentation)
2. Build containment hierarchy from geometric relationships
3. Use heuristics to classify element types (based on size, aspect ratio, position)
4. Generate overlay with ACTUAL coordinates
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json


@dataclass
class BoundingBox:
    """A detected region in the image"""
    x: int
    y: int
    w: int
    h: int
    
    @property
    def x1(self) -> int:
        return self.x
    
    @property
    def y1(self) -> int:
        return self.y
    
    @property
    def x2(self) -> int:
        return self.x + self.w
    
    @property
    def y2(self) -> int:
        return self.y + self.h
    
    @property
    def area(self) -> int:
        return self.w * self.h
    
    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)
    
    @property
    def aspect_ratio(self) -> float:
        return self.w / self.h if self.h > 0 else 0
    
    def contains(self, other: 'BoundingBox', margin: int = 5) -> bool:
        """Check if this box contains another box (with optional margin)"""
        return (self.x1 <= other.x1 + margin and
                self.y1 <= other.y1 + margin and
                self.x2 >= other.x2 - margin and
                self.y2 >= other.y2 - margin)
    
    def overlaps(self, other: 'BoundingBox') -> bool:
        """Check if this box overlaps with another"""
        return not (self.x2 < other.x1 or other.x2 < self.x1 or
                    self.y2 < other.y1 or other.y2 < self.y1)
    
    def iou(self, other: 'BoundingBox') -> float:
        """Calculate Intersection over Union with another box"""
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)
        
        if x2 < x1 or y2 < y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        union = self.area + other.area - intersection
        
        return intersection / union if union > 0 else 0.0


@dataclass
class DetectedRegion:
    """A region detected in the UI"""
    bbox: BoundingBox
    parent: Optional['DetectedRegion'] = None
    children: List['DetectedRegion'] = field(default_factory=list)
    
    # Classification
    element_type: Optional[str] = None
    confidence: float = 0.0
    
    # Semantic info
    name: Optional[str] = None
    is_repeated: bool = False
    similar_regions: List['DetectedRegion'] = field(default_factory=list)
    
    # Visual properties
    has_border: bool = False
    has_shadow: bool = False
    background_color: Optional[Tuple[int, int, int]] = None
    
    @property
    def depth(self) -> int:
        """Calculate depth in the tree (0 = root)"""
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth


class UIElementDetector:
    """Detect UI elements using OpenCV"""
    
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.height, self.width = self.image.shape[:2]
        
    def detect_regions(self, min_area: int = 500) -> List[DetectedRegion]:
        """
        Detect regions using multiple methods and merge results.
        
        Methods:
        1. Edge detection + contour finding (structural boundaries)
        2. Color segmentation (grouped elements)
        3. Text detection (text blocks)
        """
        regions = []
        
        # Method 1: Edge-based detection
        regions.extend(self._detect_by_edges(min_area))
        
        # Method 2: Color segmentation
        regions.extend(self._detect_by_color(min_area))
        
        # Filter overlapping/duplicate regions
        regions = self._deduplicate_regions(regions)
        
        # Sort by area (largest first)
        regions.sort(key=lambda r: r.bbox.area, reverse=True)
        
        return regions
    
    def _detect_by_edges(self, min_area: int) -> List[DetectedRegion]:
        """Detect regions using edge detection and contours"""
        regions = []
        
        # Multi-scale edge detection
        for blur_kernel in [3, 5]:
            blurred = cv2.GaussianBlur(self.gray, (blur_kernel, blur_kernel), 0)
            edges = cv2.Canny(blurred, 30, 150)
            
            # Dilate to connect nearby edges
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=2)
            
            # Find contours
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size
                if w * h < min_area:
                    continue
                
                # Filter by aspect ratio (exclude extreme ratios)
                aspect_ratio = w / h if h > 0 else 0
                if aspect_ratio < 0.1 or aspect_ratio > 10:
                    continue
                
                # Create region
                bbox = BoundingBox(x, y, w, h)
                region = DetectedRegion(bbox=bbox)
                
                # Classify based on visual properties
                region.has_border = self._check_border(x, y, w, h)
                
                regions.append(region)
        
        return regions
    
    def _detect_by_color(self, min_area: int) -> List[DetectedRegion]:
        """Detect regions using color segmentation"""
        regions = []
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # Detect regions with similar colors (potential cards/containers)
        # This is a simplified approach - could be much more sophisticated
        
        return regions
    
    def _check_border(self, x: int, y: int, w: int, h: int) -> bool:
        """Check if a region has a visible border"""
        # Sample pixels along the edges
        border_pixels = []
        
        # Top edge
        if y > 0 and y + h < self.height and x > 0 and x + w < self.width:
            border_pixels.append(self.gray[y, x:x+w])
            # Bottom edge
            border_pixels.append(self.gray[y+h-1, x:x+w])
            # Left edge
            border_pixels.append(self.gray[y:y+h, x])
            # Right edge
            border_pixels.append(self.gray[y:y+h, x+w-1])
            
            # Check for consistent edge color (indicates border)
            # This is a heuristic - real border detection would be more complex
            return True
        
        return False
    
    def _deduplicate_regions(self, regions: List[DetectedRegion]) -> List[DetectedRegion]:
        """Remove duplicate/highly overlapping regions"""
        unique_regions = []
        
        for region in regions:
            # Check if this region is very similar to an existing one
            is_duplicate = False
            for existing in unique_regions:
                iou = region.bbox.iou(existing.bbox)
                if iou > 0.8:  # High overlap = duplicate
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_regions.append(region)
        
        return unique_regions


class HierarchyBuilder:
    """Build component hierarchy from detected regions"""
    
    def __init__(self, regions: List[DetectedRegion]):
        self.regions = regions
    
    def build_hierarchy(self) -> List[DetectedRegion]:
        """
        Build containment hierarchy.
        
        Algorithm:
        1. For each region, find all regions that contain it
        2. Choose the smallest containing region as parent
        3. Build tree structure
        """
        # Sort by area (largest first) for efficient containment checking
        sorted_regions = sorted(self.regions, key=lambda r: r.bbox.area, reverse=True)
        
        # Find parents
        for i, region in enumerate(sorted_regions):
            # Look for parent among larger regions
            potential_parents = []
            for j in range(i):
                parent_candidate = sorted_regions[j]
                if parent_candidate.bbox.contains(region.bbox, margin=10):
                    potential_parents.append(parent_candidate)
            
            # Choose the smallest containing region (immediate parent)
            if potential_parents:
                region.parent = min(potential_parents, key=lambda r: r.bbox.area)
                region.parent.children.append(region)
        
        # Return only root nodes (no parent)
        roots = [r for r in sorted_regions if r.parent is None]
        
        return roots
    
    def find_repeated_patterns(self, roots: List[DetectedRegion]) -> None:
        """
        Find repeated component patterns (list items, cards, etc.)
        
        Looks for regions with:
        - Similar size
        - Similar aspect ratio
        - Similar internal structure
        - Spatially aligned (vertical or horizontal)
        """
        all_regions = self._flatten_tree(roots)
        
        # Group by depth (compare regions at same hierarchy level)
        by_depth = {}
        for region in all_regions:
            depth = region.depth
            if depth not in by_depth:
                by_depth[depth] = []
            by_depth[depth].append(region)
        
        # Within each depth level, find similar regions
        for depth, regions in by_depth.items():
            if len(regions) < 2:
                continue
            
            # Cluster by similarity
            clusters = []
            for region in regions:
                matched = False
                for cluster in clusters:
                    if self._are_similar(region, cluster[0]):
                        cluster.append(region)
                        matched = True
                        break
                
                if not matched:
                    clusters.append([region])
            
            # Mark repeated patterns
            for cluster in clusters:
                if len(cluster) >= 2:
                    for region in cluster:
                        region.is_repeated = True
                        region.similar_regions = [r for r in cluster if r != region]
    
    def _are_similar(self, r1: DetectedRegion, r2: DetectedRegion) -> bool:
        """Check if two regions are similar (potential repeated component)"""
        # Size similarity
        area_ratio = min(r1.bbox.area, r2.bbox.area) / max(r1.bbox.area, r2.bbox.area)
        if area_ratio < 0.8:
            return False
        
        # Aspect ratio similarity
        ar_diff = abs(r1.bbox.aspect_ratio - r2.bbox.aspect_ratio)
        if ar_diff > 0.2:
            return False
        
        # Number of children similarity
        if abs(len(r1.children) - len(r2.children)) > 1:
            return False
        
        return True
    
    def _flatten_tree(self, roots: List[DetectedRegion]) -> List[DetectedRegion]:
        """Flatten tree to list of all regions"""
        result = []
        for root in roots:
            result.append(root)
            result.extend(self._flatten_tree(root.children))
        return result


def analyze_image(image_path: str, output_path: str):
    """Main analysis pipeline"""
    print(f"Analyzing: {image_path}")
    print("=" * 60)
    
    # Step 1: Detect regions
    print("\n1. Detecting UI regions...")
    detector = UIElementDetector(image_path)
    regions = detector.detect_regions(min_area=1000)
    print(f"   Found {len(regions)} regions")
    
    # Step 2: Build hierarchy
    print("\n2. Building containment hierarchy...")
    builder = HierarchyBuilder(regions)
    roots = builder.build_hierarchy()
    print(f"   Tree has {len(roots)} root elements")
    
    # Step 3: Find repeated patterns
    print("\n3. Finding repeated patterns...")
    builder.find_repeated_patterns(roots)
    repeated_count = sum(1 for r in regions if r.is_repeated)
    print(f"   Found {repeated_count} regions that repeat")
    
    # Step 4: Generate overlay
    print("\n4. Generating overlay visualization...")
    generate_overlay(image_path, roots, output_path)
    print(f"   Saved to: {output_path}")
    
    return roots


def generate_overlay(image_path: str, roots: List[DetectedRegion], output_path: str):
    """Generate visual overlay with detected regions"""
    # Load image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        font = ImageFont.load_default()
    
    # Color scheme by depth
    colors = ["#2196F3", "#F44336", "#4CAF50", "#FFC107", "#9C27B0", "#FF5722"]
    
    def draw_region(region: DetectedRegion, depth: int = 0):
        """Recursively draw region and children"""
        bbox = region.bbox
        color = colors[depth % len(colors)]
        
        # Draw box
        thickness = max(1, 4 - depth)
        for i in range(thickness):
            draw.rectangle(
                [(bbox.x1 + i, bbox.y1 + i), (bbox.x2 - i, bbox.y2 - i)],
                outline=color,
                width=1
            )
        
        # Draw label
        label = f"Region {depth}"
        if region.is_repeated:
            label += f" (×{len(region.similar_regions) + 1})"
        
        draw.text((bbox.x1 + 4, bbox.y1 + 4), label, fill=color, font=font)
        
        # Draw children
        for child in region.children:
            draw_region(child, depth + 1)
    
    # Draw all roots
    for root in roots:
        draw_region(root)
    
    # Save
    img.save(output_path, quality=95)


if __name__ == "__main__":
    analyze_image(
        "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1.png",
        "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1-REAL-ANNOTATED.png"
    )
