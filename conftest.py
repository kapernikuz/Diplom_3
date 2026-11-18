import time
import pytest
from selenium.webdriver.common.by import By
from helpers.webdriver_factory import WebdriverFactory
from helpers.api_helper import create_user_via_api, delete_user_via_api


def _patched_get(driver, original_get):
    """Патчим driver.get, чтобы после каждой загрузки закрывать модалку-оверлей"""
    def get_with_modal_close(url):
        original_get(url)
        time.sleep(1)  # даём странице прогрузиться
        try:
            close_btn = driver.find_element(
                By.XPATH, "//button[contains(@class, 'Modal_modal__close')]"
            )
            if close_btn.is_displayed():
                driver.execute_script("arguments[0].click();", close_btn)
        except Exception:
            pass
    return get_with_modal_close


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    driver = WebdriverFactory.get_driver(request.param)
    driver.maximize_window()
    # Патчим get(), чтобы после каждой загрузки закрывать модалку
    original_get = driver.get
    driver.get = _patched_get(driver, original_get)
    yield driver
    driver.quit()


@pytest.fixture
def registered_user():
    user_data = create_user_via_api()
    yield user_data
    delete_user_via_api(user_data["token"])