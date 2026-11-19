from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        
    def click_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)
        
    def click_personal_account(self):
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        
    def click_first_ingredient(self):
        self.click_element(MainPageLocators.FIRST_INGREDIENT)
        
    def close_ingredient_modal(self):
        self.click_element(MainPageLocators.INGREDIENT_MODAL_CLOSE)
        
    def is_ingredient_modal_visible(self):
        return self.find_element(MainPageLocators.INGREDIENT_MODAL).is_displayed()

    def wait_ingredient_modal_close(self):
        self.wait_for_element_to_disappear(MainPageLocators.INGREDIENT_MODAL)
        
    def get_ingredient_counter(self):
        return int(self.get_text(MainPageLocators.INGREDIENT_COUNTER))
        
    def drag_and_drop_ingredient(self):
        """Перетаскивает ингредиент в корзину через JS (кроссбраузерно)"""
        ingredient = self.find_element(MainPageLocators.FIRST_INGREDIENT)
        basket = self.find_element(MainPageLocators.BASKET_DROP_ZONE)
        
        js_script = """
        var source = arguments[0];
        var target = arguments[1];
        var dataTransfer = new DataTransfer();
        source.dispatchEvent(new DragEvent('dragstart', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
        target.dispatchEvent(new DragEvent('dragover', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
        target.dispatchEvent(new DragEvent('drop', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
        source.dispatchEvent(new DragEvent('dragend', { dataTransfer: dataTransfer, bubbles: true, cancelable: true }));
        """
        self.execute_script(js_script, ingredient, basket)

    def click_place_order(self):
        self.click_element(MainPageLocators.PLACE_ORDER_BUTTON)
        
    def get_order_number_from_modal(self):
        self.wait.until(EC.presence_of_element_located(MainPageLocators.ORDER_NUMBER))
        
        def get_valid_number(driver):
            elements = driver.find_elements(*MainPageLocators.ORDER_NUMBER)
            for el in elements:
                if el.is_displayed() and el.text.isdigit() and el.text != "9999":
                    return el.text
            return False

        return self.wait.until(get_valid_number)
        
    def close_order_modal(self):
        """Закрывает модалку заказа через JS, чтобы обойти оверлей"""
        self.click_element_js(MainPageLocators.ORDER_MODAL_CLOSE)