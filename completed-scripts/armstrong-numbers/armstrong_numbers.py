def is_armstrong_number(number):
    string_num = str(number)
    list_num = list(map(int, string_num))
    sum =0
    l=len(list_num)
    for num in list_num[::-1]:
        sum+=num**l
    if number == 0:
        return True
    elif sum == number:
        return True
    else:
        return False                   