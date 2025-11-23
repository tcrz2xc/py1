def score(x, y):
    """
    circle_area= pi*r**2
    equation_of_circle -> x**2 + y**2 = r**2

    point distribution:
    -dart lands outside the target no points (0 points)
    -dart lands in the outer circle of the target, player earns 1 point.
    -dart lands in the middle circle, player earns 5 points.
    -dart lands in the inner circle, player earns 10 points
    
    The outer circle has a radius of 10 units (this is equivalent to the total radius for the entire target), the middle circle a radius of 5 units, and the inner circle a radius of 1.
Of course, they are all centered at the same point — that is, the circles are [concentric][] defined by the coordinates (0, 0).

    outer_circle x**2+y**2=10**2
    middle_circle x**2+y**2=5**2
    inner_circle x**2+y**2=1**2


    """
    
    if x**2+y**2<=1:
        return 10
    if x**2+y**2>1 and x**2+y**2<=5**2:
        return 5
    if x**2+y**2>5**2 and x**2+y**2<=10**2:
        return 1
    return 0
 
