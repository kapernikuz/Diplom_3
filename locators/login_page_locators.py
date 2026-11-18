from selenium.webdriver.common.by import By

class LoginPageLocators:
    # Заголовок страницы (для проверки, что мы на странице логина)
    LOGIN_TITLE = (By.XPATH, "//h2[text()='Вход']")
    
    # Поля формы
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    
    # Кнопка "Войти"
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    
    # Ссылки
    RECOVERY_LINK = (By.XPATH, "//a[text()='Восстановить пароль']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")