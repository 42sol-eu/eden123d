"""Sample pytest tests for testing the agnostic test runner."""
import pytest
from typing import List


class TestBasicMath:
    """Basic math test cases."""
    
    def test_addition(self) -> None:
        """Test that addition works correctly."""
        assert 2 + 2 == 4
        assert 10 + 5 == 15
    
    def test_subtraction(self) -> None:
        """Test that subtraction works correctly."""
        assert 10 - 5 == 5
        assert 0 - 1 == -1
    
    def test_multiplication(self) -> None:
        """Test that multiplication works correctly."""
        assert 3 * 4 == 12
        assert 7 * 0 == 0
    
    def test_division(self) -> None:
        """Test that division works correctly."""
        assert 10 / 2 == 5
        assert 15 / 3 == 5


class TestStringOperations:
    """String operation test cases."""
    
    def test_string_concatenation(self) -> None:
        """Test string concatenation."""
        assert "hello" + " " + "world" == "hello world"
        assert "test" + "123" == "test123"
    
    def test_string_methods(self) -> None:
        """Test various string methods."""
        text = "Hello World"
        assert text.lower() == "hello world"
        assert text.upper() == "HELLO WORLD"
        assert text.replace("Hello", "Hi") == "Hi World"
    
    @pytest.mark.parametrize("input_str,expected", [
        ("hello", 5),
        ("world", 5),
        ("", 0),
        ("test123", 7)
    ])
    def test_string_length(self, input_str: str, expected: int) -> None:
        """Test string length calculation."""
        assert len(input_str) == expected


class TestListOperations:
    """List operation test cases."""
    
    def test_list_creation(self) -> None:
        """Test list creation and basic operations."""
        numbers: List[int] = [1, 2, 3, 4, 5]
        assert len(numbers) == 5
        assert numbers[0] == 1
        assert numbers[-1] == 5
    
    def test_list_append(self) -> None:
        """Test list append operation."""
        items: List[str] = ["apple", "banana"]
        items.append("cherry")
        assert len(items) == 3
        assert items[-1] == "cherry"
    
    def test_list_extend(self) -> None:
        """Test list extend operation."""
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        list1.extend(list2)
        assert list1 == [1, 2, 3, 4, 5, 6]


@pytest.mark.slow
class TestSlowOperations:
    """Test cases marked as slow."""
    
    def test_slow_computation(self) -> None:
        """A test that simulates slow computation."""
        import time
        time.sleep(0.1)  # Simulate slow operation
        result = sum(range(1000))
        assert result == 499500


class TestFailures:
    """Test cases that demonstrate failures."""
    
    @pytest.mark.xfail(reason="This test is expected to fail")
    def test_expected_failure(self) -> None:
        """A test that is expected to fail."""
        assert False, "This should fail"
    
    @pytest.mark.skip(reason="Skipping this test for demo")
    def test_skipped_test(self) -> None:
        """A test that is skipped."""
        assert True


def test_standalone_function() -> None:
    """A standalone test function."""
    assert "pytest" in "testing with pytest"
