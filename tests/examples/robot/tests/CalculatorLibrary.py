"""Python-based Robot Framework test library."""
from robot.api.deco import keyword, library
from typing import Union


@library
class CalculatorLibrary:
    """Robot Framework test library for calculator operations."""
    
    def __init__(self) -> None:
        """Initialize the calculator library."""
        self.result: float = 0.0
        self.error_message: str = ""
    
    @keyword
    def add_numbers(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of the two numbers
        """
        self.result = float(a) + float(b)
        return self.result
    
    @keyword
    def subtract_numbers(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Subtract second number from first number.
        
        Args:
            a: First number (minuend)
            b: Second number (subtrahend)
            
        Returns:
            Difference of the two numbers
        """
        self.result = float(a) - float(b)
        return self.result
    
    @keyword
    def multiply_numbers(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of the two numbers
        """
        self.result = float(a) * float(b)
        return self.result
    
    @keyword
    def divide_numbers(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide first number by second number.
        
        Args:
            a: First number (dividend)
            b: Second number (divisor)
            
        Returns:
            Quotient of the division
            
        Raises:
            ValueError: If divisor is zero
        """
        if float(b) == 0:
            self.error_message = "Cannot divide by zero"
            raise ValueError(self.error_message)
        
        self.result = float(a) / float(b)
        return self.result
    
    @keyword
    def get_last_result(self) -> float:
        """
        Get the result of the last calculation.
        
        Returns:
            Last calculation result
        """
        return self.result
    
    @keyword
    def reset_calculator(self) -> None:
        """Reset calculator to initial state."""
        self.result = 0.0
        self.error_message = ""
    
    @keyword
    def result_should_be(self, expected: Union[int, float]) -> None:
        """
        Verify that the last result matches expected value.
        
        Args:
            expected: Expected result value
            
        Raises:
            AssertionError: If result doesn't match expected value
        """
        if abs(self.result - float(expected)) > 1e-10:
            raise AssertionError(
                f"Expected result {expected}, but got {self.result}"
            )
