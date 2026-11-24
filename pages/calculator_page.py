from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class CalculatorPage(BasePage):
    """Page Object для веб-приложения Simple Calculator."""

    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"

    # Защищенные локаторы элементов интерфейса (AngularJS ng-model / ng-click)
    _FIRST_NUMBER_INPUT = (By.CSS_SELECTOR, "input[ng-model='a']")
    _SECOND_NUMBER_INPUT = (By.CSS_SELECTOR, "input[ng-model='b']")
    _OPERATION_SELECT = (By.CSS_SELECTOR, "select[ng-model='operation']")
    _RESULT_DISPLAY = (By.CSS_SELECTOR, "b.result")

    # Кнопки инкремента и декремента рядом с полями ввода
    _INCREMENT_A_BTN = (By.CSS_SELECTOR, "button[ng-click='inca()']")
    _DECREMENT_A_BTN = (By.CSS_SELECTOR, "button[ng-click='deca()']")
    _INCREMENT_B_BTN = (By.CSS_SELECTOR, "button[ng-click='incb()']")
    _DECREMENT_B_BTN = (By.CSS_SELECTOR, "button[ng-click='decb()']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver, self.URL)

    def enter_first_number(self, number: int | float | str) -> None:
        """Вводит первое число (операнд A)."""
        self._type_text(self._FIRST_NUMBER_INPUT, number)

    def enter_second_number(self, number: int | float | str) -> None:
        """Вводит второе число (операнд B)."""
        self._type_text(self._SECOND_NUMBER_INPUT, number)

    def select_operation(self, operation: str) -> None:
        """Выбирает математическую операцию из выпадающего списка (+, -, *, /, **)."""
        select_element = self._find_visible(self._OPERATION_SELECT)
        Select(select_element).select_by_visible_text(operation)

    def calculate(self, first: int | float, operation: str, second: int | float) -> str:
        """Выполняет полный сценарий ввода двух чисел и выбора операции, возвращая результат."""
        self.enter_first_number(first)
        self.select_operation(operation)
        self.enter_second_number(second)
        return self.get_result_value()

    def click_increment_first(self) -> None:
        """Увеличивает первое число на 1 нажатием кнопки '+'."""
        self._click(self._INCREMENT_A_BTN)

    def click_decrement_first(self) -> None:
        """Уменьшает первое число на 1 нажатием кнопки '-'."""
        self._click(self._DECREMENT_A_BTN)

    def click_increment_second(self) -> None:
        """Увеличивает второе число на 1 нажатием кнопки '+'."""
        self._click(self._INCREMENT_B_BTN)

    def click_decrement_second(self) -> None:
        """Уменьшает второе число на 1 нажатием кнопки '-'."""
        self._click(self._DECREMENT_B_BTN)

    def get_raw_result_text(self) -> str:
        """Возвращает полный текст строки результата (например, '10 + 5 = 15')."""
        return self._find_visible(self._RESULT_DISPLAY).text.strip()

    def get_result_value(self) -> str:
        """Извлекает только вычисленное значение после знака '='."""
        raw_text = self.get_raw_result_text()
        if "=" in raw_text:
            return raw_text.split("=", maxsplit=1)[1].strip()
        return raw_text