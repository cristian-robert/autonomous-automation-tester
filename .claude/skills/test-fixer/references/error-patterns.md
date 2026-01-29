# Error Patterns Reference

Quick reference for diagnosing and fixing common Playwright test failures.

## Error Type: Timeout

### `Timeout waiting for selector`

**Symptoms:**
```
Error: locator.click: Timeout 30000ms exceeded.
waiting for locator('button[name="Submit"]')
```

**Causes:**
1. Selector is wrong or outdated
2. Element doesn't exist on page
3. Element is hidden/covered
4. Page didn't load properly

**Diagnosis:**
```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");
    // Accept cookies
    // ...

    // Check if element exists at all
    const count = await page.locator(\"button[name=Submit]\").count();

    // Get all buttons
    const buttons = await page.locator(\"button\").evaluateAll(els =>
      els.map(e => ({ text: e.textContent?.trim(), name: e.name }))
    );

    return JSON.stringify({ count, buttons }, null, 2);
  "
}'
```

**Fixes:**
- Update selector to match actual element
- Add `.first()` if multiple exist
- Wait for element: `await expect(element).toBeVisible()`
- Check for overlays/modals blocking

---

### `Timeout waiting for URL`

**Symptoms:**
```
Error: expect.toHaveURL: Timeout 5000ms exceeded.
Expected: /dashboard/
Received: /login
```

**Causes:**
1. Navigation didn't happen
2. Click opened submenu instead of navigating
3. Redirect to different URL than expected
4. Auth required

**Diagnosis:**
```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");

    const initialUrl = page.url();
    await page.click(\"selector\");
    await page.waitForTimeout(2000);
    const finalUrl = page.url();

    return JSON.stringify({
      initial: initialUrl,
      final: finalUrl,
      changed: initialUrl !== finalUrl
    }, null, 2);
  "
}'
```

**Fixes:**
- Add intermediate step (click "View all" after submenu opens)
- Update expected URL pattern
- Add explicit `waitForURL` before assertion

---

## Error Type: Strict Mode Violation

### `strict mode violation: locator resolved to N elements`

**Symptoms:**
```
Error: locator.click: Error: strict mode violation:
getByRole('button', { name: 'Submit' }) resolved to 2 elements
```

**Causes:**
1. Multiple elements match the selector
2. Page has duplicate buttons (e.g., header and form)

**Diagnosis:**
```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");

    const elements = await page.getByRole(\"button\", { name: \"Submit\" }).evaluateAll(els =>
      els.map((e, i) => ({
        index: i,
        text: e.textContent?.trim(),
        visible: e.offsetParent !== null,
        parent: e.parentElement?.className
      }))
    );

    return JSON.stringify({ count: elements.length, elements }, null, 2);
  "
}'
```

**Fixes:**
```typescript
// Option 1: Use .first()
page.getByRole('button', { name: 'Submit' }).first()

// Option 2: Use parent context
page.locator('form').getByRole('button', { name: 'Submit' })

// Option 3: Use testid if available
page.getByTestId('submit-button')

// Option 4: Use nth
page.getByRole('button', { name: 'Submit' }).nth(1)
```

---

## Error Type: Assertion Failed

### `toContainText` / `toHaveText` failed

**Symptoms:**
```
Error: expect(locator).toContainText
Expected: "Invalid credentials"
Received: "Email sau parolă incorectă"
```

**Cause:**
Test assumed error text instead of discovering actual text.

**Fix:**
Discover actual text (see Phase 1.5 in full-workflow), then update assertion:
```typescript
// Before (assumed)
await expect(page.locator('.error')).toContainText('Invalid credentials');

// After (discovered)
await expect(page.getByRole('alert')).toContainText('Email sau parolă incorectă');
```

---

### `toHaveURL` failed

**Symptoms:**
```
Error: expect(page).toHaveURL
Expected: /products/
Received: /auto-masini-moto/
```

**Cause:**
URL pattern doesn't match actual site URLs.

**Fix:**
Update regex to match actual URL:
```typescript
// Before
await expect(page).toHaveURL(/products/);

// After (discovered actual URL)
await expect(page).toHaveURL(/auto-masini-moto/);
```

---

## Error Type: Element State

### `element not visible`

**Symptoms:**
```
Error: locator.click: Error: element is not visible
```

**Causes:**
1. Element hidden by CSS
2. Element covered by overlay/modal
3. Cookie banner covering element
4. Element needs scroll

**Diagnosis:**
```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");

    const element = page.locator(\"selector\");
    const box = await element.boundingBox();
    const isVisible = await element.isVisible();

    // Check for overlays
    const overlays = await page.locator(\"[class*=modal], [class*=overlay], [class*=cookie]\").count();

    return JSON.stringify({ box, isVisible, overlays }, null, 2);
  "
}'
```

**Fixes:**
```typescript
// Dismiss cookie banner first
await page.getByRole('button', { name: /accept/i }).click();

// Scroll element into view
await element.scrollIntoViewIfNeeded();

// Wait for visibility
await expect(element).toBeVisible();
await element.click();
```

---

### `element is disabled`

**Symptoms:**
```
Error: locator.click: Error: element is disabled
```

**Cause:**
Button/input is disabled, usually waiting for validation.

**Fix:**
```typescript
// Wait for element to be enabled
await expect(element).toBeEnabled();
await element.click();

// Or fill required fields first
await page.fill('input[required]', 'value');
await element.click();
```

---

## Error Type: Navigation

### Click doesn't navigate

**Symptoms:**
Test clicks element expecting navigation, but URL doesn't change.

**Cause:**
Element opens submenu/dropdown instead of navigating directly.

**Diagnosis:**
```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");

    const before = page.url();
    await page.click(\"selector\");
    await page.waitForTimeout(1500);
    const after = page.url();

    // Check for submenus
    const submenu = await page.locator(\"[class*=submenu], [class*=dropdown]\").isVisible().catch(() => false);
    const viewAll = await page.getByRole(\"link\").filter({ hasText: /view all|vezi toate/i }).count();

    return JSON.stringify({
      navigated: before !== after,
      submenuVisible: submenu,
      viewAllLinks: viewAll
    }, null, 2);
  "
}'
```

**Fix:**
```typescript
// Add intermediate step
await page.getByRole('link', { name: 'Category' }).click();
await page.getByRole('link', { name: /View all/i }).click();
await expect(page).toHaveURL(/category/);
```

---

## Quick Diagnosis Script

Use this to quickly diagnose any page state:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"URL_HERE\");

    // Dismiss cookies
    const cookieBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await cookieBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
      await cookieBtn.click();
    }

    // Comprehensive page analysis
    const analysis = {
      url: page.url(),
      title: await page.title(),

      // All visible buttons
      buttons: await page.locator(\"button:visible\").evaluateAll(els =>
        els.map(e => ({
          text: e.textContent?.trim(),
          testid: e.dataset.testid,
          disabled: e.disabled
        }))
      ),

      // All visible inputs
      inputs: await page.locator(\"input:visible\").evaluateAll(els =>
        els.map(e => ({
          type: e.type,
          name: e.name,
          placeholder: e.placeholder
        }))
      ),

      // Error elements
      errors: await page.locator(\"[class*=error], [role=alert]\").evaluateAll(els =>
        els.filter(e => e.offsetParent !== null).map(e => ({
          text: e.textContent?.trim(),
          role: e.getAttribute(\"role\")
        }))
      ),

      // Overlays/modals
      overlays: await page.locator(\"[class*=modal], [class*=overlay]\").count()
    };

    return JSON.stringify(analysis, null, 2);
  "
}'
```
