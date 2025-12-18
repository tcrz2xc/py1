def square(number):
    if number<=0 or number > 64:
        raise ValueError("square must be between 1 and 64")
    else:
        number_at_square = 2**(number-1)
    return number_at_square

def total():
    total_squares = 64
    sum =0
    for i in range(1, 65):
        sum +=square(i)
    return sum
