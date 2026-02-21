from playwright.sync_api import Page

class RegisterPage:
    URL = "https://qa-test-web-app.vercel.app/register.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_label("First Name")
        self.last_name = page.get_by_label("Last Name")
        self.email = page.get_by_label("Email Address")
        self.phone = page.get_by_label("Phone Number")
        self.street = page.get_by_label("Street Address")
        self.city = page.get_by_label("City")
        self.zip_code = page.get_by_label("ZIP Code")
        self.password = page.get_by_label("Password", exact=True)
        self.confirm_password = page.get_by_label("Confirm Password")
        self.terms_checkbox = page.get_by_label("I agree to the Terms and Conditions")
        self.newsletter = page.get_by_label("Subscribe to newsletter")
        self.submit_button = page.get_by_role("button", name="Create Account")

    def open(self):
        self.page.goto(self.URL)

    def submit(self):
        self.submit_button.click()

    