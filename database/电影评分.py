import pymysql

table_name='猩球崛起'
def collect_in_table(table_name):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="zmh",
        password="123456",
    )
    cursur=connection.cursor()
    # 执行SQL查询
    sql = f"SELECT Score, COUNT(*) AS count FROM {table_name} GROUP BY Score LIMIT 5"
    cursur.execute(sql)

    # 获取查询结果
    results = cursur.fetchall()

    # 打印统计结果
    print("统计结果：")
    for row in results:
        print(row)
        print(row[0], ":", row[1])
    connection.close()

    scoring_criteria = {
        "力荐": 5,
        "还行": 4,
        "推荐": 3,
        "较差": 2,
        "很差": 1
    }
    final_score = 0
    number=0
    for row in results:
        number+=row[1]
        final_score += scoring_criteria[row[0]] * row[1]
    final_score=final_score/number
    print(final_score)
collect_in_table(table_name)