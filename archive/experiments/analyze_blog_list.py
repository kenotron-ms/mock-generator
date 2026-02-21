#!/usr/bin/env python3
"""
Analyze the blog-meditations-list-v1.png mockup and generate component overlay.

This demonstrates the VLM reasoning approach:
1. Identify major sections
2. Recognize repeated patterns (list items)
3. Break down into semantic components
4. Generate visual overlay for human review
"""
from component_analyzer import (
    Component, ComponentElement, analyze_mockup, export_component_spec
)

# Image dimensions: 768x1376 (mobile portrait)
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1376

def analyze_blog_meditations_list():
    """
    Analyze the blog meditations list mockup.
    
    REASONING PROCESS (simulating VLM):
    
    1. First glance: This looks like a scrollable list of meditation/article cards
       - Header at top
       - Repeating card pattern in main area
       - Possibly bottom navigation
    
    2. Pattern recognition:
       - Multiple similar cards → Reusable component
       - Each card has: image, text, metadata
       - Cards are vertically stacked → FlatList/ScrollView pattern
    
    3. Component hierarchy:
       - Screen level: Header + ScrollView + (maybe) BottomNav
       - Card level: Container with Image + Text + Metadata
    """
    
    components = []
    
    # ============================================
    # SECTION 1: Header
    # ============================================
    # Reasoning: Top ~80px typically reserved for navigation/header
    # Standard iOS/Android header pattern: back button, title, action buttons
    
    header = Component(
        name="Header",
        component_type="section",
        bbox=(0, 0, IMAGE_WIDTH, 80),
        repeats=False,
        instance_count=1,
        elements=[
            ComponentElement(
                name="BackButton",
                element_type="IconButton",
                bbox=(16, 30, 56, 70),
                reasoning="Left-aligned icon button - standard back navigation pattern"
            ),
            ComponentElement(
                name="ScreenTitle",
                element_type="Text",
                bbox=(200, 35, 568, 65),
                reasoning="Center-aligned title text - 'Meditations' or similar"
            ),
            ComponentElement(
                name="ActionButton",
                element_type="IconButton",
                bbox=(712, 30, 752, 70),
                reasoning="Right-aligned action button - filter/search/menu"
            ),
        ],
        reasoning="Standard mobile header with back button, title, and action button",
        color="#2196F3"
    )
    components.append(header)
    
    # ============================================
    # SECTION 2: MeditationArticleCard (Repeating)
    # ============================================
    # Reasoning: The filename says "blog-meditations-list" → article/blog post cards
    # Typical card: Large image + title + description + metadata (author, time)
    # Cards repeat vertically with spacing
    
    # Let's say we have 3 visible cards
    card_height = 340
    card_spacing = 20
    cards_start_y = 100
    
    for i in range(3):
        card_y = cards_start_y + i * (card_height + card_spacing)
        
        card = Component(
            name="MeditationArticleCard" if i == 0 else None,  # Only name the first one
            component_type="component",
            bbox=(16, card_y, IMAGE_WIDTH - 16, card_y + card_height),
            repeats=True if i == 0 else False,  # Mark first instance as repeating
            instance_count=3,
            elements=[
                ComponentElement(
                    name="FeaturedImage",
                    element_type="Image",
                    bbox=(16, card_y, IMAGE_WIDTH - 16, card_y + 200),
                    reasoning="Large featured image - blog post hero image with rounded corners"
                ),
                ComponentElement(
                    name="ArticleTitle",
                    element_type="Text",
                    bbox=(32, card_y + 216, IMAGE_WIDTH - 32, card_y + 260),
                    reasoning="Bold title text - article headline (2 lines max)"
                ),
                ComponentElement(
                    name="ArticleExcerpt",
                    element_type="Text",
                    bbox=(32, card_y + 268, IMAGE_WIDTH - 32, card_y + 308),
                    reasoning="Lighter body text - article description/excerpt"
                ),
                ComponentElement(
                    name="MetadataRow",
                    element_type="View",
                    bbox=(32, card_y + 316, IMAGE_WIDTH - 32, card_y + 336),
                    reasoning="Horizontal row with author, date, read time - common blog metadata pattern"
                ),
            ],
            reasoning="""
            PATTERN RECOGNITION: Blog/Article Card
            
            Visual cues:
            - Large hero image (suggests visual content)
            - Title + excerpt text (suggests article/blog)
            - Metadata row at bottom (author/time - blog pattern)
            - Rounded corners with elevation (card affordance)
            - Repeats vertically (list item pattern)
            
            Component naming:
            - Not "Card1", "Card2", "Card3" → Generic "MeditationArticleCard"
            - Reusable component used 3 times
            - Content varies (different images/text) but structure identical
            """,
            color="#F44336"
        )
        
        # Only add the named card (first instance represents all)
        if i == 0:
            components.append(card)
    
    # ============================================
    # OPTIONAL: Bottom Navigation
    # ============================================
    # Reasoning: Many mobile apps have bottom tab navigation
    # Let's include it tentatively - user can confirm/reject
    
    bottom_nav = Component(
        name="BottomTabBar",
        component_type="section",
        bbox=(0, IMAGE_HEIGHT - 90, IMAGE_WIDTH, IMAGE_HEIGHT),
        repeats=False,
        instance_count=1,
        elements=[
            ComponentElement(
                name="TabButton",
                element_type="TouchableOpacity",
                bbox=(50, IMAGE_HEIGHT - 70, 150, IMAGE_HEIGHT - 20),
                reasoning="Tab button with icon + label - repeats 4-5 times across bottom"
            ),
            # Could add more tab buttons, but keeping it simple for now
        ],
        reasoning="Optional: Standard bottom tab navigation - user can confirm if present",
        color="#9C27B0"
    )
    components.append(bottom_nav)
    
    return components


def main():
    print("=" * 60)
    print("ANALYZING: blog-meditations-list-v1.png")
    print("=" * 60)
    print()
    
    # Analyze
    components = analyze_blog_meditations_list()
    
    print("IDENTIFIED COMPONENTS:")
    print()
    for comp in components:
        marker = "🔁" if comp.repeats else "  "
        print(f"{marker} {comp.name} ({comp.component_type})")
        print(f"   └─ {comp.reasoning[:80]}...")
        if comp.repeats:
            print(f"   └─ Repeats: {comp.instance_count} instances")
        print()
    
    # Generate overlay
    input_path = "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1.png"
    output_path = "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1-ANNOTATED.png"
    spec_path = "/Users/ken/workspace/mock-generator/mockups/blog-meditations-list-v1-spec.json"
    
    print("GENERATING OVERLAY...")
    analyze_mockup(input_path, output_path, components)
    
    print()
    print("EXPORTING COMPONENT SPEC...")
    export_component_spec(components, spec_path)
    
    print()
    print("=" * 60)
    print("✓ DONE!")
    print("=" * 60)
    print()
    print("REVIEW ARTIFACTS:")
    print(f"  📸 Visual: {output_path}")
    print(f"  📄 Spec:   {spec_path}")
    print()
    print("NEXT STEPS:")
    print("  1. Review the annotated image")
    print("  2. Provide feedback on component identification")
    print("  3. Iterate until the breakdown matches your mental model")
    print()


if __name__ == "__main__":
    main()
