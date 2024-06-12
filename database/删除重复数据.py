import pymysql

table = 'movie_name'
column = 'column'

def remove_duplicates_and_reorder(table, column):
    # 连接数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="",
        password="",
    )

    try:
        with connection.cursor() as cursor:
            # 查找重复项
            query = f"SELECT `{column}`, MIN(id) AS min_id FROM `{table}` GROUP BY `{column}` HAVING COUNT(*) > 1"
            cursor.execute(query)
            duplicates = cursor.fetchall()
            print(duplicates)
            for duplicate in duplicates:
                # 删除除第一次出现以外的重复项
                query = f"DELETE FROM `{table}` WHERE id != %s AND `{column}` = %s"
                cursor.execute(query, (duplicate[1], duplicate[0]))  # 使用索引位置

            # 创建临时表并按照 id 排序
            query = f"CREATE TEMPORARY TABLE temp_table AS SELECT * FROM `{table}` ORDER BY id"
            cursor.execute(query)

            # 重新排序id列
            query = "SET @new_id := 0"
            cursor.execute(query)

            query = "UPDATE temp_table SET id = (@new_id := @new_id + 1)"
            cursor.execute(query)

            # 更新原表数据
            query = f"TRUNCATE TABLE `{table}`"
            cursor.execute(query)

            query = f"INSERT INTO `{table}` SELECT * FROM temp_table"
            cursor.execute(query)

            # 删除临时表
            query = "DROP TABLE temp_table"
            cursor.execute(query)

            # 提交更改
            connection.commit()
            print("重复项已成功删除，并且ID已重新排序！")

    finally:
        # 关闭连接
        connection.close()

remove_duplicates_and_reorder(table=table, column=column)




