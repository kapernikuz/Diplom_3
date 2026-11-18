import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.login_page import LoginPage
from locators.main_page_locators import MainPageLocators


@allure.feature("Оформление заказа")
class TestOrder:

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_user_can_place_order(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Авторизуемся под тестовым пользователем"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждём редиректа на главную после логина"):
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://qa-stellarburgers.education-services.ru/")
            )

        with allure.step("Перетаскиваем ингредиент (Краторная булка) в корзину (через JS)"):
            ingredient = main_page.find_element(MainPageLocators.FIRST_INGREDIENT)
            basket = main_page.find_element(MainPageLocators.BASKET_DROP_ZONE)
            
            js_script = """
            var source = arguments[0];
            var target = arguments[1];
            var dataTransfer = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
            target.dispatchEvent(new DragEvent('dragover', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
            target.dispatchEvent(new DragEvent('drop', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
            source.dispatchEvent(new DragEvent('dragend', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
            """
            driver.execute_script(js_script, ingredient, basket)

        with allure.step("Кликаем по кнопке «Оформить заказ»"):
            main_page.click_place_order()

        with allure.step("Проверяем, что появилось модальное окно с номером заказа"):
            order_number = main_page.get_order_number_from_modal()
            assert order_number.isdigit(), f"Ожидали номер заказа, получили: {order_number}"
            assert order_number != "9999", "Номер заказа не обновился (все еще заглушка 9999)"
            
        with allure.step("Закрываем модальное окно с номером заказа"):
            main_page.close_order_modal()