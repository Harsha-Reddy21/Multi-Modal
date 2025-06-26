import math

def calculate_square_root(number):
    return math.sqrt(number)

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def is_greater_than(a, b):
    return a > b

def basic_calculator(expression):
    try:
        return eval(expression)
    except Exception as e:
        return f"Error calculating: {str(e)}" 