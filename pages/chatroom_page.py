from pages.base_page import BasePage

class ChatroomPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.message_input = page.get_by_placeholder("보낼 메세지를 입력해주세요")
        self.send_button = page.get_by_role("button", name = "directions")

    def send_message(self, message: str):
        self.message_input.fill(message)
        self.send_button.click()

    # 채팅방 마지막 메시지 반환
    def get_last_message(self):
        messages = self.page.locator("#scrollableDiv .MuiTypography-body1")
        return messages.last.inner_text()

    # 텍스트가 화면에 나타날 때까지 5초간 대기
    def wait_for_message(self, text: str, timeout: int = 5000):
        self.page.locator("#scrollableDiv").get_by_text(text).wait_for(timeout=timeout)