#classes should be here
class Booking:
    def __init__(self, date, name, sum_people, arrival_date, number_of_days, max_bank ):

        self.max_bank = max_bank
        self.number_of_days = number_of_days
        self.arrival_date = arrival_date
        self.sum_people = sum_people
        self.name = name
        self.date = date

    def __str__(self):
        return f'{self.date} {self.name} {self.sum_people} {self.arrival_date} {self.number_of_days} {self.max_bank}'
    def __repr__(self):
        return self.__str__()
class Fund:
    def __init__(self, room, type, sum_people, comfort):
        self.comfort = comfort
        self.sum_people = sum_people
        self.type = type
        self.room = room
    def __str__(self):
        return f'{self.room} {self.type} {self.sum_people} {self.comfort}'
    def __repr__(self):
        return self.__str__()

a = Booking('01.03.2020', 'Жиренкова Надежда Евдокимовна', '1', '01.03.2020', '3', '4400')
print(a)



