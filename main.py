import connect
import pymysql.cursors
with connect.connection.cursor() as cursor:
    cursor.execute("SELECT * FROM `people` order by name")
    res = cursor.fetchall()