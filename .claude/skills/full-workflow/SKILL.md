---
name: full-workflow
description: Complete testing workflow from site discovery to test automation with Qase integration. Use when user wants end-to-end testing setup for a website. Triggers on "test this site", "create test suite for", "help me test", "full testing workflow", "automate testing for".
---

# Full Testing Workflow

Complete autonomous workflow: Discover → Design → Qase → Automate → Run

## Trigger Phrases

- "Test [URL]"
- "Create a test suite for [URL]"
- "Help me automate testing for [URL]"
- "I need tests for [website]"

## Prerequisites Check

Before starting, verify:

```
1. QASE_API_TOKEN is set
2. QASE_PROJECT_CODE is set
3. MCP config has Playwright server (mcp-config.json)
```

If missing, ask user to configure.

## Phase 1: DISCOVER

**Goal:** Map the website structure

**Use:** `site-discovery` + `mcp-client` skills (Playwright server)

```
1. Navigate to homepage (browser_navigate)
2. Take snapshot (browser_snapshot)
3. Extract navigation links
4. Visit each main section (max 20 pages for smoke)
5. Classify each page type
6. Document auth requirements
```

**Output:** Site map with classified pages

## Phase 2: DESIGN

**Goal:** Create test case specifications

**Use:** `automation-tester` skill

```
1. For each page type, apply test patterns
2. Assign priorities (P0/P1/P2)
3. Generate test case specs
4. Group into logical suites
```

**Output:** Test case list organized by suite

## Phase 3: SYNC TO QASE

**Goal:** Push test suites and cases to Qase.io

**Use:** `qase-client` skill

```bash
# Create suites
python qase_client.py create-suite PROJ '{"title": "Authentication"}'
python qase_client.py create-suite PROJ '{"title": "Navigation"}'
python qase_client.py create-suite PROJ '{"title": "Core Features"}'

# Create cases in each suite
python qase_client.py create-case PROJ '{"title": "Valid login redirects", "suite_id": 1, "severity": 1}'
# ... repeat for each case
```

**Output:** Qase case IDs mapped to test specs

## Phase 4: AUTOMATE

**Goal:** Generate Playwright test code

**Use:** `test-generation` skill

```
1. Create page objects for each tested page
2. Generate test specs for each suite
3. Link tests to Qase case IDs
4. Create playwright.config.ts if missing
```

**Output:**
```
pages/
├── login.page.ts
├── products.page.ts
tests/
├── auth.spec.ts
├── navigation.spec.ts
├── products.spec.ts
playwright.config.ts
```

## Phase 5: RUN & REPORT

**Goal:** Execute tests and report to Qase

```bash
# Install dependencies
npm install @playwright/test
npx playwright install chromium

# Run tests
npx playwright test

# Report results to Qase
python qase_client.py create-run PROJ '{"title": "Automated Run"}'
python qase_client.py report-result PROJ 1 '{"case_id": 1, "status": "passed"}'
python qase_client.py complete-run PROJ 1
```

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                      USER REQUEST                            │
│              "Test myplatform.com"                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: DISCOVER                                           │
│ • Navigate site via mcp-client (Playwright)                 │
│ • Map pages and classify types                              │
│ • Identify auth requirements                                │
│ Output: Site map                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: DESIGN                                             │
│ • Apply test patterns by page type                          │
│ • Assign P0/P1/P2 priorities                                │
│ • Group into suites                                         │
│ Output: Test case specifications                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: SYNC TO QASE                                       │
│ • Create suites via API                                     │
│ • Create cases with steps                                   │
│ • Record Qase IDs                                           │
│ Output: Cases in Qase.io                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: AUTOMATE                                           │
│ • Generate page objects                                     │
│ • Generate test specs                                       │
│ • Link to Qase IDs                                          │
│ Output: Playwright test files                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: RUN & REPORT                                       │
│ • Execute tests                                             │
│ • Create test run in Qase                                   │
│ • Report results                                            │
│ Output: Test results in Qase                                │
└─────────────────────────────────────────────────────────────┘
```

## Example Conversation

```
User: Test myplatform.com, we use Qase.io

Claude: I'll help you test myplatform.com with Qase integration.

**Setup Check**
✓ QASE_API_TOKEN detected
✓ QASE_PROJECT_CODE: MYPROJ
✓ Playwright MCP connected

**Phase 1: Discovery**
Exploring myplatform.com...

Found 8 key pages:
- / (Homepage)
- /login (Auth)
- /register (Auth)
- /products (Listing)
- /products/:id (Detail)
- /cart (Transaction)
- /checkout (Transaction)
- /account (Dashboard - requires auth)

**Phase 2: Design**
Designed 18 test cases across 4 suites:
- Authentication (5 cases)
- Navigation (3 cases)
- Products (6 cases)
- Cart (4 cases)

**Phase 3: Creating in Qase**
✓ Created suite "Authentication" (ID: 1)
✓ Created suite "Navigation" (ID: 2)
✓ Created suite "Products" (ID: 3)
✓ Created suite "Cart" (ID: 4)
✓ Created 18 test cases

View: https://app.qase.io/project/MYPROJ

**Phase 4: Generating Tests**
Created files:
- pages/login.page.ts
- pages/products.page.ts
- pages/cart.page.ts
- tests/auth.spec.ts
- tests/navigation.spec.ts
- tests/products.spec.ts
- tests/cart.spec.ts

**Phase 5: Ready to Run**
```bash
npm install
npx playwright test
```

Results will sync to Qase automatically.
```

## Decision Points

| Situation | Action |
|-----------|--------|
| No auth credentials | Test public pages only |
| Payment required | Test until payment step |
| Auth wall on first page | Ask for credentials |
| >50 pages found | Focus on main nav |
| Site errors | Document and continue |
