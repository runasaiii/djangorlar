print("This is worktree-first-duplicate/a.py")

def greet(name: str) -> str:
    return f"Hello, {name}!"

def capitalize_words(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split())

def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

def reverse_string(s: str) -> str:
    return s[::-1]

def count_vowels(s: str) -> int:
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n: int) -> list[int]:
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence 

def is_prime(num: int) -> bool:
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

def generate_random_string(length: int) -> str:
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))