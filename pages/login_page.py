from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.input_email = page.locator("#email")
        self.input_pw = page.locator("#password")
        self.login_button = page.get_by_role("button",name = "Login") # "버튼"이라는 역할과 그 위의 "Login" 텍스트로 요소 찾아냄
        self.signup_button = page.get_by_role("link", name="가입하신 적이 없으시나요? 회원가입")

    def navigate(self):
        return super().navigate("login")
    
    def signup(self):
        self.signup_button.click()
        
    def login(self, email:str, pw:str):
        self.input_email.fill(email)
        self.input_pw.fill(pw)
        self.login_button.click()
    
    # 로그인 후 메인 페이지 이동 대기
    def login_and_wait(self, email: str, password: str):
        self.page.on("dialog", lambda d: d.accept())
        self.login(email, password)
        self.page.wait_for_url("**/", timeout=5000)