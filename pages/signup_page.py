import requests   # HTTP 요청 라이브러리 - Mailpit API 호출에 사용
import re         # 정규표현식 라이브러리 - Snippet에서 인증코드 추출에 사용
import time       # 시간 관련 함수 라이브러리 - 폴링 대기에 사용

from pages.base_page import BasePage
from playwright.sync_api import expect  # Playwright 명시적 검증 라이브러리

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

    def send_auth_email(self):
        self.auth_email_button.click()

    def get_email_auth_code(self):
        # 1. 루프 시작 전, 현재 Mailpit에 있는 가장 최신 메시지 ID를 가져옴
        initial_res = requests.get("http://localhost:8025/api/v1/messages")
        initial_messages = initial_res.json()["messages"]
        last_known_id = initial_messages[0]["ID"] if initial_messages else None

        timeout = 10
        interval = 1

        for _ in range(timeout // interval):
            res = requests.get("http://localhost:8025/api/v1/messages")
            messages = res.json()["messages"]

            if messages:
                latest_message = messages[0]
                if latest_message["ID"] != last_known_id:
                    snippet = latest_message["Snippet"]
                    code = re.search(r'[a-f0-9]{8}', snippet).group()
                    return code

            time.sleep(interval)

        assert False, "❌ 신규 메일이 도착하지 않았습니다."

    def fill_and_click_auth_email_confirm(self, code):
        self.input_email_verify_code.fill(code)
        self.confirm_email_button.click()
        expect(self.input_email).to_be_disabled()  # 이메일 input 비활성화 명시적 대기

    def click_confirm_signup_button(self):
        self.confirm_signup_button.click()
