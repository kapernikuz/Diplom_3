from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    def is_login_page_opened(self):
        return self.find_element(LoginPageLocators.LOGIN_TITLE).is_displayed()

    def login(self, email, password):
        self.find_element(LoginPageLocators.EMAIL_INPUT).clear()
        self.find_element(LoginPageLocators.EMAIL_INPUT).send_keys(email)
        self.find_element(LoginPageLocators.PASSWORD_INPUT).clear()
        self.find_element(LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)

        # Ждём, пока уйдём со страницы логина
        self.wait.until(lambda d: "login" not in d.current_url)

    def click_recovery_link(self):
        self.click_element(LoginPageLocators.RECOVERY_LINK)

    def click_register_link(self):
        self.click_element(LoginPageLocators.REGISTER_LINK)