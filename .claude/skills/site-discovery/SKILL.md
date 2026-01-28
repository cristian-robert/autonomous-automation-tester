---
name: site-discovery
description: Systematic website exploration and mapping. Use when exploring a new website, mapping site structure, identifying pages to test, or understanding site architecture. Triggers on "explore", "discover", "map the site", "what pages exist", "site structure".
---

# Site Discovery

Systematically explore and map websites to understand what needs testing.

## Discovery Process

### Phase 1: Homepage Analysis
```
1. Navigate to homepage via Playwright MCP
2. Take snapshot (browser_snapshot)
3. Identify:
   - Main navigation links
   - Footer navigation
   - Authentication entry points (Login/Register)
   - Search functionality
   - Key CTAs
```

### Phase 2: Navigation Mapping
```
1. Extract all nav links from homepage
2. Categorize by location (header, footer, sidebar)
3. For each link:
   - Record URL
   - Record link text
   - Predict page type
   - Mark priority (main nav = high)
```

### Phase 3: Page Classification
For each discovered page, classify as:

| Type | Indicators |
|------|------------|
| **Authentication** | /login, /register, password field |
| **Listing** | Multiple items, filters, pagination |
| **Detail** | Single item focus, add to cart |
| **Transaction** | Cart, checkout, payment |
| **Form** | Contact, application, feedback |
| **Content** | Blog, about, FAQ |
| **Dashboard** | Requires auth, user data |

See [references/page-classification.md](references/page-classification.md) for detailed indicators.

## Output Format

```markdown
# Site Map: [Website Name]

## Statistics
- Pages discovered: X
- Requires auth: Y
- Critical paths: Z

## Pages

### Authentication (P0)
| URL | Type | Auth Required |
|-----|------|---------------|
| /login | Login | No |
| /register | Registration | No |

### Core Features (P0)
| URL | Type | Auth Required |
|-----|------|---------------|
| / | Homepage | No |
| /products | Listing | No |
| /cart | Cart | No |

### User Area (P1)
| URL | Type | Auth Required |
|-----|------|---------------|
| /account | Dashboard | Yes |
| /orders | Order History | Yes |

## URL Patterns
- /products/:id - Product detail pages
- /category/:slug - Category pages

## Auth Barriers
- /account/* requires login
- /checkout requires login
```

## Limits

| Scope | Max Pages | Max Depth |
|-------|-----------|-----------|
| Smoke | 20 | 2 |
| Regression | 100 | 4 |

## Edge Cases

**Login wall:** Map public pages first, note auth requirement
**Large site:** Focus on main nav, sample from large sections
**SPA:** Watch for URL hash changes, trigger nav via clicks
