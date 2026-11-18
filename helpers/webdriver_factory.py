from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class WebdriverFactory:
    @staticmethod
    def get_driver(browser_name):
        if browser_name == "chrome":
            options = ChromeOptions()
            # options.add_argument("--headless") # Можно включить для CI
            return webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Браузер '{browser_name}' не поддерживается")