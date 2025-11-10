# Databricks Lakehouse Architecture Diagram - Redesign Plan V3 (Horizontal Flow)

**Based on Reference Architecture Sample**
**Date**: November 10, 2025
**Objective**: Create professional horizontal-flow diagram matching official Databricks reference architecture style

---

## 1. LAYOUT STRUCTURE (Horizontal Flow - Left to Right)

### Overall Canvas
- **Size**: 1920px × 1200px (landscape orientation)
- **Flow Direction**: LEFT → RIGHT (Source → Ingestion → Lakehouse → Engagement)
- **Layout**: Vertical swim lanes with dark blue headers
- **Background**: White (#FFFFFF)

### Vertical Swim Lanes (4 main columns)

```
┌──────────────┬──────────────┬───────────────────────────────┬──────────────┐
│ Source Data  │ Data         │ Databricks Lakehouse          │ Engagement   │
│ (150px wide) │ Ingestion    │ (900px wide - CENTER FOCUS)   │ Layer        │
│              │ (200px wide) │                               │ (150px wide) │
└──────────────┴──────────────┴───────────────────────────────┴──────────────┘
```

---

## 2. COLOR PALETTE (Official Databricks Style)

### Swim Lane Headers
- **Header Background**: Dark Teal `#1B4F72` (Databricks blue-teal)
- **Header Text**: White `#FFFFFF`, 16pt bold, DM Sans

### Component Colors
- **Primary Blue**: `#00A3E0` (Databricks brand blue)
- **Delta Lake Gray**: `#E8E8E8` (light gray background)
- **Bronze**: `#CD853F` (Peru)
- **Silver**: `#C0C0C0` (Silver)
- **Gold**: `#FFD700` (Gold)
- **Databuck Emphasis RED**: `#E74856` (red outline, 3px)
- **mosaicML/AI RED**: `#FF0000` (reference red for AI components)

### Supporting Services (Bottom Icons)
- **Icon Background**: Dark blue-gray `#2C3E50`
- **Icon Color**: White `#FFFFFF`
- **Circle Size**: 80px diameter

---

## 3. SWIM LANE 1: SOURCE DATA (Left Column)

### Header
- **Text**: "Source Data"
- **Background**: `#1B4F72`
- **Height**: 40px

### Components (Vertical Stack)
1. **Databases**
   - Icon: Cylinder (blue `#00A3E0`)
   - Size: 100×60px
   - Label: "Databases"

2. **Documents**
   - Icon: Document/file icon
   - Size: 100×60px
   - Label: "Documents"

3. **SIEM** (Header, dark blue background)
   - Size: 120×30px
   - Background: `#1B4F72`

4. **Splunk** (with logo)
   - Size: 100×50px
   - Show Splunk logo

5. **Datadog** (with logo)
   - Size: 100×50px
   - Purple Datadog logo

### Cloud Platform Box (at bottom of column)
- **Header**: "Cloud Platform" `#1B4F72`
- **Icons**: AWS, Azure, Google Cloud logos
- Size: 140×120px

---

## 4. SWIM LANE 2: DATA INGESTION

### Header
- **Text**: "Data Ingestion"
- **Background**: `#1B4F72`
- **Height**: 40px

### Components (Vertical Stack)
1. **Delta Sharing**
   - Icon: Databricks Delta icon (triangle)
   - Blue `#00A3E0`
   - Size: 100×80px

2. **DLT Pipeline**
   - Icon: Pipeline/flow icon
   - Size: 100×80px
   - Dotted connector lines

3. **Lakehouse Connect** (stacked layers icon)
   - Size: 100×80px

4. **Autoloader**
   - Size: 100×80px

5. **3rd Party Tools** (purple circle icon)
   - Size: 80×80px

---

## 5. SWIM LANE 3: DATABRICKS LAKEHOUSE (Center - Main Focus)

### Header
- **Text**: "Databricks Lakehouse"
- **Background**: `#1B4F72`
- **Height**: 40px
- **Width**: 900px

### Section A: Unity Catalog (Top, spanning width)
- **Icon**: Clipboard/catalog icon (coral `#FF6B6B`)
- **Label**: "Unity Catalog"
- **Position**: Top-left of lakehouse section
- **Size**: 80×60px

### Section B: DELTA LAKE (Large gray container)
- **Background**: Light gray `#E8E8E8`
- **Border**: 2px solid `#BDBDBD`
- **Rounded**: 12px
- **Size**: 850×400px

#### Inside DELTA LAKE - Left Side: Medallion Architecture
- **Header**: "Medallion Architecture" (centered, 14pt)
- **Components**: 3 cylinders side-by-side

  1. **Bronze**
     - Color: `#CD853F`
     - Size: 120×140px
     - Label: "Raw Data" (below)

  2. **Silver**
     - Color: `#C0C0C0`
     - Size: 120×140px
     - Label: "Cleaned Data" (below)

  3. **Gold**
     - Color: `#FFD700`
     - Size: 120×140px
     - Label: "Processed Data" (below)

#### Inside DELTA LAKE - Right Side: DATABUCK DATA QUALITY ⭐

**Container**: Red outlined box (emphasis like mosaicML in reference)
- **Border**: 3px solid `#E74856` (RED - for emphasis)
- **Background**: `#FFF5F5` (light red tint)
- **Size**: 420×360px
- **Corner radius**: 8px

**Header**: "DATABUCK Data Quality" (16pt bold, centered)

**4 Components in 2×2 grid** (like mosaicML in reference):

```
┌──────────────────┬──────────────────┐
│  Vector Search   │  Trust Score     │
│  (for DQ)        │  Engine          │
├──────────────────┼──────────────────┤
│  AI/ML Anomaly   │  Circuit         │
│  Detection       │  Breaker         │
└──────────────────┴──────────────────┘
```

Each component:
- **Icon**: Red outlined `#E74856` (gear/cog/magnifying glass)
- **Size**: 180×160px
- **Background**: White
- **Border**: 2px solid `#E74856`
- **Shadow**: 2px drop shadow
- **Icon Size**: 60×60px (centered above text)
- **Label**: Below icon, 12pt, centered

#### Top Right: Monitoring Icon
- **Icon**: Dashboard/monitoring symbol (blue)
- **Position**: Top-right corner of lakehouse
- **Size**: 60×60px

### Section C: Below DELTA LAKE - Model Hub & AI Gateway

**Layout**: 3 boxes in a row

1. **Model Hub** (Left)
   - **Header**: "Model Hub" `#1B4F72`
   - **Size**: 250×120px
   - **Icons**:
     - Databricks Marketplace (stacked layers)
     - Hugging Face logo (with emoji 🤗)

2. **DATABUCK AI Gateway** (Center - RED EMPHASIS)
   - **Border**: 3px solid `#E74856` (RED outline)
   - **Size**: 350×120px
   - **Background**: White
   - **Icon**: Large stacked layers icon
   - **Text**: "Databuck AI Gateway" (16pt bold)
   - **Purpose**: Emphasize Databuck as gateway to AI/ML quality

3. **External Models** (Right)
   - **Header**: "External Models" `#1B4F72`
   - **Size**: 250×120px
   - **Logos**: Gemini, LLaMA, OpenAI (A) logos

---

## 6. SWIM LANE 4: ENGAGEMENT LAYER (Right Column)

### Header
- **Text**: "Engagement Layer"
- **Background**: `#1B4F72`
- **Height**: 40px

### Components (Vertical Stack)
1. **Databricks Apps**
   - Icon: Stacked layers (red `#E74856`)
   - Size: 100×80px

2. **Databricks AI/BI Dashboard Genie**
   - Icon: Dashboard
   - Size: 120×80px

3. **Customized Web App**
   - Icon: Browser window (blue)
   - Size: 100×80px

4. **3rd Party BI Tools** (purple circle)
   - Size: 80×80px

---

## 7. BOTTOM SECTION: SUPPORTING SERVICES (Circular Icons)

**Layout**: Horizontal row of circular icons below main diagram
**Background**: White
**Height**: 140px

### Text Label (Left)
- **Text**: "Supporting Services" (vertical, 90° rotation)
- **Font**: 14pt bold, gray `#666666`

### 7 Circular Icons (80px diameter each)

1. **Notebooks**
   - Icon: Notebook symbol
   - Background: `#2C3E50`
   - Border: 3px `#1B4F72`

2. **Data Ingestion**
   - Icon: Funnel/pipeline
   - Background: `#2C3E50`

3. **Data Transformations**
   - Icon: Gears/transform symbol
   - Background: `#2C3E50`

4. **Data Quality** ⭐ (Databuck emphasis)
   - Icon: Shield with checkmark
   - Background: `#E74856` (RED - different from others)
   - Border: 3px `#E74856`
   - Label: "Data Quality\n(Databuck)"

5. **Job Workflow**
   - Icon: Workflow/flowchart
   - Background: `#2C3E50`

6. **Security + Permissions**
   - Icon: Lock/shield
   - Background: `#2C3E50`

7. **Error Handling**
   - Icon: Alert triangle
   - Background: `#2C3E50`

---

## 8. ARROWS AND CONNECTORS

### Style
- **Stroke**: 3px solid
- **Color**: `#00A3E0` (Databricks blue)
- **Arrow heads**: Filled triangles
- **Corners**: Rounded (10px radius)

### Flow Pattern
```
Source Data → Data Ingestion → DELTA LAKE (Medallion) → Engagement Layer
                                      ↓
                                 DATABUCK DQ
                                 (Red box)
                                      ↓
                              AI Gateway (Red outline)
                                      ↓
                              External Models/Apps
```

### Special Connectors
- **Databuck to Unity Catalog**: Dashed red line (2px, `#E74856`) showing metadata integration
- **AI Gateway to Engagement**: Blue solid arrows (3px)

---

## 9. DATABRICKS LOGO & BRANDING

### Top Right Corner
- **Databricks Logo**: "BrickBuilder Accelerators" hexagon logo
- **Size**: 120×120px
- **Position**: Top-right corner (20px margin)
- **Colors**: Dark teal background, white text

---

## 10. TYPOGRAPHY SPECIFICATIONS

### Headers
- **Swim Lane Headers**: 16pt DM Sans Bold, White, ALL CAPS
- **Section Headers**: 14pt DM Sans Bold, Dark gray `#333333`
- **Component Labels**: 11pt DM Sans Medium, Dark gray `#666666`
- **Title**: 28pt DM Sans Bold, Dark teal `#1B3139`

### Title (Top of Diagram)
- **Text**: "Reference Architecture: Databricks Lakehouse with Databuck Data Quality"
- **Position**: Top-left, 40px from top
- **Font**: 28pt DM Sans Bold
- **Color**: `#1B3139`

---

## 11. KEY DIFFERENCES FROM PREVIOUS DESIGN

| Aspect | Previous (Vertical) | New (Horizontal) |
|--------|---------------------|------------------|
| **Flow** | Top → Bottom layers | Left → Right swim lanes |
| **Layout** | Horizontal swim lanes | Vertical columns |
| **Emphasis** | Purple borders on Databuck | RED outlines (3px) |
| **Structure** | 8 stacked layers | 4 vertical columns |
| **Supporting Services** | Inline in layers | Bottom circular icons |
| **Delta Lake** | Separate layer | Inside Lakehouse box |
| **AI/ML** | Separate layer | Inside Lakehouse (red box) |
| **Databuck Position** | Separate layer | Inside Delta Lake + AI Gateway |

---

## 12. DATABUCK EMPHASIS STRATEGY

### Red Outline Theme (3 locations)
1. **Inside DELTA LAKE**: Databuck DQ box (2×2 grid, red outline)
2. **AI Gateway**: Databuck AI Gateway (red outline, center bottom)
3. **Supporting Services**: Data Quality icon (red background)

### Visual Hierarchy
- **Level 1 (Highest)**: Red outlined boxes (Databuck DQ, AI Gateway)
- **Level 2**: Medallion architecture cylinders (Bronze/Silver/Gold)
- **Level 3**: Standard components (blue/gray)
- **Level 4**: Supporting icons (circular, bottom)

---

## 13. IMPLEMENTATION STEPS

### Phase 1: Canvas Setup
1. Create 1920×1200px canvas
2. Add title "Reference Architecture..." at top
3. Add Databricks logo to top-right
4. Create 4 vertical swim lane headers (dark teal)

### Phase 2: Swim Lane 1 (Source Data)
5. Add database cylinder icon
6. Add documents icon
7. Add SIEM header + Splunk + Datadog
8. Add Cloud Platform box with AWS/Azure/GCP

### Phase 3: Swim Lane 2 (Data Ingestion)
9. Add Delta Sharing icon
10. Add DLT Pipeline
11. Add Lakehouse Connect
12. Add Autoloader
13. Add 3rd Party Tools icon

### Phase 4: Swim Lane 3 (Databricks Lakehouse) - MAIN FOCUS
14. Add Unity Catalog icon (top-left)
15. Create DELTA LAKE gray container
16. Add Medallion Architecture (3 cylinders)
17. **CREATE DATABUCK DQ RED BOX** (2×2 grid)
    - Vector Search
    - Trust Score Engine
    - AI/ML Anomaly Detection
    - Circuit Breaker
18. Add Monitoring icon (top-right)
19. Add Model Hub box (bottom-left)
20. **CREATE DATABUCK AI GATEWAY RED BOX** (center-bottom)
21. Add External Models box (bottom-right)

### Phase 5: Swim Lane 4 (Engagement Layer)
22. Add Databricks Apps icon
23. Add AI/BI Dashboard Genie
24. Add Customized Web App
25. Add 3rd Party BI Tools

### Phase 6: Supporting Services (Bottom)
26. Add "Supporting Services" vertical label
27. Add 7 circular icons (80px each)
28. **EMPHASIZE Data Quality icon** with red background

### Phase 7: Connectors & Arrows
29. Add horizontal flow arrows (Source → Ingestion → Lakehouse → Engagement)
30. Add vertical arrows (Medallion → Databuck DQ → AI Gateway)
31. Add dashed red line (Databuck DQ → Unity Catalog)

### Phase 8: Final Polish
32. Add shadows to red-outlined boxes
33. Verify all fonts match specifications
34. Align all components to 10px grid
35. Export as .drawio and .png (1920px width)

---

## 14. FILE NAMING

**Draw.io File**: `03-databricks-lakehouse-horizontal-with-databuck.drawio`
**PNG Export**: `03-databricks-lakehouse-horizontal-with-databuck.png`
**Size**: 1920×1200px

---

## 15. SUCCESS CRITERIA

✅ **Layout matches reference architecture** (horizontal flow, vertical swim lanes)
✅ **Databuck emphasized with red outlines** (3 locations)
✅ **Professional Databricks color palette** (dark teal headers, blue components)
✅ **Clean visual hierarchy** (red > cylinders > standard > icons)
✅ **Supporting services at bottom** (7 circular icons)
✅ **Databricks branding present** (logo, colors, style)
✅ **All components labeled clearly** (11-16pt fonts)
✅ **Proper spacing and alignment** (10px grid)
✅ **Valid Draw.io XML** (opens without errors)

---

**Next Step**: Implement this plan to create `03-databricks-lakehouse-horizontal-with-databuck.drawio`
