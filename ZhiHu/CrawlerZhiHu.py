import random
import time
import requests
import ZhiHu_x93_jiemi
import xkTools


def request_get_data(main_url, header):
    try:
        print(f'Requesting {main_url}')
        response = requests.get(main_url, headers=header)
        random_int = random.randint(1, 20)
        time.sleep(random_int)
        return response.json()
    except Exception as e:
        print(e)


def get_all_week_hot_questions(main_url):
    user_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': '',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }


def get_all_domains_nearly_today(main_url, d_c0_x):
    x96 = ZhiHu_x93_jiemi.ZhiHuEncrypt.get_96(main_url, d_c0_x)
    user_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'referer': 'https://www.zhihu.com/creator/hot-question/hot/0/week',
        'x-requested-with': 'fetch',
        'x-zse-93': '101_3_3.0',
        'x-zse-96': x96
    }
    return request_get_data(main_url, user_header)


def get_all_week_hot_questions(main_url, save_path, d_c0_x):
    remember_count = 0
    while True:
        try:
            deal_url = main_url + 'creators/rank/hot?domain=0&limit=20&offset=' + str(remember_count) + '&period=week'
            x96 = ZhiHu_x93_jiemi.ZhiHuEncrypt.get_96(deal_url, d_c0_x)
            user_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/92.0.4515.159 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'referer': 'https://www.zhihu.com/creator/hot-question/hot/0/week',
                'x-requested-with': 'fetch',
                'x-zse-93': '101_3_3.0',
                'x-zse-96': x96
            }
            json_data = request_get_data(deal_url, user_header)
            xkTools.writeFile(save_path, str(remember_count) + '.txt', str(json_data))
            print(f'down ok --->'+str(remember_count))
            if json_data['paging']['is_end']:
                print('All Data Downloaded !')
                break
            else:
                remember_count += 20
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print(f'ZHIHU Crawler Started !')
    # step 1 : get all domains nearly today
    domain_nearly_today_main_url = 'https://www.zhihu.com/api/v4/creators/domain'
    d_c0 = 'AOBeu6OaqRiPToK4fl5bRaLX-IFmM-80Rnw=|1716478796'
    # content_json_domain = get_all_domains_nearly_today(domain_nearly_today_main_url, d_c0)

    main_save_path = '/Users/renyongkang/MyPath/ZKZD2023_Data/zhihu/'

    week_hot_question_save_path = main_save_path + '/week_hot_question/'
    week_hot_main_url = 'https://www.zhihu.com/api/v4/'
    get_all_week_hot_questions(week_hot_main_url, week_hot_question_save_path, d_c0)
