# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Mobile Button Overlap
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: Test concrete failing cases at specific mobile viewports (375px, 360px, 720px)
  - Test that buttons in `.admin-shell__actions` appear below the title without overlap for viewports ≤ 720px
  - Test implementation details from Bug Condition in design:
    - Open `admin_company_detail.html` in browser
    - Use developer tools to simulate mobile viewports (375px, 360px, 720px)
    - Verify buttons "Visualizar Estudo NR-1" and "Sair" position relative to company title
    - Check for visual overlap using element inspector
  - The test assertions should match the Expected Behavior Properties from design:
    - Buttons SHALL appear below title without overlap
    - All elements SHALL be visible and readable
    - Layout SHALL be well-organized
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
  - Document counterexamples found:
    - iPhone SE (375px): buttons overlap title
    - Samsung Galaxy S20 (360px): buttons overlap title
    - Viewport 720px: buttons overlap title
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Desktop Layout Unchanged
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy inputs (viewports > 720px)
  - Test that desktop layout remains unchanged:
    - Open `admin_company_detail.html` in browser
    - Test viewports: 1920px, 1440px, 1024px, 721px
    - Verify buttons appear horizontally aligned to the right
    - Verify `.admin-shell__header` maintains flex layout
    - Take screenshots of current behavior for comparison
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements:
    - For all viewports > 720px, layout SHALL match original design
    - Buttons SHALL remain horizontally aligned to the right
    - Visual quality SHALL be preserved
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 3. Fix for mobile button overlap

  - [x] 3.1 Implement the CSS fix
    - Open `app/static/css/style.css`
    - Locate the `@media (max-width: 720px)` section (around line 1243)
    - Verify that `.admin-shell__header` already has `flex-direction: column` applied
    - Add or update styles for `.admin-shell__actions` within the media query:
      ```css
      .admin-shell__actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          width: 100%;
      }
      ```
    - Add or update styles for `.admin-shell__actions .button`:
      ```css
      .admin-shell__actions .button {
          flex: 1 1 auto;
          min-width: fit-content;
      }
      ```
    - Ensure visual order is: title → description → buttons (top to bottom)
    - Test responsiveness at multiple viewport widths (320px, 375px, 414px, 720px)
    - _Bug_Condition: isBugCondition(viewport) where viewport.width <= 720 AND page == 'admin_company_detail.html' AND buttonsOverlapTitle('.admin-shell__actions')_
    - _Expected_Behavior: Buttons SHALL appear below title without overlap, all elements visible and readable_
    - _Preservation: Desktop layout (viewport > 720px) SHALL remain unchanged with horizontal button alignment_
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4_

  - [x] 3.2 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Mobile Button Layout Fixed
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1:
      - Open `admin_company_detail.html` in browser with fixed CSS
      - Test viewports: 375px, 360px, 720px, 320px
      - Verify buttons appear below title without overlap
      - Verify all elements are visible and readable
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.3 Verify preservation tests still pass
    - **Property 2: Preservation** - Desktop Layout Preserved
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2:
      - Open `admin_company_detail.html` in browser with fixed CSS
      - Test viewports: 1920px, 1440px, 1024px, 721px
      - Compare with screenshots from unfixed code
      - Verify buttons remain horizontally aligned to the right
      - Verify no visual differences from original
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Cross-browser and device testing
  - Test the fix on multiple browsers:
    - Chrome (desktop and mobile simulation)
    - Firefox (desktop and mobile simulation)
    - Safari (iOS devices if available)
    - Edge (desktop)
  - Test on real devices if available:
    - iPhone (any model)
    - Android phone (any model)
    - iPad or Android tablet
  - Verify that buttons are clickable and functional after CSS fix
  - Test that other pages using `.admin-shell__header` are not affected
  - Document any browser-specific issues found
  - _Requirements: 2.1, 2.2, 3.3, 3.4_

- [x] 5. Checkpoint - Ensure all tests pass
  - Verify bug condition test passes (mobile layout fixed)
  - Verify preservation tests pass (desktop layout unchanged)
  - Verify cross-browser compatibility
  - Verify no regressions in other pages
  - Ask the user if questions arise
  - Prepare for deployment to Railway production environment
