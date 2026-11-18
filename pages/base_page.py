from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except (ElementClickInterceptedException, TimeoutException):
            # Если элемент перекрыт оверлеем или не стал кликабельным, жмем через JS
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def close_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
            self.wait.until_not(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
                )
            )
        except TimeoutException:
            pass