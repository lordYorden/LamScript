import functools

def main():
    print(fib_gen(5))
    
    print(cat_strings_with(' ', 'The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog'))
    
    print(sum_of_squares([[1,2], [3,4], [5,6]]))
    
    print(factortial(3))
    print(exponent(2,3))
    
    one_liner_prog()
    original_prog()
    
    print(num_palindrom_in_list_of_lists([['101'], ['ac'], ['aca', 'bbaabb']]))
    
    #Explain the term "lazy evaluation" in the context of the following program:
    #   in python lazy evaluation is the concept of evaluating the values only when the program "needs them".
    #   in the program bellow this comes to affect as the squared_values are calculated using both methods.
    #   in Eager evaluation the program rules it should calculate them immediately using the list cast.
    #   and in Lazy evaluation the program only gives the list comprehension one value at a time using a generator function.
    print('Eager evaluation:')
    values = list(generate_values())
    squared_values = [square(x) for x in values]
    print(squared_values)

    print('\nLazy evaluation:')
    squared_values = [square(x) for x in generate_values()]
    print(squared_values)
    
    print(get_deceding_primes([1,3,4,7,11,2,23,71,6,12,80]))

def fib_gen(n):
    """Implement a Fibonacci sequence generator using a single lambda expression that
    returns a list of the first n Fibonacci numbers. The function should take n as an input"""
    return list((lambda n: functools.reduce(lambda seq, _: seq + [seq[-1] + seq[-2]], range(2, n), [0, 1])[:n])(n))
    
def cat_strings_with(delimiter=' ', *args):
    """Write the shortest Python program, that accepts a list of strings and return a
    single string that is a concatenation of all strings with a space between them. Do not
    use the "join" function. Use lambda expressions. """
    return functools.reduce(lambda x, y: x + delimiter + y, args)
    
def sum_of_squares(list_of_lists):
    """Write a Python function that takes a list of lists of numbers and return a new list
    containing the cumulative sum of squares of even numbers in each sublist. Use at
    least 5 nested lambda expressions in your solution"""
    return [(lambda lists: functools.reduce(lambda x,y: x+y, map(lambda clean_num: clean_num**2, filter(lambda num: num%2==0, functools.reduce(lambda list1, list2: list1 + list2, lists)))))(list_of_lists)]
    
def apply_on_list(bin_op):
    """Write a higher-order function that takes a binary operation (as a lambda function)
    and returns a new function that applies this operation cumulatively to a sequence.
    Use this to implement both factorial and exponentiation functions"""
    return lambda list: functools.reduce(bin_op, list)

def factortial(n):
    return apply_on_list(lambda x,y: x*y)(range(1, n+1))

def exponent(x, n):
    return apply_on_list(lambda x,y: x*y)([x]*n)

def one_liner_prog(nums = [1,2,3,4,5,6]):
    """Rewrite the following program in one line by using nested filter, map and reduce functions"""
    print(functools.reduce(lambda sum, squered: sum+squered, map(lambda even: even**2, filter(lambda num: num%2 == 0, nums))))

def original_prog():
    nums = [1,2,3,4,5,6]
    evens = []
    for num in nums:
        if num % 2 == 0:
            evens.append(num)
            
    squared = []
    for even in evens:
        squared.append(even**2)
        
    sum_squared = 0
    for x in squared:
        sum_squared += x
    print(sum_squared)
    
def num_palindrom_in_list_of_lists(list_of_lists):
    """Write one-line function that accepts as an input a list of lists containing strings
    and returns a new list containing the number of palindrome strings in each sublist.
    Use nested filter / map / reduce functions"""
    # is_palindrom = lambda string: (string == ''.join([c for c in string[::-1]]))
    # num_palindroms = lambda list1: len(list(filter(lambda string: (string == ''.join([c for c in string[::-1]])), list1)))
    return [len(list(filter(lambda string: (string == ''.join([c for c in string[::-1]])), list1))) for list1 in list_of_lists]

def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x

def get_deceding_primes(nums):
    """Write a one-line Python function that takes a list of integers and returns a new list
    containing only the prime numbers, sorted in descending order. Use lambda
    expressions and list comprehensions"""
    ##create_div = lambda num: [num%i==0 for i in range(2, num)]
    #isprime = lambda num: (functools.reduce(lambda x,y: x or y, [num%i==0 for i in range(2, num)]) == False) if num not in [1,2] else True
    return list(filter(lambda num: (functools.reduce(lambda x,y: x or y, [num%i==0 for i in range(2, num)]) == False) if num not in [1,2] else True ,sorted(nums, reverse=True)))
    
if __name__ == "__main__":
    main()