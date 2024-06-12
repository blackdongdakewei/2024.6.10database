#这个脚本用于从数据库中读取评论然后ai评价，然后保存回数据库
import pymysql

table_name='寻梦环游记'
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="zmh"
)
# 创建游标
cursor = conn.cursor()

# SQL查询
query = f"SELECT comments FROM {table_name}"

# 执行查询
cursor.execute(query)

# 获取查询结果
results = cursor.fetchall()

# 存入列表
questions = [row[0] for row in results]

from zhipuai import ZhipuAI
client = ZhipuAI(api_key="55157a9a90763aaaa6c6582293d2e531.CYZRIiYgypU2ElY9")
responses=[]

def get_response(client,question,i):
    response = client.chat.completions.create(
        model="glm-3-turbo",  # 填写需要调用的模型名称
        messages=[
        {"role":"user","content":"我接下来会给你一个影评，请你依据影评的内容将它们分为正面、负面、中立三种，只需简短的给出你的选择并给出一个十个字以内的简评（必须十个字以内），不需要说多余的话"},
        {"role": "user", "content": f"{question}"}
    ],
    )

    responses=response.choices[0].message
    finall=responses.content
    sql_query = "UPDATE {} SET AI_comment=%s WHERE id=%s".format(table_name)
    cursor.execute(sql_query, (finall, i))
    conn.commit()
    print(i,finall)
#     responses.append(response.choices[0].message)
# for question in questions:
#     get_response(client,question)
# print(responses)
# finalls=[]
# for i, response in enumerate(responses):
#    print(f"Question: {questions[i]}")
#    finalls.append(response.content)
#    print(f"Answer: {response.content}\n")
# print(finalls)
#
# def insert_AIcomment(conn, finall,i,table_name):
#     """
#     向数据库中插入评论
#     """
#     cursor = conn.cursor()
#     # cursor.execute("UPDATE user SET AI_comment=%s WHERE id=%s",(finall,i))
#     sql_query = "UPDATE {} SET AI_comment=%s WHERE id=%s".format(table_name)
#     cursor.execute(sql_query, (finall, i))
#     conn.commit()
def upgrade_AI():
    i=1
    #for finall in finalls:
    for question in questions:
        #insert_AIcomment(conn,finall,i,table_name)
        get_response(client,question,i)
        i=i+1
upgrade_AI()
# 关闭游标和连接
cursor.close()
conn.close()