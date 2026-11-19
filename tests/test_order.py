import allure
from urls import BASE_URL
from pages.main_page import MainPage
from pages.login_page import LoginPage


@allure.feature("Оформление заказа")
class TestOrder:

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_user_can_place_order(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)

        with allure.step("Авторизуемся под тестовым пользователем"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждём редиректа на главную после логина"):
            main_page.wait_for_url_to_be(BASE_URL)

        with allure.step("Перетаскиваем ингредиент (Краторная булка) в корзину"):
            main_page.drag_and_drop_ingredient()

        with allure.step("Кликаем по кнопке «Оформить заказ»"):
            main_page.click_place_order()

        with allure.step("Проверяем, что появилось модальное окно с номером заказа"):
            order_number = main_page.get_order_number_from_modal()
            assert order_number.isdigit(), f"Ожидали номер заказа, получили: {order_number}"
            assert order_number != "9999", "Номер заказа не обновился (все еще заглушка 9999)"
            
        with allure.step("Закрываем модальное окно с номером заказа"):
            main_page.close_order_modal()