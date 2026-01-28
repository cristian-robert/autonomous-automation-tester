#!/usr/bin/env python3
"""
Qase.io API Client - Create suites, cases, runs, and report results.

Usage:
  python qase_client.py projects                              # List projects
  python qase_client.py suites <project_code>                 # List suites
  python qase_client.py cases <project_code>                  # List cases
  python qase_client.py search-cases <project_code> <query>   # Search cases by title
  python qase_client.py get-case <project_code> <case_id>     # Get case details
  python qase_client.py create-suite <project_code> '<json>'  # Create suite
  python qase_client.py create-case <project_code> '<json>'   # Create case
  python qase_client.py create-run <project_code> '<json>'    # Create test run
  python qase_client.py report-result <project_code> <run_id> '<json>'  # Report result
  python qase_client.py complete-run <project_code> <run_id>  # Complete a run

Environment:
  QASE_API_TOKEN: Your Qase API token (required)

Examples:
  python qase_client.py search-cases PROJ "login"             # Find existing login tests
  python qase_client.py get-case PROJ 42                      # Get full details of case #42
  python qase_client.py create-suite PROJ '{"title": "Auth Tests"}'
  python qase_client.py create-case PROJ '{"title": "Login works", "suite_id": 1, "severity": 2}'
  python qase_client.py create-run PROJ '{"title": "Smoke Run", "cases": [1,2,3]}'
  python qase_client.py report-result PROJ 1 '{"case_id": 1, "status": "passed"}'
"""

import json
import os
import sys
from typing import Any, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# =============================================================================
# Configuration
# =============================================================================

BASE_URL = "https://api.qase.io/v1"


def get_api_token() -> str:
    """Get Qase API token from environment."""
    token = os.environ.get("QASE_API_TOKEN")
    if not token:
        raise ValueError(
            "QASE_API_TOKEN environment variable not set. "
            "Get your token from Qase → Settings → API Tokens"
        )
    return token


# =============================================================================
# HTTP Client
# =============================================================================

def make_request(
    method: str,
    endpoint: str,
    data: Optional[dict] = None
) -> dict:
    """Make HTTP request to Qase API."""
    url = f"{BASE_URL}{endpoint}"
    token = get_api_token()

    headers = {
        "Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    body = json.dumps(data).encode("utf-8") if data else None

    request = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(request, timeout=30) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data) if response_data else {}
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            raise ValueError(f"API Error: {error_data.get('errorMessage', error_body)}")
        except json.JSONDecodeError:
            raise ValueError(f"HTTP {e.code}: {error_body}")
    except URLError as e:
        raise ValueError(f"Connection error: {e.reason}")


def get(endpoint: str) -> dict:
    return make_request("GET", endpoint)


def post(endpoint: str, data: dict) -> dict:
    return make_request("POST", endpoint, data)


def patch(endpoint: str, data: dict) -> dict:
    return make_request("PATCH", endpoint, data)


def delete(endpoint: str) -> dict:
    return make_request("DELETE", endpoint)


# =============================================================================
# Commands
# =============================================================================

def cmd_projects() -> list:
    """List all projects."""
    response = get("/project")
    projects = response.get("result", {}).get("entities", [])
    return [{"code": p["code"], "title": p["title"]} for p in projects]


def cmd_suites(project_code: str) -> list:
    """List all suites in a project."""
    response = get(f"/suite/{project_code}")
    suites = response.get("result", {}).get("entities", [])
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "cases_count": s.get("cases_count", 0)
        }
        for s in suites
    ]


def cmd_cases(project_code: str, suite_id: Optional[int] = None) -> list:
    """List all cases in a project, optionally filtered by suite."""
    endpoint = f"/case/{project_code}"
    if suite_id:
        endpoint += f"?suite_id={suite_id}"

    response = get(endpoint)
    cases = response.get("result", {}).get("entities", [])
    return [
        {
            "id": c["id"],
            "title": c["title"],
            "suite_id": c.get("suite_id"),
            "priority": c.get("priority"),
            "severity": c.get("severity")
        }
        for c in cases
    ]


def cmd_search_cases(project_code: str, query: str) -> list:
    """Search for test cases by title/keyword. Use to check for existing cases before creating new ones."""
    from urllib.parse import quote
    endpoint = f"/case/{project_code}?search={quote(query)}"

    response = get(endpoint)
    cases = response.get("result", {}).get("entities", [])
    return [
        {
            "id": c["id"],
            "title": c["title"],
            "suite_id": c.get("suite_id"),
            "suite_title": c.get("suite", {}).get("title") if c.get("suite") else None,
            "priority": c.get("priority"),
            "severity": c.get("severity"),
            "automation_status": c.get("automation"),
            "status": c.get("status")
        }
        for c in cases
    ]


def cmd_get_case(project_code: str, case_id: int) -> dict:
    """Get full details of a specific test case."""
    response = get(f"/case/{project_code}/{case_id}")
    c = response.get("result", {})
    return {
        "id": c.get("id"),
        "title": c.get("title"),
        "suite_id": c.get("suite_id"),
        "description": c.get("description"),
        "preconditions": c.get("preconditions"),
        "postconditions": c.get("postconditions"),
        "priority": c.get("priority"),
        "severity": c.get("severity"),
        "automation_status": c.get("automation"),
        "steps": c.get("steps", []),
        "tags": c.get("tags", []),
        "created_at": c.get("created_at"),
        "updated_at": c.get("updated_at")
    }


