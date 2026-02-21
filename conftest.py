import pytest
from playwright.sync_api import Page
from pages.register_page import RegisterPage
from helpers.test_data import make_unique_email

@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    rp = RegisterPage(page)
    rp.open()
    return rp

@pytest.fixture
def filled_form(register_page: RegisterPage):
    register_page.first_name.fill("John")
    register_page.last_name.fill("Doe")
    register_page.email.fill(make_unique_email())
    register_page.phone.fill("0911234567")
    register_page.street.fill("123 Main Street")
    register_page.city.fill("Split")
    register_page.zip_code.fill("21000")
    register_page.password.fill("SecurePass1!")
    register_page.confirm_password.fill("SecurePass1!")
    register_page.terms_checkbox.check()
    return register_page