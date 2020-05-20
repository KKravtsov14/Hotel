# classes should be here
class Booking:
    def __init__(self, date, name, sum_people, arrival_date, number_of_days, max_bank):
        'instance initialization'

        self.max_bank = max_bank
        self.number_of_days = number_of_days
        self.arrival_date = arrival_date
        self.sum_people = sum_people
        self.name = name
        self.date = date
       
    def __str__(self):
        'instance wait and string return'
        return f'{self.date} {self.name} {self.sum_people} {self.arrival_date} ' \
               f'{self.number_of_days} {self.max_bank}'
    
    def __repr__(self):
        'getting class instance'
        return self.__str__()


class Fund:
    def __init__(self, room, type_room, sum_people, comfort, __actual_people = 0, __actual_date = 0):
        self.__actual_date = __actual_date
        self.__actual_people = __actual_people
        self.comfort = comfort
        self.sum_people = sum_people
        self.type_room = type_room
        self.room = room

    def __str__(self):
        return f'{self.room} {self.type_room} {self.sum_people} {self.comfort}'

    def __repr__(self):
        return self.__str__()

    def set_actual_people(self, __actual_people):
        self.__actual_people = __actual_people

    def get_actual_people(self):
        return self.__actual_people

    def set_actual_date(self, __actual_date):
        self.__actual_date = __actual_date

    def get_actual_date(self):
        return self.__actual_date
