"""
这个方法主要 是用于数据持久化
对zhihu_数据进行存储 
@version 1.0  sqlite_3
"""
import sqlite3
import os
import time
import json
from contextlib import closing

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql

# DB-Config
db_config = {
    'host': '---',
    'port': 3306,
    'user': 'root',
    'password': '-----',
    'database': 'zhihu_2024',
    'charset': 'utf8mb4'
}


def create_connection_db():
    return pymysql.connect(host=db_config['host'],
                           user=db_config['user'],
                           password=db_config['password'],
                           database=db_config['database'],
                           charset=db_config['charset'],
                           port=db_config['port'])


def crate_table_zhihu_domains() -> None:
    try:
        conn = create_connection_db()
        cursor = conn.cursor()
        zhihu_domains_table_str = """
        CREATE TABLE IF NOT EXISTS zhihu_domains(
            id INT AUTO_INCREMENT PRIMARY KEY,
            domain_name varchar(200),
            domain_source_id varchar(200),
            down_state varchar(200),
            down_time varchar(200)
        )
        """
        cursor.execute(zhihu_domains_table_str)
        conn.commit()
        conn.close()
        print('create zhihu_domains table success')
    except Exception as e:
        print(e)


def insert_zhihu_domains(bean_list) -> None:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                insert_sql = """
                       INSERT INTO zhihu_domains(domain_name, domain_source_id, down_state, down_time)
                       VALUES(%s, %s, %s, %s)
                       """
                down_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # 收集所有需要插入的数据
                data_to_insert = [(bean['name'], bean['source_id'], 'NO', down_time) for bean in
                                  bean_list]
                # 批量插入数据
                cursor.executemany(insert_sql, data_to_insert)
                # 提交事务
                conn.commit()
    except Exception as e:
        print(e)


def select_zhihu_domains() -> list:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                select_sql = """
                SELECT * FROM zhihu_domains where down_state = 'NO'
                """
                cursor.execute(select_sql)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(e)


def update_zhihu_domains(id) -> None:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                update_sql = """
                UPDATE zhihu_domains SET down_state = 'YES' WHERE id = %s
                """
                cursor.execute(update_sql, (id,))
                conn.commit()
                print('update zhihu_domains success')
    except Exception as e:
        print(e)


def create_table_zhihu_questions() -> None:
    try:
        conn = create_connection_db()
        cursor = conn.cursor()
        questions_sql_str = """
        create table zhihu_week_hot_questions(
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            question_url varchar(255), 
            question_created varchar(255), 
            question_updated_time varchar(255), 
            question_title varchar(500), 
            question_highlight_title varchar(255), 
            question_type varchar(255), 
            question_id varchar(255), 
            question_token varchar(255), 
            question_is_recent_hot varchar(255), 
            question_have_answer varchar(255), 
            question_question_answer_url varchar(255), 
            question_topics varchar(500), 
            question_label varchar(255), 
            reaction_new_pv varchar(255), 
            reaction_new_pv_7_days varchar(255), 
            reaction_new_follow_num varchar(255), 
            reaction_new_follow_num_7_days varchar(255), 
            reaction_new_answer_num varchar(255), 
            reaction_new_answer_num_7_days varchar(255), 
            reaction_new_upvote_num varchar(255), 
            reaction_new_upvote_num_7_days varchar(255), 
            reaction_pv varchar(255), 
            reaction_follow_num varchar(255), 
            reaction_answer_num varchar(255), 
            reaction_upvote_num varchar(255), 
            reaction_pv_incr_rate varchar(255), 
            reaction_head_percent varchar(255), 
            reaction_new_pv_yesterday varchar(255), 
            reaction_new_pv_t_yesterday varchar(255), 
            reaction_score varchar(255), 
            reaction_score_level varchar(255), 
            reaction_text varchar(255)
            )
        """
        cursor.execute(questions_sql_str)
        cursor.close()
        conn.commit()
        conn.close()
        print('create zhihu_week_hot_questions table success')
    except Exception as e:
        print(e)


def insert_zhihu_questions(bean_list, batch_size) -> None:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                insert_sql = """
                INSERT INTO zhihu_week_hot_questions(source_stype,question_url,question_created,question_updated_time,question_title,
                question_highlight_title,question_type,question_id,question_token,question_is_recent_hot,
                question_have_answer,question_question_answer_url,question_topics,question_label,reaction_new_pv,
                reaction_new_pv_7_days,reaction_new_follow_num,reaction_new_follow_num_7_days,reaction_new_answer_num,
                reaction_new_answer_num_7_days,reaction_new_upvote_num,reaction_new_upvote_num_7_days,reaction_pv,
                reaction_follow_num,reaction_answer_num,reaction_upvote_num,reaction_pv_incr_rate,reaction_head_percent,
                reaction_new_pv_yesterday,reaction_new_pv_t_yesterday,reaction_score,reaction_score_level,reaction_text)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s,
                 %s, %s, %s, %s, %s, %s, %s)
                """
                for i in range(0, len(bean_list), batch_size):
                    batch = bean_list[i:i + batch_size]
                    cursor.executemany(insert_sql,
                                       [(b['source_stype'], b['question_url'], b['question_created'],
                                         b['question_updated_time'],
                                         b['question_title'], b['question_highlight_title'], b['question_type'],
                                         b['question_id'], b['question_token'], b['question_is_recent_hot'],
                                         b['question_have_answer'], b['question_question_answer_url'],
                                         b['question_topics'], b['question_label'], b['reaction_new_pv'],
                                         b['reaction_new_pv_7_days'], b['reaction_new_follow_num'],
                                         b['reaction_new_follow_num_7_days'], b['reaction_new_answer_num'],
                                         b['reaction_new_answer_num_7_days'], b['reaction_new_upvote_num'],
                                         b['reaction_new_upvote_num_7_days'], b['reaction_pv'],
                                         b['reaction_follow_num'], b['reaction_answer_num'], b['reaction_upvote_num'],
                                         b['reaction_pv_incr_rate'], b['reaction_head_percent'],
                                         b['reaction_new_pv_yesterday'], b['reaction_new_pv_t_yesterday'],
                                         b['reaction_score'], b['reaction_score_level'], b['reaction_text'])
                                        for b in batch])
                    conn.commit()
    except Exception as e:
        print(e.args)
        print(e)


def select_zhihu_questions() -> list:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                select_sql = """
                select * from zhihu_week_hot_questions where down_state = 'NO'
                """
                cursor.execute(select_sql)
                return cursor.fetchall()
    except Exception as e:
        print(e)


def update_zhihu_questions(id) -> None:
    try:
        with closing(create_connection_db()) as conn:
            with conn.cursor() as cursor:
                update_sql = """
                update zhihu_week_hot_questions set down_state = 'YES' where id = %s
                """
                cursor.execute(update_sql, (id,))
                conn.commit()
    except Exception as e:
        print(e)




if __name__ == '__main__':
    crate_table_zhihu_domains()
