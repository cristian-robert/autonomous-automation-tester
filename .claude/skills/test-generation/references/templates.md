# Test Generation Templates

## Page Object Template

```typescript
import { Page, Locator, expect } from '@playwright/test';

export class {{PageName}}Page {
  readonly page: Page;
  // Locators
  {{#each elements}}
  readonly {{name}}: Locator;
  {{/each}}

  constructor(page: Page) {
    this.page = page;
    {{#each elements}}
    this.{{name}} = page.{{selector}};
    {{/each}}
  }

  async goto() {
    await this.page.goto('{{url}}');
  }

  async expectLoaded() {
    await expect(this.{{primaryElement}}).toBeVisible();
  }

  // Actions
  {{#each actions}}
  async {{name}}({{params}}) {
    {{implementation}}
  }
  {{/each}}
}
```

## Test Spec Template

```typescript
import { test, expect } from '@playwright/test';
import { {{PageName}}Page } from '../pages/{{pageName}}.page';

test.describe('{{Feature}} - {{Context}}', () => {
  let page: {{PageName}}Page;

  test.beforeEach(async ({ page: browserPage }) => {
    page = new {{PageName}}Page(browserPage);
    await page.goto();
  });

  {{#each testCases}}
  test('{{title}}', async ({ page: browserPage }) => {
    // Arrange
    {{arrange}}

    // Act
    {{act}}

    // Assert
    {{assert}}
  });
  {{/each}}
});
```

## E2E Flow Template

```typescript
import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/home.page';
import { ProductPage } from '../pages/product.page';
import { CartPage } from '../pages/cart.page';

test.describe('E2E: {{FlowName}}', () => {
  test('{{flowDescription}}', async ({ page }) => {
    // Step 1: Start
    const homePage = new HomePage(page);
    await homePage.goto();

    // Step 2: Navigate
    await homePage.{{navigation}};
    const productPage = new ProductPage(page);
    await productPage.expectLoaded();

    // Step 3: Action
    await productPage.{{action}};

    // Step 4: Verify
    const cartPage = new CartPage(page);
    await cartPage.expectLoaded();
    await expect(cartPage.{{element}}).{{assertion}};
  });
});
```

## Common Page Objects

### Navigation Component
```typescript
export class HeaderNav {
  readonly page: Page;
  readonly logo: Locator;
  readonly searchInput: Locator;
  readonly cartButton: Locator;
  readonly accountButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.logo = page.getByRole('link', { name: /logo/i });
    this.searchInput = page.getByRole('searchbox');
    this.cartButton = page.getByRole('link', { name: /cart/i });
    this.accountButton = page.getByRole('button', { name: /account/i });
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
  }

  async openCart() {
    await this.cartButton.click();
  }
}
```

### Form Component
```typescript
export class FormHelper {
  readonly page: Page;
  readonly form: Locator;

  constructor(page: Page, formSelector: string = 'form') {
    this.page = page;
    this.form = page.locator(formSelector);
  }

  async fill(data: Record<string, string>) {
    for (const [label, value] of Object.entries(data)) {
      await this.page.getByLabel(label).fill(value);
    }
  }

  async submit() {
    await this.form.getByRole('button', { name: /submit/i }).click();
  }

  async expectError(field: string, message: string) {
    const errorId = await this.page.getByLabel(field).getAttribute('aria-describedby');
    if (errorId) {
      await expect(this.page.locator(`#${errorId}`)).toContainText(message);
    }
  }
}
```

## Playwright Config Template

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list'],
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

## Test Tags

```typescript
// Priority tags
test('critical feature @P0', async () => {});
test('important feature @P1', async () => {});
test('nice to have @P2', async () => {});

// Type tags
test('login flow @smoke @auth', async () => {});
test('checkout @regression @checkout', async () => {});

// Run specific tags
// npx playwright test --grep @smoke
// npx playwright test --grep @P0
```
