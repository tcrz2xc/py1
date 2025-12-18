def classify(number):
    """ A perfect number equals the sum of its positive divisors.

    :param number: int a positive integer
    :return: str the classification of the input integer
    """
    if number>0:
        sum=0
        for i in range(1, number):
            if number%i==0:
                sum+=i
        if sum == number:
            return "perfect"
        elif sum>number:
            return "abundant"
        else:
            return "deficient"
    else:
        raise ValueError("Classification is only possible for positive integers.")
    
