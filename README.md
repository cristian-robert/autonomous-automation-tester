# Autonomous Automation Tester

> An AI-powered QA automation framework for Claude Code that autonomously discovers, designs, and implements end-to-end test suites with Qase.io integration.

```
     ___         __
    /   | __  __/ /_____  ____  ____  ____ ___  ____  __  _______
   / /| |/ / / / __/ __ \/ __ \/ __ \/ __ `__ \/ __ \/ / / / ___/
  / ___ / /_/ / /_/ /_/ / / / / /_/ / / / / / / /_/ / /_/ (__  )
 /_/  |_\__,_/\__/\____/_/ /_/\____/_/ /_/ /_/\____/\__,_/____/

 ████████╗███████╗███████╗████████╗███████╗██████╗
 ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║   █████╗  ███████╗   ██║   █████╗  ██████╔╝
    ██║   ██╔══╝  ╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║   ███████╗███████║   ██║   ███████╗██║  ██║
    ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

---

## Overview

This framework transforms Claude Code into a **senior QA automation engineer** that can autonomously:

- **Discover** website structure via browser automation
- **Design** test cases based on risk and page types
- **Sync** test suites to Qase.io test management
- **Generate** Playwright test code with Page Object Model
- **Execute** tests and report results back to Qase

Just say **"Test [URL]"** and watch the magic happen.

---

## The Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DISCOVER  │───▶│   DESIGN    │───▶│    QASE     │───▶│  AUTOMATE   │───▶│     RUN     │
│             │    │             │    │             │    │             │    │             │
│  Explore    │    │  Create     │    │  Sync to    │    │  Generate   │    │  Execute &  │
│  website    │    │  test       │    │  Qase.io    │    │  Playwright │    │  report     │
│  via MCP    │    │  cases      │    │  platform   │    │  code       │    │  results    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Quick Commands

| You Say | Claude Does |
|---------|-------------|
| `Test https://mysite.com` | Full workflow: Discover → Qase → Automate |
| `Explore https://mysite.com` | Site discovery and mapping only |
| `Create test cases for mysite.com` | Design test cases + push to Qase |
| `Automate the test cases` | Generate Playwright code from Qase cases |

---

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/autonomous-automation-tester.git
cd autonomous-automation-tester
npm install
```

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your Qase.io credentials:

```bash
# Qase.io Integration
QASE_TESTOPS_API_TOKEN=your_api_token_here  # Get from https://app.qase.io/user/api/token
QASE_TESTOPS_PROJECT=ATP                     # Your project code in Qase
QASE_MODE=testops                            # Enable Qase reporting
```

### 3. Configure MCP (Browser Automation)

```bash
cp .claude/skills/mcp-client/references/mcp-config.example.json \
   .claude/skills/mcp-client/references/mcp-config.json
```

### 4. Install Playwright Browsers

```bash
npx playwright install chromium
```

---

## Project Structure

```
autonomous-automation-tester/
├── .claude/
│   ├── settings.local.json          # Claude Code settings
│   └── skills/                       # Modular skill system
│       ├── automation-tester/        # Test planning & prioritization
│       ├── site-discovery/           # Website exploration
│       ├── qase-client/              # Qase.io integration
│       ├── test-generation/          # Playwright code generation
│       ├── mcp-client/               # Browser automation via MCP
│       └── full-workflow/            # End-to-end orchestration
├── scripts/
│   └── qase_client.py                # CLI for Qase API operations
├── tests/                            # Generated test specs
│   ├── auth.spec.ts
│   └── navigation.spec.ts
├── pages/                            # Generated Page Objects
│   ├── login.page.ts
│   └── products.page.ts
├── .env.example                      # Environment template
├── CLAUDE.md                         # Claude instructions
└── playwright.config.ts              # Playwright configuration
```

---

## Skills System

The framework uses a modular **skills architecture** that gives Claude specialized capabilities:

### Core Skills

| Skill | Purpose | Triggers |
|-------|---------|----------|
| **automation-tester** | Test planning, prioritization, risk analysis | "what should I test", "test strategy", "P0 P1 P2" |
| **site-discovery** | Website exploration and mapping | "explore", "discover", "map the site" |
| **qase-client** | Qase.io test management | "Qase", "create suite", "sync to Qase" |
| **test-generation** | Playwright code generation | "write tests", "page object", "generate automation" |
| **mcp-client** | Browser automation via MCP servers | "use Playwright", "browser navigate", "snapshot" |
| **full-workflow** | End-to-end orchestration | "test this site", "full testing workflow" |

---

## Priority System

Test cases are automatically prioritized using a risk-based approach:

| Priority | Definition | Examples |
|----------|------------|----------|
| **P0** | App broken if fails | Login, checkout, core navigation |
| **P1** | Major feature broken | Search, filters, form validation |
| **P2** | Minor/edge cases | Tooltips, animations, rare flows |

### Decision Flowchart

```
Can users complete their primary goal?
├── No → P0
└── Yes → Continue

Is a major feature broken?
├── Yes → P1
└── No → Continue

Is it visible to most users?
├── Yes → P1
└── No → P2
```

---

## Qase.io Integration

### Manual API Operations

Use the included Python client for direct Qase operations:

```bash
# Set your API token
export QASE_API_TOKEN=your_token_here