def cmd_create_suite(project_code: str, data: dict) -> dict:
    """Create a new test suite."""
    response = post(f"/suite/{project_code}", data)
    result = response.get("result", {})
    return {
        "id": result.get("id"),
        "title": data.get("title"),
        "status": "created"
    }


def cmd_create_case(project_code: str, data: dict) -> dict:
    """Create a new test case."""
    response = post(f"/case/{project_code}", data)
    result = response.get("result", {})
    return {
        "id": result.get("id"),
        "title": data.get("title"),
        "suite_id": data.get("suite_id"),
        "status": "created"
    }


def cmd_create_run(project_code: str, data: dict) -> dict:
    """Create a new test run."""
    # Default to autotest
    if "is_autotest" not in data:
        data["is_autotest"] = True

    response = post(f"/run/{project_code}", data)
    result = response.get("result", {})
    return {
        "id": result.get("id"),
        "title": data.get("title"),
        "status": "created"
    }


def cmd_report_result(project_code: str, run_id: int, data: dict) -> dict:
    """Report a test result."""
    response = post(f"/result/{project_code}/{run_id}", data)
    result = response.get("result", {})
    return {
        "hash": result.get("hash"),
        "case_id": data.get("case_id"),
        "status": data.get("status"),
        "recorded": True
    }


def cmd_bulk_results(project_code: str, run_id: int, results: list) -> dict:
    """Report multiple test results at once."""
    response = post(f"/result/{project_code}/{run_id}/bulk", {"results": results})
    return {
        "count": len(results),
        "status": "recorded"
    }


def cmd_complete_run(project_code: str, run_id: int) -> dict:
    """Complete a test run."""
    response = post(f"/run/{project_code}/{run_id}/complete", {})
    return {
        "run_id": run_id,
        "status": "completed"
    }


# =============================================================================
# CLI Interface
# =============================================================================

def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, default=str))


def print_error(message: str, error_type: str = "error") -> None:
    """Print error as JSON."""
    print(json.dumps({"error": message, "type": error_type}))


def print_usage():
    """Print usage information."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command in ("--help", "-h", "help"):
        print_usage()
        sys.exit(0)

    try:
        if command == "projects":
            result = cmd_projects()
            print_json(result)

        elif command == "suites":
            if len(sys.argv) < 3:
                print_error("Usage: suites <project_code>", "usage")
                sys.exit(1)
            result = cmd_suites(sys.argv[2])
            print_json(result)

        elif command == "cases":
            if len(sys.argv) < 3:
                print_error("Usage: cases <project_code> [suite_id]", "usage")
                sys.exit(1)
            suite_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
            result = cmd_cases(sys.argv[2], suite_id)
            print_json(result)

        elif command == "search-cases":
            if len(sys.argv) < 4:
                print_error("Usage: search-cases <project_code> <query>", "usage")
                sys.exit(1)
            result = cmd_search_cases(sys.argv[2], sys.argv[3])
            print_json(result)

        elif command == "get-case":
            if len(sys.argv) < 4:
                print_error("Usage: get-case <project_code> <case_id>", "usage")
                sys.exit(1)
            result = cmd_get_case(sys.argv[2], int(sys.argv[3]))
            print_json(result)

        elif command == "create-suite":
            if len(sys.argv) < 4:
                print_error("Usage: create-suite <project_code> '<json>'", "usage")
                sys.exit(1)
            data = json.loads(sys.argv[3])
            result = cmd_create_suite(sys.argv[2], data)
            print_json(result)

        elif command == "create-case":
            if len(sys.argv) < 4:
                print_error("Usage: create-case <project_code> '<json>'", "usage")
                sys.exit(1)
            data = json.loads(sys.argv[3])
            result = cmd_create_case(sys.argv[2], data)
            print_json(result)

        elif command == "create-run":
            if len(sys.argv) < 4:
                print_error("Usage: create-run <project_code> '<json>'", "usage")
                sys.exit(1)
            data = json.loads(sys.argv[3])
            result = cmd_create_run(sys.argv[2], data)
            print_json(result)

        elif command == "report-result":
            if len(sys.argv) < 5:
                print_error("Usage: report-result <project_code> <run_id> '<json>'", "usage")
                sys.exit(1)
            data = json.loads(sys.argv[4])
            result = cmd_report_result(sys.argv[2], int(sys.argv[3]), data)
            print_json(result)

        elif command == "bulk-results":
            if len(sys.argv) < 5:
                print_error("Usage: bulk-results <project_code> <run_id> '<json_array>'", "usage")
                sys.exit(1)
            results = json.loads(sys.argv[4])
            result = cmd_bulk_results(sys.argv[2], int(sys.argv[3]), results)
            print_json(result)

        elif command == "complete-run":
            if len(sys.argv) < 4:
                print_error("Usage: complete-run <project_code> <run_id>", "usage")
                sys.exit(1)
            result = cmd_complete_run(sys.argv[2], int(sys.argv[3]))
            print_json(result)

        else:
            print_error(f"Unknown command: {command}", "usage")
            print_usage()
            sys.exit(1)

    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}", "invalid_json")
        sys.exit(1)
    except ValueError as e:
        print_error(str(e), "validation")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {e}", "error")
        sys.exit(1)


if __name__ == "__main__":
    main()
