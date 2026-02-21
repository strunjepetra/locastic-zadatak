from playwright.sync_api import Page

class LoginPage:
    URL  = "https://qa-test-web-app.vercel.app/index.html"

    def __init__(self, page: Page):
        self.page = page
        self.email = page.get_by_label("Email Address")
        self.password = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button")

    def open(self):
        self.page.goto(self.URL)

    def login(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        self.submit_button.click()
        