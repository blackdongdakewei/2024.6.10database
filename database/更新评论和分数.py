#这个脚本用于修改评论和得分，前提是执行过爬取脚本
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

table_name='猩球崛起'
url = "https://movie.douban.com/subject/36069854/comments?status=P"
def extract_titles(url):
    # 使用Selenium打开Edge浏览器
    driver = webdriver.Edge()
    print(0)
    try:
        # 打开网页
        driver.get(url)
        print(1)
        # 等待元素加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class*=rating]')))

        # 初始化结果列表
        titles = []
        collected_comments = []

        # 定义六种class值
        class_values = ['allstar00', 'allstar10', 'allstar20', 'allstar30', 'allstar40', 'allstar50']

        # 循环直到所有评论加载完毕
        while len(titles) < 200:
            # 找到当前页面中的所有评论
            time.sleep(1)
            comments = driver.find_elements(By.CSS_SELECTOR, 'span[class*=rating][title]')

            # 遍历评论，如果有任何一种class出现，则将其标题添加到列表中
            for comment in comments:
                class_attribute = comment.get_attribute('class')
                if any(class_value in class_attribute for class_value in class_values):
                    titles.append(comment.get_attribute('title'))

            # 模拟缓慢滚动页面
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 滚动间隔，决定调整
            short_elements = driver.find_elements(By.CLASS_NAME, 'short')
            # 提取文本内容
            short_comments = [element.text.strip() for element in short_elements]

            # 将提取的评论添加到已收集的评论中
            collected_comments.extend(short_comments)
            # 检查是否已经到达页面底部
            last_height = driver.execute_script("return document.body.scrollHeight")
            new_height = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if new_height == last_height:
                try:
                    next_button = driver.find_element(By.CLASS_NAME, 'next')
                    next_button.click()
                except NoSuchElementException:
                    break

        return titles[0:200], collected_comments[0:200]

    except Exception as e:
        print("发生错误：", e)
    finally:
        # 关闭浏览器
        driver.quit()


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="zmh"
)

# 更新评论数据
def insert_comment(conn, comment,i,table_name):

    cursor = conn.cursor()
    # cursor.execute("UPDATE user SET comments=%s WHERE id=%s",(comment,i))
    sql_query = "UPDATE {} SET comments=%s WHERE id=%s".format(table_name)
    cursor.execute(sql_query, (comment, i))
    conn.commit()


# 更新评分数据
def insert_score(conn, title, i,table_name):
    cursor = conn.cursor()
    # cursor.execute("UPDATE user SET Score=%s WHERE id=%s", (title, i))
    sql_query = "UPDATE {} SET Score=%s WHERE id=%s".format(table_name)
    cursor.execute(sql_query, (title, i))
    conn.commit()



titles, comments = extract_titles(url)

def upgrade_comment():
    i=1
    for comment in comments:
        insert_comment(conn,comment,i,table_name)
        i=i+1
def upgrade_score():
    i=1
    for title in titles:
        insert_score(conn,title,i,table_name)
        i=i+1
upgrade_comment()
upgrade_score()