# Bugfix Requirements Document

## Introduction

When users click "Imprimir Relatório" (Print Report) button on the NR-1 company report page (`admin_company_nr1.html`) or individual submission page (`admin_submission_detail.html`), the generated PDF contains blank pages and missing content. This bug affects the ability to generate professional PDF reports for clinical documentation and organizational health assessments.

The root causes include:
- Missing `@media print` CSS rules for NR-1 specific classes (`.nr1-page`, `.nr1-header`, `.nr1-kpis`, `.nr1-chart-container`, etc.)
- Chart.js canvas elements don't render in print media without explicit handling
- No page-break rules for chart containers causing layout issues
- Responsive CSS hiding content that should appear in print

This bugfix ensures that all NR-1 report content renders correctly in PDF format with proper layout, visible charts, and professional formatting suitable for clinical documentation.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a user clicks "Imprimir Relatório" on `admin_company_nr1.html` or "Imprimir / PDF" on `admin_submission_detail.html` THEN the system generates a PDF with blank pages where charts should appear

1.2 WHEN the print dialog is triggered for NR-1 reports THEN the system hides critical content (KPIs, tables, sections) due to missing print media CSS rules

1.3 WHEN Chart.js canvas elements (horizontal bar chart and radar chart) are rendered in print media THEN the system displays blank spaces because Chart.js requires explicit print event handling

1.4 WHEN chart containers span page boundaries during print THEN the system breaks charts across pages creating unreadable output

1.5 WHEN the PDF is generated THEN the system does not include a professional footer with company branding on each page

1.6 WHEN responsive CSS rules are applied during print THEN the system hides elements like `.nr1-table__bar-wrap` that should be visible in PDF output

1.7 WHEN print layout is rendered THEN the system does not optimize spacing, colors, and borders for A4 paper format

### Expected Behavior (Correct)

2.1 WHEN a user clicks "Imprimir Relatório" on `admin_company_nr1.html` or "Imprimir / PDF" on `admin_submission_detail.html` THEN the system SHALL generate a complete PDF with all charts rendered as static images

2.2 WHEN the print dialog is triggered for NR-1 reports THEN the system SHALL display all critical content (KPIs, tables, sections, legends) with print-optimized styling

2.3 WHEN Chart.js canvas elements are rendered in print media THEN the system SHALL convert charts to static images using Chart.js `beforePrint` and `afterPrint` event handlers

2.4 WHEN chart containers span page boundaries during print THEN the system SHALL apply `page-break-inside: avoid` to keep charts intact on single pages

2.5 WHEN the PDF is generated THEN the system SHALL include a professional footer on every page with a horizontal line and text "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital"

2.6 WHEN responsive CSS rules are evaluated during print THEN the system SHALL override mobile-specific hiding rules to ensure all content is visible in PDF

2.7 WHEN print layout is rendered THEN the system SHALL optimize layout for A4 paper with print-friendly colors, appropriate margins, and professional formatting

### Unchanged Behavior (Regression Prevention)

3.1 WHEN users view NR-1 reports in a web browser (screen media) THEN the system SHALL CONTINUE TO display the current responsive design with interactive charts

3.2 WHEN users interact with Chart.js charts on screen THEN the system SHALL CONTINUE TO provide tooltips, hover effects, and interactive features

3.3 WHEN users navigate between pages using action buttons THEN the system SHALL CONTINUE TO show all navigation buttons and controls on screen

3.4 WHEN the viewport is resized on screen THEN the system SHALL CONTINUE TO apply responsive CSS rules for mobile and tablet layouts

3.5 WHEN users view other admin pages (not NR-1 reports) THEN the system SHALL CONTINUE TO use existing print styles without modification

3.6 WHEN the print dialog is cancelled THEN the system SHALL CONTINUE TO display the page in its original screen format without artifacts

## Bug Condition Derivation

### Bug Condition Function

```pascal
FUNCTION isBugCondition(X)
  INPUT: X of type PrintRequest
  OUTPUT: boolean
  
  // Returns true when print is triggered for NR-1 report pages
  RETURN (X.page = "admin_company_nr1.html" OR X.page = "admin_submission_detail.html")
         AND X.mediaType = "print"
END FUNCTION
```

### Property Specification: Fix Checking

```pascal
// Property: Fix Checking - NR-1 Print Rendering
FOR ALL X WHERE isBugCondition(X) DO
  result ← renderPrint'(X)
  
  ASSERT result.chartsVisible = true
  ASSERT result.blankPages = 0
  ASSERT result.kpisVisible = true
  ASSERT result.tablesVisible = true
  ASSERT result.footerPresent = true
  ASSERT result.pageBreaksCorrect = true
  ASSERT result.contentComplete = true
END FOR
```

**Key Definitions:**
- **F**: The original (unfixed) rendering function - generates PDFs with blank pages and missing content
- **F'**: The fixed rendering function - generates complete PDFs with all content visible

### Property Specification: Preservation Checking

```pascal
// Property: Preservation Checking - Screen Display Unchanged
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT F(X) = F'(X)
END FOR

// Specifically:
// - Screen media rendering remains unchanged
// - Other admin pages print behavior unchanged
// - Interactive features on screen remain functional
// - Responsive behavior on screen remains unchanged
```

This ensures that for all non-print contexts (screen display) and non-NR-1 pages, the fixed code behaves identically to the original.

### Counterexample

**Concrete example demonstrating the bug:**

```
Input: User clicks "Imprimir Relatório" on admin_company_nr1.html
       with consolidated chart and radar chart visible

Current Output (F):
  - PDF page 1: Header and KPIs visible
  - PDF page 2: Blank space where consolidated chart should be
  - PDF page 3: Blank space where radar chart should be
  - PDF page 4: Table partially visible
  - No footer on any page

Expected Output (F'):
  - PDF page 1: Header, KPIs, legend, consolidated chart (rendered)
  - PDF page 2: Radar chart (rendered), dimension table
  - PDF page 3: Distribution section, risk ranking
  - Footer on all pages: "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital"
```
