def calculate_average(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    return total / count

numbers = [1, 2, 3, 4, 5]
result = calculate_average(numbers)
print(f"The average is: {result}")

# This line contains the bug
empty_list = []
average_of_empty = calculate_average(empty_list)
print(f"The average of an empty list is: {average_of_empty}")
