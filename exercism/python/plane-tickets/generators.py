"""Functions to automate Conda airlines ticketing system."""


def generate_seat_letters(number):
    """Generate a series of letters for airline seats.

    :param number: int - total number of seat letters to be generated.
    :return: generator - generator that yields seat letters.

    Seat letters are generated from A to D.
    After D it should start again with A.

    Example: A, B, C, D

    """
    gen =["A", "B", "C","D"]
    count=0
    while count<number:
        yield gen[count%4]
        count+=1
        
        

    


def generate_seats(number):
    """Generate a series of identifiers for airline seats.

    :param number: int - total number of seats to be generated.
    :return: generator - generator that yields seat numbers.

    A seat number consists of the row number and the seat letter.

    There is no row 13.
    Each row has 4 seats.

    Seats should be sorted from low to high.

    Example: 3C, 3D, 4A, 4B

    """

    gen =["A", "B", "C", "D"]
    count =0
    while count<number:
        seat_num = count//4
        letter = gen[count%4]
        if seat_num < 12:
            yield str(seat_num+1)+str(letter)
        else:
            yield str(seat_num+2) + str(letter)
        count+=1

def assign_seats(passengers):
    """Assign seats to passengers.

    :param passengers: list[str] - a list of strings containing names of passengers.
    :return: dict - with the names of the passengers as keys and seat numbers as values.

    Example output: {"Adele": "1A", "Björk": "1B"}

    """
    gen1 = ["A", "B", "C", "D"]
    temp={}
    for i, name in enumerate(passengers):
        seat_num= i//4
        letter = gen1[i%4]
        if seat_num <12:
            seat= f"{seat_num+1}{letter}"
        else:
            seat = f"{seat_num+2}{letter}"
        temp[name]=seat
    return temp

def generate_codes(seat_numbers, flight_id):
    """Generate codes for a ticket.

    :param seat_numbers: list[str] - list of seat numbers.
    :param flight_id: str - string containing the flight identifier.
    :return: generator - generator that yields 12 character long ticket codes.

    """
    for element in seat_numbers:
        partial1 = element.split()
        partial2 = flight_id.split()
        partial1.extend(partial2)
        var=("").join(partial1)
        num = 12-len(var)
        code =var+("0"*num)
        yield code

    
