from connect import connection

class Money:
    def __init__(self, id, money_value):
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE `gamers` SET money = money + {money_value} WHERE id_user = {id};")
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
        cursor.execute(f"SELECT name, money FROM `gamers` ORDER BY money DESC")
        money_value = cursor.fetchmany(5)
        for row in money_value:
            table_leaders += f"{money_value.index(row)+1}. {row['name']} --> Золото: {row['money']}\n"
    return table_leaders