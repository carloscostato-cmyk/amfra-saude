# NR-1 PDF/Print Bugfix Design

## Overview

This design addresses the blank pages and missing content issue when printing NR-1 reports to PDF. The fix implements comprehensive `@media print` CSS rules, Chart.js print event handlers, and a professional footer to ensure all report content renders correctly in PDF format suitable for clinical documentation.

The solution focuses on three core areas:
1. **CSS Print Styles**: Add print-specific rules for all NR-1 classes to ensure visibility and proper layout
2. **Chart.js Print Handling**: Convert canvas elements to static images during print using beforePrint/afterPrint events
3. **Professional Footer**: Add branded footer on every printed page with company identification

This approach ensures minimal changes to existing code while maximizing PDF output quality.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when print media is triggered for NR-1 report pages (admin_company_nr1.html or admin_submission_detail.html)
- **Property (P)**: The desired behavior - all charts, KPIs, tables, and sections render correctly in PDF with professional formatting
- **Preservation**: Existing screen display behavior and interactive features that must remain unchanged by the fix
- **@media print**: CSS media query that applies styles only when printing or generating PDFs
- **Chart.js beforePrint/afterPrint**: Event handlers that execute when print dialog opens/closes, used to convert canvas to static images
- **page-break-inside**: CSS property that prevents elements from breaking across page boundaries
- **A4 paper**: Standard paper size (210mm x 297mm) used for PDF optimization

## Bug Details

### Bug Condition

The bug manifests when a user clicks "Imprimir Relatório" on admin_company_nr1.html or "Imprimir / PDF" on admin_submission_detail.html. The browser's print media query is triggered, but the system lacks print-specific CSS rules for NR-1 classes, causing content to be hidden or improperly rendered. Chart.js canvas elements render as blank spaces because they require explicit print handling.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type PrintRequest
  OUTPUT: boolean
  
  RETURN (input.page = "admin_company_nr1.html" OR input.page = "admin_submission_detail.html")
         AND input.mediaType = "print"
         AND (chartCanvasExists(input.page) OR nr1ClassesPresent(input.page))
