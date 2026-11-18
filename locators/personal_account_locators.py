from selenium.webdriver.common.by import By

class PersonalAccountLocators:
    # Ссылки навигации в личном кабинете
    PROFILE_LINK = (By.XPATH, "//a[text()='Профиль']")
    HISTORY_BUTTON = (By.XPATH, "//a[text()='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    
    # Заголовок/элемент, подтверждающий, что мы в личном кабинете
    ACCOUNT_TITLE = (By.XPATH, "//p[contains(text(), 'В этом разделе вы можете изменить свои персональные данные')]")