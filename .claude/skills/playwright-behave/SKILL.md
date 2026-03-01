---
name: playwright-behave
description: Use when writing Playwright browser tests with Python Behave - creating step definitions, page objects, debugging flaky UI tests, or handling browser lifecycle in environment.py
---

# Playwright + Behave Testing

## Overview

Test UI behavior through user-visible interactions, not DOM structure. Playwright's auto-waiting and role-based selectors make tests resilient to implementation changes.

**Core principle:** If your test breaks when CSS classes change, you're testing the wrong thing.

## When to Use

- Writing browser automation tests with Python Behave
- Creating page objects for UI components
- Debugging "element not found" or flaky test failures
- Setting up browser lifecycle in `environment.py`
- Converting manual UI tests to automated BDD tests

## When NOT to Use

| Situation | Use Instead |
|-----------|-------------|
| API endpoint testing | `requests` + pytest |
| Unit testing Python code | pytest directly |
| Static HTML validation | BeautifulSoup/lxml |
| Load/performance testing | Locust or k6 |

## Quick Reference

| Task | Pattern |
|------|---------|
| Find button | `page.get_by_role("button", name="Submit")` |
| Find form field | `page.get_by_label("Email")` |
| Find by text | `page.get_by_text("Welcome")` |
| Find by test ID | `page.get_by_test_id("submit-btn")` |
| Wait for load | `page.wait_for_load_state("networkidle")` |
| Assert visible | `expect(element).to_be_visible()` |
| Assert URL | `expect(page).to_have_url_matching(r".*/dashboard")` |
| Debug selectors | `playwright codegen http://localhost:8501` |
| View trace | `playwright show-trace traces/scenario.zip` |

## Selector Priority (Most to Least Preferred)

1. **Role** - `get_by_role("button", name="Submit")` - mirrors accessibility
2. **Label** - `get_by_label("Email")` - form fields
3. **Text** - `get_by_text("Welcome")` - visible content
4. **Test ID** - `get_by_test_id("submit-btn")` - stable, requires `data-testid` attribute
5. **CSS/XPath** - last resort only

## Complete Example: Login Flow

**Directory structure:**
```
features/
├── environment.py      # Browser lifecycle hooks
├── login.feature       # Gherkin scenarios
├── pages/
│   ├── base_page.py    # Shared navigation
│   └── login_page.py   # Login-specific selectors
└── steps/
    └── login_steps.py  # Step implementations
```

**environment.py** - Browser lifecycle:
```python
from playwright.sync_api import sync_playwright

def before_scenario(context, scenario):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    context.page = context.browser.new_page()

def after_scenario(context, scenario):
    context.page.close()
    context.browser.close()
    context.playwright.stop()
```

**pages/base_page.py** - Shared behavior:
```python
class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
```

**pages/login_page.py** - Page object:
```python
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Login")

    def login(self, user: str, pwd: str):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
```

**steps/login_steps.py** - Step definitions:
```python
from behave import given, when, then
from playwright.sync_api import expect
from pages.login_page import LoginPage

@given("the user is on the login page")
def step_impl(context):
    context.login_page = LoginPage(context.page)
    context.login_page.navigate("http://localhost:8501")

@when('they enter username "{user}" and password "{pwd}"')
def step_impl(context, user, pwd):
    context.login_page.login(user, pwd)

@then("they should see the dashboard")
def step_impl(context):
    expect(context.page).to_have_url_matching(r".*/dashboard")
```

**login.feature** - Gherkin:
```gherkin
@uiLayout
Feature: User Login

  Scenario: Successful login
    Given the user is on the login page
    When they enter username "testuser" and password "secret"
    Then they should see the dashboard
```

## Debugging Workflow

```
1. Test fails
      ↓
2. Run codegen to find correct selector
   $ playwright codegen http://localhost:8501
      ↓
3. If still failing, enable tracing (see below)
      ↓
4. View trace to see what happened
   $ playwright show-trace traces/scenario.zip
      ↓
5. Update selector in page object
      ↓
6. Re-run test
```

### Enable Tracing for Failed Tests

```python
# environment.py - with tracing
def before_scenario(context, scenario):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    context.browser_context = context.browser.new_context()
    context.browser_context.tracing.start(screenshots=True, snapshots=True)
    context.page = context.browser_context.new_page()

def after_scenario(context, scenario):
    # Save trace on failure
    if scenario.status == "failed":
        trace_path = f"traces/{scenario.name.replace(' ', '_')}.zip"
        context.browser_context.tracing.stop(path=trace_path)
    else:
        context.browser_context.tracing.stop()
    context.page.close()
    context.browser_context.close()
    context.browser.close()
    context.playwright.stop()
```

## Data-Focused Assertions

```python
# Table row count
rows = page.locator("table tbody tr")
expect(rows).to_have_count(5)

# First element visible
bars = page.locator("svg rect.bar")
expect(bars.first).to_be_visible()

# Extract and validate text
cell_text = page.locator("td.amount").first.text_content()
assert float(cell_text.replace("$", "")) > 0
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `sleep()` for waits | Playwright auto-waits; use `wait_for_load_state()` if needed |
| CSS selectors for buttons | Use `get_by_role("button", name="...")` |
| Selectors in step definitions | Move to page objects for maintainability |
| Sharing state between scenarios | Each scenario gets fresh browser context |
| Using async API with Behave | Use `sync_api`; async conflicts with Behave's event loop |
| Hardcoded URLs in steps | Pass URL to page object's `navigate()` method |

## Key Principles

- **Test isolation**: Each scenario gets fresh browser context
- **No shared state**: Don't rely on previous scenario's side effects
- **Playwright auto-waits**: No need for explicit `sleep()` calls
- **Keep selectors in page objects**: Steps should read like English
- **Async note**: Use `sync_api` with Behave; async API conflicts with Behave's event loop
