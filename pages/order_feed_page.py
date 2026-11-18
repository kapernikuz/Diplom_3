from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    def get_done_all_time(self):
        return int(self.get_text(OrderFeedLocators.DONE_ALL_TIME))
        
    def get_done_today(self):
        return int(self.get_text(OrderFeedLocators.DONE_TODAY))
        
    def click_first_order(self):
        self.click_element(OrderFeedLocators.FIRST_ORDER)
        
    def check_order_modal_is_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(OrderFeedLocators.ORDER_MODAL_NUMBER))
            return True
        except Exception:
            return False
        
    def is_order_in_feed(self, order_number):
        locator = OrderFeedLocators.get_order_by_number_locator(order_number)
        try:
            self.find_element(locator)
            return True
        except:
            return False
            
    def is_order_in_progress(self, order_number, timeout=15):
        """Проверяет, есть ли точный номер заказа в блоке 'В работе'"""
        locator = OrderFeedLocators.get_order_in_progress_locator(order_number)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            # Для отладки: выводим все номера, которые есть в блоке "В работе"
            elements = self.driver.find_elements(*OrderFeedLocators.IN_PROGRESS_ORDER_ITEM)
            print(f"\n[ОТЛАДКА] Номера в блоке 'В работе': {[el.text for el in elements]}")
            print(f"[ОТЛАДКА] Искали номер: {order_number}\n")
            return False