import re
def is_isogram(string):
    test_string = re.sub(r'[^a-zA-Z]', "", string)
    test_string = test_string.lower()
    iso = set(test_string)
    iso_test = list(map(str, test_string))
    if string =="":
        return True
    if len(iso) == len(iso_test):
        return True
    
    return False
