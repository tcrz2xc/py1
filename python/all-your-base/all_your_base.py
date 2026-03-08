def rebase(input_base, digits, output_base):
    #error checking before doing the math
    if input_base<2:
        raise ValueError("input base must be >= 2")
    elif output_base<2:
        raise ValueError("output base must be >= 2")
    else:
        for d in digits:
            if d >=input_base or d < 0:
                raise ValueError("all digits must satisfy 0 <= d < input base") 
                
    #to allow the change of base with the use of an empty list for digits.
    r=[]
    if digits ==[]:
        r.append(0)
        return r
    if all(d==0 for d in digits):
        return [0]
    value = 0
    for d in digits:
        value = value * input_base +d

    results =[]
    while value>0:
        value, remainder = divmod(value, output_base)
        results.append(remainder)
    return results[::-1]