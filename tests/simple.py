# Simple test file for WhatThePy obfuscator

def greet(name):
    message = f"Hello, {name}!"
    print(message)
    return message

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old.")

if __name__ == "__main__":
    greet("World")

    result = calculate_sum([1, 2, 3, 4, 5])
    print(f"Sum: {result}")

    person = Person("Alice", 30)
    person.introduce()
