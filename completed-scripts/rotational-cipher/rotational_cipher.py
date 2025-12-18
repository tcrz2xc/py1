import re
def rotate(text, key):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    list_alpha = list(alpha)
    transform = []
    for letter in range(len(list_alpha)):
        transform.append(list_alpha[(letter+key)%len(list_alpha)])
    transform_str = "".join(transform)
    case_ins = alpha+alpha.upper()
    t_case = transform_str+transform_str.upper()
    map = str.maketrans(case_ins, t_case)
    encrypt = text.translate(map)
    return encrypt