import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.personal_account_page import PersonalAccountPage


@allure.feature("Личный кабинет")
class TestPersonalAccount:

    @allure.title("Переход по клику на «Личный кабинет» (авторизованный юзер)")
    def test_go_to_personal_account(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)
        
        with allure.step("Кликаем на «Личный кабинет» — попадаем на страницу логина"):
            main_page.click_personal_account()
            
        with allure.step("Авторизуемся под тестовым пользователем"):
            LoginPage(driver).login(registered_user["email"], registered_user["password"])
            
        with allure.step("Ждём редиректа на главную после логина"):
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://qa-stellarburgers.education-services.ru/")
            )
            
        with allure.step("Кликаем на «Личный кабинет» ещё раз"):
            main_page.click_personal_account()
            
        with allure.step("Проверяем, что открылся личный кабинет"):
            assert "account" in driver.current_url

    @allure.title("Переход в раздел «История заказов»")
    def test_go_to_order_history(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)
        
        with allure.step("Авторизуемся"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])
            
        with allure.step("Ждём редиректа на главную"):
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://qa-stellarburgers.education-services.ru/")
            )
            
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account()
            
        with allure.step("Кликаем на «История заказов»"):
            PersonalAccountPage(driver).click_order_history()
            
        with allure.step("Проверяем, что открылась история заказов"):
            assert "order-history" in driver.current_url

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)
        
        with allure.step("Авторизуемся"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])
            
        with allure.step("Ждём редиректа на главную"):
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://qa-stellarburgers.education-services.ru/")
            )
            
        with allure.step("Закрываем возможную модалку"):
            main_page.close_modal_if_present()
            
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account()
            
        with allure.step("Кликаем на «Выход»"):
            PersonalAccountPage(driver).click_logout()
            
        with allure.step("Ждём редиректа на страницу логина"):
            WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url