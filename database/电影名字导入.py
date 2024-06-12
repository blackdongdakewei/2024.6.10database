import pymysql

table_name='喜剧电影'
movie_name='疯狂动物城'
date='2016'
# i=input('如果添加就输入0，否则输入要修改的id\n')
# i=int(i)
i=0
def lead_movie_name(i,table_name,movie_name,date):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="zmh",
        password="123456",
    )
    cursur=connection.cursor()
    if i==0:
        query = f"SELECT MAX(id) FROM {table_name}"
        cursur.execute(query)
        j = cursur.fetchone()[0] or 0
        print(cursur.fetchone())
        sql_query = "INSERT INTO {} (id,电影名,上映时间) VALUES (%s,%s,%s)".format(table_name)
        cursur.execute(sql_query, (j + 1, movie_name, date))
    else:
        j=i
        sql_query = "UPDATE {} SET 电影名=%s,上映时间=%s WHERE id=%s".format(table_name)
        cursur.execute(sql_query, (movie_name, date,j))

    connection.commit()
lead_movie_name(i,table_name,movie_name,date)