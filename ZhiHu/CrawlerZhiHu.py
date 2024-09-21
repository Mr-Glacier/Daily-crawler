import json
import random
import time
import requests
import ZhiHu_x93_jiemi
import xkTools
import ZhiHuDao


def request_get_data(main_url, header):
    try:
        # print(f'Requesting {main_url}')
        response = requests.get(main_url, headers=header)
        random_int = random.randint(5, 10)
        time.sleep(random_int)
        print(f'{response.status_code}')
        return response.json()
    except Exception as e:
        print(e)


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


def analysis_all_domains_nearly_today(content_json, save_path):
    time_str = time.strftime("%Y%m%d%H%M", time.localtime())
    xkTools.writeFile(save_path, 'domains_' + time_str + '.txt', str(content_json))
    bean_list = []
    domains = content_json['domains'][0]['items']
    for item in domains:
        bean_domain = {
            'source_id': item['id'],
            'name': item['name']
        }
        bean_list.append(bean_domain)
    ZhiHuDao.insert_zhihu_domains(bean_list)
    print('All Domains Downloaded and Insert to DB  !')


def while_domains_to_down_questions(save_path, d_c0_x):
    domains = ZhiHuDao.select_zhihu_domains()
    for item in domains:
        source_id = item[2]
        name = item[1].replace('/', '')
        get_all_week_hot_questions(week_hot_main_url, save_path, d_c0_x, source_id, name)
        time.sleep(random.randint(2, 6))
        print(f'Download {name}  Questions OK!')
        ZhiHuDao.update_zhihu_domains(item[0])


def get_all_week_hot_questions(main_url, save_path, d_c0_x, domain_id, name):
    remember_count = 0
    while True:
        try:
            deal_url = main_url + 'creators/rank/hot?domain=' + str(domain_id) + '&limit=20&offset=' + str(
                remember_count) + '&period=week'
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
                'x-zse-96': x96,
                'x-zse-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZfTY0-4Lm'
                            '-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_'
                            'R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPF_gmuwVftcxqIuwsz9SBGMp9aDr1-'
                            'vNxLUcL8UYO6bp9WqXYauc8-wtYnhoTv721wwSfBJxLLhpCwwN8Igt1YMtMQQ9LDBwKr0cGBiCqjU3GhBCsIDCC_'
                            'q3f9ccCJePsZhw18hwO66oMTgwBJ0OysweYUGN9o7VssutBxwNfsvN_'
                            '8GSxVqfzBcOy6RxKr6XVHvXfsHc_Hgpq_gL8_'
                            'hc_b9g8tBXGhvX_Wwx0MvXB6wxOiqw8eBYMfMN18GxqTwH8hDL8HqFG-bXYkHo8AhgBTgVKeqxqrXgOCwLLGwYC'
            }
            json_data = request_get_data(deal_url, user_header)
            json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
            xkTools.writeFile(save_path, name + '_' + str(remember_count) + '.txt', json_str)
            print(f'down ok --->' + str(remember_count))
            if json_data['paging']['is_end']:
                print('All Data Downloaded !')
                break
            else:
                remember_count += 20
        except Exception as e:
            print(e)


def analysis_all_week_hot_questions(save_path):
    bean_list = []
    for file_name in xkTools.getFolderFileNames(save_path):
        print(file_name)
        source_stype = file_name.split('_')[0]
        file_content = json.loads(xkTools.readFile(save_path, file_name))
        for item_a in file_content['data']:
            item = item_a['question']
            item2 = item_a['reaction']
            bean_list.append({
                'source_stype': source_stype,
                'question_url': item['url'],
                'question_created': item['created'],
                'question_updated_time': item['updated_time'],
                'question_title': item['title'],
                'question_highlight_title': item['highlight_title'],
                'question_type': item['type'],
                'question_id': item['id'],
                'question_token': item['token'],
                'question_is_recent_hot': item['is_recent_hot'],
                'question_have_answer': item['have_answer'],
                'question_question_answer_url': item['question_answer_url'],
                'question_topics': str(item['topics']),
                'question_label': item['label'],
                'reaction_new_pv': item2['new_pv'],
                'reaction_new_pv_7_days': item2['new_pv_7_days'],
                'reaction_new_follow_num': item2['new_follow_num'],
                'reaction_new_follow_num_7_days': item2['new_follow_num_7_days'],
                'reaction_new_answer_num': item2['new_answer_num'],
                'reaction_new_answer_num_7_days': item2['new_answer_num_7_days'],
                'reaction_new_upvote_num': item2['new_upvote_num'],
                'reaction_new_upvote_num_7_days': item2['new_upvote_num_7_days'],
                'reaction_pv': item2['pv'],
                'reaction_follow_num': item2['follow_num'],
                'reaction_answer_num': item2['answer_num'],
                'reaction_upvote_num': item2['upvote_num'],
                'reaction_pv_incr_rate': item2['pv_incr_rate'],
                'reaction_head_percent': item2['head_percent'],
                'reaction_new_pv_yesterday': item2['new_pv_yesterday'],
                'reaction_new_pv_t_yesterday': item2['new_pv_t_yesterday'],
                'reaction_score': item2['score'],
                'reaction_score_level': item2['score_level'],
                'reaction_text': item2['text']
            })
    ZhiHuDao.insert_zhihu_questions(bean_list, 50)


