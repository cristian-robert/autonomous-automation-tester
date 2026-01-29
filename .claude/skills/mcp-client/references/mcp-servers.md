# Available MCP Servers

## Playwright (Browser Automation)

**Purpose:** Navigate websites, take snapshots, interact with elements for test discovery.

**Config:**
```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

### CRITICAL: Session Behavior

**Each MCP tool call creates a NEW browser session!**

- `browser_navigate` → Opens new browser, navigates, returns snapshot, browser closes
- `browser_click` → Opens new browser (fresh page!), clicks, browser closes
- `browser_snapshot` → If called right after navigate in same MCP session, uses existing browser

**For multi-step operations, use `browser_run_code`!**

### Key Tools

| Tool | Session | Purpose | Example Args |
|------|---------|---------|--------------|
| `browser_navigate` | New | Open URL, get snapshot | `{"url": "https://example.com"}` |
| **`browser_run_code`** | **Single** | **Run multiple steps** | `{"code": "await page.goto('...')"}` |
| `browser_snapshot` | Reuse | Get accessibility tree | `{}` |
| `browser_screenshot` | Reuse | Capture visual | `{}` |
| `browser_click` | New | Click element | `{"element": "Submit button"}` |
| `browser_type` | New | Type into field | `{"element": "Email", "text": "user@test.com"}` |
| `browser_hover` | New | Hover for menus | `{"element": "Products menu"}` |
| `browser_select_option` | New | Select dropdown | `{"element": "Country", "value": "US"}` |

### Recommended Workflows

#### Simple Page Load (Use `browser_navigate`)
```bash
python mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
```
Returns page content AND accessibility snapshot in one call.

#### Multi-Step (Use `browser_run_code`)
```bash
python mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Accept cookies if present
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Click navigation
    await page.getByRole(\"link\", { name: /products/i }).click();
    await page.waitForLoadState(\"networkidle\");

    // Return final state
    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify({ url: page.url(), snapshot }, null, 2);
  "
}'
```

#### Form Exploration
```bash
python mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com/login\");

    // Get all form elements with attributes
    const inputs = await page.locator(\"input\").evaluateAll(els =>
      els.map(e => ({
        type: e.type,
        name: e.name,
        id: e.id,
        placeholder: e.placeholder,
        testid: e.dataset.testid,
        ariaLabel: e.getAttribute(\"aria-label\")
      }))
    );

    const buttons = await page.locator(\"button\").evaluateAll(els =>
      els.map(e => ({
        text: e.textContent?.trim(),
        type: e.type,
        testid: e.dataset.testid
      }))
    );

    return JSON.stringify({ inputs, buttons }, null, 2);
  "
}'
```

#### Menu/Dropdown Behavior Discovery
```bash
python mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Click menu item
    const menuItem = page.getByRole(\"link\", { name: /Category/i }).first();
    await menuItem.click();
    await page.waitForTimeout(1000);

    // Check if it navigated or opened submenu
    const didNavigate = !page.url().endsWith(\"/\");
    const submenu = await page.locator(\"[class*=submenu], [class*=dropdown]\").isVisible().catch(() => false);

    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify({
      clickResult: didNavigate ? \"navigated\" : submenu ? \"opened_submenu\" : \"unknown\",
      url: page.url(),
      snapshot
    }, null, 2);
  "
}'
```

---

## Sequential Thinking (Reasoning)

**Purpose:** Structured problem-solving through step-by-step thinking.

**Config:**
```json
"sequential-thinking": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
}
```

**Usage:**
```bash
python mcp_client.py call sequential-thinking sequentialthinking '{
  "thought": "First, I need to understand the login flow...",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 5
}'
```

---

## GitHub (Repository Operations)

**Purpose:** Create issues, PRs, read files, manage repositories.

**Config:**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxx"
  }
}
```

**Key Tools:**
- `search_repositories` - Find repos
- `get_file_contents` - Read files
- `create_issue` - Create issues
- `create_pull_request` - Create PRs

---

## Filesystem (File Access)

**Purpose:** Read/write files in allowed directories.

**Config:**
```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
}
```

**Key Tools:**
- `read_file` - Read file contents
- `write_file` - Write to file
- `list_directory` - List directory contents

---

## Zapier (Integrations)

**Purpose:** Connect to 8,000+ apps via Zapier.

**Config:**
```json
"zapier": {
  "url": "https://mcp.zapier.com/api/v1/connect",
  "api_key": "YOUR_API_KEY"
}
```

Get API key from: https://mcp.zapier.com/

**Note:** 1 MCP tool call = 2 Zapier tasks from your quota.

---

## Adding New Servers

1. Find the MCP server package (npm or custom)
2. Add to `mcp-config.json`:
   ```json
   "server-name": {
     "command": "npx",
     "args": ["-y", "package-name"]
   }
   ```
3. Test with: `python mcp_client.py tools server-name`

## Transport Types

| Type | Config | Use Case |
|------|--------|----------|
| stdio | `command` + `args` | Local servers (most common) |
| sse | `url` | Remote servers with SSE |
| streamable_http | `url` ending in `/mcp` | Modern HTTP transport |
| fastmcp | `url` + `api_key` | Bearer auth (Zapier) |
