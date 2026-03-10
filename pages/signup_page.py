from pages.base_page import BasePage

class SignupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.input_username = page.get_by_role("textbox", name="Username")
        self.input_email = page.get_by_role("textbox", name="Email Address")
        self.input_pw = page.get_by_role("textbox", name="Password")

        self.auth_email_button = page.get_by_role("button", name="인증")
        self.input_email_verify_code = page.get_by_role("textbox", name="Code")
        self.confirm_email_button = page.get_by_role("button", name="확인")

        self.confirm_signup_button = page.get_by_role("button", name="Sign Up")

    def fill_signup_field(self, user_name:str, email:str, pw:str):
        self.input_username.fill(user_name)
        self.input_email.fill(email)
        self.input_pw.fill(pw)