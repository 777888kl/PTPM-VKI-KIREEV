import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.calculator_page import CalculatorPage


class TestSimpleCalculator(unittest.TestCase):
    """Набор автоматизированных UI-тестов для Simple Calculator."""

    def setUp(self) -> None:
        """Инициализация браузера и открытие страницы перед каждым тестом."""
        chrome_options = Options()
        # Раскомментируйте строку ниже для запуска без графического интерфейса (CI/CD):
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1280,800")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.calculator_page = CalculatorPage(self.driver)
        self.calculator_page.open()

    def tearDown(self) -> None:
        """Закрытие сессии браузера после каждого теста."""
        if self.driver:
            self.driver.quit()

    # --- Тесты базовых арифметических операций ---

    def test_addition(self) -> None:
        """Проверка операции сложения (+)."""
        result = self.calculator_page.calculate(15, "+", 27)
        self.assertEqual(result, "42")

    def test_subtraction(self) -> None:
        """Проверка операции вычитания (-)."""
        result = self.calculator_page.calculate(50, "-", 18)
        self.assertEqual(result, "32")

    def test_multiplication(self) -> None:
        """Проверка операции умножения (*)."""
        result = self.calculator_page.calculate(7, "*", 8)
        self.assertEqual(result, "56")

    def test_division(self) -> None:
        """Проверка операции деления (/)."""
        result = self.calculator_page.calculate(84, "/", 4)
        self.assertEqual(result, "21")

    def test_negative_subtraction_result(self) -> None:
        """Проверка получения отрицательного результата при вычитании."""
        result = self.calculator_page.calculate(5, "-", 12)
        self.assertEqual(result, "-7")

    # --- Граничные значения и особые случаи ---

    def test_division_by_zero(self) -> None:
        """Проверка обработки деления на ноль (в AngularJS отображается 'null')."""
        result = self.calculator_page.calculate(10, "/", 0)
        self.assertEqual(result, "null")

    def test_negative_numbers(self) -> None:
        """Проверка вычислений с отрицательными числами."""
        result = self.calculator_page.calculate(-12, "+", -8)
        self.assertEqual(result, "-20")

    def test_floating_point_numbers(self) -> None:
        """Проверка вычислений с дробными числами."""
        result = self.calculator_page.calculate(2.5, "*", 4)
        self.assertEqual(result, "10")

    def test_zero_multiplication_and_division(self) -> None:
        """Проверка умножения на ноль и деления нуля на число."""
        self.assertEqual(self.calculator_page.calculate(99, "*", 0), "0")
        self.assertEqual(self.calculator_page.calculate(0, "/", 5), "0")

    def test_large_numbers(self) -> None:
        """Проверка работы с большими целыми числами."""
        result = self.calculator_page.calculate(1_000_000, "+", 2_500_000)
        self.assertEqual(result, "3500000")

    def test_increment_and_decrement_buttons(self) -> None:
        """Проверка кнопок инкремента (+) и декремента (-) для операндов."""
        self.calculator_page.enter_first_number(5)
        self.calculator_page.enter_second_number(10)
        self.calculator_page.select_operation("+")

        self.calculator_page.click_increment_first()   # 5 -> 6
        self.calculator_page.click_decrement_second()  # 10 -> 9

        self.assertEqual(self.calculator_page.get_result_value(), "15")
        self.assertEqual(self.calculator_page.get_raw_result_text(), "6 + 9 = 15")


if __name__ == "__main__":
    unittest.main(verbosity=2)