import pytest
from helpers.webdriver_factory import WebdriverFactory
from helpers.api_helper import create_user_via_api, delete_user_via_api

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    driver = WebdriverFactory.get_driver(request.param)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def registered_user():
    user_data = create_user_via_api()
    yield user_data
    delete_user_via_api(user_data["token"])