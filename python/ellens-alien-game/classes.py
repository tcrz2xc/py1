"""Solution to Ellen's Alien Game exercise."""


class Alien:
    """Create an Alien object with location x_coordinate and y_coordinate.

    Attributes
    ----------
    (class)total_aliens_created: int
    x_coordinate: int - Position on the x-axis.
    y_coordinate: int - Position on the y-axis.
    health: int - Number of health points.

    Methods
    -------
    hit(): Decrement Alien health by one point.
    is_alive(): Return a boolean for if Alien is alive (if health is > 0).
    teleport(new_x_coordinate, new_y_coordinate): Move Alien object to new coordinates.
    collision_detection(other): Implementation TBD.
    """

    health=3
    total_aliens_created=0


#TODO:  create the new_aliens_collection() function below to call your Alien class with a list of coordinates.
    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate
        Alien.total_aliens_created+=1

    def hit(self):
        self.health-=1

    def is_alive(self):
        return bool(self.health>0)
    def teleport(self, x_coord, y_coord):
        self.x_coordinate=x_coord
        self.y_coordinate=y_coord
    def collision_detection(self, other_object):
        pass

def new_aliens_collection(list1):
    aliens=[]
    for element in list1:
        x_coordinate=element[0]
        y_coordinate=element[1]
        aliens.append(Alien(x_coordinate, y_coordinate))
    return aliens
        