import allure
from urls import BASE_URL
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from helpers.api_helper import create_order_via_api


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    def test_click_order_opens_modal(self, driver):
        feed = OrderFeedPage(driver)
        feed.open_page(f"{BASE_URL}/feed")
        
        with allure.step("Кликаем на первый заказ в ленте"):
            feed.click_first_order()
            
        with allure.step("Проверяем, что открылось модальное окно и в нем есть номер"):
            assert feed.check_order_modal_is_visible() is True and "#" in feed.get_modal_number_text()

    @allure.title("Заказы пользователя из «Истории заказов» отображаются на странице «Лента заказов»")
    def test_user_order_in_feed(self, driver, registered_user):
        with allure.step("Создаем заказ через API"):
            order_response = create_order_via_api(registered_user["token"])
            order_number = str(order_response["order"]["number"])
            
        feed = OrderFeedPage(driver)
        feed.open_page(f"{BASE_URL}/feed")
        
        with allure.step(f"Проверяем, что заказ {order_number} есть в ленте"):
            assert feed.is_order_in_feed(order_number) is True

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_done_all_time_counter_increases(self, driver, registered_user):
        feed = OrderFeedPage(driver)
        feed.open_page(f"{BASE_URL}/feed")
        
        start_count = feed.get_done_all_time()
        create_order_via_api(registered_user["token"])
        
        def counter_increased(d):
            return feed.get_done_all_time() > start_count
            
        with allure.step("Проверяем, что счетчик увеличился (с ожиданием)"):
            assert feed.wait.until(counter_increased) is True

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_done_today_counter_increases(self, driver, registered_user):
        feed = OrderFeedPage(driver)
        feed.open_page(f"{BASE_URL}/feed")
        
        start_count = feed.get_done_today()
        create_order_via_api(registered_user["token"])
        
        def counter_increased(d):
            return feed.get_done_today() > start_count
            
        with allure.step("Проверяем, что счетчик увеличился (с ожиданием)"):
            assert feed.wait.until(counter_increased) is True

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_number_in_progress_section(self, driver, registered_user):
        main_page = MainPage(driver)
        main_page.open_page(BASE_URL)

        main_page.click_personal_account()
        LoginPage(driver).login(registered_user["email"], registered_user["password"])
        main_page.wait_for_url_to_be(BASE_URL)

        main_page.drag_and_drop_ingredient()
        main_page.click_place_order()

        order_number_ui = main_page.get_order_number_from_modal()
        main_page.close_order_modal()

        feed = OrderFeedPage(driver)
        feed.open_page(f"{BASE_URL}/feed")
            
        with allure.step(f"Проверяем, что заказ {order_number_ui} есть в разделе «В работе»"):
            assert feed.is_order_in_progress(order_number_ui, timeout=15) is True