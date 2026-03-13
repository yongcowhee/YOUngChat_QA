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

    def click_my_page(self):
        self.mypage_button.click()

    def click_logout(self):
        self.logout_button.click()

    def verify_user_name(self, page, expect_username:str):
        assert page.get_by_text(f"{expect_username} 님")