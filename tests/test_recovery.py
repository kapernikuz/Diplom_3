import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.recovery_page import RecoveryPage


@allure.feature("Восстановление пароля")
class TestRecovery:

    @allure.title("Переход на страницу восстановления пароля по кнопке «Восстановить пароль»")
    def test_go_to_recovery_page(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        MainPage(driver).click_personal_account()

        with allure.step("Кликаем по ссылке «Восстановить пароль»"):
            LoginPage(driver).click_recovery_link()

        with allure.step("Проверяем, что открылась страница восстановления"):
            assert "forgot-password" in driver.current_url
            assert RecoveryPage(driver).is_recovery_page_opened()

    @allure.title("Ввод почты и клик по кнопке «Восстановить»")
    def test_recovery_email_submit(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/forgot-password")
        recovery = RecoveryPage(driver)

        with allure.step("Вводим email существующего пользователя"):
            recovery.enter_email(registered_user["email"])

        with allure.step("Кликаем на кнопку «Восстановить»"):
            recovery.click_restore()

        with allure.step("Проверяем, что произошёл переход на страницу /reset-password"):
            WebDriverWait(driver, 10).until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url

    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным — подсвечивает его")
    def test_show_password_activates_field(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/forgot-password")
        recovery = RecoveryPage(driver)

        with allure.step("Вводим email существующего пользователя"):
            recovery.enter_email(registered_user["email"])

        with allure.step("Кликаем на кнопку «Восстановить»"):
            recovery.click_restore()

        with allure.step("Ждём перехода на страницу /reset-password"):
            WebDriverWait(driver, 10).until(EC.url_contains("reset-password"))

        with allure.step("Кликаем на иконку «глазик» в поле пароля"):
            recovery.click_show_password()
            time.sleep(1)  # Даем время на изменение DOM

        with allure.step("Проверяем, что пароль стал видимым (type='text')"):
            assert recovery.is_password_field_active() is True