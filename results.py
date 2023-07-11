from connect import connection
from random import randint as r

class Money:
    def __init__(self, id, money_value, value):
        if value == 'coin':
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `gamers` SET money = money + {money_value} WHERE id_user = {id};")
                connection.commit()
        elif value == 'diam':
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `gamers` SET money = money + 10000 WHERE id_user = {id};")
                connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `gamers` SET diamonds = diamonds + 1 WHERE id_user = {id};")
                connection.commit()

        elif value == 'treasure':
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `gamers` SET money = money + {r(0, 100000)} WHERE id_user = {id};")
                connection.commit()

            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `gamers` SET treasure = treasure + 1 WHERE id_user = {id};")
                connection.commit()

# Баланс игрока
def balance(id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT money FROM `gamers` WHERE id_user = {id}")
        money_value = cursor.fetchone()
        return money_value['money']

# Таблица лидеров
def leaders(id):
    table_leaders = ""
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name, money, diamonds FROM `gamers` ORDER BY money DESC")
        money_value = cursor.fetchmany(5)
        for row in money_value:
            table_leaders += f"{money_value.index(row)+1}. {row['name']} " \
                             f"--> Золото: {row['money']} " \
                             f"| Алмазов: {row['diamonds']}\n"
    return table_leaders