def download_all_week_hot_questions_details(save_path, d_c0_x):
    for item in ZhiHuDao.select_zhihu_questions():
        question_token = item[9]
        print(f'Begin Down {item[0]}--> ')
        page = 1
        deal_url = 'https://www.zhihu.com/api/v4/questions/'+question_token+'/feeds?cursor=bd4645fbc296babaa2060fc3697eca50&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1726918884060360112&ws_qiangzhisafe=1'
        while True:
            try:
                x96_ = ZhiHu_x93_jiemi.ZhiHuEncrypt.get_96(deal_url, d_c0_x)
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
                    'referer': 'https://www.zhihu.com/question/'+question_token,
                    'x-requested-with': 'fetch',
                    'x-zse-93': '101_3_3.0',
                    'x-zse-96': x96_,
                    'Cookie': 'zap=1a883145-8b31-4fe5-865e-eb9007da8afa; d_c0=AXATIYtD0xePTguFBb0MMATntNCvME-TNOQ=|1702094667; __snaker__id=GA9yMB4gKwShCZrV; YD00517437729195%3AWM_NI=yMR7YtGk3kFZPeXEr8TorkirBOiPp35hM%2F%2FxMpDsx20xvsa9odAcmZKIPcHRY8QV98nF%2BBNmHozQpsF6SLfth8Zk6R0s9IS417yNpC4hg%2BQAocSfHGlXhSiEpuXHFcesemk%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee87b53a93ad83a6bb5fa6b08aa2d54a829e9aacc4348598a49bb57a8288af85d22af0fea7c3b92abb939ed8dc8085b5fd8cc55294bb98a6f13498b1be8cec7a8291a7b1f339f7b883d0ae748fb08c94fb3af4a8ba94e433adbc8f84f0528997a084cb5a9be89fb7bc34ae9ae5a3cd678cb1b6b2f37986ea9dade580ace8968cb55af4adf7aad240f3e9b7aff349f8b8a9ccd44badbd9d87cb4db088a8b4ec4fb4ab98a9c569a7adab8eea37e2a3; YD00517437729195%3AWM_TID=PaGMt2nlBIhEQRVBAUaEtCC1juqVTKdS; q_c1=d04f3efd7de44fb48dba018dc5d8694b|1702094700000|1702094700000; _xsrf=VpF9PI1a9FhUGVTRUNPBIp20HFYweYz8; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1726915645; HMACCOUNT=6B501506DC83CCBE; z_c0=2|1:0|10:1726915647|4:z_c0|80:MS4xSWdQYkNRQUFBQUFtQUFBQVlBSlZUVF95MjJkRGhUZWhxZUhIblNLb2FNd2pPTk5HYzI1Y1B3PT0=|3aabcebd1cfd8e61f0b417dd43cc981c38b883e46aa6a82ec6494be2cfe1a765; __zse_ck=003_bvVAbrbJkoR=6Fj3yZkJJZkNS3BWcPDcT3Kv5sdvpdeLpAFjay=33uuFdQj5a/MwiqpcPc0R6WNVbNemcQLIy6ij1a7F7jsonXvNrr8pnz6U; tst=r; SUBMIT_0=e9fd0054-a0c4-433d-aa58-792efcb85d39; SESSIONID=94bCvxTUhP5nv4LEWYTSe6n0cF3FIEcspB9oP1gBAvY; JOID=VVoSCkvX4z1BW-7ac9mxay7Xowtk69JRCyqTiyi4tg0hJN2TMxBY1ClZ7tF0IwE2BZq3rnCqAkGcB1gGUs-rX8c=; osd=Vl8RAkjU5j5JWO3fcNGyaCvUqwhn7tFZCCmWiCC7tQgiLN6QNhNQ1ypc7dl3IAQ1DZm0q3OiAUKZBFAFUcqoV8Q=; BEC=1a391e0da683f9b1171c7ee6de8581cb; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1726918885'
                }
                data_json = request_get_data(deal_url, user_header)
                json_str = json.dumps(data_json, ensure_ascii=False, indent=4)
                xkTools.writeFile(save_path, question_token + '_' + str(page) + '.txt', json_str)
                print(data_json['paging']['is_end'])
                if data_json['paging']['is_end'] and page > 1 :
                    ZhiHuDao.update_zhihu_questions(item[0])
                    print(f'{question_token} IS DOWNLOADED OK !')
                    break
                else:
                    deal_url = data_json['paging']['next']
                    page = page + 1
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print(f'ZHIHU Crawler Started !')
    domain_nearly_today_main_url = 'https://www.zhihu.com/api/v4/creators/domain'
    d_c0 = 'AXATIYtD0xePTguFBb0MMATntNCvME-TNOQ=|1702094667'
    main_save_path = '/Users/renyongkang/MyPath/ZKZD2023_Data/zhihu/'

    domains_savePath = main_save_path + '/domains/'
    xkTools.createFolder(domains_savePath)
    # step 1 : get all domains nearly today

    # content_json_domain = get_all_domains_nearly_today(domain_nearly_today_main_url, d_c0)
    # analysis_all_domains_nearly_today(content_json_domain, domains_savePath)

    # step 2 : down all week hot questions for each domain
    week_hot_question_save_path = main_save_path + '/week_hot_question/'
    week_hot_main_url = 'https://www.zhihu.com/api/v4/'
    # while_domains_to_down_questions(week_hot_question_save_path, d_c0)
    # analysis_all_week_hot_questions(week_hot_question_save_path)

    # step 3 : down all week hot questions details
    save_path_questinions_details = main_save_path + '/week_hot_question_details/'
    xkTools.createFolder(save_path_questinions_details)
    download_all_week_hot_questions_details(save_path_questinions_details, d_c0)
