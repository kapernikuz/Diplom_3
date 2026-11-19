from pages.base_page import BasePage
from locators.recovery_page_locators import RecoveryPageLocators


class RecoveryPage(BasePage):
    def is_recovery_page_opened(self):
        """Проверяет, что открыта страница восстановления пароля"""
        return self.find_element(RecoveryPageLocators.RECOVERY_TITLE).is_displayed()

    def enter_email(self, email):
        """Вводит email в поле на странице /forgot-password"""
        self.find_element(RecoveryPageLocators.EMAIL_INPUT).clear()
        self.find_element(RecoveryPageLocators.EMAIL_INPUT).send_keys(email)

    def click_restore(self):
        """Кликает на кнопку «Восстановить»"""
        self.click_element(RecoveryPageLocators.RESTORE_BUTTON)

    # --- Методы для страницы /reset-password ---

    def click_show_password(self):
        """Кликает на иконку «глазик» через JS, чтобы обойти перекрытия"""
        self.click_element_js(RecoveryPageLocators.SHOW_PASSWORD_BUTTON)

    def is_password_field_active(self):
        """
        Проверяет, что пароль стал видимым (тип поля изменился на text).
        Использует WebDriverWait, чтобы дождаться обновления DOM без time.sleep().
        """
        try:
            return self.wait.until(
                lambda d: self.find_element(
                    RecoveryPageLocators.NEW_PASSWORD_INPUT
                ).get_attribute("type") == "text"
            )
        except Exception:
            return False