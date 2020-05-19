#A program that handles hotel room occupancy
#Work done by:
import classes as cl
import random as r


def main():
    lost_profit = 0.00

    with open('fund.txt', 'r', encoding='utf-8') as fund:
        all_rooms = []
        for i in fund:
            room, type_room, sum_people, comfort = i.split()
            room = cl.Fund(room, type_room, sum_people, comfort)
            all_rooms.append(room)

    with open('booking.txt', 'r', encoding='utf-8') as booking:
        reserved_rooms = []
        day = 0
        prices = {'одноместный': '2900.00', 'двухместный': '2300.00', 'полулюкс': '3200.00', 'люкс': '4100.00',
                  'стандарт': '1.0', 'стандарт_улучшенный': '1.2', 'апартамент': '1.5',
                  'Без питания': '0.00', 'Завтрак': '280.00', 'Полупансион': '1000.00'}

        for i in booking:
            date, name_1, name_2, name_3, sum_people, arrival_date, number_of_days, max_bank = i.split()
            guest = cl.Booking(date, name_1, sum_people, arrival_date, number_of_days, max_bank)
            suitable_rooms = []

            if int(guest.date[:2]) > day and len(reserved_rooms) > 0:
                day = int(guest.date[:2])

                reserved_rooms_work = []
                for j in range(len(reserved_rooms)):
                    room_reserved = all_rooms[int(reserved_rooms[j]) - 1]
                    room_reserved.set_actual_date(int(room_reserved.get_actual_date()) - 1)

                    if room_reserved.get_actual_date() == 0:
                        print('Номер освободился:', reserved_rooms[j])
                        room_reserved.set_actual_people(0)
                        reserved_rooms_work.append(reserved_rooms[j])

                for j in reserved_rooms_work:
                    number = -1000
                    for g in range(len(reserved_rooms)):
                        if reserved_rooms[g] == j:
                            number = g

                    if number >= 0:
                        del reserved_rooms[g]

            for j in range(len(all_rooms)):
                if not all_rooms[j].room in reserved_rooms:
                    room_j = all_rooms[j]
                    price_one = float(prices[room_j.type_room]) * float(prices[room_j.comfort])

                    if room_j.sum_people == guest.sum_people:
                        difference = float(guest.max_bank) - price_one
                        if difference > 0:
                            if 280.00 <= difference < 1000.00:
                                price_one += 280.00

                            elif difference >= 1000.00:
                                price_one += 1000.00

                            suitable_rooms.append([price_one, 0.00, room_j.room])

                    elif room_j.sum_people > guest.sum_people:
                        difference = float(guest.max_bank) - 0.7 * (price_one * float(room_j.sum_people))
                        if difference > 0:
                            if 280.00 * 0.7 <= difference < 1000.0 * 0.7:
                                price_one += 280.00 * 0.7

                            elif difference >= 1000.00 * 0.7:
                                price_one += 1000.00 * 0.7

                            suitable_rooms.append([price_one,
                                                   (float(room_j.sum_people) - float(guest.sum_people)),
                                                   room_j.room])

            if len(suitable_rooms) > 0:
                suitable_rooms.sort(key=lambda j: (j[1], -j[0]))

                probability_of_failure = r.randint(0, 100)

                if probability_of_failure <= 25:
                    print('Отказ')
                    lost_profit += float(guest.max_bank) * float(guest.sum_people) * float(guest.number_of_days)

                else:
                    print('забронирован номер', suitable_rooms[0][2])
                    reserved_rooms.append(suitable_rooms[0][2])
                    all_rooms[int(suitable_rooms[0][2]) - 1].set_actual_people(guest.sum_people)
                    all_rooms[int(suitable_rooms[0][2]) - 1].set_actual_date(str(int(guest.arrival_date[:2])
                                                                                 + int(guest.number_of_days)))

            else:
                print('Нет подходящих комнат')
                lost_profit += float(guest.max_bank) * float(guest.sum_people) * float(guest.number_of_days)

main()