# Full Workflow Checklist

Use this checklist to ensure you complete all phases correctly.

## Pre-Flight Checks

- [ ] `QASE_API_TOKEN` environment variable is set
- [ ] `QASE_TESTOPS_PROJECT` environment variable is set
- [ ] MCP config exists at `.claude/skills/mcp-client/references/mcp-config.json`
- [ ] Playwright MCP server is configured in MCP config

## Phase 0: Check Existing Coverage

- [ ] Search Qase for existing test cases by feature keywords
- [ ] List existing suites to understand structure
- [ ] Document existing case IDs for reuse
- [ ] Identify gaps that need new test cases
- [ ] **Decision:** Skip to Phase 4 if full coverage exists

**Commands:**
```bash
python scripts/qase_client.py search-cases PROJ "login"
python scripts/qase_client.py search-cases PROJ "navigation"
python scripts/qase_client.py suites PROJ
```

## Phase 1: Site Discovery

- [ ] Navigate to homepage with `browser_run_code`
- [ ] Accept cookies in same session
- [ ] Extract navigation links
- [ ] Extract footer links
- [ ] Identify forms (login, search, etc.)
- [ ] Capture accessibility snapshot
- [ ] Visit key subpages (each in fresh session with cookie handling)
- [ ] Classify each page type
- [ ] Document auth requirements
- [ ] Document navigation behavior (submenus, dropdowns)

**Output:** Site map with classified pages

## Phase 1.5: Discover Behavioral Data

**MANDATORY for negative tests!**

- [ ] Discover login error behavior
  - [ ] Trigger with invalid credentials
  - [ ] Capture error message text
  - [ ] Capture error element selector/role
- [ ] Discover form validation behavior
  - [ ] Test empty field submission
  - [ ] Test invalid format submission
  - [ ] Capture HTML5 vs custom validation
- [ ] Discover success states
  - [ ] Capture redirect URLs
  - [ ] Capture success messages
- [ ] Document all discovered text/selectors

**Output:** Real text and selectors for test assertions

## Phase 2: Test Design

- [ ] Apply test patterns by page type (see automation-tester skill)
- [ ] Assign priorities (P0/P1/P2)
- [ ] Group into logical suites
- [ ] Skip cases that already exist in Qase
- [ ] Use discovered text for negative test assertions
- [ ] Document test case specifications

**Output:** Test case list organized by suite

## Phase 3: Sync to Qase

- [ ] Create suites (only if not exists)
- [ ] Create test cases with proper severity
- [ ] Record all Qase case IDs (existing + new)
- [ ] Verify cases were created successfully

**Commands:**
```bash
python scripts/qase_client.py create-suite PROJ '{"title": "Suite Name"}'
python scripts/qase_client.py create-case PROJ '{"title": "Case", "suite_id": 1, "severity": 1}'
```

**Output:** Qase case IDs mapped to test specs

## Phase 4: Generate Automation

- [ ] Create page objects for each tested page
  - [ ] Use discovered selectors
  - [ ] Include cookie acceptance method
  - [ ] Include assertion helpers
- [ ] Generate test specs for each suite
  - [ ] Link tests to Qase case IDs
  - [ ] Use discovered error text in assertions
  - [ ] Follow AAA pattern (Arrange/Act/Assert)
- [ ] Create/update playwright.config.ts if needed
- [ ] Verify all imports are correct

**Output:**
```
pages/*.page.ts
tests/*.spec.ts
playwright.config.ts
```

## Phase 5: Run & Report

- [ ] Install dependencies (`npm install`)
- [ ] Install browsers (`npx playwright install chromium`)
- [ ] Run tests (`npx playwright test`)
- [ ] Review results
- [ ] If tests fail → Use test-fixer skill (MANDATORY)
- [ ] Report results to Qase

**Commands:**
```bash
npm install
npx playwright install chromium
npx playwright test
```

## Post-Run

- [ ] All tests passing?
  - Yes → Done!
  - No → Use test-fixer skill
- [ ] Results synced to Qase?
- [ ] Any new issues discovered?
