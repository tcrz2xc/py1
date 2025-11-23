import re
def is_valid(isbn):
    non_hype = re.sub("-", "", isbn)
    if re.search(r'^[0-9]{9}[\dX]$', non_hype):
        usbn_list = [int(c) if c.isdigit() else 10 for c in non_hype]
        test =0
        for i, digit in enumerate(usbn_list):
            test += digit*(10-i)
        if test %11 == 0:
            return True
    return False