import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.api_helper import create_order_via_api
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    def test_click_order_opens_modal(self, driver):
        driver.get("https://qa-stellarburgers.education-services.ru/feed")
        feed = OrderFeedPage(driver)
        
        with allure.step("Кликаем на первый заказ в ленте"):
            feed.click_first_order()
            
        with allure.step("Проверяем, что открылось модальное окно с деталями"):
            assert feed.check_order_modal_is_visible() == True
            
        with allure.step("Проверяем, что внутри модалки отображается номер заказа (с решеткой #)"):
            modal_number = feed.get_text(OrderFeedLocators.ORDER_MODAL_NUMBER)
            assert "#" in modal_number, f"В модалке не найден номер заказа. Получено: {modal_number}"

    @allure.title("Заказы пользователя из «Истории заказов» отображаются на странице «Лента заказов»")
    def test_user_order_in_feed(self, driver, registered_user):
        with allure.step("Создаем заказ через API"):
            order_response = create_order_via_api(registered_user["token"])
            order_number = str(order_response["order"]["number"])
            
        driver.get("https://qa-stellarburgers.education-services.ru/feed")
        feed = OrderFeedPage(driver)
        
        with allure.step(f"Проверяем, что заказ {order_number} есть в ленте"):
            time.sleep(2)
            assert feed.is_order_in_feed(order_number), f"Заказ {order_number} не найден в ленте"

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_done_all_time_counter_increases(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/feed")
        feed = OrderFeedPage(driver)
        
        with allure.step("Запоминаем начальное значение счетчика"):
            start_count = feed.get_done_all_time()
            
        with allure.step("Создаем новый заказ через API"):
            create_order_via_api(registered_user["token"])
            
        with allure.step("Ждем обновления счетчика и обновляем страницу"):
            time.sleep(2)
            driver.refresh()
            
        with allure.step("Проверяем, что счетчик увеличился"):
            new_count = feed.get_done_all_time()
            assert new_count > start_count, f"Счетчик не увеличился: было {start_count}, стало {new_count}"

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_done_today_counter_increases(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/feed")
        feed = OrderFeedPage(driver)
        
        with allure.step("Запоминаем начальное значение счетчика"):
            start_count = feed.get_done_today()
            
        with allure.step("Создаем новый заказ через API"):
            create_order_via_api(registered_user["token"])
            
        with allure.step("Ждем обновления счетчика и обновляем страницу"):
            time.sleep(2)
            driver.refresh()
            
        with allure.step("Проверяем, что счетчик увеличился"):
            new_count = feed.get_done_today()
            assert new_count > start_count, f"Счетчик не увеличился: было {start_count}, стало {new_count}"

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_number_in_progress_section(self, driver, registered_user):
        driver.get("https://qa-stellarburgers.education-services.ru/")
        main_page = MainPage(driver)

        with allure.step("Авторизуемся под тестовым пользователем"):
            main_page.click_personal_account()
            LoginPage(driver).login(registered_user["email"], registered_user["password"])

        with allure.step("Ждем редиректа на главную после логина"):
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

        with allure.step("Получаем номер заказа из модального окна"):
            order_number_ui = main_page.get_order_number_from_modal()
            main_page.close_order_modal()

        with allure.step("Переходим в Ленту заказов"):
            driver.get("https://qa-stellarburgers.education-services.ru/feed")
            feed = OrderFeedPage(driver)
            
        with allure.step(f"Проверяем, что заказ {order_number_ui} есть в разделе «В работе»"):
            # Ждем до 15 секунд появления заказа в блоке In Progress
            is_in_progress = feed.is_order_in_progress(order_number_ui, timeout=15)
            assert is_in_progress, f"Заказ {order_number_ui} не найден в разделе 'В работе'."