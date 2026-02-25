class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, path=""): # 기본값이 빈 문자열 -> / "루트" 페이지로 이동
        from conftest import FRONT_URL # conftest.py 파일에서 FRONT_URL 가져옴
        self.page.goto(f"{FRONT_URL}/{path}")

    def wait_for_alert_and_accept(self):
        self.page.on("dialog", lambda dialog: dialog.accept()) # alert 발생 시 자동으로 확인 버튼 클릭