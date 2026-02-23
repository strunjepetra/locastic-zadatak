# QA Test Automation — Locastic Task

Automated test suite for the QA Test Web Application registration and login flow, built with Playwright + Pytest following the Page Object Model pattern.

**Application under test:** https://qa-test-web-app.vercel.app/

---

## Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.14.3 |
| Playwright | 1.58.0 |
| pytest | 9.0.2 |
| pytest-playwright | 0.7.2 |

---

## Project Structure

```
locastic-zadatak/
├── pages/
│   ├── __init__.py
│   ├── register_page.py      # RegisterPage — all locators and actions
│   └── login_page.py         # LoginPage — all locators and actions
├── helpers/
│   ├── __init__.py
│   └── test_data.py          # Utility: unique email generator
├── tests/
│   ├── __init__.py
│   └── test_registration.py  # All test classes
├── conftest.py               # Shared fixtures (register_page, filled_form)
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.11 or higher
- Git

### 1. Clone the repository

```bash
git clone https://github.com/strunjepetra/locastic-zadatak.git
cd locastic-zadatak
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install chromium
```

---

## Running Tests

```bash
# Run all tests (headless)
python -m pytest tests/ -v

# Run with browser visible
python -m pytest tests/ -v --headed

# Run a specific test class
python -m pytest tests/ -v -k "TestPageLoaded"

# Run a specific test
python -m pytest tests/ -v -k "test_page_title_is_correct"

# Generate HTML report
python -m pytest tests/ -v --html=report.html --self-contained-html
```

---

## Test Classes

| Class | Description | Expected Result |
|-------|-------------|-----------------|
| `TestPageLoaded` | Page title, field visibility, default checkbox states | PASS |
| `TestSuccessfulRegistration` | Valid registration flow with and without newsletter | FAIL* |
| `TestRequiredFields` | Required field enforcement (email, password, terms) | PASS |
| `TestEmailValidation` | Invalid email format rejection | PASS |
| `TestPasswordStrength` | Password rules (length, uppercase, special character) | PASS |
| `TestPasswordConfirmation` | Password mismatch detection | PASS |
| `TestEdgeCases` | Whitespace-only input, SQL injection | PASS |
| `TestLoginFlow` | Login with valid/invalid credentials | FAIL* |

> **\*Note on failures:** Both failures share the same root cause — registration submitted through Playwright does not save the user to the database, even though the form fills and submits without errors. This is a confirmed application behaviour difference between automation and manual testing, not a test script error. See the QA Test Report for full details.

---

## Test Results Summary

| | |
|-|-|
| Total tests | 21 |
| Passed | 19 |
| Failed | 2 |
| Pass rate | 90% |
| Execution time | 36.68s |