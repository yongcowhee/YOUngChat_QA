class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, path=""):  # 기본값이 빈 문자열 -> / "루트" 페이지로 이동
        from conftest import FRONT_URL  # conftest.py 파일에서 FRONT_URL 가져옴
        self.page.goto(f"{FRONT_URL}/{path}")

    def confirm_alert_massage(self, expected_message: str, trigger):
        # expect_event("dialog")로 alert가 뜰 때까지 대기 + 잡기
        with self.page.expect_event("dialog", timeout=5000) as dialog_info:
            trigger()

        dialog = dialog_info.value
        assert expected_message in dialog.message, \
            f"❌ 예상 메시지: {expected_message}, 실제 메시지: {dialog.message}"
        dialog.accept()
