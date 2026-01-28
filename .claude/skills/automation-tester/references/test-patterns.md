# Test Patterns by Page Type

## Authentication Pages

### Login
| Priority | Test Case |
|----------|-----------|
| P0 | Valid credentials redirect to dashboard |
| P0 | Page loads with all elements |
| P1 | Invalid email shows error |
| P1 | Invalid password shows error |
| P1 | Empty submission shows required errors |
| P1 | Forgot password link works |
| P2 | Remember me functionality |
| P2 | Session timeout behavior |

### Registration
| Priority | Test Case |
|----------|-----------|
| P0 | Valid registration succeeds |
| P0 | Form displays all fields |
| P1 | Email validation |
| P1 | Password requirements enforced |
| P1 | Required fields validated |
| P2 | Duplicate email handling |

## Listing/Search Pages

### Product Listing
| Priority | Test Case |
|----------|-----------|
| P0 | Page loads with items |
| P0 | Items are clickable |
| P1 | Filters work |
| P1 | Sorting works |
| P1 | Pagination works |
| P2 | Empty results state |
| P2 | URL reflects filters |

### Search
| Priority | Test Case |
|----------|-----------|
| P0 | Search accepts input |
| P0 | Returns relevant results |
| P1 | No results message |
| P1 | Search suggestions |
| P2 | Special character handling |

## Detail Pages

### Product Detail
| Priority | Test Case |
|----------|-----------|
| P0 | Page loads with info |
| P0 | Add to cart works |
| P0 | Price displayed |
| P1 | Quantity selector |
| P1 | Image gallery |
| P1 | Variant selection |
| P2 | Out of stock state |
| P2 | Wishlist |

## Transaction Pages

### Cart
| Priority | Test Case |
|----------|-----------|
| P0 | Items display correctly |
| P0 | Totals accurate |
| P0 | Proceed to checkout works |
| P1 | Quantity update |
| P1 | Remove item |
| P1 | Promo code field |
| P2 | Empty cart state |

### Checkout
| Priority | Test Case |
|----------|-----------|
| P0 | Form accepts valid input |
| P0 | Can progress through steps |
| P0 | Order summary accurate |
| P1 | Address validation |
| P1 | Shipping options |
| P2 | Back navigation |

## Form Pages

### Contact Form
| Priority | Test Case |
|----------|-----------|
| P0 | Form displays fields |
| P0 | Valid submission succeeds |
| P1 | Required validation |
| P1 | Email format validation |
| P2 | File upload |

## Navigation

### Homepage
| Priority | Test Case |
|----------|-----------|
| P0 | Page loads |
| P0 | Main nav works |
| P0 | Search accessible |
| P1 | Hero displays |
| P1 | Footer links work |
| P2 | Cookie consent |
