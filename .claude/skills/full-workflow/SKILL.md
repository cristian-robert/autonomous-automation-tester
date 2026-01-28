---
name: full-workflow
description: Complete testing workflow from site discovery to test automation with Qase integration. Use when user wants end-to-end testing setup for a website. Triggers on "test this site", "create test suite for", "help me test", "full testing workflow", "automate testing for".
---

# Full Testing Workflow

Complete autonomous workflow: Check Existing → Discover → Design → Qase → Automate → Run

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

## Phase 0: CHECK EXISTING (MANDATORY)

**Goal:** Check Qase for existing test cases before creating new ones

**Use:** `qase-client` skill

```bash
# Search for existing cases by feature keywords
python scripts/qase_client.py search-cases PROJ "login"
python scripts/qase_client.py search-cases PROJ "navigation"
python scripts/qase_client.py search-cases PROJ "homepage"

# List existing suites
python scripts/qase_client.py suites PROJ

# Get details of existing cases if needed
python scripts/qase_client.py get-case PROJ <case_id>
```

**Output:**
- List of existing test cases and their coverage
- Gaps that need new test cases
- Existing Qase case IDs to reuse for automation

**Decision:**
- If comprehensive coverage exists → Skip to Phase 4 (Automate)
- If partial coverage exists → Note existing IDs, create only missing cases
- If no coverage exists → Continue with full workflow

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
│ PHASE 0: CHECK EXISTING (MANDATORY)                         │
│ • Search Qase for existing test cases                       │
│ • Identify existing coverage                                │
│ • Note gaps and reusable case IDs                          │
│ Output: Existing coverage + gaps list                       │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
          (if full coverage)    (if gaps exist)
                    │                   │
                    ▼                   ▼
          Skip to Phase 4      Continue workflow
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
│ • Group into suites (skip existing cases)                   │
│ Output: Test case specifications (gaps only)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: SYNC TO QASE                                       │
│ • Create suites via API (only if not exists)                │
│ • Create cases with steps (gaps only)                       │
│ • Record Qase IDs (existing + new)                          │
│ Output: Complete case ID mapping                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: AUTOMATE                                           │
│ • Generate page objects                                     │
│ • Generate test specs                                       │
│ • Link to Qase IDs (existing + new)                         │
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

**Phase 0: Checking Existing Cases**
Searching Qase for existing test cases...

Found existing coverage:
- Suite "Authentication" (ID: 1) - 3 cases
  - Login with valid credentials (ID: 1)
  - Login with invalid password (ID: 2)
  - Logout successfully (ID: 3)
- Suite "Navigation" (ID: 2) - 2 cases
  - Main menu links work (ID: 4)
  - Footer links work (ID: 5)

Gaps identified:
- No registration tests
- No product listing tests
- No cart/checkout tests

**Phase 1: Discovery**
Exploring myplatform.com for gaps...

Found 8 key pages:
- / (Homepage)
- /login (Auth - COVERED)
- /register (Auth - GAP)
- /products (Listing - GAP)
- /products/:id (Detail - GAP)
- /cart (Transaction - GAP)
- /checkout (Transaction - GAP)
- /account (Dashboard - requires auth)

**Phase 2: Design**
Designed 12 NEW test cases (reusing 5 existing):
- Authentication: +2 new (registration tests)
- Products: +6 new
- Cart: +4 new

**Phase 3: Creating in Qase (gaps only)**
✓ Using existing suite "Authentication" (ID: 1)
✓ Created suite "Products" (ID: 3)
✓ Created suite "Cart" (ID: 4)
✓ Created 12 new test cases (cases 6-17)

Total coverage: 17 test cases (5 existing + 12 new)

**Phase 4: Generating Tests**
Created files:
- pages/login.page.ts
- pages/products.page.ts
- pages/cart.page.ts
- tests/auth.spec.ts (includes existing case IDs 1-5)
- tests/products.spec.ts (case IDs 6-11)
- tests/cart.spec.ts (case IDs 12-17)

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