# List all projects
python scripts/qase_client.py projects

# Create a test suite
python scripts/qase_client.py create-suite ATP '{"title": "Authentication"}'

# Create a test case
python scripts/qase_client.py create-case ATP '{"title": "Valid login succeeds", "suite_id": 1, "severity": 1}'

# List all cases
python scripts/qase_client.py cases ATP
```

### Playwright Integration

Tests automatically report to Qase using the `playwright-qase-reporter`:

```typescript
import { test, expect } from '@playwright/test';
import { qase } from 'playwright-qase-reporter';

test(qase(1, 'Valid login redirects to dashboard'), async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

---

## Test Patterns

The framework includes pre-defined test patterns for common page types:

### Authentication Pages

| Priority | Test Case |
|----------|-----------|
| P0 | Valid credentials redirect to dashboard |
| P0 | Page loads with all elements |
| P1 | Invalid email shows error |
| P1 | Empty submission shows required errors |
| P2 | Remember me functionality |

### Product Listing

| Priority | Test Case |
|----------|-----------|
| P0 | Page loads with items |
| P0 | Items are clickable |
| P1 | Filters work correctly |
| P1 | Sorting changes order |
| P2 | URL reflects active filters |

### Cart & Checkout

| Priority | Test Case |
|----------|-----------|
| P0 | Items display correctly |
| P0 | Totals are accurate |
| P0 | Can proceed to checkout |
| P1 | Quantity updates work |
| P1 | Promo code applies discount |

---

## Browser Automation (MCP)

The framework uses **Model Context Protocol (MCP)** servers for browser automation:

```bash
# Navigate to a URL
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'

# Take an accessibility snapshot (primary discovery tool)
python scripts/mcp_client.py call playwright browser_snapshot '{}'

# Click an element
python scripts/mcp_client.py call playwright browser_click '{"element": "Login button"}'

# Type into a field
python scripts/mcp_client.py call playwright browser_type '{"element": "Email", "text": "user@test.com"}'
```

### Supported MCP Servers

| Server | Purpose |
|--------|---------|
| **Playwright** | Browser navigation, snapshots, interactions |
| **Sequential Thinking** | Structured problem-solving |
| **GitHub** | Repository operations |
| **Filesystem** | File access in allowed directories |
| **Zapier** | 8,000+ app integrations |

---

## Running Tests

```bash
# Run all tests (results sync to Qase automatically)
npx playwright test

# Run specific test file
npx playwright test tests/auth.spec.ts

# Run in headed mode (visible browser)
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium

# Disable Qase reporting (local only)
QASE_MODE=off npx playwright test

# Run with specific tags
npx playwright test --grep @P0
npx playwright test --grep @smoke
```

---

## Autonomy Rules

Claude makes decisions autonomously for:

- Which pages to explore
- Page type classification
- Test case priorities (P0/P1/P2)
- Selector strategies
- Test file organization

Claude asks you when:

- Login credentials are needed
- Payment/transaction testing is required
- Destructive operations (delete account, etc.)
- Business logic is ambiguous
- 3+ consecutive failures occur

---

## Example Session

```
You: Test https://myshop.com

Claude: I'll help you test myshop.com with full Qase integration.

**Setup Check**
✓ QASE_API_TOKEN configured
✓ Project: SHOP
✓ Playwright MCP connected

**Phase 1: Discovery**
Exploring myshop.com...

Found 12 pages:
• / (Homepage) - P0
• /login (Authentication) - P0
• /products (Listing) - P0
• /products/:id (Detail) - P0
• /cart (Transaction) - P0
• /checkout (Transaction) - P0
• /account (Dashboard - auth required) - P1
• /about (Content) - P2
...

**Phase 2: Design**
Created 24 test cases across 5 suites:
• Authentication (4 cases)
• Navigation (3 cases)
• Products (8 cases)
• Cart (5 cases)
• Checkout (4 cases)

**Phase 3: Syncing to Qase**
✓ Suite: Authentication (ID: 1)
✓ Suite: Navigation (ID: 2)
✓ Suite: Products (ID: 3)
✓ Suite: Cart (ID: 4)
✓ Suite: Checkout (ID: 5)
✓ 24 test cases created

View: https://app.qase.io/project/SHOP

**Phase 4: Generating Tests**
Created:
• pages/login.page.ts
• pages/products.page.ts
• pages/cart.page.ts
• tests/auth.spec.ts
• tests/products.spec.ts
• tests/cart.spec.ts

**Ready to Run**
npm install && npx playwright test
Results will sync to Qase automatically.
```

---

## Configuration Files

| File | Purpose | Gitignored |
|------|---------|------------|
| `.env` | API tokens and secrets | Yes |
| `.env.example` | Template for .env | No |
| `qase.config.json` | Alternative Qase config | Yes |
| `mcp-config.json` | MCP server configuration | Yes |
| `playwright.config.ts` | Playwright settings | No |

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - feel free to use this for your projects.

---

## Links

- [Qase.io Documentation](https://developers.qase.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Claude Code](https://claude.ai/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

<p align="center">
  <strong>Built for autonomous QA with Claude Code</strong>
</p>
