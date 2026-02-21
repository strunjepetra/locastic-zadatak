import pytest
from playwright.sync_api import expect
from pages.register_page import RegisterPage
from helpers.test_data import make_unique_email

class TestPageLoaded:
    """
    Verifies registration page loads correctly and all fields are visible.
    All elements are in default (empty) state.

    Expect all cases to PASS
    """

    def test_page_title_is_correct(self, register_page: RegisterPage):
        expect(register_page.page).to_have_title("QA Test Application - Register")

    def test_all_fields_are_visible(self, register_page: RegisterPage):
        expect(register_page.first_name).to_be_visible()
        expect(register_page.last_name).to_be_visible()
        expect(register_page.email).to_be_visible()
        expect(register_page.phone).to_be_visible()
        expect(register_page.street).to_be_visible()
        expect(register_page.city).to_be_visible()
        expect(register_page.zip_code).to_be_visible()
        expect(register_page.password).to_be_visible()
        expect(register_page.confirm_password).to_be_visible()
        expect(register_page.terms_checkbox).to_be_visible()
        expect(register_page.submit_button).to_be_visible()

    def test_terms_are_unchecked_by_default(self, register_page: RegisterPage):
        expect(register_page.terms_checkbox).not_to_be_checked()

    def test_newsletter_unchecked_by_default(self, register_page: RegisterPage):
        expect(register_page.newsletter).not_to_be_checked()

    def test_login_link_visible_and_works(self, register_page: RegisterPage):
        link = register_page.page.get_by_role(
            "link", name="Already have an account? Login")
        expect(link).to_be_visible()
        link.click()
        expect(register_page.page).to_have_url(
            "https://qa-test-web-app.vercel.app/index.html"
        )

class TestSuccessfulRegistration:
    """
    Verifies valid regisztration succeeds
    NOTE: These tests FAIL because of application bugs:
    - App does not redirect after successful registration
    - No success message is displayed

    Expected to FAIL.
    """
    def test_valid_registration_succeeds(self, register_page: RegisterPage):
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
        register_page.submit()

        url_changed = register_page.page.url != RegisterPage.URL
        shows_success = register_page.page.get_by_text("success").is_visible()
        body = register_page.page.inner_text("body").lower()

        assert url_changed or shows_success, (
            f"Registration should succeed. "
            f"URL: {register_page.page.url} | "
            f"Page: {body[:150]}"
        )

    def test_checked_newsletter(self, register_page: RegisterPage):
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
        register_page.newsletter.check()
        register_page.submit()

        url_changed = register_page.page.url != RegisterPage.URL
        shows_success = register_page.page.get_by_text("success").is_visible()
        body = register_page.page.inner_text("body").lower()

        assert url_changed or shows_success, (
            f"Registration with newsletter should succeed. "
            f"URL: {register_page.page.url} | "
            f"Page: {body[:150]}"
        )


class TestRequiredFields:
    """
    Verifies form can not be submitted without required fields.

    Expect to PASS.
    """
    def test_missing_email_blocks_form(self, filled_form: RegisterPage):
        filled_form.email.clear()
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Form should not submit without email. "
            f"Current URL: {filled_form.page.url}"
        )

    def test_missing_password_blocks_form(self, filled_form: RegisterPage):
        filled_form.password.clear()
        filled_form.confirm_password.clear()
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Form should not submit without password. "
            f"Current URL: {filled_form.page.url}"
        )
        
    def test_unchecked_terms_blocks_form(self, filled_form: RegisterPage):
        filled_form.terms_checkbox.uncheck()
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Form should not submit without password. "
            f"Current URL: {filled_form.page.url}"
        )

class TestEmailValidation:
    """
    Verifies invalid email formats are rejected.
    
    Expect to PASS
    """

    def test_email_without_at_is_rejected(self, filled_form: RegisterPage):
        filled_form.email.fill("johndoeexample.com")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Email without @ should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )
        
    def test_email_without_domain_is_rejected(self, filled_form: RegisterPage):
        filled_form.email.fill("johndoeexample@")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Plain text should not be accepted as email. "
            f"Current URL: {filled_form.page.url}"
        )
        
    def test_plain_text_as_email_is_rejected(self, filled_form: RegisterPage):
        filled_form.email.fill("johndoeexample")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Email without domain should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )


class TestPasswordStrength:
    """
    Verifies weak passwords are rejected.

    Expect to FAIL.
    """

    def test_password_too_short_is_rejected(self, filled_form: RegisterPage):
       filled_form.password.fill("Pa1!")
       filled_form.confirm_password.fill("Pa1!")
       filled_form.submit()
       assert filled_form.page.url == RegisterPage.URL, (
            f"Password is too short and should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )

    def test_password_without_uppercase_is_rejected(self, filled_form: RegisterPage):
        filled_form.password.fill("pa1!")
        filled_form.confirm_password.fill("pa1!")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Password without uppercase should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )

    def test_password_without_spec_character_is_rejected(self, filled_form: RegisterPage):
        filled_form.password.fill("Pass1")
        filled_form.confirm_password.fill("Pass1")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Password without uppercase should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )


class TestPasswordConfirmation:
    """
    Verifies passwords should match to complete form
    
    Expected to FAIL.
    """

    def test_different_passwords_should_be_rejected(self, filled_form: RegisterPage):
        filled_form.password.fill("Pass1!")
        filled_form.confirm_password.fill("Password1!")
        filled_form.submit()
        assert filled_form.page.url == RegisterPage.URL, (
            f"Passwords that do not match should be rejected. "
            f"Current URL: {filled_form.page.url}"
        )

class TestEdgeCases:
    """
    Verifies application behavior wit unusual or malicious input.
    Expect: whitespace to FAIL, SQL to PASS
    """

    def test_whitespace_only_should_be_rejected(self, register_page: RegisterPage):
        register_page.first_name.fill(" ")
        register_page.last_name.fill(" ")
        register_page.email.fill(make_unique_email())
        register_page.phone.fill("          ")
        register_page.street.fill(" ")
        register_page.city.fill(" ")
        register_page.zip_code.fill("     ")
        register_page.password.fill("      ")
        register_page.confirm_password.fill("      ")
        register_page.terms_checkbox.check()
        register_page.submit()

        assert register_page.page.url == RegisterPage.URL, ("Whitespace only should be rejected!")

    def test_sql_injection_no_error(self, register_page: RegisterPage):
        register_page.first_name.fill("John")
        register_page.last_name.fill("Doe")
        register_page.email.fill(make_unique_email())
        register_page.phone.fill("098759523")
        register_page.street.fill("Test Street")
        register_page.city.fill("Split")
        register_page.zip_code.fill("21000")
        register_page.password.fill("Pass1!")
        register_page.confirm_password.fill("Pass1!")
        register_page.terms_checkbox.check()
        register_page.submit()

        body = register_page.page.inner_text("body").lower()
        assert "sql" not in body and "database" not in body, (
            f"SQL injection should not expose db errors"
            f"Page content: {body[:200]}"
            )