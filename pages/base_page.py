from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех Page Object."""

    def __init__(self, driver: WebDriver, url: str, timeout: int = 10):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        """Открывает целевую страницу."""
        self.driver.get(self.url)

    def _find_visible(self, locator: tuple[str, str]) -> WebElement:
        """Ожидает появления и видимости элемента на странице."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _find_clickable(self, locator: tuple[str, str]) -> WebElement:
        """Ожидает, пока элемент станет кликабельным."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _type_text(self, locator: tuple[str, str], value: str | int | float) -> None:
        """Очищает поле ввода и вводит новое значение."""
        element = self._find_visible(locator)
        element.clear()
        element.send_keys(str(value))

    def _click(self, locator: tuple[str, str]) -> None:
        """Выполняет клик по элементу."""
        element = self._find_clickable(locator)
        element.click()