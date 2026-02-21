---
skill:
  name: icon-finding
  version: 1.0.0
  description: VLM-guided icon selection with topology awareness. NEVER use emoji for UI icons.
  keywords: [icons, svg, emoji, topology, nano-banana, mockup]
  author: Ken
  license: MIT
---

# Icon Finding Skill: VLM-Guided Icon Selection

## The Problem

When implementing UI mockups, we need icons for navigation, actions, and UI elements.

**NEVER use:**
- ❌ Emoji (🧘🧘🎙️) - Tacky, unprofessional, inconsistent across platforms
- ❌ Generated 1K images (1024x1024, 500KB+) - Wasteful, slow, unnecessary

**ALWAYS use:**
- ✅ SVG icons from established libraries (<1KB, scalable, professional)
- ✅ Generate only if no suitable icon exists in libraries

---

## The Icon Finding Process

### Step 1: Use VLM to Describe What Icon LOOKS Like (Not What It Means)

**Prompt Nano Banana Pro:**
```
Look at the bottom navigation in this mockup.

For each icon, describe what you ACTUALLY SEE (mechanical description, not concept):
- What shapes make up the icon?
- How are the shapes arranged?
- What does it visually look like?

Example: "A circle with a dot in the center" NOT "a target icon"
```

**Example VLM Response:**
```
Icon 1: "A cluster of five small interconnected circles - one central, four radiating"
Icon 2: "An open book shape - larger rectangle with smaller offset rectangle"
Icon 3: "Vertical line with horizontal bars at top and bottom, curved top"
```

---

### Step 2: Map Visual Description to Icon Concepts

| VLM Visual Description | Likely Concept | Icon Library Name |
|------------------------|----------------|-------------------|
| "5 interconnected circles" | Network/Share | ⚠️ WRONG - see semantic check below |
| "Open book shape" | Book | `book-open` ✓ |
| "Vertical line with bars and curve" | Microphone | `microphone` or `mic` ✓ |

---

### Step 3: **CRITICAL - Semantic Check (Understand What Icon MEANS)**

**THIS IS WHERE THE EMOJI MISTAKE HAPPENS!**

**Wrong approach:**
```
VLM says: "5 interconnected circles"
You think: "Share/network icon"
You search: Lucide "share" or "network"
Result: ❌ Wrong icon - these mean NETWORKING, not EXPLORATION
```

**Correct approach:**
```
VLM says: "5 interconnected circles"
Semantic check: What does THIS BUTTON DO in the app?
Button label: "Explore"
Concept: Discovery, browsing, finding new content
Search: Lucide "compass" or "explore" or "search"
Result: ✅ Compass icon (semantically correct)
```

**The Rule:**
1. VLM describes what icon LOOKS LIKE (topology)
2. YOU understand what icon MEANS (semantics)
3. Search for icons matching BOTH topology AND semantics

---

### Step 4: Search Icon Libraries (in order)

**1. Lucide Icons (first choice)**
- URL: https://lucide.dev/icons
- ~1,400 icons
- Consistent style, modern, clean
- Free, MIT licensed
- React/Vue/etc components available

**2. Heroicons (fallback)**
- URL: https://heroicons.com/
- ~300 icons
- Outline and solid styles
- Free, MIT licensed
- Tailwind-friendly

**3. Feather Icons (fallback)**
- URL: https://feathericons.com/
- ~280 icons
- Minimalist style
- Free, MIT licensed

**4. Font Awesome (only if necessary)**
- URL: https://fontawesome.com/icons
- Thousands of icons
- Free tier has ~2,000 icons
- Pro requires license

---

### Step 5: Verify Icon Match

**For each icon:**

1. **Topology match:** Does it visually look like what VLM described?
2. **Semantic match:** Does it represent what the button/action DOES?
3. **Style match:** Does it fit the design aesthetic?

**Example:**

| Button | VLM Description | Semantic Meaning | Wrong Icon | Right Icon |
|--------|----------------|-----------------|------------|------------|
| Explore | 5 circles radiating | Discovery, browse | `share-2` (networking) | `compass` (navigation) |
| Meditations | Open book | Reading, content | `book` (reading) | `book-open` (active reading) |
| Voice | Mic with bars | Audio, recording | `mic` (generic) | `mic-2` (stylized) |

---

## Critical Learnings

### 🚨 The Emoji Trap

**What happened in our session:**
```
Initial: Used emoji (🧘🧘🎙️) 
Problem: Tacky, inconsistent, unprofessional
Fix: Switched to Lucide icons
```

