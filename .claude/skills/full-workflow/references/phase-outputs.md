# Phase Outputs Reference

Expected outputs from each phase of the workflow.

## Phase 0: Existing Coverage Check

**Output Format:**
```markdown
## Existing Qase Coverage

### Suites Found
- Suite "Authentication" (ID: 1) - 3 cases
- Suite "Navigation" (ID: 2) - 2 cases

### Existing Cases
| ID | Suite | Title | Severity |
|----|-------|-------|----------|
| 1 | Authentication | Login with valid credentials | Critical |
| 2 | Authentication | Login with invalid password | Critical |
| 3 | Authentication | Logout successfully | High |
| 4 | Navigation | Main menu links work | Critical |
| 5 | Navigation | Footer links work | Medium |

### Coverage Gaps Identified
- No registration tests
- No product listing tests
- No cart/checkout tests
- No negative validation tests

### Decision
Partial coverage exists. Will create cases for gaps only.
Reusing case IDs: 1, 2, 3, 4, 5
```

## Phase 1: Site Discovery

**Output Format:**
```markdown
# Site Map: example.com

## Statistics
- Pages discovered: 12
- Requires auth: 4
- Critical paths: 3

## Pages

### Authentication (P0)
| URL | Type | Auth Required | Notes |
|-----|------|---------------|-------|
| /login | Login | No | Redirects to login.example.com |
| /register | Registration | No | Multi-step form |
| /forgot-password | Password Reset | No | Email verification |

### Core Features (P0)
| URL | Type | Auth Required | Notes |
|-----|------|---------------|-------|
| / | Homepage | No | Cookie banner on first visit |
| /products | Listing | No | Pagination, filters |
| /products/:id | Detail | No | Add to cart button |
| /cart | Cart | No | Requires items |

### User Area (P1)
| URL | Type | Auth Required | Notes |
|-----|------|---------------|-------|
| /account | Dashboard | Yes | Profile, orders |
| /orders | Order History | Yes | Filterable |
| /settings | Settings | Yes | Password change |

## URL Patterns
- /products/:id - Product detail pages
- /category/:slug - Category listing pages

## Navigation Behavior
- Category links open submenus → click "View all" to navigate
- User menu requires click to reveal dropdown
- Mobile menu is hamburger icon

## Auth Barriers
- /account/* requires login
- /checkout requires login
- /orders requires login
```

## Phase 1.5: Behavioral Data Discovery

**Output Format:**
```markdown
## Discovered UI Behaviors

### Login Error States

#### Invalid Credentials
- **Trigger:** Submit with wrong email/password
- **Error text:** "Email sau parolă incorectă"
- **Element:** `[role="alert"]`
- **Selector:** `page.getByRole('alert')`

#### Empty Email
- **Trigger:** Submit with empty email field
- **Validation type:** HTML5 native
- **Message:** "Please fill out this field"
- **Check:** `el.validity.valueMissing === true`

#### Invalid Email Format
- **Trigger:** Submit with "not-an-email"
- **Validation type:** HTML5 native
- **Message:** "Please include an '@' in the email address"
- **Check:** `el.validity.typeMismatch === true`

#### Empty Password
- **Trigger:** Submit with empty password
- **Validation type:** HTML5 native
- **Message:** "Please fill out this field"
- **Check:** `el.validity.valueMissing === true`

### Form Validation

#### Search
- **Empty search:** Submits, shows "No results"
- **Success:** URL changes to `/search?q={query}`

### Success States

#### Login Success
- **Redirect URL:** `/dashboard` or `/account`
- **Cookie set:** `session_id`

#### Add to Cart Success
- **Response:** Toast notification "Added to cart"
- **UI change:** Cart count increments
```

## Phase 2: Test Design

