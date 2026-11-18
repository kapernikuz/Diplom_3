import allure
import time
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators


@allure.feature("Основной функционал")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Кликаем на «Лента заказов», чтобы уйти с главной"):
            main_page.click_order_feed()

        with allure.step("Кликаем на «Конструктор»"):
            main_page.click_constructor()

        with allure.step("Проверяем, что вернулись на главную"):
            assert driver.current_url == "https://qa-stellarburgers.education-services.ru/"

    @allure.title("Переход по клику на «Лента заказов»")
    def test_go_to_order_feed(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Кликаем на «Лента заказов»"):
            main_page.click_order_feed()

        with allure.step("Проверяем URL"):
            assert "feed" in driver.current_url

    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Кликаем на первый ингредиент (Краторная булка)"):
            main_page.click_first_ingredient()

        with allure.step("Проверяем, что модальное окно отображается"):
            assert main_page.is_ingredient_modal_visible() is True

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        main_page.click_first_ingredient()
        assert main_page.is_ingredient_modal_visible() is True

        with allure.step("Кликаем по крестику"):
            main_page.close_ingredient_modal()

        with allure.step("Проверяем, что модальное окно исчезло"):
            main_page.wait.until_not(
                lambda d: main_page.is_ingredient_modal_visible()
            )

    @allure.title("При добавлении ингредиента в заказ увеличивается каунтер")
    def test_ingredient_counter_increases(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Запоминаем начальное значение каунтера"):
            start_count = main_page.get_ingredient_counter()

        with allure.step("Перетаскиваем ингредиент в конструктор (через JS)"):
            ingredient = main_page.find_element(MainPageLocators.FIRST_INGREDIENT)
            basket = main_page.find_element(MainPageLocators.BASKET_DROP_ZONE)

            # JS-скрипт для симуляции Drag-and-Drop (кроссбраузерно)
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

        with allure.step("Ждём, что каунтер обновится"):
            time.sleep(1)

        with allure.step("Проверяем, что каунтер увеличился"):
            new_count = main_page.get_ingredient_counter()
            assert new_count > start_count