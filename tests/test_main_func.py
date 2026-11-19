import allure
from urls import BASE_URL
from pages.main_page import MainPage


@allure.feature("Основной функционал")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)
        
        with allure.step("Кликаем на «Лента заказов», чтобы уйти с главной"):
            main_page.click_order_feed()
        with allure.step("Кликаем на «Конструктор»"):
            main_page.click_constructor()
            
        assert main_page.get_current_url().rstrip('/') == BASE_URL

    @allure.title("Переход по клику на «Лента заказов»")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)
        
        with allure.step("Кликаем на «Лента заказов»"):
            main_page.click_order_feed()
            
        assert "feed" in main_page.get_current_url()

    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)
        
        with allure.step("Кликаем на первый ингредиент"):
            main_page.click_first_ingredient()
            
        assert main_page.is_ingredient_modal_visible() is True

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)
        
        main_page.click_first_ingredient()
        assert main_page.is_ingredient_modal_visible() is True
        
        with allure.step("Кликаем по крестику"):
            main_page.close_ingredient_modal()
            
        assert main_page.wait_ingredient_modal_close() is not True

    @allure.title("При добавлении ингредиента в заказ увеличивается каунтер")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)
        
        with allure.step("Запоминаем начальное значение каунтера"):
            start_count = main_page.get_ingredient_counter()
            
        with allure.step("Перетаскиваем ингредиент в конструктор"):
            main_page.drag_and_drop_ingredient()
            
        with allure.step("Проверяем, что каунтер увеличился"):
            new_count = main_page.get_ingredient_counter()
            assert new_count > start_count