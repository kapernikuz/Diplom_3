from selenium.webdriver.common.by import By

class OrderFeedLocators:
    # Счетчики
    DONE_ALL_TIME = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    DONE_TODAY = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    
    # Лента заказов
    FIRST_ORDER = (By.XPATH, "(//li[contains(@class, 'OrderHistory_listItem')])[1]")
    
    # Модальное окно с деталями заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox')]//p[contains(@class, 'text_type_digits-default')]")
    
    # Раздел "В работе" (класс взят с твоего скриншота)
    IN_PROGRESS_ORDER_ITEM = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    
    @staticmethod
    def get_order_by_number_locator(order_number):
        """Возвращает локатор для поиска заказа по его номеру в ленте (с решеткой)"""
        return (By.XPATH, f"//p[contains(@class, 'text_type_digits-default') and contains(text(), '{order_number}')]")
        
    @staticmethod
    def get_order_in_progress_locator(order_number):
        """
        Ищем заказ в блоке 'В работе'.
        Используем точку '.', чтобы захватить весь текст элемента (включая '0' и номер).
        """
        return (By.XPATH, f"//ul[contains(@class, 'OrderFeed_orderListReady')]/li[contains(., '{order_number}')]")