END FUNCTION
```

### Examples

- **Company NR-1 Report**: User clicks "Imprimir Relatório" → PDF shows blank space where consolidated horizontal bar chart should appear → Expected: Chart rendered as static image
- **Individual Submission**: User clicks "Imprimir / PDF" → PDF hides KPI cards and dimension table → Expected: All content visible with print-optimized styling
- **Chart Spanning Pages**: Radar chart breaks across page boundary → Expected: Chart kept intact on single page with page-break-inside: avoid
- **Missing Footer**: PDF pages have no company branding → Expected: "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital" footer on every page

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Screen display of NR-1 reports must continue to show responsive design with interactive Chart.js charts
- Hover effects, tooltips, and datalabels on charts must continue to work on screen
- Navigation buttons ("Voltar", "Copiar link") must continue to be visible on screen
- Responsive CSS breakpoints for mobile and tablet must continue to function on screen
- Other admin pages (not NR-1 reports) must continue to use existing print styles without modification

**Scope:**
All inputs that do NOT involve print media for NR-1 pages should be completely unaffected by this fix. This includes:
- Screen media rendering (default browser view)
- Print behavior for other admin pages (admin_dashboard.html, admin_company_detail.html, etc.)
- Interactive JavaScript functionality on screen
- Responsive layout behavior on screen

## Hypothesized Root Cause

Based on the bug description and code analysis, the root causes are:

1. **Missing Print CSS Rules**: The existing `@media print` block in style.css does not include rules for NR-1-specific classes (.nr1-page, .nr1-header, .nr1-kpis, .nr1-chart-container, etc.). These classes are defined only for screen media.

2. **Chart.js Canvas Rendering**: Chart.js uses HTML5 canvas elements which do not automatically render in print media. The canvas content is generated dynamically via JavaScript and requires explicit conversion to static images using Chart.js print event handlers.

3. **No Page Break Management**: Chart containers lack `page-break-inside: avoid` rules, causing charts to break across page boundaries and become unreadable.

4. **Missing Professional Footer**: No CSS rules exist to add a footer on printed pages using `@page` or fixed positioning techniques.

5. **Responsive CSS Conflicts**: Mobile-specific rules like `.nr1-table__bar-wrap { display: none; }` at max-width 600px may hide content that should be visible in PDF output.

## Correctness Properties

Property 1: Bug Condition - NR-1 Print Rendering

_For any_ print request where the bug condition holds (isBugCondition returns true), the fixed rendering function SHALL generate a complete PDF with all charts rendered as static images, all KPIs and tables visible, proper page breaks, and a professional footer on every page.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7**

Property 2: Preservation - Screen Display Unchanged

_For any_ rendering request where the bug condition does NOT hold (screen media or non-NR-1 pages), the fixed code SHALL produce exactly the same behavior as the original code, preserving all interactive features, responsive layouts, and existing print behavior for other pages.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

## Fix Implementation

### Changes Required

Assuming our root cause analysis is correct, we will implement the following changes:

**File 1**: `app/templates/admin_company_nr1.html`

**Location**: Inside the existing `<style>` block (after the responsive rules, before `</style>`)

**Specific Changes**:

1. **Add @media print CSS block** with comprehensive rules for all NR-1 classes:
   - Hide navigation buttons (.nr1-header__actions)
   - Optimize page layout (remove max-width, set margins)
   - Style KPI cards for print (remove shadows, add borders)
   - Ensure chart containers are visible with page-break-inside: avoid
   - Style tables for print (visible borders, no hover effects)
   - Add professional footer using @page or fixed positioning
   - Override responsive hiding rules

2. **Add Chart.js Print Event Handlers** in the existing `<script>` block:
   - Implement window.addEventListener('beforeprint') to convert charts to images
   - Implement window.addEventListener('afterprint') to restore interactive charts
   - Handle both consolidatedChart and radarChart instances

**File 2**: `app/templates/admin_submission_detail.html`

**Location**: Inside the existing `<style>` block (after the responsive rules, before `</style>`)

**Specific Changes**:

1. **Add @media print CSS block** with comprehensive rules for submission detail classes:
   - Hide navigation buttons (.sub-header__actions)
   - Optimize page layout for A4 paper
   - Style KPI cards, legend, and interpretation box for print
   - Ensure radar chart container is visible with page-break-inside: avoid
   - Style dimension table and answer items for print
   - Add professional footer matching company report
   - Override responsive hiding rules

2. **Add Chart.js Print Event Handlers** in the existing `<script>` block:
   - Implement beforeprint/afterprint handlers for radarChart
   - Ensure chart converts to static image during print

### Detailed CSS Implementation

**Print Styles Structure** (to be added to both files):

```css
@media print {
    /* ── Page Setup ────────────────────────── */
    @page {
        size: A4;
        margin: 20mm 15mm;
    }
    
    body {
        background: #fff;
        color: #000;
        font-size: 11pt;
        line-height: 1.4;
    }
    
    /* ── Hide Interactive Elements ─────────── */
    .nr1-header__actions,
    .sub-header__actions,
    button,
    .button {
        display: none !important;
    }
    
    /* ── Page Container ────────────────────── */
    .nr1-page,
    .sub-page {
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* ── Header ────────────────────────────── */
    .nr1-header,
    .sub-header {
        page-break-after: avoid;
        border-bottom: 2px solid #333;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* ── KPIs ──────────────────────────────── */
    .nr1-kpis,
    .sub-kpis {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        page-break-inside: avoid;
        margin-bottom: 1.5rem;
    }
    
    .nr1-kpi,
    .sub-kpi {
        border: 1px solid #ddd;
        background: #f9f9f9;
        page-break-inside: avoid;
    }
    
    /* ── Legend ────────────────────────────── */
    .nr1-legend,
    .sub-legend {
        page-break-inside: avoid;
        border: 1px solid #ddd;
        background: #f9f9f9;
    }
    
    /* ── Sections ──────────────────────────── */
    .nr1-section,
    .sub-section {
        page-break-inside: avoid;
        margin-bottom: 2rem;
    }
    
    .nr1-section__head,
    .sub-section__head {
        page-break-after: avoid;
    }
    
    /* ── Charts ────────────────────────────── */
    .nr1-chart-container,
    .sub-radar-wrap {
        page-break-inside: avoid !important;
        page-break-before: auto;
        page-break-after: auto;
        border: 1px solid #ddd;
        background: #fff;
        padding: 1rem;
    }
    
    canvas {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* ── Tables ────────────────────────────── */
    .nr1-table,
    .sub-table {
        page-break-inside: auto;
        border-collapse: collapse;
        width: 100%;
    }
    
    .nr1-table thead,
    .sub-table thead {
        display: table-header-group;
    }
    
    .nr1-table tr,
    .sub-table tr {
        page-break-inside: avoid;
    }
    
    .nr1-table td,
    .nr1-table th,
    .sub-table td,
    .sub-table th {
        border: 1px solid #ddd;
    }
    
    /* ── Progress Bars (ensure visible) ────── */
    .nr1-table__bar-wrap,
    .sub-progress {
        display: block !important;
        visibility: visible !important;
    }
    
    /* ── Distribution Grid ─────────────────── */
    .nr1-dist-grid {
        page-break-inside: avoid;
    }
    
    /* ── Risk List ─────────────────────────── */
    .nr1-risk-list,
    .sub-answers {
        page-break-inside: auto;
    }
    
    .nr1-risk-item,
    .sub-answer-item {
        page-break-inside: avoid;
    }
    
    /* ── Interpretation Grid ───────────────── */
    .sub-interp-grid {
        page-break-inside: avoid;
        display: block;
    }
    
    .sub-interp-box,
    .sub-radar-wrap {
        page-break-inside: avoid;
        margin-bottom: 1rem;
    }
    
    /* ── Professional Footer ───────────────── */
    @page {
        @bottom-center {
            content: "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital";
            font-size: 9pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 8pt;
        }
    }
    
    /* Fallback footer for browsers that don't support @page @bottom-center */
    body::after {
        content: "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital";
        display: block;
        text-align: center;
        font-size: 9pt;
        color: #666;
        border-top: 1px solid #ddd;
        padding-top: 8pt;
        margin-top: 2rem;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #fff;
    }
    
    /* ── Color Adjustments for Print ───────── */
    .nr1-kpi__value--baixo,
    .sub-kpi__value--baixo,
    .nr1-risk-item__avg--baixo {
        color: #c00 !important;
    }
    
    .nr1-kpi__value--medio,
    .sub-kpi__value--medio {
        color: #c60 !important;
    }
    
    .nr1-kpi__value--alto,
    .sub-kpi__value--alto,
    .nr1-risk-item__avg--alto {
        color: #060 !important;
    }
}
```

### Detailed JavaScript Implementation

**Chart.js Print Handlers** (to be added to both files):

```javascript
// Add this code inside the existing <script> block, after chart initialization

// Store chart instances globally for print handling
let consolidatedChartInstance = null; // For admin_company_nr1.html
let radarChartInstance = null; // For both files

// Update chart creation to store instance
// For consolidated chart (admin_company_nr1.html only):
consolidatedChartInstance = new Chart(ctx, { /* existing config */ });

// For radar chart (both files):
radarChartInstance = new Chart(radarCtx, { /* existing config */ });

// Print event handlers
window.addEventListener('beforeprint', function() {
    // Convert charts to static images before printing
    if (consolidatedChartInstance) {
        const canvas = consolidatedChartInstance.canvas;
        const imageData = canvas.toDataURL('image/png');
        const img = new Image();
        img.src = imageData;
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        canvas.style.display = 'none';
        canvas.parentNode.insertBefore(img, canvas);
        canvas.dataset.printImage = 'true';
    }
    
    if (radarChartInstance) {
        const canvas = radarChartInstance.canvas;
        const imageData = canvas.toDataURL('image/png');
        const img = new Image();
        img.src = imageData;
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        canvas.style.display = 'none';
        canvas.parentNode.insertBefore(img, canvas);
        canvas.dataset.printImage = 'true';
    }
});

window.addEventListener('afterprint', function() {
    // Restore interactive charts after printing
    if (consolidatedChartInstance) {
        const canvas = consolidatedChartInstance.canvas;
        if (canvas.dataset.printImage) {
            const img = canvas.previousSibling;
            if (img && img.tagName === 'IMG') {
                img.remove();
            }
            canvas.style.display = '';
            delete canvas.dataset.printImage;
        }
    }
    
    if (radarChartInstance) {
        const canvas = radarChartInstance.canvas;
        if (canvas.dataset.printImage) {
            const img = canvas.previousSibling;
            if (img && img.tagName === 'IMG') {
                img.remove();
            }
            canvas.style.display = '';
            delete canvas.dataset.printImage;
        }
    }
});
```

### Implementation Strategy

**Phase 1: Add Print CSS**
1. Open admin_company_nr1.html
2. Locate the closing `</style>` tag (after responsive rules)
3. Insert the complete @media print block before `</style>`
4. Repeat for admin_submission_detail.html

**Phase 2: Add Chart.js Print Handlers**
1. Open admin_company_nr1.html
2. Locate the chart initialization code inside `<script>` block
3. Store chart instances in variables (consolidatedChartInstance, radarChartInstance)
4. Add beforeprint and afterprint event listeners after chart creation
5. Repeat for admin_submission_detail.html (only radarChartInstance)

**Phase 3: Testing**
1. Open admin_company_nr1.html in browser
2. Click "Imprimir Relatório"
3. Verify charts appear as static images in print preview
4. Verify all KPIs, tables, and sections are visible
5. Verify footer appears on all pages
6. Repeat for admin_submission_detail.html

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code, then verify the fix works correctly and preserves existing behavior.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm or refute the root cause analysis. If we refute, we will need to re-hypothesize.

**Test Plan**: Open NR-1 report pages in browser, trigger print dialog, and observe the print preview. Document all missing content, blank spaces, and layout issues. Run these tests on the UNFIXED code to confirm the bug manifestation.

**Test Cases**:
1. **Company Report Consolidated Chart**: Open admin_company_nr1.html, click "Imprimir Relatório", observe blank space where horizontal bar chart should be (will fail on unfixed code)
2. **Company Report Radar Chart**: Same page, observe blank space where radar chart should be (will fail on unfixed code)
3. **Individual Submission Radar**: Open admin_submission_detail.html, click "Imprimir / PDF", observe blank space where radar chart should be (will fail on unfixed code)
4. **Missing KPIs**: Observe if KPI cards are hidden or improperly styled in print preview (will fail on unfixed code)
5. **Missing Footer**: Observe that no footer appears on any page (will fail on unfixed code)
6. **Chart Page Breaks**: Observe if charts break across page boundaries (may fail on unfixed code)

**Expected Counterexamples**:
- Chart canvas elements render as blank white spaces in print preview
- KPI cards may be hidden or have incorrect styling
- No footer appears on printed pages
- Charts may break across page boundaries
- Possible causes: missing @media print rules, no Chart.js print handlers, no page-break management

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed function produces the expected behavior.

**Pseudocode:**
```
FOR ALL input WHERE isBugCondition(input) DO
  result := renderPrint_fixed(input)
  ASSERT result.chartsVisible = true
  ASSERT result.blankPages = 0
  ASSERT result.kpisVisible = true
  ASSERT result.tablesVisible = true
  ASSERT result.footerPresent = true
  ASSERT result.pageBreaksCorrect = true
  ASSERT result.contentComplete = true
END FOR
```

**Test Plan**: After implementing the fix, open both NR-1 report pages, trigger print dialog, and verify all content renders correctly in print preview.

**Test Cases**:
1. **Company Report Full Render**: Verify consolidated chart, radar chart, KPIs, tables, and footer all appear correctly
2. **Individual Submission Full Render**: Verify radar chart, KPIs, dimension table, answer items, and footer all appear correctly
3. **Chart Quality**: Verify charts are rendered as high-quality static images, not pixelated
4. **Page Breaks**: Verify charts do not break across pages
5. **Footer on All Pages**: Verify footer appears on every page of multi-page PDFs
6. **Color Accuracy**: Verify risk level colors (red, orange, green) are visible and distinguishable in print

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL input WHERE NOT isBugCondition(input) DO
  ASSERT renderOriginal(input) = renderFixed(input)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the input domain
- It catches edge cases that manual unit tests might miss
- It provides strong guarantees that behavior is unchanged for all non-buggy inputs

**Test Plan**: Observe behavior on UNFIXED code first for screen display and other pages, then verify this behavior continues after fix.

**Test Cases**:
1. **Screen Display Preservation**: Observe that NR-1 reports display correctly on screen with interactive charts on unfixed code, then verify this continues after fix
2. **Chart Interactivity Preservation**: Observe that hovering over charts shows tooltips on unfixed code, then verify this continues after fix
3. **Responsive Layout Preservation**: Observe that resizing browser window triggers responsive breakpoints on unfixed code, then verify this continues after fix
4. **Other Pages Print Preservation**: Observe that printing admin_dashboard.html works correctly on unfixed code, then verify this continues after fix
5. **Navigation Buttons Preservation**: Observe that "Voltar" and "Copiar link" buttons are visible on screen on unfixed code, then verify this continues after fix

### Unit Tests

- Test that @media print rules are applied only in print media context
- Test that Chart.js beforeprint event converts canvas to image
- Test that Chart.js afterprint event restores interactive canvas
- Test that page-break-inside: avoid prevents chart splitting
- Test that footer CSS is applied in print media

### Property-Based Tests

- Generate random NR-1 report data and verify print rendering works correctly for all data variations
- Generate random screen sizes and verify responsive behavior is preserved on screen
- Test that all Chart.js chart types (bar, radar) convert correctly to images during print
- Verify that print behavior is consistent across different browsers (Chrome, Firefox, Safari)

### Integration Tests

- Test full workflow: load company report → click print → verify PDF contains all content → cancel print → verify screen display unchanged
- Test full workflow: load individual submission → click print → verify PDF contains all content → cancel print → verify screen display unchanged
- Test multi-page PDF generation with footer on all pages
- Test that PDF can be saved and reopened with all content intact
- Test that printed PDF is suitable for clinical documentation (professional appearance, readable text, clear charts)
