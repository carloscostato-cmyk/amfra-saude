# Design Document: Copy Link Button Improvements

## Overview

This design document specifies the technical implementation for improving the user experience of the "Copy Link" button in the company detail page (`admin_company_detail.html`). The feature enhances visual feedback when copying token links and prevents interaction with expired tokens.

### Context

The AMFRA system manages individual employee tokens for clinical assessment questionnaires. Each company has a table displaying tokens with their status (available/used). Currently, the copy button provides minimal feedback, and used tokens still display interactive elements that could confuse administrators.

### Goals

1. Provide clear visual feedback when a token link is successfully copied
2. Prevent interaction with expired (used) tokens through disabled button states
3. Maintain existing functionality and layout without breaking changes
4. Implement clean, maintainable CSS and JavaScript solutions

### Non-Goals

- Modifying the token generation or validation logic
- Changing the overall page layout or table structure
- Adding new token management features beyond button improvements
- Implementing clipboard API fallbacks for older browsers

## Architecture

### Component Overview

The implementation involves three main components:

1. **HTML Template** (`app/templates/admin_company_detail.html`)
   - Conditional rendering of button states based on token.used property
   - Button markup with data attributes for JavaScript interaction

2. **CSS Styles** (`app/static/css/style.css`)
   - Success state styling (green background, transition effects)
   - Disabled state styling (gray background, no-interaction cursor)
   - Transition animations for smooth state changes

3. **JavaScript Event Handlers** (inline script in `admin_company_detail.html`)
   - Copy to clipboard functionality
   - Success state management with timeout
   - Event listener attachment to copy buttons

### Data Flow

```
User Click → JavaScript Handler → Clipboard API → Success State → Timeout → Reset State
                                                ↓
                                          Visual Feedback (CSS)
```

For disabled tokens:
```
Template Render → Check token.used → Render Disabled Button → CSS Disabled Styles
```

## Components and Interfaces

### HTML Template Changes

**File:** `app/templates/admin_company_detail.html`

**Current Implementation:**
```html
<button type="button" class="button button--compact button--primary copy-token-btn" 
        data-token-url="{{ request.url_root }}q/{{ token.token }}">
    <span class="btn-text">Copiar Link</span>
    <span class="btn-text-copied" style="display:none;">✓ Copiado</span>
</button>
```

**Proposed Changes:**

1. Add conditional class for disabled state:
```html
{% if not token.used %}
    <button type="button" 
            class="button button--compact button--primary copy-token-btn" 
            data-token-url="{{ request.url_root }}q/{{ token.token }}">
        <span class="btn-text">Copiar Link</span>
        <span class="btn-text-copied" style="display:none;">✓ Copiado</span>
    </button>
{% else %}
    <button type="button" 
            class="button button--compact button--disabled" 
            disabled>
        Link Expirado
    </button>
{% endif %}
```

**Interface Contract:**
- Input: `token.used` (boolean) - Jinja2 template variable
- Output: Rendered button element with appropriate state classes
- Behavior: Conditionally renders interactive or disabled button based on token status

### CSS Style Definitions

**File:** `app/static/css/style.css`

**New CSS Classes:**

```css
/* Success state for copy button */
.button--success {
    background: linear-gradient(135deg, var(--healthy) 0%, #1f5d51 100%) !important;
    color: var(--text-inverse);
    box-shadow: 0 16px 34px rgba(47, 118, 103, 0.35);
    transition: all 0.3s ease;
}

/* Disabled state for expired tokens */
.button--disabled {
    background: #e5e7eb !important;
    color: #9ca3af !important;
    cursor: not-allowed !important;
    opacity: 0.6;
    box-shadow: none !important;
    border-color: #d1d5db !important;
}

.button--disabled:hover {
    transform: none !important;
    box-shadow: none !important;
}
```

**Design Rationale:**
- Uses existing CSS variable `--healthy` for success color consistency
- `!important` flags ensure state styles override base button styles
- Disabled state uses neutral gray palette to indicate non-interactivity
- Transitions provide smooth visual feedback

### JavaScript Implementation

**File:** `app/templates/admin_company_detail.html` (inline script section)

