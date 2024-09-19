"""
这个方法主要 是用于数据持久化
对zhihu_数据进行存储 
@version 1.0  sqlite_3
"""
import sqlite3
import os
import time
import json

global_data_path = ''


def crate_table_zhihu_domains() -> None:
    try:
        conn = sqlite3.connect(global_data_path)
        cursor = conn.cursor()
        zhihu_domians_table_str = """
        CREATE TABLE IF NOT EXISTS zhihu_domains(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_name TEXT,
            domain_url TEXT,
            domain_type TEXT,
            domain_desc TEXT,
            domain_state INTEGER,
            domain_create_time TEXT,
            domain_update_time TEXT
        )
        """
        cursor.execute(zhihu_domians_table_str)
        conn.commit()
        conn.close()
        print('create zhihu_domains table success')
    except Exception as e:
       print(e)
