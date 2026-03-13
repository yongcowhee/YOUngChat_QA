from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.base_page import BasePage
from conftest import *

def test_signup(setup):
    page = setup
    base_page = BasePage(page)
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    test_username = TEST_USER_NAME
    test_email = TEST_USER_EMAIL
    test_pw = TEST_USER_PASSWORD

    base_page.navigate()

    login_page.signup()
    signup_page.fill_signup_field(test_username, test_email, test_pw)

    # 이메일 인증 버튼 클릭 + alert 검증
    base_page.confirm_alert_massage(
        "이메일에 코드가 전송되었습니다.",
        lambda: signup_page.send_auth_email()
    )

    code = signup_page.get_email_auth_code()
    print(f"📨 수신된 인증코드: {code}")

    # 이메일 인증 확인 버튼 클릭
    signup_page.fill_and_click_auth_email_confirm(code)

    # 회원가입 버튼 클릭 + alert 검증
    base_page.confirm_alert_massage(
        "회원가입을 축하드립니다!",
        lambda: signup_page.click_confirm_signup_button()
    )


