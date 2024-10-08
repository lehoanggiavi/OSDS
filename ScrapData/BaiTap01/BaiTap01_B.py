from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sqlite3

######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('MUSICIANS.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE Musicians (
            id integer primary key autoincrement,
            Name text,
            YearActive Integer
        )
    ''')
except Exception as e:
    print(e)

def them(Name, YearActive):
    conn = sqlite3.connect('MUSICIANS.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO MUSICIANS(Name, YearActive)
        VALUES (:Name, :YearActive)
    ''',
      {
          'Name': Name,
          'YearActive': YearActive
      })
    conn.commit()
    conn.close()


"Khoi tao web"
driver = webdriver.Chrome()

"Mo trang web"
url = "https://en.wikipedia.org/wiki/Lists_of_musicians"
driver.get(url)
time.sleep(2)

"""Trích xuất các liên kết đến trang web chứa thông tin về các nhạc sĩ chuyên về thể loại âm 
nhạc bắt đầu bằng chữ "A". In ra toàn bộ các đường link có liên quan đến các nhạc sĩ (bắt 
đầu bằng chữ List of)."""

"Tim tat ca the ul"
tags_ul = driver.find_elements(By.TAG_NAME, "ul")

"Tim the ul muon lay cac the loai nhac bat dau bang chu A"
# for index, value in enumerate(tags_ul):
#     print(f"Index: {index}, Value: {value.text}")

"Lay tat ca cac the li trong thr ul[21]"
tags_li = tags_ul[21].find_elements(By.TAG_NAME, "li")

links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href")for tag in tags_li]
# for link in links:
    # print(link)

url2 = driver.get(links[0])
time.sleep(5)
# print(driver.get(links[0]))
"Tim tat ca the ul"
tags_ul = driver.find_elements(By.TAG_NAME, "ul")

"Tim the ul tuong ung"
# for index, value in enumerate(tags_ul):
#     print(f"Index: {index}, Value: {value.text}")

"Lay tat ca the li trong the ul[24]"
tags_li = tags_ul[24].find_elements(By.TAG_NAME, "li")

"Trong the li lay the a "
"Vi the a co chua Atribute href va title"
links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href")for tag in tags_li]
titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title")for tag in tags_li]

for link in links:
    # print(link)0
    driver.get(link)

    "Lay ten"
    try:
        # Name_element = driver.find_element(By.XPATH, "//h1[span[text()]]")
        Name_element = driver.find_element(By.XPATH, "//h1[@id='firstHeading']//span[@class='mw-page-title-main']")
        Name = Name_element.text
    except:
        ""

    "Lay ngay hoat dong"
    try:
        Year_active_element = driver.find_element(By.XPATH,
                                                  """//th[span[contains(text(), 'Years active')]]/following-sibling::td""")
        # Year_active_element = driver.find_element(By.XPATH, "//td[contains(text(), '1965–1969, 1973, 1984, 2015')]")
        YearActive = Year_active_element.text
    except:
        ""
    them(Name, YearActive)

    "Tao dictionary thong tin nhac si"

    # musician_dict = {"Name": Name, "Year active": YearActive}
    # musician_df = pd.DataFrame([musician_dict])
    # print(musician_df)

    "Them thong tin vao dataframe"
    # d = pd.concat([d, musician_df], ignore_index=True)
# print(d)

# # determining the name of the file
# file_name = 'Musicians.xlsx'

# # saving the Excel
# d.to_excel(file_name)
# print('DataFrame is written to Excel File successfully.')

time.sleep(4)
driver.quit()
