from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from selenium.webdriver.support import expected_conditions as EC


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

    def get_modal_number_text(self):
        return self.get_text(OrderFeedLocators.ORDER_MODAL_NUMBER)
        
    def is_order_in_feed(self, order_number):
        locator = OrderFeedLocators.get_order_by_number_locator(order_number)
        try:
            # Ждем появления заказа в ленте до 10 секунд
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except:
            return False
            
    def is_order_in_progress(self, order_number, timeout=15):
        locator = OrderFeedLocators.get_order_in_progress_locator(order_number)
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False