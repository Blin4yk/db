import pymysql.cursors
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully...")

    try:
        # with connection.cursor() as cursor:
        #     create_table = "CREATE TABLE `people`(id INT AUTO_INCREMENT," \
        #                    " name VARCHAR(32), " \
        #                    "email VARCHAR(32), " \
        #                    "password VARCHAR(32), PRIMARY KEY(id));"
        #     cursor.execute(create_table)

    #     Заполнение таблицы
        with connection.cursor() as cursor:
            for i in range(100):
                cursor.execute(f"INSERT INTO `people`(name, email, password) VALUES ('{i}____{i}', '{i,i,i,i,i,i}@mail.ru','{i,i,i,i,i,i,i,i,i}');")
                connection.commit()
    finally:
        connection.close()

except Exception as ex:
    print(f"ERROR... {ex}")