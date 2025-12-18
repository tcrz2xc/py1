def equilateral(sides):
    a, b, c = sides
    if all(x ==0 for x in sides):
        return False
    elif a + b >= c and b + c >= a and a + c >= b and a==b and a ==c:
        return True
    else:
        return False

def isosceles(sides):
    a, b, c = sides
    if all(x ==0 for x in sides):
        return False
    elif a + b >= c and b + c >= a and a + c >= b and (a==b or a ==c or b==c):
        return True
    else:
        return False

def scalene(sides):
    a, b, c = sides
    if all(x ==0 for x in sides):
        return False
    elif a + b >= c and b + c >= a and a + c >= b and a !=b and a !=c and b!=c:
        return True
    else:
        return False