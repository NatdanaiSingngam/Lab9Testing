from src.fizzbuzz import fizzbuzz


def test_multiple_of_three_is_fizz():
    assert fizzbuzz(3) == "Fizz"


def test_one_is_one():
    assert fizzbuzz(1) == "1"


def test_multiple_of_five_is_buzz():
    assert fizzbuzz(5) == "Buzz"


def test_multiple_of_three_and_five_is_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"


def test_seven_is_seven():
    assert fizzbuzz(7) == "7"
