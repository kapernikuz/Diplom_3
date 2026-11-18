from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


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
        
    def get_ingredient_counter(self):
        return int(self.get_text(MainPageLocators.INGREDIENT_COUNTER))
        
    def click_place_order(self):
        self.click_element(MainPageLocators.PLACE_ORDER_BUTTON)
        
    def get_order_number_from_modal(self):
        # Ждем, пока появится хотя бы одна модалка с номером
        self.wait.until(EC.presence_of_element_located(MainPageLocators.ORDER_NUMBER))
        
        # Функция проверки: ищем видимый элемент с номером, который не '9999'
        def get_valid_number(driver):
            elements = driver.find_elements(*MainPageLocators.ORDER_NUMBER)
            for el in elements:
                if el.is_displayed() and el.text.isdigit() and el.text != "9999":
                    return el.text
            return False

        # Ждем до 15 секунд, пока не появится реальный номер
        order_number = WebDriverWait(self.driver, 15).until(get_valid_number)
        return order_number
        
    def close_order_modal(self):
        self.click_element(MainPageLocators.ORDER_MODAL_CLOSE)