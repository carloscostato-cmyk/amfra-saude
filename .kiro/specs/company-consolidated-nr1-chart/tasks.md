# Tasks: Company Consolidated NR-1 Chart

## Phase 1: Backend Verification

### Task 1.1: Verify NR1StudyAgent Data Structure
- [ ] 1.1.1 Read `app/services/nr1_agent.py` and verify `risk_distribution` is returned
- [ ] 1.1.2 Verify classification keys are "BAIXO", "MÉDIO", "ALTO"
- [ ] 1.1.3 Verify counts are integers
- [ ] 1.1.4 Verify zero counts are included for missing classifications

### Task 1.2: Test Backend Data
- [ ] 1.2.1 Create test company with known submissions
- [ ] 1.2.2 Call `NR1StudyAgent.run_study()` and inspect output
- [ ] 1.2.3 Verify `risk_distribution` matches expected counts
- [ ] 1.2.4 Test with empty company (zero submissions)

## Phase 2: Frontend Implementation

### Task 2.1: Add Chart.js Datalabels Plugin
- [ ] 2.1.1 Add datalabels plugin CDN link to `admin_company_nr1.html` head section
- [ ] 2.1.2 Place after existing Chart.js script tag
- [ ] 2.1.3 Verify plugin loads without errors

### Task 2.2: Create Chart Container HTML
- [ ] 2.2.1 Add new section after KPIs, before "Níveis de Risco por Colaborador"
- [ ] 2.2.2 Add section header with kicker and title
- [ ] 2.2.3 Add chart container div with canvas element
- [ ] 2.2.4 Add conditional rendering (only when status is "success")

### Task 2.3: Add Chart CSS Styling
- [ ] 2.3.1 Add `.nr1-chart-container` styles to page `<style>` block
- [ ] 2.3.2 Set fixed height (300px desktop, 250px mobile)
- [ ] 2.3.3 Add responsive media query for mobile
- [ ] 2.3.4 Match existing design system (border, radius, padding)

### Task 2.4: Prepare Chart Data in Template
- [ ] 2.4.1 Create Jinja2 variables for labels, counts, colors
- [ ] 2.4.2 Loop through classifications in order: BAIXO, MÉDIO, ALTO
- [ ] 2.4.3 Extract counts from `report.risk_distribution`
- [ ] 2.4.4 Map colors: BAIXO=#ef4444, MÉDIO=#f59e0b, ALTO=#10b981
- [ ] 2.4.5 Convert to JSON for JavaScript consumption

### Task 2.5: Implement Chart.js Initialization
- [ ] 2.5.1 Add script block at end of template
- [ ] 2.5.2 Wrap in DOMContentLoaded event listener
- [ ] 2.5.3 Get canvas element by ID
- [ ] 2.5.4 Create Chart instance with configuration
- [ ] 2.5.5 Set chart type to 'bar' with indexAxis: 'y'
- [ ] 2.5.6 Configure datasets with data, colors, borders
- [ ] 2.5.7 Configure datalabels plugin for count and percentage
- [ ] 2.5.8 Configure scales (x-axis starts at 0, integer steps)
- [ ] 2.5.9 Disable legend (colors are self-explanatory)
- [ ] 2.5.10 Add try-catch for error handling

### Task 2.6: Add Accessibility Features
- [ ] 2.6.1 Add aria-label to canvas element
- [ ] 2.6.2 Add role="img" to canvas
- [ ] 2.6.3 Add aria-describedby with text description of data
- [ ] 2.6.4 Create hidden div with text description for screen readers
- [ ] 2.6.5 Verify color contrast meets WCAG AA standards

## Phase 3: Testing

### Task 3.1: Unit Tests (Backend)
- [ ] 3.1.1 Write test for distribution count accuracy
- [ ] 3.1.2 Write test for percentage calculation
- [ ] 3.1.3 Write test for zero submissions handling
- [ ] 3.1.4 Write test for all classifications present
- [ ] 3.1.5 Run tests and verify all pass

### Task 3.2: Integration Tests
- [ ] 3.2.1 Test chart renders with real data
- [ ] 3.2.2 Test chart does not render when status is "empty"
- [ ] 3.2.3 Test chart displays correct counts
- [ ] 3.2.4 Test chart displays correct percentages
- [ ] 3.2.5 Test chart uses correct colors

