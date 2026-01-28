# Autonomous Automation Tester

> A Claude Code skills blueprint that transforms Claude into an autonomous QA engineer capable of discovering, designing, and implementing end-to-end test suites with Qase.io integration.

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

## What Is This?

This is **not** a traditional testing framework - it's a **skills blueprint for Claude Code**.

When you open this project in Claude Code and say **"Test [URL]"**, Claude becomes an autonomous QA engineer that will:

1. **Discover** your website structure via browser automation
2. **Design** test cases based on risk and page types
3. **Sync** test suites to Qase.io test management
4. **Generate** Playwright test code with Page Object Model
5. **Execute** tests and report results back to Qase

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

## Quick Start

### 1. Clone This Blueprint

```bash
git clone https://github.com/yourusername/autonomous-automation-tester.git
cd autonomous-automation-tester
```

### 2. Initialize Playwright

This blueprint requires a Playwright project. Initialize one:

```bash
npm init -y
npm install -D @playwright/test playwright-qase-reporter dotenv
npx playwright install chromium
```

### 3. Configure Environment

Copy and edit the environment file:

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

### 4. Configure MCP (Optional - for Browser Discovery)

If you want Claude to explore websites via browser automation:

```bash
cp .claude/skills/mcp-client/references/mcp-config.example.json \
   .claude/skills/mcp-client/references/mcp-config.json
```

### 5. Create Playwright Config

Create `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '.env') });

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html'],
    ['playwright-qase-reporter', {
      mode: process.env.QASE_MODE || 'off',
      debug: true,
      testops: {
        api: {
          token: process.env.QASE_TESTOPS_API_TOKEN,
        },
        project: process.env.QASE_TESTOPS_PROJECT || 'ATP',
        uploadAttachments: true,
        run: {
          complete: true,
          title: 'Playwright Automated Test Run',
        },
      },
    }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### 6. Open in Claude Code

```bash
claude
```

Now just say: **"Test https://yoursite.com"**

---

## Current Project Structure

```
autonomous-automation-tester/
├── .claude/
│   └── skills/                       # Claude Code skills (the brain)
│       ├── automation-tester/        # Test planning & prioritization logic
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── test-patterns.md  # Test patterns by page type
│       │       └── priority-matrix.md
│       ├── site-discovery/           # Website exploration logic
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── page-classification.md
│       ├── qase-client/              # Qase.io integration
│       │   ├── skill.md
│       │   └── references/
│       │       ├── qase-api.md
│       │       └── qase-config.example.json
│       ├── test-generation/          # Playwright code generation
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── templates.md
│       ├── mcp-client/               # Browser automation via MCP
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── mcp-servers.md
│       │       └── mcp-config.example.json
│       └── full-workflow/            # End-to-end orchestration
│           └── SKILL.md
├── scripts/
│   └── qase_client.py                # CLI for Qase API operations
├── .env.example                      # Environment template
├── CLAUDE.md                         # Main instructions for Claude
├── README.md                         # This file
└── .gitignore                        # Protects sensitive files
```

### After Running Tests (Generated by Claude)

Claude will create these directories and files as needed:

```
autonomous-automation-tester/
├── ...existing files...
├── package.json                      # Node.js dependencies
├── playwright.config.ts              # Playwright configuration
├── tests/                            # Generated test specs
│   ├── auth.spec.ts
│   ├── navigation.spec.ts
│   └── products.spec.ts
└── pages/                            # Generated Page Objects
    ├── login.page.ts
    ├── products.page.ts
    └── cart.page.ts
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

## Skills System

The framework uses a modular **skills architecture** that gives Claude specialized capabilities:

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

### Getting Your API Token

1. Go to [Qase.io](https://app.qase.io)
2. Navigate to **User Settings** → **API Tokens**
3. Create a new token and copy it to your `.env` file

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

### Playwright Test Integration

Tests link to Qase using the `qase()` function:

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

The number in `qase(1, ...)` is the Qase case ID.

---

## Test Patterns Reference

The blueprint includes pre-defined test patterns for common page types:

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

## Running Tests

After Claude generates your tests:

```bash
# Run all tests (results sync to Qase automatically)
npx playwright test

# Run specific test file
npx playwright test tests/auth.spec.ts

# Run in headed mode (visible browser)
npx playwright test --headed

# Disable Qase reporting (local only)
QASE_MODE=off npx playwright test

# Run with specific tags
npx playwright test --grep @P0
npx playwright test --grep @smoke
```

---

## Autonomy Rules

**Claude decides autonomously:**
- Which pages to explore
- Page type classification
- Test case priorities (P0/P1/P2)
- Selector strategies
- Test file organization

**Claude asks you when:**
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
npx playwright test
Results will sync to Qase automatically.
```

---

## Configuration Files

| File | Purpose | Gitignored |
|------|---------|------------|
| `.env` | API tokens and secrets | Yes |
| `.env.example` | Template for .env | No |
| `mcp-config.json` | MCP server configuration | Yes |
| `playwright.config.ts` | Playwright settings | No |

---

## Requirements

- **Node.js** 18+
- **Python** 3.8+ (for Qase client script)
- **Claude Code** CLI
- **Qase.io** account (free tier available)

---

## Links

- [Qase.io](https://qase.io) - Test management platform
- [Playwright](https://playwright.dev) - Browser automation
- [Claude Code](https://claude.ai/claude-code) - AI coding assistant
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP servers

---

<p align="center">
  <strong>A skills blueprint for autonomous QA with Claude Code</strong>
  <br>
  <em>Just say "Test [URL]" and let Claude do the rest.</em>
</p>
