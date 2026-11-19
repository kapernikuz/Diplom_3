from selenium.webdriver.common.by import By


class RecoveryPageLocators:
    # --- Страница /forgot-password ---
    RECOVERY_TITLE = (By.XPATH, "//h2[text()='Восстановление пароля']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")

    # --- Страница /reset-password ---
    NEW_PASSWORD_INPUT = (By.XPATH, "//input[@name='Введите новый пароль']")
    SHOW_PASSWORD_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'input_type_password')]"
        "//div[contains(@class, 'input__icon-action')]",
    )
    PASSWORD_FIELD_ACTIVE = (
        By.XPATH,
        "//div[contains(@class, 'input_type_password') "
        "and contains(@class, 'input_status_active')]",
    )