**Output Format:**
```markdown
## Test Cases Design

### Suite: Authentication (ID: 1)

#### Existing Cases (reuse)
- [1] Login with valid credentials
- [2] Login with invalid password
- [3] Logout successfully

#### New Cases (to create)
| Priority | Title | Preconditions | Steps | Expected |
|----------|-------|---------------|-------|----------|
| P0 | Empty email shows validation | On login page | 1. Leave email empty 2. Click submit | HTML5 validation message |
| P0 | Invalid email format shows error | On login page | 1. Enter "invalid" 2. Click submit | HTML5 format validation |
| P1 | Empty password shows validation | On login page | 1. Enter valid email 2. Leave password empty 3. Click submit | HTML5 validation message |
| P1 | Forgot password link works | On login page | 1. Click "Forgot password" | Navigate to reset page |

### Suite: Landing Page (ID: 2 - NEW)

| Priority | Title | Preconditions | Steps | Expected |
|----------|-------|---------------|-------|----------|
| P0 | Homepage loads successfully | None | 1. Navigate to / | Title contains "Example", search visible |
| P0 | Search returns results | On homepage | 1. Enter "test" 2. Click search | URL contains search query |
| P1 | Category navigation works | On homepage | 1. Click category 2. Click "View all" | Navigate to category page |
```

## Phase 3: Qase Sync

**Output Format:**
```markdown
## Qase Sync Results

### Suites
| Action | Title | ID |
|--------|-------|-----|
| Existing | Authentication | 1 |
| Created | Landing Page | 6 |
| Created | Products | 7 |

### Cases Created
| Suite | Title | Qase ID | Severity |
|-------|-------|---------|----------|
| Authentication | Empty email shows validation | 51 | Critical |
| Authentication | Invalid email format shows error | 52 | Critical |
| Authentication | Empty password shows validation | 53 | High |
| Authentication | Forgot password link works | 54 | Medium |
| Landing Page | Homepage loads successfully | 55 | Critical |
| Landing Page | Search returns results | 56 | Critical |

### Complete Case ID Mapping
| Test | Qase ID | Status |
|------|---------|--------|
| Login valid credentials | 1 | Existing |
| Login invalid password | 2 | Existing |
| Empty email validation | 51 | New |
| Invalid email format | 52 | New |
| Homepage loads | 55 | New |
| Search works | 56 | New |
```

## Phase 4: Automation

**Output Format:**
```markdown
## Generated Files

### Page Objects
- `pages/login.page.ts` - Login page interactions
- `pages/landing.page.ts` - Homepage interactions
- `pages/products.page.ts` - Product listing interactions

### Test Specs
- `tests/auth-negative.spec.ts` - Authentication negative tests (IDs: 51-54)
- `tests/landing.spec.ts` - Landing page tests (IDs: 55-56)
- `tests/products.spec.ts` - Product tests (IDs: 57-60)

### Config
- `playwright.config.ts` - Updated with Qase reporter
```

**Example Generated Test:**
```typescript
// tests/auth-negative.spec.ts
import { test, expect } from '@playwright/test';
import { qase } from 'playwright-qase-reporter';
import { LoginPage } from '../pages/login.page';

test.describe('Authentication - Negative Tests', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.acceptCookies();
  });

  test(qase(51, 'Empty email shows validation error'), async () => {
    await loginPage.clickLogin();
    const validationMessage = await loginPage.emailInput.evaluate(
      (el: HTMLInputElement) => el.validationMessage
    );
    expect(validationMessage).toBeTruthy();
  });

  test(qase(52, 'Invalid credentials shows error'), async () => {
    await loginPage.login('fake@test.com', 'wrongpass');
    // Using DISCOVERED error text
    await expect(loginPage.page.getByRole('alert'))
      .toContainText('Email sau parolă incorectă');
  });
});
```

## Phase 5: Run Results

**Output Format:**
```markdown
## Test Run Results

### Summary
- Total: 10 tests
- Passed: 9
- Failed: 1
- Skipped: 0

### Results by Suite
| Suite | Passed | Failed |
|-------|--------|--------|
| Authentication | 5 | 1 |
| Landing Page | 4 | 0 |

### Failed Tests
| Test | Error | Action |
|------|-------|--------|
| Invalid credentials shows error | Timeout waiting for alert | Use test-fixer |

### Next Steps
1. Run test-fixer skill for failed test
2. Re-run failed test after fix
3. Sync results to Qase
```
