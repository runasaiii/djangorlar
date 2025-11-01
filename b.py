import random


def random_list(n):
    return [random.randint(1, 100) for _ in range(n)]

def generate_numbers(n):
    return [random.randint(1, 100) for _ in range(n)]

def sort_numbers(numbers):
    return sorted(numbers)

def filter_even_numbers(numbers):
    return [num for num in numbers if num % 2 == 0]

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def find_maximum(numbers):
    if not numbers:
        return None
    return max(numbers)

def find_minimum(numbers):
    if not numbers:
        return None
    return min(numbers) 

def sum_numbers(numbers):
    return sum(numbers)

def multiply_numbers(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def reverse_numbers(numbers):
    return list(reversed(numbers))

def unique_numbers(numbers):
    return list(set(numbers))

def shuffle_numbers(numbers):
    random.shuffle(numbers)
    return numbers

def split_numbers(numbers, n):
    """Split the list of numbers into chunks of size n."""
    for i in range(0, len(numbers), n):
        yield numbers[i:i + n]

def merge_numbers(list1, list2):
    return list1 + list2
