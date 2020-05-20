#A program that handles hotel room occupancy
#Work done by: Kravtsov - 80%
#              Mauter - 15%
#              Mikhailov - 20%
import classes as cl
import random as r

#This function consider income and losses of the hotel
def main():
    lost_profit = 0.00
    day_profit = 0.00

    with open('fund.txt', 'r', encoding='utf-8') as fund:
        all_rooms = []
        one_p_rooms = []
        two_p_rooms = []
        l_rooms = []
        pl_rooms = []
        for i in fund:
            room, type_room, sum_people, comfort = i.split()
            room = cl.Fund(room, type_room, sum_people, comfort)
            all_rooms.append(room)
            if room.type_room == 'одноместный':
                one_p_rooms.append(room.room)
            elif room.type_room == 'двухместный':
                two_p_rooms.append(room.room)
            elif room.type_room == 'полулюкс':
                pl_rooms.append(room.room)
            else:
                l_rooms.append(room.room)
                
    with open('booking.txt', 'r', encoding='utf-8') as booking:
        reserved_rooms = []
        day = 1
        prices = {'одноместный': '2900.00', 'двухместный': '2300.00', 'полулюкс': '3200.00', 'люкс': '4100.00',
                  'стандарт': '1.0', 'стандарт_улучшенный': '1.2', 'апартамент': '1.5',
                  '0': 'без питания', '280': 'завтрак', '1000': 'полупансион'}

        for i in booking:
            date, name_1, name_2, name_3, sum_people, arrival_date, number_of_days, max_bank = i.split()
            name = name_1 + ' ' + name_2 + ' ' + name_3
            guest = cl.Booking(date, name, sum_people, arrival_date, number_of_days, max_bank)

            suitable_rooms = []
            
            #settelment of people
            if int(guest.date[:2]) > day and len(reserved_rooms) > 0:
                print('=' * 86)
                print('Итог за ', day, guest.date[2:], sep='')
                print('Количество занятых номеров:', len(reserved_rooms))
                print('Количество свободных номеров:', len(all_rooms) - len(reserved_rooms))
                print('Занятость по категориям:')
                k = 0
                for j in one_p_rooms:
                    if j in reserved_rooms:
                        k += 1
                print('Одноместных:', k, 'из', len(one_p_rooms))
                k = 0
                for j in two_p_rooms:
                    if j in reserved_rooms:
                        k += 1
                print('Двухместных:', k, 'из', len(two_p_rooms))
                k = 0
                for j in pl_rooms:
                    if j in reserved_rooms:
                        k += 1
                print('Полулюкс:', k, 'из', len(pl_rooms))
                k = 0
                for j in l_rooms:
                    if j in reserved_rooms:
                        k += 1
                print('Люкс:', k, 'из', len(l_rooms))
                print('Процент загруженности гостиницы:',
                      float(len(reserved_rooms)) / float(len(all_rooms)) * 100.00, '%')
                print('Доход за день:', day_profit, 'руб')
                print('Упущенный доход:', lost_profit, 'руб')

                day_profit = 0.00
                lost_profit = 0.00
                day = int(guest.date[:2])
                
                #check for a reserved room
                reserved_rooms_work = []
                for j in range(len(reserved_rooms)):
                    room_reserved = all_rooms[int(reserved_rooms[j]) - 1]
                    room_reserved.set_actual_date(int(room_reserved.get_actual_date()) - 1)

                    if room_reserved.get_actual_date() == 1:
                        room_reserved.set_actual_people(0)
                        reserved_rooms_work.append(j)

                reserved_rooms_work.sort()
                reserved_rooms_work.reverse()
                for j in reserved_rooms_work:
                    del reserved_rooms[j]

            print('-' * 86)
            print('Поступила заявка на бронирование:')
            print(guest)
            
            #room selection
            for j in range(len(all_rooms)):
                if not all_rooms[j].room in reserved_rooms:
                    room_j = all_rooms[j]
                    price_one = float(prices[room_j.type_room]) * float(prices[room_j.comfort])

                    if room_j.sum_people == guest.sum_people:
                        difference = float(guest.max_bank) - price_one
                        food = '0'

                        if difference > 0:
                            if 280.00 <= difference < 1000.00:
                                price_one += 280.00
                                food = '280'

                            elif difference >= 1000.00:
                                price_one += 1000.00
                                food = '1000'

                            suitable_rooms.append([price_one, 0.00, room_j.room, food, price_one + float(food)])

                    elif room_j.sum_people > guest.sum_people:
                        difference = float(guest.max_bank) - 0.7 * (price_one * float(room_j.sum_people))
                        food = '0'

                        if difference > 0:
                            if 280.00 * 0.7 <= difference < 1000.0 * 0.7:
                                price_one += 280.00 * 0.7
                                food = '280'

                            elif difference >= 1000.00 * 0.7:
                                price_one += 1000.00 * 0.7
                                food = '1000'

                            suitable_rooms.append([price_one,
                                                   (float(room_j.sum_people) - float(guest.sum_people)),
                                                   room_j.room, food, price_one + float(food)])

            if len(suitable_rooms) > 0:

                suitable_rooms.sort(key=lambda j: (j[1], -j[0]))

                probability_of_failure = r.randint(0, 100)
                
                #room suitability
                if probability_of_failure <= 25:
                    print('Найден:')
                    number_room = all_rooms[int(suitable_rooms[0][2]) - 1]
                    print('Номер', number_room.room, number_room.type_room, number_room.comfort,
                          'расчитан на', number_room.sum_people, 'чел.', 'фактически',
                          guest.sum_people, 'чел.', prices[suitable_rooms[0][3]],
                          suitable_rooms[0][4], 'руб./сут')
                    print('Клиент отказался от варианта.')

                    lost_profit += float(guest.max_bank) * float(guest.sum_people) * float(guest.number_of_days)

                else:
                    print('Найден:')
                    number_room = all_rooms[int(suitable_rooms[0][2]) - 1]
                    print('Номер', number_room.room, number_room.type_room, number_room.comfort,
                          'расчитан на', number_room.sum_people, 'чел.', 'фактически',
                          guest.sum_people, 'чел.', prices[suitable_rooms[0][3]],
                          suitable_rooms[0][4], 'руб./сут')
                    print('Клиент согласен. Номер забронирован.')

                    reserved_rooms.append(suitable_rooms[0][2])
                    all_rooms[int(suitable_rooms[0][2]) - 1].set_actual_people(guest.sum_people)
                    all_rooms[int(suitable_rooms[0][2]) - 1].set_actual_date(str(int(guest.arrival_date[:2])
                                                                                 + int(guest.number_of_days)))

                    day_profit += float(suitable_rooms[0][3]) * float(guest.sum_people) \
                                  * float(guest.number_of_days)

            else:
                print('Предложений по данному запросу нет. В бронировании отказано.')
                lost_profit += float(guest.max_bank) * float(guest.sum_people) * float(guest.number_of_days)

    print('=' * 86)
    print('Итог за ', day, guest.date[2:], sep='')
    print('Количество занятых номеров:', len(reserved_rooms))
    print('Количество свободных номеров:', len(all_rooms) - len(reserved_rooms))
    print('Занятость по категориям:')
    k = 0
    for j in one_p_rooms:
        if j in reserved_rooms:
            k += 1
    print('Одноместных:', k, 'из', len(one_p_rooms))
    k = 0
    for j in two_p_rooms:
        if j in reserved_rooms:
            k += 1
    print('Двухместных:', k, 'из', len(two_p_rooms))
    k = 0
    for j in pl_rooms:
        if j in reserved_rooms:
            k += 1
    print('Полулюкс:', k, 'из', len(pl_rooms))
    k = 0
    for j in l_rooms:
        if j in reserved_rooms:
            k += 1
    print('Люкс:', k, 'из', len(l_rooms))
    print('Процент загруженности гостиницы:',
          float(len(reserved_rooms)) / float(len(all_rooms)) * 100.00, '%')
    print('Доход за день:', day_profit, 'руб')
    print('Упущенный доход:', lost_profit, 'руб')


main()
