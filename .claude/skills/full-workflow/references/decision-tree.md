# Decision Tree

Quick reference for handling different scenarios during the workflow.

## Phase 0: Existing Coverage Decisions

```
Search Qase for existing cases
           │
           ▼
┌─────────────────────────┐
│ Cases found for feature?│
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────┐   ┌──────────────┐
│ Compare │   │ Full workflow│
│ coverage│   │ from Phase 1 │
└─────────┘   └──────────────┘
     │
     ▼
┌─────────────────────────┐
│ Coverage comprehensive? │
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Skip to     │  │ Note existing │
│ Phase 4     │  │ IDs, create   │
│ (Automate)  │  │ only gaps     │
└─────────────┘  └───────────────┘
```

## Phase 1: Discovery Decisions

### Site Has Login Wall

```
Homepage requires login?
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Ask user    │  │ Continue with │
│ for creds   │  │ discovery     │
└─────────────┘  └───────────────┘
     │
     ▼
┌─────────────────────────┐
│ Credentials provided?   │
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Login and   │  │ Test only     │
│ explore     │  │ public pages  │
└─────────────┘  └───────────────┘
```

### Large Site (>50 pages)

```
Pages discovered > 50?
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Focus on:   │  │ Full coverage │
│ - Main nav  │  │ possible      │
│ - Top 20    │  └───────────────┘
│ - Critical  │
│   paths     │
└─────────────┘
```

### Navigation Behavior

```
Click on nav item
       │
       ▼
┌─────────────────────────┐
│ What happened?          │
└─────────────────────────┘
       │
  ┌────┼────┬────────┐
  │    │    │        │
  ▼    ▼    ▼        ▼
Navigated  Submenu  Dropdown  Nothing
  │        opened   opened      │
  │          │        │         ▼
  ▼          ▼        ▼      ┌──────┐
┌────┐   ┌───────┐ ┌──────┐  │Check │
│Done│   │Click  │ │Select│  │JS err│
└────┘   │"View  │ │option│  └──────┘
         │all"   │ └──────┘
         └───────┘
```

## Phase 1.5: Behavioral Discovery Decisions

### Error Message Discovery

```
Triggered error condition
         │
         ▼
┌─────────────────────────┐
│ Error visible?          │
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Capture:    │  │ Check:        │
│ - Text      │  │ - Network tab │
│ - Selector  │  │ - Console     │
│ - Role      │  │ - Toast/snack │
└─────────────┘  │ - Modal       │
                 └───────────────┘
```

### Validation Type

```
Submit empty/invalid form
         │
         ▼
┌─────────────────────────┐
│ What validation?        │
└─────────────────────────┘
     │              │
  HTML5         Custom
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Use:        │  │ Capture:      │
│ validity    │  │ - Error text  │
│ .valid      │  │ - Error class │
│ .message    │  │ - Location    │
└─────────────┘  └───────────────┘
```

## Phase 4: Automation Decisions

### Selector Strategy

```
Element needs selector
         │
         ▼
┌─────────────────────────┐
│ Has accessible role+name│
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ getByRole() │  │ Has testid?   │
└─────────────┘  └───────────────┘
                      │        │
                     Yes      No
                      │        │
                      ▼        ▼
                 ┌────────┐ ┌──────┐
                 │testid()│ │CSS   │
                 └────────┘ │attr  │
                            └──────┘
```

### Multiple Elements Match

```
Selector matches multiple
         │
         ▼
┌─────────────────────────┐
│ Are they same type?     │
└─────────────────────────┘
     │              │
    Yes            No
     │              │
     ▼              ▼
┌─────────────┐  ┌───────────────┐
│ Use:        │  │ Make selector │
│ .first()    │  │ more specific │
│ or .nth(n)  │  │ with parent   │
└─────────────┘  └───────────────┘
```

## Phase 5: Test Failure Decisions

```
Test failed
    │
    ▼
┌─────────────────────────┐
│ MANDATORY: Use          │
│ test-fixer skill        │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Error type?             │
└─────────────────────────┘
    │
┌───┴───┬───────┬─────────┬────────┐
│       │       │         │        │
▼       ▼       ▼         ▼        ▼
Timeout Strict  Text      Element  Nav
        mode    mismatch  not found
│       │       │         │        │
▼       ▼       ▼         ▼        ▼
Wait    .first  Discover  Update   waitFor
longer  or more ACTUAL    selector URL
        specific text
```

## When to Ask User

| Situation | Action |
|-----------|--------|
| Need login credentials | Ask user |
| Payment/transaction testing | Ask user |
| Destructive operations | Ask user |
| Ambiguous business logic | Ask user |
| 3+ consecutive failures | Ask user |
| Site blocks automation | Ask user |
| CAPTCHA encountered | Ask user |
