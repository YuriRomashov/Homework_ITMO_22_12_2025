import math

tests_number = int(input())
for i in range(tests_number):
    quantity_of_numbers = int(input()) 
    digits = [int(numb) for numb in input().replace(" ", "")] 
    digits[min(enumerate(digits), key=lambda item: item[1])[0]] += 1
    print(math.prod(digits))