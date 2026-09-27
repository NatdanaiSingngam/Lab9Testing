"""FizzBuzz kata."""


def is_multiple(number: int, divisor: int) -> bool:
    return number % divisor == 0


def fizzbuzz(number: int) -> str:
    if is_multiple(number, 15):
        return "FizzBuzz"
    if is_multiple(number, 3):
        return "Fizz"
    if is_multiple(number, 5):
        return "Buzz"
    return str(number)