**Why emoji fails:**
- Platform-dependent rendering (looks different on iOS/Android/Windows)
- Size inconsistency
- Color inconsistency (can't style with CSS)
- Accessibility issues (screen readers)
- Unprofessional appearance

**When is emoji acceptable?**
- NEVER for UI icons
- Maybe for decorative content (user-generated)
- Maybe for playful marketing copy

---

### 🔍 The Topology vs Semantics Problem

**Case study: The "Explore" button**

**Topology:** 5 interconnected circles (looks like network/share icon)

**Semantic options:**
- If button means "Share with friends" → `share-2` icon ✓
- If button means "Explore content" → `compass` icon ✓

**We initially picked:** Share icon (matched topology, not semantics)  
**Should have picked:** Compass icon (matched semantics)

**The Fix:**
1. Ask: "What does this button DO in the app context?"
2. User confirmed: "Explore/discover content"
3. Searched Lucide for "explore" → Found `compass` → Perfect match

---

### 📊 One-to-Many vs Many-to-Many Icon Relationships

**One-to-many (straightforward):**
```
VLM: "Open book"
Concept: Reading
Lucide search: "book"
Result: book, book-open, book-marked (pick best)
```

**Many-to-many (requires semantic check):**
```
VLM: "5 circles radiating"
Could mean: Share, network, explore, connect, group
Must check: App context determines which
```

**How to handle many-to-many:**
1. List all possible semantic meanings
2. Check UI context (button label, surrounding content)
3. Ask user if ambiguous
4. Pick icon matching BOTH topology and confirmed semantics

---

## The Complete Icon Finding Workflow

```
1. VLM describes icon topology
   "What shapes do you see?"
   
2. Identify semantic meaning
   "What does this button DO?"
   
3. Search Lucide/Heroicons for matches
   Use keywords from BOTH topology and semantics
   
4. Verify match
   - Looks like description? ✓
   - Means the right thing? ✓
   - Fits aesthetic? ✓
   
5. If no match found in libraries
   → THEN generate with Nano Banana Pro
   → NOT before checking libraries
```

---

## When to Generate vs Use Library Icons

### Use Library Icons (99% of cases)
- Standard actions (search, menu, close, back)
- Navigation (home, profile, settings)
- Media controls (play, pause, volume)
- Social (share, like, comment)
- Common objects (calendar, camera, mail)

### Generate Custom Icons (rare)
- Brand-specific symbols
- Unique product features
- Decorative illustrations (not functional icons)
- When library icons genuinely don't fit the aesthetic

**Example from our session:**
- ✓ Used Lucide for all 3 bottom nav icons
- ✗ Didn't need to generate any custom icons

---

## Icon Implementation (React/Tailwind Example)

**Using Lucide React:**
```jsx
import { Compass, BookOpen, Mic2 } from 'lucide-react'

<nav className="flex justify-between">
  <button>
    <Compass className="w-6 h-6 text-gray-600" />
    <span>Explore</span>
  </button>
  <button>
    <BookOpen className="w-6 h-6 text-gray-600" />
    <span>Meditations</span>
  </button>
  <button>
    <Mic2 className="w-6 h-6 text-gray-600" />
    <span>Voice</span>
  </button>
</nav>
```

**Benefits:**
- Icons scale with size classes
- Colors match design system
- Accessible (proper aria labels)
- Tree-shakeable (only bundle used icons)
- No HTTP requests (inlined SVG)

---

## Troubleshooting

### "Can't find an icon that matches"
1. Broaden search terms
2. Try different libraries
3. Ask: Is the semantic meaning clear?
4. Last resort: Generate with Nano Banana

### "Icon looks right but doesn't feel right"
1. Check semantic meaning
2. Verify UI context
3. Ask user for feedback

### "VLM gave vague description"
1. Ask VLM to be more specific
2. Show VLM the mockup region cropped
3. Ask: "Describe the shapes in detail"

---

## Success Metrics

✓ **90%+ of icons found in libraries** (not generated)  
✓ **0 emoji used for functional UI icons**  
✓ **Topology AND semantics match**  
✓ **Consistent style across all icons**  
✓ **User confirms icons make sense**

---

## Summary

**The Golden Rule:** NEVER use emoji for UI icons. Always search libraries first.

**The Process:**
1. VLM describes topology
2. Identify semantics from context
3. Search Lucide → Heroicons → Feather
4. Verify both topology and semantic match
5. Generate only if libraries have nothing suitable

**Critical insight:** Icon selection requires BOTH visual matching (topology) AND conceptual understanding (semantics). VLMs handle topology; you handle semantics.
