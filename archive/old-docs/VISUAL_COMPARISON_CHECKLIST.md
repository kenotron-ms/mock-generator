# Visual Comparison Checklist

## What I Just Applied (Build: Latest)

### ✅ Applied Changes:

**Global:**
- Background: `#F3EFE7` (warm beige) - was gray
- Font family: Serif (Georgia) - was sans-serif
- Accent color: `#C66E5B` (terracotta) - was blue

**ScreenHeader:**
- Title size: `32px` with `font-bold` - was smaller
- Gap between title and tabs: `24px` (gap-lg) - was 8px
- Tab active indicator: `3px` height, terracotta color - was different
- Tab font size: `16px` - was text-base

**HeroArticleCard:**
- Border radius: `16px` (rounded-hero) - was rounded-lg
- Gradient: `to top` from `rgba(0,0,0,0.5)` - was to bottom 0.7
- Content padding: `24px` (p-hero-content) - was 16px
- Title size: `28px` bold, `line-height: 1.2` - was text-xl
- Metadata size: `12px` - was text-sm
- Using `/hero-bg.png` - was Unsplash

**ArticleListItem:**
- Background: white with shadow - was white
- Padding: `16px` (p-list-item) - was p-md
- Margin bottom: `24px` (mb-lg) - was mb-sm
- Border radius: `16px` (rounded-card) - was rounded-lg
- Thumbnail border radius: `12px` (rounded-thumb) - was rounded-md
- Thumbnail gap: `16px` (gap-thumb-gap) - was gap-md
- Title size: `18px` semibold - was text-base
- Description size: `14px` - was text-sm
- Metadata tag: green background with green text - was gray
- Using `/thumb-1.png`, `/thumb-2.png` - was Unsplash

**BottomNavBar:**
- Border radius: `30px` (rounded-nav) - was square
- Shadow: `shadow-nav` - was border-t
- Padding: `32px` horizontal, `12px` vertical - was 16px/8px
- Label size: `11px` - was text-xs
- Active color: terracotta - was black
- Opacity: 0.6 for inactive - was color change

## ⚠️ Likely Remaining Differences:

### 1. Main Content Spacing
```
Current: p-md gap-md (16px padding, 16px gaps)
Tokens say: screen horizontal: 20px, component-gaps: 24px
→ FIX: Change to px-screen-h gap-lg
```

### 2. Metadata Tag Colors
```
Current: All using green (#768763)
Original: Some green, some red (#C66E5B)
→ FIX: Vary the tag colors (alternate or based on index)
```

### 3. Hero Card Gradient Opacity
```
Current: rgba(0,0,0,0.5)
Tokens say: opacity: 0.4
→ FIX: Change to 0.4
```

### 4. Article List Item Spacing
```
Current: mb-lg (24px)
Tokens say: list-items gap is 16px
→ FIX: Should be mb-md (16px) or no margin if using gap
```

### 5. Missing Articles
```
Current: Only have thumb-1.png and thumb-2.png
Need: thumb-3.png through thumb-5.png
→ Status: Still generating in background
```

### 6. Navigation Icons
```
Current: Using emoji placeholders
Need: Actual minimal icons
→ FIX: Generate icon-explore.png, icon-meditations.png, icon-voice.png
```

## Quick Fixes I Can Do Now:

1. Fix main content spacing (px-screen-h, gap-lg)
2. Fix hero gradient opacity (0.4 instead of 0.5)
3. Add tag color variation (alternate green/red)
4. Fix list item margins

## What I Can't Fix Without Visual Feedback:

- Overall vertical rhythm (need to see if sections are too close/far)
- Exact alignment issues
- Color matching (need to see if extracted colors are truly exact)
- Font rendering differences (serif might look different across browsers)
