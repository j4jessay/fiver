# 🎨 Databricks Lakehouse v2 Diagram - Creation Methodology & Reusable Prompts

**Document Purpose**: Complete guide to recreate professional Databricks architecture diagrams
**Created**: December 8, 2025
**Source Diagrams**: `databricks-lakehouse-final-v2.drawio`, `01-lakehouse-architecture-professional-v2.drawio`

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [Official Databricks Standards](#official-databricks-standards)
4. [The Creation Process](#the-creation-process)
5. [Reusable Prompts](#reusable-prompts)
6. [Technical Specifications](#technical-specifications)
7. [Key Learnings](#key-learnings)

---

## Overview

### What Was Created

**Two professional-grade architecture diagrams** following official Databricks reference architecture standards:

1. **Lakehouse Architecture (v2)** - 8-layer swim lane diagram
2. **Data Flow Diagrams** - 3 flows with DQ checkpoints

### Core Principle

> **"Match official Databricks reference architecture visual quality while prominently featuring Databuck as the primary data quality solution"**

---

## Design Philosophy

### The Three Pillars

#### 1. **Visual Consistency**
- Use official Databricks color palette (exact hex codes)
- Apply consistent typography hierarchy
- Maintain uniform spacing and alignment
- Professional depth through shadows and rounded corners

#### 2. **Prominent Databuck Integration**
- Dedicated purple layer for Data Quality
- Thicker borders (3px vs 2px) for emphasis
- Stronger shadows for visual prominence
- Performance badges (100M records/60sec)
- Trust Score indicators

#### 3. **Enterprise Readiness**
- Clean, professional appearance
- Print-ready at high resolution
- Accessible color contrast (WCAG AA)
- Legend and annotations for clarity

---

## Official Databricks Standards

### Color Palette (Exact Hex Codes)

| **Element** | **Fill Color** | **Border Color** | **Purpose** |
|-------------|----------------|------------------|-------------|
| **Data Sources** | `#E3F2FD` | `#1976D2` | Light blue - External inputs |
| **Ingestion** | `#C8E6C9` | `#388E3C` | Light green - Data ingestion |
| **Data Quality (Databuck)** | `#F3E5F5` | `#7B1FA2` | Light purple - DQ layer ⭐ |
| **Processing** | `#FFF9C4` | `#F57F17` | Light yellow - Transformation |
| **Storage/Governance** | `#FFE0B2` | `#E65100` | Light orange - Delta/Unity |
| **AI/ML** | `#E1BEE7` | `#6A1B9A` | Light purple - ML services |
| **Consumption** | `#FFCCBC` | `#D84315` | Light coral - BI/Analytics |
| **Security/Monitoring** | `#FFEBEE` | `#C62828` | Light red - Security layer |

**Brand Colors:**
- Primary: `#FF3621` (Red Orange)
- Dark Text: `#1B3139` (Gable Green)
- Accent: `#40D1F5` (Cyan)
- Alert: `#EB1600` (Bright Red)

### Typography Standards

| **Element** | **Font** | **Size** | **Weight** | **Color** |
|-------------|----------|----------|------------|-----------|
| Diagram Title | Calibri (DM Sans) | 24-26pt | Bold (700) | `#1B3139` |
| Layer Titles | Calibri | 16-18pt | Bold (600) | Layer color |
| Component Labels | Calibri | 11-12pt | Medium (500) | `#0B2026` or white |
| Descriptions | Calibri | 10-11pt | Regular (400) | `#4A4A4A` |
| Annotations | Calibri | 9-10pt | Italic (400) | Layer color |

### Component Styling

**Standard Component:**
```
Shape: Rounded rectangle
Width: 95-130px
Height: 60-70px
Rounded corners: 10-12px
Border: 2px solid
Shadow: 0 4px 12px rgba(0,0,0,0.1)
Fill: White or layer light color
```

**Databuck Component (Emphasized):**
```
Shape: Rounded rectangle
Width: 140-160px (20% larger)
Height: 70px
Rounded corners: 10px
Border: 3px solid #7B1FA2 (thicker)
Shadow: 0 6px 16px rgba(123,31,162,0.2) (stronger)
Fill: #7B1FA2 (solid purple)
Label: 14pt Bold, white text
```

### Spacing Standards

| **Element** | **Spacing** |
|-------------|-------------|
| Swim Lane Height | 90-140px |
| Horizontal Gap | 30-40px between components |
| Vertical Gap | 20-30px between layers |
| Outer Margin | 40px all sides |
| Inner Padding | 15px inside containers |

### Arrow Specifications

| **Type** | **Width** | **Color** | **Style** |
|----------|-----------|-----------|-----------|
| Primary Flow | 4px | Layer-specific | Solid, block arrowhead |
| DQ Checkpoints | 4px | `#7B1FA2` (purple) | Solid with emphasis |
| Secondary | 3px | `#A0A0A0` (gray) | Solid or dashed |
| Error Paths | 2-3px | `#F44336` (red) | Dashed |

---

## The Creation Process

### Phase 1: Research & Planning

**Step 1: Analyze Reference Architecture**
```
Task: Study official Databricks reference diagrams
Goal: Identify patterns, colors, spacing, typography
Output: List of design standards to follow
```

**Key Questions Asked:**
- What colors does Databricks use officially?
- What's the typical layout pattern (swim lanes, hierarchical, flow)?
- How do they emphasize important components?
- What typography and sizing do they use?

**Step 2: Define Requirements**
```
Task: List all components and their relationships
Goal: Complete architecture inventory
Output: Component list with 8 layers, 40+ services
```

**Requirements Gathered:**
- 8 architecture layers (Sources → Security)
- Databuck as prominent DQ layer
- Bronze-Silver-Gold medallion architecture
- AI/ML capabilities (RAG, Agentic AI, MLflow)
- Unity Catalog integration
- Performance specifications

### Phase 2: Design System Creation

**Step 3: Create Color Palette**
```xml
<!-- Draw.io Custom Colors -->
<colors>
  <color name="Databricks-Primary" value="#FF3621"/>
  <color name="Databricks-Dark" value="#1B3139"/>
  <color name="Databricks-Cyan" value="#40D1F5"/>
  <color name="Layer-Sources" value="#E3F2FD"/>
  <color name="Layer-Ingestion" value="#C8E6C9"/>
  <color name="Layer-DQ-Databuck" value="#F3E5F5"/>
  <color name="Layer-Processing" value="#FFF9C4"/>
  <color name="Layer-Storage" value="#FFE0B2"/>
  <color name="Layer-AIML" value="#E1BEE7"/>
  <color name="Layer-Consumption" value="#FFCCBC"/>
  <color name="Layer-Security" value="#FFEBEE"/>
</colors>
```

**Step 4: Define Component Templates**

**Template 1: Standard Service Component**
```
<!-- Reusable component template -->
Shape: Rectangle
Width: 120px
Height: 60px
Rounded: 10px
Border: 2px [layer-color]
Fill: White or layer-light
Shadow: Yes (0 4px 12px)
Font: Calibri 11pt Medium
Alignment: Center
```

**Template 2: Databuck DQ Component**
```
<!-- Emphasized component template -->
Shape: Rectangle
Width: 160px
Height: 70px
Rounded: 10px
Border: 3px #7B1FA2
Fill: #7B1FA2 (solid)
Shadow: Yes (0 6px 16px, stronger)
Font: Calibri 14pt Bold
Color: White
Badge: "100M/60sec" or "Trust Score"
```

### Phase 3: Diagram Construction

**Step 5: Canvas Setup**
```
Canvas Size: 1600px × 1200px (or 11" × 17" for print)
Background: #FFFFFF (white) or #FAFAFA (light gray)
Grid: 10px (for alignment)
Snap to Grid: Enabled
Orientation: Landscape
```

**Step 6: Create Swim Lanes (8 Layers)**

```
For each layer (i = 1 to 8):
  - Create container rectangle
  - Width: 1520px
  - Height: 90-140px (varies by content)
  - Y-position: 80px + (i-1) × (height + 20px gap)
  - Border: 2-3px, layer-specific color
  - Fill: Layer-specific light color
  - Rounded: 12px
  - Add layer title (left-aligned, 15px padding)
```

**Example for Layer 3 (Databuck):**
```xml
<mxCell id="layer3-bg"
  value=""
  style="rounded=1;whiteSpace=wrap;html=1;
         fillColor=#F3E5F5;
         strokeColor=#7B1FA2;
         strokeWidth=3;  <!-- Thicker for emphasis -->
         arcSize=12"
  vertex="1" parent="1">
  <mxGeometry x="40" y="340" width="1520" height="120"/>
</mxCell>

<mxCell id="layer3-title"
  value="DATA QUALITY &amp; VALIDATION LAYER ⭐"
  style="text;html=1;
         strokeColor=none;
         fillColor=none;
         align=left;
         verticalAlign=middle;
         fontSize=18;
         fontStyle=1;
         fontColor=#7B1FA2"
  vertex="1" parent="1">
  <mxGeometry x="60" y="350" width="400" height="30"/>
</mxCell>
```

**Step 7: Add Components to Each Layer**

```
For each component in layer:
  1. Use component template (standard or emphasized)
  2. Position with 30-40px horizontal gap
  3. Vertically center in layer
  4. Add label with appropriate font
  5. Apply shadow effect
  6. If Databuck: use emphasized template
```

**Databuck Component Code:**
```xml
<mxCell id="databuck-main"
  value="DATABUCK by FirstEigen"
  style="rounded=1;whiteSpace=wrap;html=1;
         fillColor=#7B1FA2;
         strokeColor=#7B1FA2;
         strokeWidth=3;
         fontColor=#ffffff;
         fontStyle=1;
         fontSize=16;
         shadow=1;
         arcSize=10"
  vertex="1" parent="1">
  <mxGeometry x="280" y="385" width="220" height="65"/>
</mxCell>
```

**Step 8: Add Sub-components (Databuck Features)**

```
Databuck Sub-components:
  - Trust Score Engine (130px × 65px, lighter purple)
  - AI/ML Anomaly Detection (130px × 65px, lighter purple)
  - Circuit Breaker (110px × 65px, lighter purple)
  - Position: Right side of main Databuck component
  - Gap: 20px between sub-components
```

**Step 9: Create Data Flow Arrows**

```
Primary Data Flow (vertical between layers):
  - Style: Solid arrow
  - Width: 4px
  - Color: #40D1F5 (cyan) or layer-specific
  - Curve: Smooth (rounded edges)
  - Arrowhead: Block style

Connection Pattern:
  Sources → Ingestion → DQ → Processing → Storage → AI/ML → Consumption
```

**Arrow Code Example:**
```xml
<mxCell id="arrow-sources-ingestion"
  style="edgeStyle=orthogonalEdgeStyle;
         rounded=1;
         orthogonalLoop=1;
         jettySize=auto;
         strokeWidth=4;
         strokeColor=#40D1F5;
         endArrow=block"
  edge="1" parent="1"
  source="source-component"
  target="ingestion-component">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**Step 10: Add Legend**

```
Legend Container:
  - Position: Bottom-right or right-side panel
  - Size: 280px W × 200px H
  - Fill: #F5F5F5 (light gray)
  - Border: 2px #424242
  - Rounded: 8px

Legend Content:
  - Title: "LEGEND" (14pt Bold)
  - Color blocks: 20px × 20px squares
  - Labels: Layer names with colors
  - Symbols: Arrow types, status indicators
```

**Step 11: Add Key Features Box**

```
Features Box:
  - Position: Right side, middle
  - Size: 280px W × 220px H
  - Fill: #E8F5E9 (light green)
  - Border: 2px #2E7D32 (green)
  - Rounded: 10px

Content:
  ✓ Databuck: 100M records/60sec validation
  ✓ Data Trust Score in Unity Catalog
  ✓ AI/ML anomaly detection
  ✓ Circuit breaker for bad data
  ✓ Real-time + Batch processing
  ✓ RAG, Agentic AI capabilities
  ✓ 250GB/day data volume
```

**Step 12: Add Title and Annotations**

```
Main Title:
  - Text: "Enterprise Databricks Lakehouse Architecture with Databuck"
  - Position: Top center, 40px from edge
  - Font: Calibri 26pt Bold
  - Color: #1B3139
  - Alignment: Center

Annotations:
  - Layer descriptions (italic, 10pt)
  - Performance notes
  - Data flow indicators
```

### Phase 4: Refinement & Polish

**Step 13: Quality Checks**

```
Visual Quality Checklist:
  ☑ All colors match Databricks palette
  ☑ Typography hierarchy is consistent
  ☑ Spacing is uniform (30-40px gaps)
  ☑ All elements aligned to grid
  ☑ Shadows applied correctly
  ☑ No overlapping elements
  ☑ Databuck layer stands out
  ☑ Legend is complete
  ☑ Arrows are clear and directional
  ☑ Text is readable at 100% zoom
```

**Step 14: Accessibility Check**

```
Color Contrast:
  - Text on light backgrounds: 4.5:1 minimum
  - Text on dark backgrounds: Check white text on purple
  - Use WebAIM Contrast Checker

Readability:
  - Minimum font size: 10pt
  - Bold for emphasis only
  - No critical info in color alone
```

**Step 15: Export & Test**

```
Export Settings:
  - Format: PNG (1600px wide, 300 DPI)
  - Format: PDF (high quality, embedded fonts)
  - Format: SVG (for scalability)

Test Views:
  - 50% zoom (overview)
  - 100% zoom (detail)
  - 150% zoom (accessibility)
  - Print test page
```

---

## Reusable Prompts

### Prompt 1: Initial Architecture Analysis

```
Analyze the following architecture and create a comprehensive diagram
following official Databricks design standards:

Requirements:
- 8-layer swim lane architecture
- [List specific layers and components]
- Prominent feature: [e.g., Databuck as primary DQ solution]
- Use official Databricks color palette
- Professional typography (Calibri or DM Sans)
- Rounded corners and drop shadows
- Clear data flow arrows
- Legend and key features box

Reference Standards:
- Colors: [Provide hex codes from table above]
- Spacing: 30-40px horizontal, 20-30px vertical
- Component size: 120px W × 60px H standard
- Arrow width: 4px for primary flows
- Canvas: 1600px × 1200px

Special Emphasis:
- [Component name] should be 20% larger
- Use 3px borders instead of 2px
- Stronger shadow (0 6px 16px)
- Solid fill color instead of white
```

### Prompt 2: Databuck Emphasis

```
Create a Data Quality layer for Databricks architecture with
prominent Databuck integration:

Component Layout:
- Main component: "DATABUCK by FirstEigen" (220px W × 65px H)
- Sub-components:
  * Trust Score Engine
  * AI/ML Anomaly Detection
  * Circuit Breaker
- Additional DQ tools: DLT Expectations, Lakehouse Monitoring

Styling:
- Fill: #7B1FA2 (solid purple)
- Border: 3px #7B1FA2
- Shadow: 0 6px 16px rgba(123,31,162,0.2)
- Label: 16pt Bold, white text

Performance Badges:
- "100M records / 60 seconds"
- "99.9% Trust Score"
- Display next to main component
```

### Prompt 3: Data Flow Diagram

```
Create a data flow diagram showing end-to-end data movement
with quality checkpoints:

Flows to Include:
1. Batch Processing: Sources → Auto Loader → Databuck → Bronze/Silver/Gold → BI
2. Real-Time: Kafka → Streaming → Databuck → Circuit Breaker → Delta → Apps
3. ML Pipeline: Delta → Databuck → Feature Store → MLflow → Model Serving

Visual Elements:
- Colored containers for each flow (blue, purple, yellow)
- DQ checkpoints as purple boxes with shield icon
- Circuit breaker as diamond decision point
- Status indicators: ✓ (green), ⚠ (orange), ✗ (red)
- 4px arrows with smooth curves
- Pass/Fail paths clearly marked

Layout:
- 3 horizontal flows stacked vertically
- 260px height per flow
- 20px vertical gap between flows
- Legend at bottom with status explanations
```

### Prompt 4: Component Creation

```
Create a [SERVICE_NAME] component for Draw.io diagram:

Specifications:
- Shape: Rounded rectangle
- Size: [WIDTH]px W × [HEIGHT]px H
- Rounded corners: 10px
- Border: [2 or 3]px solid [COLOR]
- Fill: [FILL_COLOR]
- Shadow: 0 4px 12px rgba(0,0,0,0.1)
- Label: "[LABEL_TEXT]"
- Font: Calibri [SIZE]pt [WEIGHT]
- Text color: [COLOR]
- Alignment: Center

Position:
- Layer: [LAYER_NAME]
- X: [X_POSITION]px
- Y: [Y_POSITION]px
- Gap from previous: 35px

If emphasized component (like Databuck):
- Increase size by 20%
- Use 3px border
- Stronger shadow: 0 6px 16px rgba(...)
- Solid fill color
```

### Prompt 5: Comprehensive Diagram Review

```
Review this architecture diagram for professional quality:

Check List:
1. Color Consistency
   - All colors from official palette?
   - Databuck layer in distinct purple?
   - Good contrast for readability?

2. Typography
   - Consistent font family?
   - Proper size hierarchy (26pt > 16pt > 12pt)?
   - Bold used appropriately?

3. Layout
   - Swim lanes properly aligned?
   - 30-40px horizontal spacing?
   - 20-30px vertical gaps?
   - Elements on grid?

4. Visual Hierarchy
   - Important components emphasized?
   - Clear data flow direction?
   - Legend and annotations present?

5. Professional Polish
   - Rounded corners (10-12px)?
   - Shadows applied?
   - No overlapping elements?
   - Clean, enterprise-ready appearance?

Provide specific feedback for improvements.
```

---

## Technical Specifications

### Draw.io XML Structure

**Basic Component Structure:**
```xml
<mxCell id="[unique-id]"
  value="[Label Text]"
  style="[style-properties]"
  vertex="1" parent="1">
  <mxGeometry x="[x]" y="[y]" width="[w]" height="[h]" as="geometry"/>
</mxCell>
```

**Style Properties (Common):**
```
rounded=1                    // Enable rounded corners
whiteSpace=wrap             // Text wrapping
html=1                      // HTML formatting
fillColor=#HEXCODE          // Background color
strokeColor=#HEXCODE        // Border color
strokeWidth=2               // Border thickness
fontColor=#HEXCODE          // Text color
fontSize=12                 // Font size
fontStyle=1                 // 0=regular, 1=bold, 2=italic
fontFamily=Calibri          // Font family
shadow=1                    // Enable shadow
arcSize=10                  // Corner rounding amount (0-100)
```

**Arrow/Edge Structure:**
```xml
<mxCell id="[unique-id]"
  style="edgeStyle=orthogonalEdgeStyle;
         rounded=1;
         orthogonalLoop=1;
         jettySize=auto;
         html=1;
         strokeWidth=4;
         strokeColor=#40D1F5;
         endArrow=block"
  edge="1" parent="1"
  source="[source-component-id]"
  target="[target-component-id]">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="[x1]" y="[y1]"/>
      <mxPoint x="[x2]" y="[y2]"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### Canvas Setup Commands

**For Draw.io Desktop/Web:**
```
1. File → New → Blank Diagram
2. Set canvas size:
   - Right panel → Diagram → Page Setup
   - Size: Custom (1600px × 1200px)
   - Background: White (#FFFFFF)
3. Enable grid:
   - View → Grid → Grid Size: 10px
   - View → Snap to Grid: Enabled
4. Import custom colors:
   - Format → Color → Custom → Add hex codes
```

### Color Management

**Add Custom Palette:**
```javascript
// In Draw.io, use browser console or library
var colors = [
  '#FF3621', // Databricks Primary
  '#1B3139', // Dark Text
  '#40D1F5', // Cyan
  '#E3F2FD', // Layer 1
  '#C8E6C9', // Layer 2
  '#F3E5F5', // Layer 3 (Databuck)
  '#FFF9C4', // Layer 4
  '#FFE0B2', // Layer 5
  '#E1BEE7', // Layer 6
  '#FFCCBC', // Layer 7
  '#FFEBEE'  // Layer 8
];

// Add to custom colors palette
```

---

## Key Learnings

### What Worked Well

1. **Official Color Palette**
   - Using exact Databricks hex codes created instant professionalism
   - Layer-specific colors improved visual hierarchy
   - Distinct purple for Databuck made DQ prominent

2. **Swim Lane Architecture**
   - Clear horizontal layers matched industry standard
   - Left-to-right flow is intuitive
   - Easy to add/remove components without redesign

3. **Visual Emphasis Techniques**
   - 3px borders vs 2px (50% thicker) - noticeable
   - Stronger shadows made components "pop"
   - Solid fill vs white background - strong emphasis
   - 20% larger size - clear hierarchy

4. **Typography Hierarchy**
   - 26pt title → 16pt layers → 12pt components → 10pt notes
   - Bold for titles and emphasis only
   - Consistent font family (Calibri) throughout

5. **Spacing and Alignment**
   - Grid-based layout (10px grid)
   - 30-40px gaps prevented cramping
   - Consistent vertical alignment in layers
   - 40px outer margins created breathing room

### What Didn't Work (Lessons Learned)

1. **Initial Color Choices**
   - ❌ Generic blue/green - looked amateur
   - ✅ Official palette - instant professionalism

2. **Component Sizing**
   - ❌ All components same size - no hierarchy
   - ✅ 20% larger for emphasized - clear priority

3. **Arrow Thickness**
   - ❌ 2px arrows - too thin, hard to follow
   - ✅ 4px primary arrows - bold and clear

4. **Databuck Integration**
   - ❌ Same styling as other components - lost in noise
   - ✅ Dedicated layer + emphasis - stands out

5. **Legend Placement**
   - ❌ Bottom of diagram - easy to miss
   - ✅ Right side panel - always visible

### Design Principles Discovered

1. **The 20% Rule**
   - Important components should be 20% larger
   - Creates clear hierarchy without overwhelming

2. **Border Thickness = Importance**
   - 2px = standard component
   - 3px = emphasized component (50% thicker)
   - 4px = critical flow/connection

3. **Shadow Depth = Layer Hierarchy**
   - Subtle shadow: background elements
   - Medium shadow: standard components
   - Strong shadow: emphasized components

4. **Color Psychology in Architecture**
   - Blue: Trust, stability (sources)
   - Green: Growth, movement (ingestion)
   - Purple: Premium, quality (DQ layer)
   - Yellow: Energy, transformation (processing)
   - Orange: Reliability (storage)
   - Red: Protection, attention (security)

5. **The Three-Second Rule**
   - User should identify key components in 3 seconds
   - Databuck purple layer stands out immediately
   - Clear data flow left-to-right
   - Legend explains everything else

---

## Reusable Workflow

### Quick Start: Create New Architecture Diagram

```bash
# Step 1: Gather Requirements
- List all components and layers
- Identify what needs emphasis (e.g., Databuck)
- Define data flows

# Step 2: Setup Canvas
- Open Draw.io (app.diagrams.net)
- Canvas: 1600px × 1200px
- Grid: 10px, snap enabled
- Add custom colors (from table above)

# Step 3: Create Base Structure
- Draw 8 swim lanes (or required layers)
- Apply layer-specific colors
- Add layer titles (18pt Bold)

# Step 4: Add Components
- Use standard template (120px × 60px)
- Use emphasized template for key components
- Position with 35px gaps
- Apply shadows

# Step 5: Create Connections
- 4px primary arrows
- 3px secondary arrows
- Color-code by function
- Add arrowheads

# Step 6: Add Legend & Annotations
- Legend box (280px × 200px)
- Key features box (280px × 220px)
- Title (26pt Bold)
- Performance notes

# Step 7: Quality Check
- Run checklist from Phase 4
- Check accessibility
- Verify alignment

# Step 8: Export
- PNG: 1600px, 300 DPI
- PDF: High quality, embedded fonts
- SVG: For scalability
```

### Time Estimates

| **Phase** | **Duration** | **Output** |
|-----------|--------------|------------|
| Requirements Gathering | 30 min | Component list, flow definitions |
| Design System Setup | 30 min | Colors, templates, standards |
| Canvas & Base Structure | 45 min | Swim lanes, basic layout |
| Component Creation | 90 min | All services and components |
| Connections & Flows | 45 min | All arrows and connections |
| Legend & Annotations | 30 min | Legend, features box, title |
| Quality & Polish | 30 min | Alignment, checks, refinement |
| **TOTAL** | **~5 hours** | **Professional architecture diagram** |

---

## Appendix: Common Variations

### Variation 1: Cloud-Specific Architecture

```
Azure Databricks:
- Replace AWS icons with Azure icons
- Keep same color palette and structure
- Azure services: ADLS Gen2, ADF, Event Hubs, etc.

GCP Databricks:
- Replace with GCP icons
- GCP services: Cloud Storage, Dataflow, Pub/Sub, etc.
```

### Variation 2: Simplified Version

```
For executive presentations:
- Reduce to 4-5 layers
- Larger components (150px × 80px)
- Fewer details, more emphasis on flows
- Bigger fonts (20pt layer titles, 14pt components)
```

### Variation 3: Detailed Technical Version

```
For engineering teams:
- Add API protocols on arrows
- Include port numbers and protocols
- Add capacity/performance metrics
- More granular sub-components
- Network zones and security groups
```

---

## Quick Reference Card

### Essential Hex Codes
```
Databuck Purple: #7B1FA2
Primary Flow: #40D1F5
Dark Text: #1B3139
Layer Borders: [See table]
Layer Fills: [See table]
```

### Key Measurements
```
Canvas: 1600 × 1200px
Component: 120 × 60px (standard), 160 × 70px (emphasized)
Gaps: 35px horizontal, 25px vertical
Border: 2px (standard), 3px (emphasized)
Font: 26pt title, 18pt layer, 12pt component
Arrow: 4px primary, 3px secondary
Rounded: 10-12px
Shadow: 0 4px 12px rgba(0,0,0,0.1)
```

### Draw.io Shortcuts
```
Ctrl+D: Duplicate
Ctrl+G: Group
Ctrl+Shift+G: Ungroup
Alt+Arrow: Nudge 1px
Ctrl+Alt+Arrow: Nudge 10px
Ctrl+Shift+L: Align left
Ctrl+Shift+E: Align center
Ctrl+Shift+R: Align right
```

---

## Conclusion

This methodology produces **enterprise-grade, professional architecture diagrams** that:
- ✅ Match official Databricks reference quality
- ✅ Prominently feature key components (Databuck)
- ✅ Are presentation-ready and print-quality
- ✅ Follow consistent design standards
- ✅ Can be created in ~5 hours
- ✅ Are fully reusable and adaptable

**Key Success Factors:**
1. Use official color palette (exact hex codes)
2. Apply visual emphasis (size, border, shadow)
3. Maintain consistent spacing and typography
4. Include legend and key features
5. Follow the 3-second rule (immediate clarity)

---

**Document Version**: 1.0
**Created**: December 8, 2025
**Source**: Analysis of databricks-lakehouse-final-v2.drawio
**Ready for Reuse**: ✅ Yes

