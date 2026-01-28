# Available MCP Servers

## Playwright (Browser Automation)

**Purpose:** Navigate websites, take snapshots, interact with elements for test discovery.

**Config:**
```json
"playwright": {
  "command": "npx",
  "args": ["@anthropic/mcp-playwright"]
}
```

**Key Tools:**

| Tool | Purpose | Example Args |
|------|---------|--------------|
| `browser_navigate` | Open a URL | `{"url": "https://example.com"}` |
| `browser_snapshot` | Get accessibility tree | `{}` |
| `browser_screenshot` | Capture visual | `{}` |
| `browser_click` | Click element | `{"element": "Submit button"}` |
| `browser_type` | Type into field | `{"element": "Email", "text": "user@test.com"}` |
| `browser_hover` | Hover for menus | `{"element": "Products menu"}` |
| `browser_select_option` | Select dropdown | `{"element": "Country", "value": "US"}` |

**Usage for Testing:**
```bash
# Navigate
python mcp_client.py call playwright browser_navigate '{"url": "https://mysite.com"}'

# Get page structure (primary tool for test discovery)
python mcp_client.py call playwright browser_snapshot '{}'

# Interact
python mcp_client.py call playwright browser_click '{"element": "Login button"}'
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
