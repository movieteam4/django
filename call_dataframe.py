# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 00:29:05 2024

@author: ASUS
"""

def unify_date(date):
    import datetime
    from datetime import datetime
    import pandas as pd
    import re
    pattern= re.compile('\d{4}/\d{1,2}/\d{1,2}')
    pattern2= re.compile('\d{1,2}/\d{1,2}')
    pattern3= re.compile(r'\d{1,2}[\u4e00-\u9fff]\d{1,2}[\u4e00-\u9fff]')
    pattern4= re.compile('\d{1,2}-\d{1,2}')
    pattern5=re.compile(r'\d{4}\s[\u4e00-\u9fff]\s\d{1,2}\s[\u4e00-\u9fff]\s\d{1,2}\s[\u4e00-\u9fff]')
    if pattern.search(date):
        date=pattern.search(date).group()
        today = pd.to_datetime('today')
        current_year = today.year

        # 解析日期並組合成完整的日期（默認設置為今年）
        # full_date_str = f"{current_year}/{date}"

        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)

        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)

        # date=date.strftime('%Y-%m-%d')
        # date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    elif pattern2.search(date):
        date=pattern2.search(date).group()
        today = pd.to_datetime('today')
        current_year = today.year

        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"

        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)

        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)

        # date=date.strftime('%Y-%m-%d')
        # date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    elif pattern4.search(date):
        date=pattern4.search(date).group()
        date = date.replace('-','/')
        today = pd.to_datetime('today')
        current_year = today.year

        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"

         # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)

        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
    elif pattern3.search(date):
        date=pattern3.search(date).group()
        date = re.sub(r'[\u4e00-\u9fff]', '/', date)[:-1]
        today = pd.to_datetime('today')
        current_year = today.year

        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"

        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)

        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
    elif pattern5.search(date):
        date=date.replace(' ','')
        date = re.sub(r'[\u4e00-\u9fff]', '/', date)[:-1]
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)
    return date

def remove_space(x):
    full_width_punctuations = {
    '。': '.',  # 全形句號 -> 半形句號
    '，': ',',  # 全形逗號 -> 半形逗號
    '！': '!',  # 全形驚嘆號 -> 半形驚嘆號
    '？': '?',  # 全形問號 -> 半形問號
    '：': ':',  # 全形冒號 -> 半形冒號
    '；': ';',  # 全形分號 -> 半形分號
    '（': '(',  # 全形左括號 -> 半形左括號
    '）': ')',  # 全形右括號 -> 半形右括號
    '【': '[',  # 全形左中括號 -> 半形左中括號
    '】': ']',  # 全形右中括號 -> 半形右中括號
    '《': '<',  # 全形左尖括號 -> 半形左尖括號
    '》': '>',  # 全形右尖括號 -> 半形右尖括號
    '「': '"',  # 全形左引號 -> 半形引號
    '」': '"',  # 全形右引號 -> 半形引號
    '、': ',',  # 全形頓號 -> 半形逗號
}
    x=x.replace(' ','')
    translation_table = str.maketrans(full_width_punctuations)
    x=x.translate(translation_table)
    return x
def call_dataframe():
    import threading
    import mysql.connector
    import pandas as pd
    db_config = {
        'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        'user': 'dhv81sqnky35oozt',
        'password': 'rrdv8ehsrp8pdzqn',
        'database': 'xltc236odfo1enc9',
        'charset': 'utf8mb4'
    }
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("成功連接到 MariaDB 資料庫")

    cursor=connection.cursor()
    cursor.execute('SELECT * FROM movies_html ORDER BY id DESC LIMIT 1')
    result=cursor.fetchall()
    res=result[0][1]
    final_data=pd.read_html(res)[0]
    cursor.execute('SELECT * FROM vieshow_html ORDER BY id DESC LIMIT 1')
    result=cursor.fetchall()
    res=result[0][1]
    vieshow_data=pd.read_html(res)[0]
    cursor.execute('SELECT * FROM vieshow_html2 ORDER BY id DESC LIMIT 1')
    result=cursor.fetchall()
    res=result[0][1]
    vieshow_data2=pd.read_html(res)[0]
    # vieshow_data['日期']=vieshow_data['日期'].apply(unify_date)
    final_data=pd.concat([vieshow_data,final_data,vieshow_data2])
    final_data['日期']=final_data['日期'].apply(unify_date)
    final_data['日期'] = pd.to_datetime(final_data['日期'])
    # cinema_to_be_fill=final_data.groupby('電影院名稱').count().index
    # columns_to_be_filled=['導演','演員','類型','宣傳照']
    # # final_data['中文片名']=final_data['中文片名'].apply(remove_space)
    # for cinema in cinema_to_be_fill:
    #     to_fill=final_data[final_data['電影院名稱']==cinema]
    #     ch_names=to_fill.groupby('中文片名').count().index
    #     for ch_name in ch_names:
    #         for col in columns_to_be_filled:
    #             final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))]=final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))].fillna(value=to_fill[[col,'中文片名']][to_fill['中文片名']==ch_name].iloc[0][col])
    return final_data
def week_ranking(final_data):
    # from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    # from selenium.webdriver.support.wait import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    # from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    # import os
    # import traceback
    ranking_error='排行榜 程式完美'
    ranking_data =''
    #排行榜網頁
    # front_page_web = "https://boxofficetw.tfai.org.tw/statistic/"
    # Week/100/0/all/False/ReleaseDate/2024-10-04 #周/顯示數量/第幾頁/all/逆排序/主要排序依據/日期
    # 日期
    date = datetime.now().date()
    # 統計方式
    # statistical_method = ["week", "month"]
    # try:
    #         s="week"
    #         # 建立list
    #         l_name = []
    #         l_release_time = []
    #         l_little_money = []
    #         l_little_ticket = []
    #         l_all_money = []
    #         l_all_ticket = []
    #         # 寫入要搜尋的url資訊
    #         url = front_page_web + s + "/100/0/all/False/ReleaseDate/" + str(date)
    #         # 使用動態抓取,並用隱性等待駛往詹資訊完整抓取資料
    #         chrome_options = webdriver.ChromeOptions()
    #         chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #         chrome_options.add_argument("--headless") #無頭模式
    #         chrome_options.add_argument("--disable-dev-shm-usage")
    #         chrome_options.add_argument("--no-sandbox")
    #         chrome_options.add_argument("--window-size=1920,1080")
    #         from selenium.webdriver.chrome.service import Service
    #         service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    #         driver = webdriver.Chrome(service=service, options=chrome_options)
    #         # driver = webdriver.Chrome()
    #         driver.get(url)
    #         driver.implicitly_wait(10)
    #         # 顯性等待最多40秒，每0.8秒尋找一次，於等待時間內尋找特定的字串出现。
    #         WebDriverWait(driver, 40, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME, "nowrap.ordered")))
    #         ranking_html = driver.page_source
    #         ranking_soup = BeautifulSoup(ranking_html,"html.parser")
    #         f_lists = ranking_soup.select("div.statistic-table-container tbody > tr") #找到排名表格列表位置
    #         for m_list in f_lists: #依排名表格儲存資料
    #             f_name = m_list.select("td.left.min-60")[0] # 電影名字
    #             f_release_time = m_list.select("td.nowrap.ordered")[0] # 上映日
    #             f_all_money = m_list.select("td.right")[7] # 總累積金額
    #             f_all_ticket = m_list.select("td.right")[8] # 總票房
    #             l_name.append(f_name.text)
    #             l_release_time.append(f_release_time.text)
    #             l_all_money.append(f_all_money.text)
    #             l_all_ticket.append(f_all_ticket.text)
    #             f_little_money = m_list.select("td.right")[1] # 當周金額
    #             f_little_ticket = m_list.select("td.right")[3] # 當周票房
    #             l_little_money.append(eval(f_little_money.text.replace(',','')))
    #             l_little_ticket.append(eval(f_little_ticket.text.replace(',','')))
    #             print("中文片名 :",f_name.text)
    #             print("上映日 :",f_release_time.text)
    #             print("當周金額 :"if s == "week" else "當月金額 :",f_little_money.text)
    #             print("當周票房數 :"if s == "week" else "當月金額票房數 :",f_little_ticket.text)
    #             print("總金額 :",f_all_money.text)
    #             print("總票房 :",f_all_ticket.text)
    #             print()
    #         if s == "week": #紀錄當周排行
    #             ranking_week_data = pd.DataFrame({
    #                                     "中文片名" : l_name,
    #                                     "上映日" : l_release_time,
    #                                     "當周金額" : l_little_money,
    #                                     "當周票房數" :l_little_money ,
    #                                     "總金額" : l_all_money,
    #                                     "總票房" : l_all_ticket,
    #                                     })
    #             # ranking_week_data.to_csv("當周排行.csv", encoding="big5")
    #         # elif s == "month":#紀錄當月排行
    #         #     ranking_month_data = pd.DataFrame({
    #         #                             "中文片名" : l_name,
    #         #                             "上映日" : l_release_time,
    #         #                             "當周金額"if s == "week" else "當月金額" : l_little_money,
    #         #                             "當周票房數"if s == "week" else "當月金額票房數" :l_little_money ,
    #         #                             "總金額" : l_all_money,
    #         #                             "總票房" : l_all_ticket,
    #         #                             })
    #             # ranking_month_data.to_csv("當月排行.csv",encoding="big5")

    # finally:
    #     driver.quit()
    # ranking_week_data['中文片名']= ranking_week_data['中文片名'].apply(remove_space)
    # final_data = pd.merge(final_data, ranking_week_data[['中文片名', '當周票房數']], on='中文片名', how='left')
    final_data=final_data.sort_values(by='當周票房數', ascending=False)
    final_data = final_data.drop_duplicates(subset='中文片名', keep='first')
    # final_data = final_data[['中文片名',"當周金額","當周票房數","總金額","總票房"]].sort_values(by='當周票房數', ascending=False).head(10)
    return final_data
def month_ranking(final_data):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    import os
    import traceback
    ranking_error='排行榜 程式完美'
    ranking_data =''
    #排行榜網頁
    front_page_web = "https://boxofficetw.tfai.org.tw/statistic/"
    # Week/100/0/all/False/ReleaseDate/2024-10-04 #周/顯示數量/第幾頁/all/逆排序/主要排序依據/日期
    # 日期
    date = datetime.now().date()
    # 統計方式
    # statistical_method = ["week", "month"]
    try:
            s="month"
            # 建立list
            l_name = []
            l_release_time = []
            l_little_money = []
            l_little_ticket = []
            l_all_money = []
            l_all_ticket = []
            # 寫入要搜尋的url資訊
            url = front_page_web + s + "/100/0/all/False/ReleaseDate/" + str(date)
            # 使用動態抓取,並用隱性等待駛往詹資訊完整抓取資料
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless") #無頭模式
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            from selenium.webdriver.chrome.service import Service
            service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=chrome_options)
            # driver = webdriver.Chrome()
            # driver = webdriver.Chrome()
            driver.get(url)
            driver.implicitly_wait(10)
            # 顯性等待最多40秒，每0.8秒尋找一次，於等待時間內尋找特定的字串出现。
            WebDriverWait(driver, 40, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME, "nowrap.ordered")))
            ranking_html = driver.page_source
            ranking_soup = BeautifulSoup(ranking_html,"html.parser")
            f_lists = ranking_soup.select("div.statistic-table-container tbody > tr") #找到排名表格列表位置
            for m_list in f_lists: #依排名表格儲存資料
                f_name = m_list.select("td.left.min-60")[0] # 電影名字
                f_release_time = m_list.select("td.nowrap.ordered")[0] # 上映日
                f_all_money = m_list.select("td.right")[7] # 總累積金額
                f_all_ticket = m_list.select("td.right")[8] # 總票房
                l_name.append(f_name.text)
                l_release_time.append(f_release_time.text)
                l_all_money.append(f_all_money.text)
                l_all_ticket.append(f_all_ticket.text)
                f_little_money = m_list.select("td.right")[1] # 當周金額
                f_little_ticket = m_list.select("td.right")[3] # 當周票房
                l_little_money.append(eval(f_little_money.text.replace(',','')))
                l_little_ticket.append(eval(f_little_ticket.text.replace(',','')))
                print("中文片名 :",f_name.text)
                print("上映日 :",f_release_time.text)
                print("當周金額 :"if s == "week" else "當月金額 :",f_little_money.text)
                print("當周票房數 :"if s == "week" else "當月金額票房數 :",f_little_ticket.text)
                print("總金額 :",f_all_money.text)
                print("總票房 :",f_all_ticket.text)
                print()
            # if s == "week": #紀錄當周排行
            #     ranking_week_data = pd.DataFrame({
            #                             "中文片名" : l_name,
            #                             "上映日" : l_release_time,
            #                             "當周金額" : l_little_money,
            #                             "當周票房數" :l_little_money ,
            #                             "總金額" : l_all_money,
            #                             "總票房" : l_all_ticket,
            #                             })
                # ranking_week_data.to_csv("當周排行.csv", encoding="big5")
            if s == "month":#紀錄當月排行
                ranking_month_data = pd.DataFrame({
                                        "中文片名" : l_name,
                                        "上映日" : l_release_time,
                                        "當周金額"if s == "week" else "當月金額" : l_little_money,
                                        "當周票房數"if s == "week" else "當月金額票房數" :l_little_money ,
                                        "總金額" : l_all_money,
                                        "總票房" : l_all_ticket,
                                        })
                # ranking_month_data.to_csv("當月排行.csv",encoding="big5")

    finally:
        driver.quit()
    ranking_month_data['中文片名']= ranking_month_data['中文片名'].apply(remove_space)
    final_data = pd.merge(final_data, ranking_month_data[['中文片名', '當月金額票房數']], on='中文片名', how='left')
    final_data=final_data.sort_values(by='當月金額票房數', ascending=False)
    final_data = final_data.drop_duplicates(subset='中文片名', keep='first')
    # final_data = final_data[['中文片名',"當周金額","當周票房數","總金額","總票房"]].sort_values(by='當周票房數', ascending=False).head(10)
    return final_data
def address():
    import mysql.connector
    import pandas as pd
    db_config = {
        'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        'user': 'dhv81sqnky35oozt',
        'password': 'rrdv8ehsrp8pdzqn',
        'database': 'xltc236odfo1enc9',
        'charset': 'utf8mb4'
    }
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("成功連接到 MariaDB 資料庫")
    cursor=connection.cursor()
    # data=pd.read_csv('臺灣地區32碼郵遞區號.csv')
    # data=data.to_html(classes='table table-striped', index=False).replace(r"'",'’')
    cursor.execute('SELECT * FROM address')
    result=cursor.fetchall()
    res=result[0][0]
    df=pd.read_html(res)[0]
    return df
# che=call_dataframe()
# che2 = che[che['電影院名稱'].str.contains('威秀')]

