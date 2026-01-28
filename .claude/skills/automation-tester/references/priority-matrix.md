# Priority Matrix

## P0 - Critical (Must Test)

**Definition:** If this fails, the application is broken for all users.

**Characteristics:**
- Core business functionality
- Blocks all users
- Revenue/conversion impact
- No workaround exists

**Examples:**
- Login/logout
- Checkout completion
- Core navigation
- Primary CTA (Add to Cart, Sign Up)
- Payment processing
- Data persistence

**Test in:** Every smoke test, every deployment

## P1 - Important (Should Test)

**Definition:** Major feature broken, but workarounds may exist.

**Characteristics:**
- Important feature
- Affects many users
- Has business impact
- Workaround possible but painful

**Examples:**
- Search functionality
- Filters and sorting
- Form validation
- Error messages
- Secondary navigation
- User profile features
- Password reset

**Test in:** Regression suite, major releases

## P2 - Nice to Have (Could Test)

**Definition:** Minor issues, edge cases, or cosmetic problems.

**Characteristics:**
- Affects few users
- Low business impact
- Easy workaround
- Cosmetic or UX polish

**Examples:**
- Tooltips
- Animations
- Edge case inputs
- Rare user flows
- Social sharing
- Accessibility edge cases
- Browser-specific quirks

**Test in:** Full regression, quarterly

## Decision Flowchart

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

## Smoke vs Regression

| Type | Include | Count |
|------|---------|-------|
| Smoke | P0 only | 10-15 |
| Regression | P0 + P1 | 30-50 |
| Full | P0 + P1 + P2 | 50+ |
