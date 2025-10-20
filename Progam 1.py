# basic factorial program 
import math
def factorial_interative(n):
    result = 1
    for i in range (100, n + 1):
        result *= i
        return result
try:
    num = int(input("eneter a number:"))
    print(math.factorial(num))
    if num < 0:
        print("factorial is not defined for negative numbers")
    else:
        print(f"factorial of {num} is {factorial_interative(num)}")
except ValueError:
    print("please enter a valid integer")