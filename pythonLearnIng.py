import datetime
import random
import time

import requests
from bs4 import BeautifulSoup
import sqlite3
import xkTools

# sqlite connect config
dataBasePath = '/Users/renyongkang/MyPath/SQLData/myTest.db'


# create brand table
def create_brand_table():
    conn = sqlite3.connect(dataBasePath)
    curs = conn.cursor()
    curs.execute('''Create table if not exists tobacco_brand (
    id int primary kry,
    brand_type TEXT,
    brand_name TEXT,
    brand_url TEXT,
    down_state TEXT,
    down_time TEXT 
    )
    ''')
    curs.close()
    conn.close()


# insert into brand table
def insert_brand_table(brand_beans, batch_size):
    sql_insert_brand = """
        INSERT INTO tobacco_brand (brand_type, brand_name, brand_url,down_state,down_time)
        VALUES (?, ?, ?, ?, ?);
        """
    try:
        # 分批插入数据
        for i in range(0, len(brand_beans), batch_size):
            conn = sqlite3.connect(dataBasePath)
            curs = conn.cursor()
            now = datetime.datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            batch = brand_beans[i:i + batch_size]
            curs.executemany(sql_insert_brand,
                             [(b['brand_style'], b['brand_name'], b['brand_url'], 'NO', formatted_now) for b in batch])
            conn.commit()
            curs.close()
            conn.close()
            print(f'bath{i}----->OK')
        print(f"All {len(brand_beans)} brands inserted successfully.")
    except Exception as e:
        print(e)


# select all brand to down
def select_brand_table():
    try:
        conn = sqlite3.connect(dataBasePath)
        curs = conn.cursor()
        sqlStr = ''' select * from tobacco_brand where down_state = 'NO' '''
        curs.execute(sqlStr)
        all_brands = curs.fetchall()
        curs.close()
        conn.close()
        return all_brands
    except Exception as e:
        print(f'{e}')


def update_brand_table(id):
    try:
        conn = sqlite3.connect(dataBasePath)
        curs = conn.cursor()
        sql_str = '''update tobacco_brand set down_state = 'YES' where id =  ? '''
        curs.execute(sql_str, (id,))
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        print(f'{e}')


# request headers
header = {
    "Content-Type": "application/json",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Host": "www.etmoc.com"
}


# this is request html method
def getHtml(url):
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        random_int = random.randint(1, 6)
        time.sleep(random_int)
        return response.text
    else:
        print(f"Error{response.status_code}")


allBrandUrl = 'http://www.etmoc.com/Firms/BrandAll'


# 解析全部品牌
def AnalysisAllBrandHtml(soup_html):
    list_brand_bean_list = []
    # create beautifulSoup example
    soup = BeautifulSoup(soup_html, 'html.parser')
    # select all container
    paragraphs = soup.select("div.container")
    # only chose my need tab-bar
    tab_bars = paragraphs[2].select("div.tab-bar")
    # to remember brand style names
    tab_list_name = []
    for tab in tab_bars:
        txt = tab.text
        tab_list_name.append(txt)
    # this is all brand details
    tab_bars_list_brands = paragraphs[2].select("ul.list-inline.detail")
    i = 0
    for tab_bars_list_brand in tab_bars_list_brands:
        brand_style = tab_list_name[i]
        i = i + 1
        print(brand_style)
        brand_list = tab_bars_list_brand.select("li")
        for brand in brand_list:
            # http://www.etmoc.com/Firms/BrandShow?Id=15
            brand_name = brand.select("a")[0].text
            brand_url = 'http://www.etmoc.com/Firms/' + brand.select("a")[0]['href']
            brand_bean = {'brand_name': brand_name,
                          'brand_url': brand_url,
                          'brand_style': brand_style}
            list_brand_bean_list.append(brand_bean)

    return list_brand_bean_list


def downFirstBrandPage(save_path):
    allBrands = select_brand_table()
    for allBrand in allBrands:
        url = allBrand[3]
        print(f'{url}')
        source_id = allBrand[2]
        html = getHtml(url)
        xkTools.writeFile(save_path, source_id + '.txt', html)
        update_brand_table(allBrand[0])


def analysisFirstBrandPage(savePath):
    fileNames = xkTools.getFolderFileNames(savePath)
    for fileName in fileNames:
        html = xkTools.readFile(savePath, fileName)



mainSavePath = '/Users/renyongkang/MyPath/ZKZD2023_Data/tobacco/'

if __name__ == '__main__':
    # step1 : down and analysis all brand
    # html = getHtml(allBrandUrl)
    # brand_bean_list = AnalysisAllBrandHtml(html)
    # print(f'{len(brand_bean_list)}')
    # insert_brand_table(brand_bean_list, 50)

    # step 2 : down first brand page
    first_page_path = '/tobacco_brand_first_page/'
    downFirstBrandPage(mainSavePath + first_page_path)

    # step 3 : analysis first brand page

