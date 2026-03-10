import time     # 시간 관련 함수 라이브러리 - 이메일 수신 대기에 사용
import requests  # HTTP 요청 라이브러리 - Mailpit API 호출에 사용
import re        # 정규표현식 라이브러리 - 메일 본문에서 인증코드 추출에 사용

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

    def click_auth_email(self):
        self.auth_email_button.click()
        time.sleep(2)  # 메일이 Mailpit에 도달할 때까지 2초 대기

    def get_email_auth_code(self, to_email: str):
        res = requests.get("http://localhost:8025/api/v1/messages")
        messages = res.json()["messages"]

        assert len(messages) > 0, "❌ Mailpit에 수신된 메일이 없습니다. 이메일 발송이 됐는지 확인해주세요."

        latest_message = messages[0]
        snippet = latest_message["Snippet"]  # "YOUngChat 인증 코드입니다. CODE : 75a2329b" 형태

        print("📨 수신된 메시지 본문 : " ,snippet)

        code = re.search(r'[a-f0-9]{8}', snippet).group()

        assert code is not None, "❌ 인증코드를 찾을 수 없습니다."

        return code