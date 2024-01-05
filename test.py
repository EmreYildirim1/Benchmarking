import time

# Example function with a loop and mathematical operations
def compute_operations():
    result = 0
    for i in range(10**6):
        result += i ** 2 + i * 3 - 1
    return result

# Example function with I/O operations
def perform_io_operations():
    with open('example_file.txt', 'w') as f:
        for i in range(10**5):
            f.write('This is line {}\n'.format(i))

# Example function with recursion
def recursive_function(n):
    if n <= 0:
        return 1
    return n * recursive_function(n - 1)

# Main function
def main():

    result = compute_operations()

    perform_io_operations()
    result = recursive_function(100)
  

if __name__ == "__main__":
    main()
