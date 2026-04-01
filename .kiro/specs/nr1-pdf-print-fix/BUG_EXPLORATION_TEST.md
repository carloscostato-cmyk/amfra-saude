# Bug Condition Exploration Test - NR-1 PDF Print

## Test Objective
Confirm that the bug exists on UNFIXED code by demonstrating blank pages and missing content when printing NR-1 reports.

## Bug Condition
```
isBugCondition(input) = 
  (input.page = "admin_company_nr1.html" OR input.page = "admin_submission_detail.html")
  AND input.mediaType = "print"
```

## Test Procedure (UNFIXED CODE)

### Test Case 1: Company NR-1 Report - Consolidated Chart
1. Open browser and navigate to admin_company_nr1.html
2. Click "Imprimir Relatório" button
3. Observe print preview

**Expected Failure**: Blank space where consolidated horizontal bar chart should appear

### Test Case 2: Company NR-1 Report - Radar Chart
1. Same page as Test Case 1
2. Scroll to "Perfil das 7 Dimensões HSE-IT" section in print preview
3. Observe radar chart area

**Expected Failure**: Blank space where radar chart should appear

### Test Case 3: Individual Submission - Radar Chart
1. Open browser and navigate to admin_submission_detail.html
2. Click "Imprimir / PDF" button
3. Observe print preview

**Expected Failure**: Blank space where radar chart should appear

### Test Case 4: Missing KPIs
1. In print preview of either page
2. Observe KPI cards section

**Expected Failure**: KPI cards may be hidden or improperly styled

### Test Case 5: Missing Footer
1. In print preview of either page
2. Scroll through all pages
3. Look for footer at bottom of each page

**Expected Failure**: No footer "AMFRA SAÚDE MENTAL - Avaliação Clínica Digital" appears

### Test Case 6: Chart Page Breaks
1. In print preview with multi-page output
2. Observe if charts span across page boundaries

**Expected Failure**: Charts may break across pages making them unreadable

## Test Results (UNFIXED CODE)

**Status**: EXPECTED TO FAIL (this confirms the bug exists)

**Counterexamples Found**:
- [ ] Consolidated chart renders as blank space
- [ ] Radar chart (company) renders as blank space
- [ ] Radar chart (individual) renders as blank space
- [ ] KPI cards hidden or improperly styled
- [ ] Footer missing on all pages
- [ ] Charts break across page boundaries

## Root Cause Confirmation
- Missing @media print CSS rules for NR-1 classes
- Chart.js canvas elements require explicit print handling
- No page-break management for chart containers
- No footer CSS implementation

## Next Steps
Proceed to Task 2: Write preservation property tests
Then Task 3: Implement the fix
