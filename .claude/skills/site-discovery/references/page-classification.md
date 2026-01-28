# Page Classification Reference

## Authentication Pages

**URL Patterns:**
- /login, /signin, /sign-in
- /register, /signup, /sign-up
- /forgot-password, /reset-password
- /verify, /confirm

**Element Indicators:**
- Password input field
- "Remember me" checkbox
- OAuth buttons (Google, Facebook, etc.)
- Links to registration or password reset

**Priority:** P0 (critical path)

## Listing/Search Pages

**URL Patterns:**
- /products, /items, /catalog
- /search?q=
- /category/*, /collection/*
- /results

**Element Indicators:**
- Grid/list of similar items
- Filter sidebar or dropdowns
- Sort dropdown
- Pagination controls
- Result count display

**Priority:** P0 if main feature, P1 otherwise

## Detail Pages

**URL Patterns:**
- /products/:id
- /item/:slug
- /p/:sku
- Numeric ID in URL

**Element Indicators:**
- Single item focus
- Large product image
- Price display
- Add to cart/wishlist button
- Quantity selector
- Variant options (size, color)
- Reviews section

**Priority:** P0

## Transaction Pages

**URL Patterns:**
- /cart, /basket, /bag
- /checkout, /checkout/*
- /payment
- /order-confirmation, /thank-you

**Element Indicators:**
- Item list with totals
- Quantity adjusters
- Remove buttons
- Promo code field
- Shipping/billing forms
- Payment method selection
- Order summary

**Priority:** P0

## Form Pages

**URL Patterns:**
- /contact, /contact-us
- /support, /help
- /apply, /application
- /feedback, /survey

**Element Indicators:**
- Multiple input fields
- Textarea for message
- Submit button
- Required field indicators
- File upload

**Priority:** P1

## Content Pages

**URL Patterns:**
- /about, /about-us
- /blog, /blog/*
- /faq, /help
- /terms, /privacy
- /press, /news

**Element Indicators:**
- Primarily text content
- Limited interactivity
- Share buttons
- Comment section (blog)
- Accordion (FAQ)

**Priority:** P2

## Dashboard/Account Pages

**URL Patterns:**
- /account, /my-account
- /dashboard
- /profile, /settings
- /orders, /order-history
- /wishlist, /favorites

**Element Indicators:**
- Requires authentication
- User-specific data
- Edit/update buttons
- Tabs or sections
- Data tables

**Priority:** P1 (if auth available)

## Navigation/Landing Pages

**URL Patterns:**
- / (homepage)
- /home
- Section landing pages

**Element Indicators:**
- Hero section
- Featured content
- Multiple CTAs
- Category cards
- Promotional banners

**Priority:** P0 (homepage), P2 (other landing)