### Task 3.3: Browser Testing
- [ ] 3.3.1 Test on Chrome (latest)
- [ ] 3.3.2 Test on Firefox (latest)
- [ ] 3.3.3 Test on Safari (latest)
- [ ] 3.3.4 Test on Edge (latest)
- [ ] 3.3.5 Test on mobile Chrome (Android)
- [ ] 3.3.6 Test on mobile Safari (iOS)

### Task 3.4: Accessibility Testing
- [ ] 3.4.1 Run axe DevTools scan
- [ ] 3.4.2 Test with NVDA screen reader (Windows)
- [ ] 3.4.3 Test with VoiceOver (Mac)
- [ ] 3.4.4 Verify keyboard navigation
- [ ] 3.4.5 Test with 200% browser zoom
- [ ] 3.4.6 Verify color contrast ratios

### Task 3.5: Responsive Testing
- [ ] 3.5.1 Test at 1920px width (desktop)
- [ ] 3.5.2 Test at 1024px width (tablet)
- [ ] 3.5.3 Test at 768px width (tablet portrait)
- [ ] 3.5.4 Test at 375px width (mobile)
- [ ] 3.5.5 Verify chart adapts correctly at all sizes

### Task 3.6: Performance Testing
- [ ] 3.6.1 Measure page load time before and after
- [ ] 3.6.2 Measure chart initialization time
- [ ] 3.6.3 Check memory usage in DevTools
- [ ] 3.6.4 Verify no console errors
- [ ] 3.6.5 Test with 100+ submissions

## Phase 4: Documentation and Deployment

### Task 4.1: Update Documentation
- [ ] 4.1.1 Add chart feature to README (if applicable)
- [ ] 4.1.2 Document Chart.js dependency
- [ ] 4.1.3 Document datalabels plugin dependency
- [ ] 4.1.4 Add troubleshooting section for chart issues

### Task 4.2: Code Review
- [ ] 4.2.1 Review HTML structure and semantics
- [ ] 4.2.2 Review CSS for consistency with design system
- [ ] 4.2.3 Review JavaScript for best practices
- [ ] 4.2.4 Review accessibility implementation
- [ ] 4.2.5 Review error handling

### Task 4.3: Deploy to Railway
- [ ] 4.3.1 Commit changes to git
- [ ] 4.3.2 Push to Railway-connected branch
- [ ] 4.3.3 Monitor Railway build logs
- [ ] 4.3.4 Verify successful deployment
- [ ] 4.3.5 Test chart in production environment

### Task 4.4: Post-Deployment Verification
- [ ] 4.4.1 Load NR-1 report page in production
- [ ] 4.4.2 Verify chart displays correctly
- [ ] 4.4.3 Verify data accuracy
- [ ] 4.4.4 Check browser console for errors
- [ ] 4.4.5 Test on mobile device
- [ ] 4.4.6 Verify print functionality works

### Task 4.5: Monitoring
- [ ] 4.5.1 Monitor Railway logs for JavaScript errors
- [ ] 4.5.2 Monitor page load performance metrics
- [ ] 4.5.3 Collect user feedback (if applicable)
- [ ] 4.5.4 Document any issues found
- [ ] 4.5.5 Create tickets for future improvements

## Phase 5: Property-Based Testing (Optional)

### Task 5.1: Setup Hypothesis
- [ ] 5.1.1 Add hypothesis to requirements.txt
- [ ] 5.1.2 Install hypothesis in development environment
- [ ] 5.1.3 Create test file for property tests

### Task 5.2: Implement Property Tests
- [ ] 5.2.1 Write property test for distribution sum equals total
- [ ] 5.2.2 Write property test for percentages sum to 100
- [ ] 5.2.3 Write property test for all classifications present
- [ ] 5.2.4 Configure tests to run 100 iterations minimum
- [ ] 5.2.5 Add property test tags referencing design document

### Task 5.3: Run Property Tests
- [ ] 5.3.1 Run all property tests
- [ ] 5.3.2 Verify all tests pass
- [ ] 5.3.3 Review any edge cases found
- [ ] 5.3.4 Fix any bugs discovered
- [ ] 5.3.5 Re-run tests to confirm fixes

## Notes

- All tasks should be completed in order within each phase
- Phases can be executed sequentially or with some overlap
- Testing phase should not be skipped
- Property-based testing (Phase 5) is optional but recommended
- Deployment should only occur after all tests pass