**Current Implementation:**
```javascript
document.querySelectorAll('.copy-token-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const url = this.dataset.tokenUrl;
        navigator.clipboard.writeText(url);
        
        const btnText = this.querySelector('.btn-text');
        const btnCopied = this.querySelector('.btn-text-copied');
        
        btnText.style.display = 'none';
        btnCopied.style.display = 'inline';
        
        setTimeout(() => {
            btnText.style.display = 'inline';
            btnCopied.style.display = 'none';
        }, 2000);
    });
});
```

**Proposed Enhancement:**
```javascript
document.querySelectorAll('.copy-token-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const url = this.dataset.tokenUrl;
        navigator.clipboard.writeText(url);
        
        const btnText = this.querySelector('.btn-text');
        const btnCopied = this.querySelector('.btn-text-copied');
        
        // Add success state class
        this.classList.add('button--success');
        this.classList.remove('button--primary');
        
        // Toggle text visibility
        btnText.style.display = 'none';
        btnCopied.style.display = 'inline';
        
        // Reset after 2 seconds
        setTimeout(() => {
            this.classList.remove('button--success');
            this.classList.add('button--primary');
            btnText.style.display = 'inline';
            btnCopied.style.display = 'none';
        }, 2000);
    });
});
```

**Interface Contract:**
- Input: Click event on `.copy-token-btn` elements
- Output: Clipboard write operation, CSS class manipulation, text content toggle
- Side Effects: Modifies button appearance for 2 seconds, copies URL to clipboard
- Error Handling: Relies on browser's clipboard API (no explicit error handling in this iteration)

## Data Models

### Token Model (Existing)

**File:** `app/models.py` (reference only, no changes)

```python
class EmployeeToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)  # Key property for button state
    employee_name = db.Column(db.String(200))
    used_at = db.Column(db.DateTime)
```

**Relevant Properties:**
- `used` (Boolean): Determines button state (interactive vs disabled)
- `token` (String): Used to construct the copy URL
- `employee_name` (String): Display information (not used in button logic)
- `used_at` (DateTime): Display information (not used in button logic)

### Button State Model (Conceptual)

The button has three distinct states:

```typescript
type ButtonState = 
  | { type: 'normal', interactive: true, classes: ['button--primary'] }
  | { type: 'success', interactive: true, classes: ['button--success'], duration: 2000 }
  | { type: 'disabled', interactive: false, classes: ['button--disabled'] }
```

**State Transitions:**
- `normal` → `success`: On successful clipboard write
- `success` → `normal`: After 2000ms timeout
- `disabled`: Terminal state (no transitions, token.used === true)


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Clipboard Write on Click

*For any* copy button in normal state with a valid token URL, when clicked, the button SHALL write the token URL to the system clipboard.

**Validates: Requirements 1.1**

### Property 2: Success State Visual Feedback

*For any* copy button that successfully writes to the clipboard, the button SHALL immediately display both visual indicators of success: the CSS class `button--success` SHALL be applied AND the text content SHALL change to "✓ Copiado".

**Validates: Requirements 1.2, 1.3**

### Property 3: Success State Duration

*For any* copy button in success state, the button SHALL maintain the success visual state (green background and "✓ Copiado" text) for exactly 2000 milliseconds before transitioning back to normal state.

**Validates: Requirements 1.4**

### Property 4: Complete State Reset After Timeout

*For any* copy button that has entered success state, after exactly 2000 milliseconds, the button SHALL return to its original state with all original properties restored: the `button--primary` class SHALL be present, the `button--success` class SHALL be removed, and the text content SHALL be "Copiar Link".

**Validates: Requirements 1.5, 1.6**

### Property 5: Conditional Rendering Based on Token Status

*For any* token in the token table, if the token's `used` property is `True`, then the rendered button SHALL have the `disabled` attribute and the `button--disabled` class; if the token's `used` property is `False`, then the rendered button SHALL have the `button--primary` class and no `disabled` attribute.

**Validates: Requirements 2.1, 2.7**

### Property 6: Disabled Button Text Content

*For any* button rendered in disabled state (token.used === True), the button's text content SHALL be "Link Expirado".

**Validates: Requirements 2.2**

### Property 7: Disabled Button Styling Properties

*For any* button rendered in disabled state, the button SHALL have all disabled styling properties applied: gray background color, reduced opacity, cursor style "not-allowed", and no transform animation on hover.

**Validates: Requirements 2.3, 2.5, 2.6**

### Property 8: Disabled Button Non-Interactivity

