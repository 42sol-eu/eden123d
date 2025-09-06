"""Sample pytest tests for calculator functionality."""
import pytest


class Calculator:
    """Simple calculator class for testing."""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


@pytest.fixture
def calculator():
    """Provide a calculator instance for tests."""
    return Calculator()


class TestBasicOperations:
    """Test basic calculator operations."""
    
    def test_addition(self, calculator):
        """Test addition operation."""
        result = calculator.add(2, 3)
        assert result == 5
    
    def test_subtraction(self, calculator):
        """Test subtraction operation."""
        result = calculator.subtract(5, 3)
        assert result == 2
    
    def test_multiplication(self, calculator):
        """Test multiplication operation."""
        result = calculator.multiply(4, 3)
        assert result == 12
    
    def test_division(self, calculator):
        """Test division operation."""
        result = calculator.divide(10, 2)
        assert result == 5.0
    
    def test_division_by_zero(self, calculator):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)


class TestEdgeCases:
    """Test edge cases for calculator."""
    
    def test_negative_numbers(self, calculator):
        """Test operations with negative numbers."""
        assert calculator.add(-2, 3) == 1
        assert calculator.subtract(-2, 3) == -5
        assert calculator.multiply(-2, 3) == -6
        assert calculator.divide(-6, 2) == -3.0
    
    def test_decimal_numbers(self, calculator):
        """Test operations with decimal numbers."""
        assert calculator.add(2.5, 3.7) == pytest.approx(6.2)
        assert calculator.multiply(2.5, 2) == 5.0
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (0, 5, 5),
        (-1, 1, 0),
        (100, 200, 300)
    ])
    def test_addition_parametrized(self, calculator, a, b, expected):
        """Test addition with multiple parameter sets."""
        assert calculator.add(a, b) == expected


@pytest.mark.slow
class TestPerformance:
    """Performance tests (marked as slow)."""
    
    def test_large_numbers(self, calculator):
        """Test with large numbers."""
        large_num = 1_000_000
        result = calculator.add(large_num, large_num)
        assert result == 2_000_000
    
    def test_many_operations(self, calculator):
        """Test many sequential operations."""
        result = 0
        for i in range(100):
            result = calculator.add(result, i)
        assert result == sum(range(100))
