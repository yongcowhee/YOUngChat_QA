from pages.base_page import BasePage

class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.friend_button = page.get_by_role("button", name = "Friend")
        self.chat_button    = page.get_by_role("button", name="Chat")
        self.mypage_button  = page.get_by_role("button", name="MyPage")
        self.logout_button  = page.get_by_role("button", name="Logout")

    def click_friend(self):
        self.friend_button.click()

    def click_chat(self):
        self.chat_button.click()

    def click_mypage(self):
        self.mypage_button.click()

    def click_logout(self):
        self.wait_for_alert_and_accept()
        self.logout_button.click()