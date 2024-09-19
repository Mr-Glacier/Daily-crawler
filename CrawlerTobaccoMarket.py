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
        INSERT INTO tobacco_brand (source_id,brand_type, brand_name, brand_url,down_state,down_time)
        VALUES (?, ?, ?, ?, ?, ?);
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
                             [(b['source_id'], b['brand_style'], b['brand_name'], b['brand_url'], 'NO', formatted_now)
                              for b in batch])
            conn.commit()
            curs.close()
            conn.close()
            print(f'bath{i}----->OK')
        print(f"All {len(brand_beans)} brands inserted successfully.")
    except Exception as e:
        print(e)


def insert_tobacco_brand_details(brand_beans, batch_size):
    sql_insert_brand_details = """INSERT INTO tobacco_brand_details (source_id,brand_title, brand_pinyin, 
    brand_introduce, brand_image_url,page_number,down_state,down_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
    try:
        # 分批插入数据
        for i in range(0, len(brand_beans), batch_size):
            conn = sqlite3.connect(dataBasePath)
            curs = conn.cursor()
            now = datetime.datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            batch = brand_beans[i:i + batch_size]
            curs.executemany(sql_insert_brand_details,
                             [(b['source_id'], b['brand_title'], b['brand_english'], b['brand_introduce'],
                               b['brand_image_url'], b['page_number'], 'NO', formatted_now)
                              for b in batch])
            conn.commit()
            curs.close()
            conn.close()
            print(f'bath{i}----->OK')
        print(f"All {len(brand_beans)} brands_details inserted successfully.")
    except Exception as e:
        print(e)


def select_tobacco_brand_details():
    try:
        conn = sqlite3.connect(dataBasePath)
        curs = conn.cursor()
        sqlStr = ''' select * from tobacco_brand_details where down_state = 'NO' '''
        curs.execute(sqlStr)
        all_brands_details = curs.fetchall()
        curs.close()
        conn.close()
        return all_brands_details
    except Exception as e:
        print(f'{e}')


def update_brand_table_details(id):
    try:
        conn = sqlite3.connect(dataBasePath)
        curs = conn.cursor()
        sql_str = '''update tobacco_brand_details set down_state = 'YES' where id =  ? '''
        curs.execute(sql_str, (id,))
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        print(f'{e}')


def insert_specifications_table(bean_list, bach_size):
    sql_insert_specifications = """INSERT INTO tobacco_specifications (brand_source_id,specifications_source_id, 
    specifications_name, specifications_url, specifications_pic_url,specifications_norm,specifications_xh_number, 
    specifications_th_number,specifications_price,down_state,down_time) VALUES (?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?);"""
    try:
        # 分批插入数据
        for i in range(0, len(bean_list), bach_size):
            conn = sqlite3.connect(dataBasePath)
            curs = conn.cursor()
            now = datetime.datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            batch = bean_list[i:i + bach_size]
            curs.executemany(sql_insert_specifications,
                             [(b['brand_source_id'], b['specifications_source_id'], b['specifications_name'],
                               b['specifications_url'], b['specifications_pic_url'], b['specifications_norm'],
                               b['specifications_xh_number'], b['specifications_th_number'], b['specifications_price'],
                               'NO', formatted_now)
                              for b in batch])
            conn.commit()
            curs.close()
            conn.close()
            print(f'bath{i}----->OK')
        print(f"All {len(bean_list)} specifications inserted successfully.")
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
                          'brand_style': brand_style,
                          'source_id': brand_url.replace('http://www.etmoc.com/Firms/BrandShow?Id=', '')}
            list_brand_bean_list.append(brand_bean)

    return list_brand_bean_list


def downFirstBrandPage(save_path):
    allBrands = select_brand_table()
    for allBrand in allBrands:
        url = allBrand[4]
        print(f'{url}')
        source_id = allBrand[1]
        html = getHtml(url)
        xkTools.writeFile(save_path, source_id + '.txt', html)
        update_brand_table(allBrand[0])


def analysisFirstBrandPage(save_path):
    fileNames = xkTools.getFolderFileNames(save_path)
    bean_list = []
    for fileName in fileNames:
        print(fileName)
        html = xkTools.readFile(save_path, fileName)
        soup = BeautifulSoup(html, 'html.parser')
        brand_title = soup.select('div.brand-title')[0].text
        brand_title_small = soup.select('div.brand-title')[0].select('small')[0].text
        deal_band_title = brand_title.replace(brand_title_small, '')
        # Handling special escape characters
        brand_introduce = (soup.select('div.detail.brand-detail')[0].text.replace(' ', '')
                           .replace('\n', '').replace('\t', '').replace('\r', ''))
        #  http://www.etmoc.com/Firm/brandpic/20150813235228.png
        brand_image_url = 'http://www.etmoc.com' + soup.select('p.brandImg.detailshad')[0].select('img')[0]['src']
        page_content = soup.select('ul.pagination')[0].select('li')
        if len(page_content) != 0:
            print('------>' + page_content[len(page_content) - 2].select('a')[0].text)
            pageNumber = int(page_content[len(page_content) - 2].select('a')[0].text.replace('...', ''))
            print(pageNumber)
        else:
            pageNumber = 1
        bean_brand_detail = {'brand_title': deal_band_title.replace('\n', '').replace('\t', '').replace('\r', ''),
                             'brand_english': brand_title_small.replace('\n', '').replace('\t', '').replace('\r', ''),
                             'brand_introduce': brand_introduce,
                             'brand_image_url': brand_image_url,
                             'page_number': pageNumber,
                             'source_id': fileName.replace('.txt', '')
                             }
        bean_list.append(bean_brand_detail)
    return bean_list


def downBrandDetailsPage(save_path):
    all_brand_details = select_tobacco_brand_details()
    for all_brand_detail in all_brand_details:
        page_number = all_brand_detail[6]
        source_id = all_brand_detail[1]
        if page_number == 1:
            url = 'http://www.etmoc.com/Firms/BrandShow?Id=' + source_id
            html = getHtml(url)
            xkTools.writeFile(save_path, source_id + '_1.txt', html)
            update_brand_table_details(all_brand_detail[0])
        else:
            for i in range(1, page_number + 1):
                # http://www.etmoc.com/Firms/BrandShow?page=2&Id=260
                url = 'http://www.etmoc.com/Firms/BrandShow?page=' + str(i) + '&Id=' + source_id
                print(f'{url}')
                html = getHtml(url)
                xkTools.writeFile(save_path, source_id + '_' + str(i) + '.txt', html)
            update_brand_table_details(all_brand_detail[0])
        print(f'OK---->{source_id}')


def analysisBrandDetailsPage(save_path):
    fileNames = xkTools.getFolderFileNames(save_path)
    bean_list = []
    for fileName in fileNames:
        print(fileName)
        html = xkTools.readFile(save_path, fileName)
        soup = BeautifulSoup(html, 'html.parser')
        specifications_area = soup.select('ul.detail.list-p')[0].select('li')
        for specifications in specifications_area:
            specifications_url = 'http://www.etmoc.com/Firms/' + specifications.select('a')[0]['href']
            specifications_pic_url = 'http://www.etmoc.com' + specifications.select('img')[0]['src']
            specifications_name = specifications.select('img')[0]['alt']
            specifications_norm = specifications.select('div.li-p-t')[0].select('p')[0].text
            number_list = specifications.select('div.li-p-b')[0].select('p')
            specifications_th_number = ''
            specifications_xh_number = ''
            if len(number_list) > 1:
                specifications_xh_number = specifications.select('div.li-p-b')[0].select('p')[0].text
                specifications_th_number = specifications.select('div.li-p-b')[0].select('p')[1].text
            if len(number_list) == 1:
                specifications_xh_number = specifications.select('div.li-p-b')[0].select('p')[0].text
                specifications_th_number = ''
            specifications_price = specifications.select('div.li-p-p')[0].text
            specifications_source_id = specifications_url.replace('http://www.etmoc.com/Firms/Product?Id=', '')
            bean_brand_details = {
                'specifications_name': specifications_name.replace('\n', '').replace('\r', '').replace('\t', ''),
                'specifications_url': specifications_url,
                'specifications_pic_url': specifications_pic_url,
                'specifications_norm': specifications_norm.replace('                 ', '  ').replace('  ', '|')
                .replace('\n', '').replace('\r', '').replace('\t', ''),
                'specifications_xh_number': specifications_xh_number.replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                 ''),
                'specifications_th_number': specifications_th_number.replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                 ''),
                'specifications_price': specifications_price.replace('\n', '').replace('\r', '').replace('\t', ''),
                'brand_source_id': fileName.split('_')[0],
                'specifications_source_id': specifications_source_id
            }
            bean_list.append(bean_brand_details)
    return bean_list


if __name__ == '__main__':
    #  this is main savePath for all tobacco data
    mainSavePath = '/Users/renyongkang/MyPath/ZKZD2023_Data/tobacco/'
    #  the first url
    allBrandUrl = 'http://www.etmoc.com/Firms/BrandAll'

    # step1 : down and analysis all brand
    # html = getHtml(allBrandUrl)
    # brand_bean_list = AnalysisAllBrandHtml(html)
    # print(f'{len(brand_bean_list)}')
    # insert_brand_table(brand_bean_list, 50)

    # step 2 : down first brand page
    first_page_path = '/tobacco_brand_first_page/'
    # downFirstBrandPage(mainSavePath + first_page_path)

    # step 3 : analysis first brand page
    # bean_list_brand_details = analysisFirstBrandPage(mainSavePath + first_page_path)
    # insert_tobacco_brand_details(bean_list_brand_details, 50)

    # step 4 : down tobacco brand details all pages
    tobacco_brand_details_path = '/tobacco_brand_details/'
    # downBrandDetailsPage(mainSavePath + tobacco_brand_details_path)
    bean_specifications = analysisBrandDetailsPage(mainSavePath + tobacco_brand_details_path)
    insert_specifications_table(bean_specifications, 50)
