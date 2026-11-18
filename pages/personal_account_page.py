from pages.base_page import BasePage
from locators.personal_account_locators import PersonalAccountLocators


class PersonalAccountPage(BasePage):
    def is_account_page_opened(self):
        """Проверяет, что открыта страница личного кабинета"""
        return self.find_element(PersonalAccountLocators.ACCOUNT_TITLE).is_displayed()

    def click_order_history(self):
        """Кликает на раздел 'История заказов'"""
        self.click_element(PersonalAccountLocators.HISTORY_BUTTON)

    def click_logout(self):
        """Кликает на кнопку 'Выход'"""
        self.click_element(PersonalAccountLocators.LOGOUT_BUTTON)