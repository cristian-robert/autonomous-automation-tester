# Qase API Reference

Base URL: `https://api.qase.io/v1`

## Authentication

All requests require header:
```
Token: YOUR_API_TOKEN
```

## Endpoints

### Projects

**List projects**
```
GET /project
```

**Get project**
```
GET /project/{code}
```

### Suites

**List suites**
```
GET /suite/{code}
```

**Create suite**
```
POST /suite/{code}

{
  "title": "Authentication Tests",
  "description": "Tests for login and registration",
  "preconditions": "User must be logged out",
  "parent_id": null  // Optional: for nested suites
}
```

**Update suite**
```
PATCH /suite/{code}/{id}
```

**Delete suite**
```
DELETE /suite/{code}/{id}
```

### Cases

**List cases**
```
GET /case/{code}
GET /case/{code}?suite_id=1  // Filter by suite
```

**Create case**
```
POST /case/{code}

{
  "title": "Valid login redirects to dashboard",
  "suite_id": 1,
  "severity": 2,
  "priority": 1,
  "behavior": 1,
  "automation": 2,
  "preconditions": "User exists",
  "postconditions": "User is logged in",
  "steps": [
    {
      "action": "Navigate to /login",
      "expected_result": "Form visible"
    }
  ]
}
```

**Severity values:**
- 0: Not set
- 1: Blocker
- 2: Critical
- 3: Major
- 4: Normal
- 5: Minor
- 6: Trivial

**Priority values:**
- 0: Not set
- 1: High
- 2: Medium
- 3: Low

**Automation values:**
- 0: Not automated
- 1: To be automated
- 2: Automated

### Runs

**List runs**
```
GET /run/{code}
```

**Create run**
```
POST /run/{code}

{
  "title": "Smoke Test - 2024-01-15",
  "description": "Automated smoke test",
  "cases": [1, 2, 3],  // Case IDs to include
  "is_autotest": true
}
```

**Complete run**
```
POST /run/{code}/{id}/complete
```

### Results

**Report result**
```
POST /result/{code}/{run_id}

{
  "case_id": 1,
  "status": "passed",
  "time_ms": 1500,
  "comment": "Test passed successfully",
  "stacktrace": null,
  "attachments": []
}
```

**Bulk report**
```
POST /result/{code}/{run_id}/bulk

{
  "results": [
    {"case_id": 1, "status": "passed", "time_ms": 1000},
    {"case_id": 2, "status": "failed", "time_ms": 2000, "comment": "Assertion failed"}
  ]
}
```

**Status values:**
- passed
- failed
- blocked
- skipped
- invalid

## Response Format

All responses follow:
```json
{
  "status": true,
  "result": { ... }
}
```

## Error Handling

```json
{
  "status": false,
  "errorMessage": "Description of error"
}
```

## Rate Limits

- 600 requests per minute
- Bulk operations recommended for large test suites
