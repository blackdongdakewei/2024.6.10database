import pymysql

table_name='喜剧电影'
movie_name='疯狂动物城'


def select_in_table(table_name,movie_name):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="zmh",
        password="123456",
    )
    cursur=connection.cursor()

    query=f'SELECT * FROM {table_name} WHERE 电影名=%s'
    cursur.execute(query,(movie_name))
    result = cursur.fetchone()

    if result:
        print(f'id:{result[0]}',f'电影名:{movie_name}',f"上映时间:{result[2]}")
select_in_table(table_name,movie_name)
