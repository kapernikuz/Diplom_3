import allure
from urls import BASE_URL
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.personal_account_page import PersonalAccountPage


@allure.feature("Личный кабинет")
class TestPersonalAccount:

    @allure.title("Переход по клику на «Личный кабинет» (авторизованный юзер)")
    def test_go_to_personal_account(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)

        with allure.step("Кликаем на «Личный кабинет» — попадаем на страницу логина"):
            main_page.click_personal_account()

        with allure.step("Авторизуемся под тестовым пользователем"):
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждём редиректа на главную после логина"):
            main_page.wait_for_url_to_be(BASE_URL)

        with allure.step("Кликаем на «Личный кабинет» ещё раз"):
            main_page.click_personal_account()

        with allure.step("Проверяем, что открылся личный кабинет"):
            assert "account" in main_page.get_current_url()

    @allure.title("Переход в раздел «История заказов»")
    def test_go_to_order_history(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)

        with allure.step("Авторизуемся"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждём редиректа на главную"):
            main_page.wait_for_url_to_be(BASE_URL)

        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account()

        with allure.step("Кликаем на «История заказов»"):
            PersonalAccountPage(driver).click_order_history()

        with allure.step("Проверяем, что открылась история заказов"):
            assert "order-history" in main_page.get_current_url()

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)

        with allure.step("Авторизуемся"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждём редиректа на главную"):
            main_page.wait_for_url_to_be(BASE_URL)

        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account()

        with allure.step("Кликаем на «Выход»"):
            PersonalAccountPage(driver).click_logout()

        with allure.step("Ждём редиректа на страницу логина"):
            # Явное ожидание, чтобы тест не падал раньше времени
            main_page.wait_for_url_contains("login")

        assert "login" in main_page.get_current_url()