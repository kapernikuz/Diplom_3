from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_page(self, url):
        """Открывает страницу, ждет полной загрузки и закрывает модалку-заглушку"""
        self.driver.get(url)
        # Ждем полной загрузки страницы (document.readyState == "complete")
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.close_modal_if_present()

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_url_to_be(self, url):
        """Ждет совпадения URL, игнорируя слэш на конце"""
        normalized_url = url.rstrip('/')
        return self.wait.until(
            lambda d: d.current_url.rstrip('/') == normalized_url
        )

    def wait_for_url_contains(self, text):
        return self.wait.until(EC.url_contains(text))

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except (TimeoutException, ElementClickInterceptedException):
            # Если элемент перекрыт модалкой или не кликабелен, кликаем через JS
            self.click_element_js(locator)

    def click_element_js(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def wait_for_element_to_disappear(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def close_modal_if_present(self):
        """Закрывает модалку, если она перекрывает экран"""
        try:
            close_btn_locator = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(close_btn_locator)
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")))
        except TimeoutException:
            pass