*For any* button rendered in disabled state, clicking the button SHALL NOT trigger any clipboard write operation and SHALL NOT change the button's visual state.

**Validates: Requirements 2.4**

### Example Test 1: Success CSS Class Definition

The CSS stylesheet SHALL contain a `.button--success` class definition that includes:
- Background using CSS variable `--healthy` or equivalent green color
- Color set to `--text-inverse` or white
- Box shadow with green tint
- Transition property for smooth state changes

**Validates: Requirements 3.1**

### Example Test 2: Disabled CSS Class Definition

The CSS stylesheet SHALL contain a `.button--disabled` class definition that includes:
- Gray background color (#e5e7eb or similar)
- Gray text color (#9ca3af or similar)
- Cursor property set to "not-allowed"
- Reduced opacity (0.6 or similar)
- Hover pseudo-class that prevents transform animations

**Validates: Requirements 3.2, 3.3, 3.4**

## Error Handling

### Clipboard API Failures

**Scenario:** Browser denies clipboard access or clipboard API is unavailable

**Current Behavior:** The implementation uses `navigator.clipboard.writeText()` without explicit error handling. If the operation fails, the success state will still be triggered, creating a false positive.

**Proposed Handling:**
```javascript
btn.addEventListener('click', async function() {
    const url = this.dataset.tokenUrl;
    
    try {
        await navigator.clipboard.writeText(url);
        // Success state logic here
    } catch (err) {
        console.error('Failed to copy:', err);
        // Optionally show error state (future enhancement)
    }
});
```

**Decision:** For this iteration, we will add error logging but not implement error UI feedback. The existing behavior (showing success even on failure) is acceptable for the current use case since:
1. Clipboard API is widely supported in modern browsers
2. The admin interface is used in controlled environments
3. Adding error UI would require additional design work

### Disabled Button Click Attempts

**Scenario:** User clicks on a disabled button

**Handling:** The HTML `disabled` attribute prevents click events from firing. No additional JavaScript handling is needed. The CSS cursor style provides visual feedback that the button is not interactive.

### Race Conditions in State Transitions

**Scenario:** User rapidly clicks the copy button multiple times

**Current Behavior:** Each click starts a new 2-second timeout. Multiple timeouts could overlap, causing unpredictable state transitions.

**Proposed Handling:**
```javascript
let resetTimeout = null;

btn.addEventListener('click', async function() {
    // Clear any existing timeout
    if (resetTimeout) {
        clearTimeout(resetTimeout);
    }
    
    const url = this.dataset.tokenUrl;
    await navigator.clipboard.writeText(url);
    
    // Apply success state
    this.classList.add('button--success');
    this.classList.remove('button--primary');
    btnText.style.display = 'none';
    btnCopied.style.display = 'inline';
    
    // Set new timeout
    resetTimeout = setTimeout(() => {
        this.classList.remove('button--success');
        this.classList.add('button--primary');
        btnText.style.display = 'inline';
        btnCopied.style.display = 'none';
        resetTimeout = null;
    }, 2000);
});
```

**Decision:** Implement timeout clearing to prevent race conditions. This ensures only one timeout is active per button at any time.

### Missing DOM Elements

**Scenario:** JavaScript tries to access `.btn-text` or `.btn-text-copied` elements that don't exist

**Handling:** The current implementation assumes these elements exist. If they're missing, the code will fail silently (setting `style.display` on `null` doesn't throw an error, but the feature won't work).

**Proposed Handling:** Add defensive checks:
```javascript
const btnText = this.querySelector('.btn-text');
const btnCopied = this.querySelector('.btn-text-copied');

if (!btnText || !btnCopied) {
    console.error('Button text elements not found');
    return;
}
```

**Decision:** Add defensive checks to prevent silent failures and aid debugging.

## Testing Strategy

### Dual Testing Approach

This feature will be tested using both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests** will verify specific examples, edge cases, and integration points
- **Property tests** will verify universal properties across randomized inputs
- Together, they provide comprehensive coverage where unit tests catch concrete bugs and property tests verify general correctness

### Unit Testing

**Framework:** Jest with jsdom for DOM manipulation testing

**Test Categories:**

1. **CSS Class Existence Tests** (Example Tests)
   - Verify `.button--success` class exists in stylesheet
   - Verify `.button--disabled` class exists in stylesheet
   - Verify class properties match specifications

2. **Template Rendering Tests**
   - Test button rendering with `token.used = True`
   - Test button rendering with `token.used = False`
   - Verify correct classes and attributes are applied

3. **Edge Cases**
   - Rapid clicking (race condition handling)
   - Missing DOM elements (defensive checks)
   - Clipboard API unavailable

4. **Integration Tests**
   - Full click-to-copy-to-reset cycle
   - Multiple buttons on same page
   - Interaction with existing page JavaScript

### Property-Based Testing

**Framework:** fast-check (JavaScript property-based testing library)

**Configuration:** Minimum 100 iterations per property test

**Property Tests:**

1. **Property 1: Clipboard Write on Click**
   ```javascript
   // Feature: copy-link-button-improvements, Property 1: Clipboard Write on Click
   fc.assert(
     fc.asyncProperty(fc.webUrl(), async (tokenUrl) => {
       const button = createMockButton(tokenUrl, false);
       await simulateClick(button);
       const clipboardContent = await navigator.clipboard.readText();
       return clipboardContent === tokenUrl;
     }),
     { numRuns: 100 }
   );
   ```

2. **Property 2: Success State Visual Feedback**
   ```javascript
   // Feature: copy-link-button-improvements, Property 2: Success State Visual Feedback
   fc.assert(
     fc.asyncProperty(fc.webUrl(), async (tokenUrl) => {
       const button = createMockButton(tokenUrl, false);
       await simulateClick(button);
       const hasSuccessClass = button.classList.contains('button--success');
       const hasSuccessText = button.querySelector('.btn-text-copied').style.display !== 'none';
       return hasSuccessClass && hasSuccessText;
     }),
     { numRuns: 100 }
   );
   ```

3. **Property 3: Success State Duration**
   ```javascript
   // Feature: copy-link-button-improvements, Property 3: Success State Duration
   fc.assert(
     fc.asyncProperty(fc.webUrl(), async (tokenUrl) => {
       const button = createMockButton(tokenUrl, false);
       await simulateClick(button);
       
       // Check state at 1900ms (should still be in success state)
       await sleep(1900);
       const stillInSuccessState = button.classList.contains('button--success');
       
       // Check state at 2100ms (should be reset)
       await sleep(200);
       const hasReset = !button.classList.contains('button--success');
       
       return stillInSuccessState && hasReset;
     }),
     { numRuns: 100 }
   );
   ```

4. **Property 4: Complete State Reset After Timeout**
   ```javascript
   // Feature: copy-link-button-improvements, Property 4: Complete State Reset After Timeout
   fc.assert(
     fc.asyncProperty(fc.webUrl(), async (tokenUrl) => {
       const button = createMockButton(tokenUrl, false);
       const originalState = captureButtonState(button);
       
       await simulateClick(button);
       await sleep(2100);
       
       const resetState = captureButtonState(button);
       return statesAreEqual(originalState, resetState);
     }),
     { numRuns: 100 }
   );
   ```

5. **Property 5: Conditional Rendering Based on Token Status**
   ```javascript
   // Feature: copy-link-button-improvements, Property 5: Conditional Rendering Based on Token Status
   fc.assert(
     fc.property(
       fc.record({
         tokenUrl: fc.webUrl(),
         used: fc.boolean()
       }),
       ({ tokenUrl, used }) => {
         const button = renderButtonFromTemplate(tokenUrl, used);
         
         if (used) {
           return button.hasAttribute('disabled') && 
                  button.classList.contains('button--disabled');
         } else {
           return !button.hasAttribute('disabled') && 
                  button.classList.contains('button--primary');
         }
       }
     ),
     { numRuns: 100 }
   );
   ```

6. **Property 6: Disabled Button Text Content**
   ```javascript
   // Feature: copy-link-button-improvements, Property 6: Disabled Button Text Content
   fc.assert(
     fc.property(fc.webUrl(), (tokenUrl) => {
       const button = renderButtonFromTemplate(tokenUrl, true);
       return button.textContent.trim() === 'Link Expirado';
     }),
     { numRuns: 100 }
   );
   ```

7. **Property 7: Disabled Button Styling Properties**
   ```javascript
   // Feature: copy-link-button-improvements, Property 7: Disabled Button Styling Properties
   fc.assert(
     fc.property(fc.webUrl(), (tokenUrl) => {
       const button = renderButtonFromTemplate(tokenUrl, true);
       const styles = window.getComputedStyle(button);
       
       const hasGrayBackground = styles.backgroundColor.includes('229, 231, 235'); // #e5e7eb
       const hasNotAllowedCursor = styles.cursor === 'not-allowed';
       const hasReducedOpacity = parseFloat(styles.opacity) < 1;
       
       // Simulate hover and check no transform
       button.dispatchEvent(new MouseEvent('mouseenter'));
       const hoverStyles = window.getComputedStyle(button);
       const noTransform = hoverStyles.transform === 'none';
       
       return hasGrayBackground && hasNotAllowedCursor && hasReducedOpacity && noTransform;
     }),
     { numRuns: 100 }
   );
   ```

8. **Property 8: Disabled Button Non-Interactivity**
   ```javascript
   // Feature: copy-link-button-improvements, Property 8: Disabled Button Non-Interactivity
   fc.assert(
     fc.asyncProperty(fc.webUrl(), async (tokenUrl) => {
       const button = renderButtonFromTemplate(tokenUrl, true);
       const initialClipboard = await navigator.clipboard.readText();
       
       await simulateClick(button);
       
       const finalClipboard = await navigator.clipboard.readText();
       const clipboardUnchanged = initialClipboard === finalClipboard;
       const stateUnchanged = !button.classList.contains('button--success');
       
       return clipboardUnchanged && stateUnchanged;
     }),
     { numRuns: 100 }
   );
   ```

### Test Helpers

```javascript
// Helper functions for property tests
function createMockButton(tokenUrl, isDisabled) {
  const button = document.createElement('button');
  button.className = isDisabled ? 'button button--disabled' : 'button button--primary copy-token-btn';
  button.dataset.tokenUrl = tokenUrl;
  if (isDisabled) button.disabled = true;
  
  const btnText = document.createElement('span');
  btnText.className = 'btn-text';
  btnText.textContent = 'Copiar Link';
  
  const btnCopied = document.createElement('span');
  btnCopied.className = 'btn-text-copied';
  btnCopied.textContent = '✓ Copiado';
  btnCopied.style.display = 'none';
  
  button.appendChild(btnText);
  button.appendChild(btnCopied);
  
  return button;
}

function captureButtonState(button) {
  return {
    classes: Array.from(button.classList),
    textContent: button.textContent,
    btnTextDisplay: button.querySelector('.btn-text')?.style.display,
    btnCopiedDisplay: button.querySelector('.btn-text-copied')?.style.display
  };
}

function statesAreEqual(state1, state2) {
  return JSON.stringify(state1) === JSON.stringify(state2);
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Testing Balance

- **Unit tests** focus on specific scenarios and edge cases (CSS class definitions, template rendering, error conditions)
- **Property tests** verify universal behaviors across many randomized inputs (state transitions, conditional rendering, timing)
- Avoid writing too many unit tests for behaviors already covered by property tests
- Property tests handle comprehensive input coverage through randomization

### Test Execution

- Run tests in CI/CD pipeline on every commit
- Property tests run with 100 iterations minimum
- Use jsdom for DOM manipulation in Node.js test environment
- Mock clipboard API for testing environments

## Implementation Notes

### Browser Compatibility

- Clipboard API (`navigator.clipboard`) requires HTTPS or localhost
- Supported in all modern browsers (Chrome 66+, Firefox 63+, Safari 13.1+)
- No fallback to `document.execCommand('copy')` in this iteration

### Performance Considerations

- CSS transitions are GPU-accelerated (transform, opacity)
- Timeout management prevents memory leaks from abandoned timeouts
- Event listeners are attached once on page load, not per interaction

### Accessibility

- Disabled buttons are properly marked with `disabled` attribute for screen readers
- Color changes are supplemented with text changes ("✓ Copiado") for color-blind users
- Cursor changes provide visual feedback for keyboard and mouse users

### Future Enhancements

1. **Error State Feedback:** Visual indication when clipboard write fails
2. **Keyboard Support:** Allow copying via keyboard shortcut (Ctrl+C when button focused)
3. **Toast Notifications:** Global notification system for copy confirmations
4. **Analytics:** Track copy button usage and success rates
5. **Batch Copy:** Select multiple tokens and copy all links at once
