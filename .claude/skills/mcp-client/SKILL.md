---
name: mcp-client
description: Universal MCP client for connecting to any MCP server with progressive disclosure. Wraps MCP servers as skills to avoid context window bloat from tool definitions. Use when interacting with external MCP servers (Playwright, GitHub, filesystem, etc.), listing available tools, or executing MCP tool calls. Triggers on "connect to MCP", "list MCP tools", "call MCP", "use Playwright", "browser navigate", "browser snapshot".
---

# Universal MCP Client

Connect to any MCP server without bloating context with tool definitions.

## How It Works

Instead of loading all MCP tool schemas into context, this client:
1. Lists available servers from config
2. Queries tool schemas on-demand
3. Executes tools with JSON arguments

## Configuration

Config location priority:
1. `MCP_CONFIG_PATH` environment variable
2. `.claude/skills/mcp-client/references/mcp-config.json`
3. `.mcp.json` in current directory
4. `~/.claude.json`

## Commands

```bash
# List configured servers
python scripts/mcp_client.py servers

# List tools from a specific server
python scripts/mcp_client.py tools playwright

# Call a tool
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
```

## Common Workflows

### Playwright Browser Exploration

```bash
# Navigate to page
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'

# Get accessibility snapshot (primary exploration tool)
python scripts/mcp_client.py call playwright browser_snapshot '{}'

# Take screenshot
python scripts/mcp_client.py call playwright browser_screenshot '{}'

# Click element
python scripts/mcp_client.py call playwright browser_click '{"element": "Login button"}'

# Type into field
python scripts/mcp_client.py call playwright browser_type '{"element": "Email input", "text": "user@example.com"}'
```

### Sequential Thinking

```bash
# Use for complex reasoning
python scripts/mcp_client.py call sequential-thinking sequentialthinking '{"thought": "...", "nextThoughtNeeded": true, "thoughtNumber": 1, "totalThoughts": 5}'
```

## Available Servers

See [references/mcp-servers.md](references/mcp-servers.md) for:
- Playwright (browser automation)
- GitHub (repository operations)
- Filesystem (file access)
- Sequential Thinking (reasoning)
- And more...

## Setup

1. Copy the example config:
   ```bash
   cp .claude/skills/mcp-client/references/mcp-config.example.json \
      .claude/skills/mcp-client/references/mcp-config.json
   ```

2. The config should contain:
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

3. Install dependencies:
   ```bash
   pip install mcp fastmcp
   ```

## Config Example

See [references/mcp-config.example.json](references/mcp-config.example.json)

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "No MCP config found" | Missing config file | Create mcp-config.json |
| "Server not found" | Server not in config | Add server to config |
| "Connection failed" | Server not running | Start the MCP server |
| "Invalid JSON" | Bad tool arguments | Check argument format |

## Dependencies

```bash
pip install mcp fastmcp
```
