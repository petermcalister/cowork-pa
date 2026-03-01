---
paths: "**/features/**/*ui*.py, **/features/**/*playwright*.py, **/pages/**/*.py"
---

# Playwright + Behave Testing Patterns

**Purpose:** Browser automation testing patterns for Streamlit or web UIs using Playwright with Python Behave.

---

## Setup

### Environment.py

```python
from playwright.sync_api import sync_playwright

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    context.base_url = os.getenv("APP_URL", "http://localhost:8501")

def before_scenario(context, scenario):
    context.page = context.browser.new_page()
    context.page.set_default_timeout(10000)

def after_scenario(context, scenario):
    if hasattr(context, 'page'):
        context.page.close()

def after_all(context):
    context.browser.close()
    context.playwright.stop()
```

---

## Page Object Pattern

```python
# pages/dashboard_page.py
class DashboardPage:
    def __init__(self, page):
        self.page = page

    def navigate(self, base_url: str):
        self.page.goto(base_url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        return self.page.title()

    def click_button(self, label: str):
        self.page.get_by_role("button", name=label).click()

    def fill_input(self, label: str, value: str):
        self.page.get_by_label(label).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()
```

---

## Step Definitions

```python
@given('I am on the Dashboard page')
def step_navigate_dashboard(context):
    context.dashboard = DashboardPage(context.page)
    context.dashboard.navigate(context.base_url)

@when('I enter "{text}" in the search field')
def step_enter_search(context, text):
    context.dashboard.fill_input("Search", text)

@when('I click the "{button_name}" button')
def step_click_button(context, button_name):
    context.dashboard.click_button(button_name)

@then('I should see "{expected_text}"')
def step_verify_text(context, expected_text):
    content = context.page.content()
    assert expected_text in content, f"Expected '{expected_text}' not found"
```

---

## Streamlit-Specific Selectors

```python
# Streamlit renders custom elements - use these patterns:

# Text input by label
page.get_by_label("Name")

# Button by text
page.get_by_role("button", name="Submit")

# Selectbox (Streamlit uses custom dropdowns)
page.locator('[data-testid="stSelectbox"]').first

# Sidebar elements
page.locator('[data-testid="stSidebar"]').get_by_label("Filter")

# Wait for Streamlit to finish re-running
page.wait_for_load_state("networkidle")
```

---

## Feature File Example

```gherkin
@ui
Feature: Dashboard Interaction

  Background:
    Given I am on the Dashboard page

  Scenario: Search returns results
    When I enter "test query" in the search field
    And I click the "Search" button
    Then I should see "Results"

  Scenario: Empty state shown
    Then I should see "No data available"
```

---

## Debugging Flaky Tests

```python
# Take screenshot on failure
def after_scenario(context, scenario):
    if scenario.status == "failed" and hasattr(context, 'page'):
        context.page.screenshot(path=f"screenshots/{scenario.name}.png")
    if hasattr(context, 'page'):
        context.page.close()
```

```bash
# Run with headed browser for debugging
# Set HEADLESS=false in environment.py

# Run specific UI tests
poetry run behave --tags=@ui -v --no-capture
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Element not found | Wait for `networkidle` after navigation/clicks |
| Timeout on Streamlit rerun | Increase timeout, wait for load state |
| Flaky selector | Use `get_by_role` or `get_by_label` over CSS selectors |
| Browser not closed | Always close in `after_scenario` and `after_all` |
| Screenshots missing on CI | Create `screenshots/` directory before test run |
