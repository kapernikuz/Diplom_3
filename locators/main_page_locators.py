from selenium.webdriver.common.by import By


class MainPageLocators:
    # --- Шапка сайта (Header) ---
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")

    # --- Ингредиенты ---
    # Первая булка "Краторная булка N-200i" — берём родительский <a>
    FIRST_INGREDIENT = (By.XPATH, "//p[text()='Краторная булка N-200i']/ancestor::a")

    # Счётчик первого ингредиента
    INGREDIENT_COUNTER = (By.XPATH, "(//p[contains(@class, 'counter_counter__num')])[1]")

    # Зона корзины для Drag-and-Drop — первый <li> в списке (верхняя булка)
    BASKET_DROP_ZONE = (By.XPATH, "//li[contains(@class, 'BurgerConstructor_basket__listItem')][1]")

    # Кнопка «Оформить заказ»
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    # --- Модальное окно с номером заказа ---
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow')]")
    ORDER_MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    # --- Модальное окно ингредиента ---
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox')]")
    INGREDIENT_MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    # --- Кнопка «Войти в аккаунт» (если не авторизован) ---
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")