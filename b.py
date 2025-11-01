import random

def greet(name: str) -> str:
    return f"Hello, {name}!"

def generate_numbers(n):
    """Generate a list of n random integers between 1 and 100."""
    return [random.randint(1, 100) for _ in range(n)]

def sort_numbers(numbers):
    """Sort a list of numbers in ascending order."""
    return sorted(numbers)

def filter_even_numbers(numbers):
    """Filter out even numbers from a list."""
    return [num for num in numbers if num % 2 == 0]

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def find_maximum(numbers):
    """Find the maximum number in a list."""
    if not numbers:
        return None
    return max(numbers)

def find_minimum(numbers):
    """Find the minimum number in a list."""
    if not numbers:
        return None
    return min(numbers) 

def sum_numbers(numbers):
    """Calculate the sum of a list of numbers."""
    return sum(numbers)

def multiply_numbers(numbers):
    """Calculate the product of a list of numbers."""
    result = 1
    for num in numbers:
        result *= num
    return result

def reverse_numbers(numbers):
    """Reverse the order of elements in a list."""
    return list(reversed(numbers))

def unique_numbers(numbers):
    """Return a list of unique numbers from the input list."""
    return list(set(numbers))

def shuffle_numbers(numbers):
    """Shuffle the elements of a list randomly."""
    random.shuffle(numbers)
    return numbers

def split_numbers(numbers, n):
    """Split the list of numbers into chunks of size n."""
    for i in range(0, len(numbers), n):
        yield numbers[i:i + n]

def merge_numbers(list1, list2):
    """Merge two lists of numbers."""
    return list1 + list2

def calculator():
    """A simple calculator function."""
    while True:
        try:
            expr = input("Enter expression (or 'exit' to quit): ")
            if expr.lower() == 'exit':
                break
            result = eval(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")