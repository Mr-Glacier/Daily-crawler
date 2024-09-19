# This is a daily python practice project

## project 1 : _Crawler Tobacco Market_

1. Use of Package  
   use BeautifulSoup , requests , sqlite3  
   Install using pip command :

        pip install beautifulsoup4  
        pip install requests
        pip install sqlite3

2. Knowledge point record
    1. How to use beautifulsoup  
       example :  
       ```
       <div class="proBars">
            <div class="proBar proBarB proBar2">
                <div><span>产品类型：</span>烤烟型</div>
                <div><span>焦油量：</span>10mg</div>
            </div>
            <div class="proBar proBar2">
                <div><span>烟碱量：</span>1.0mg</div>
                <div><span>一氧化碳量：</span>12mg</div>
            </div>
       </div> 
       ```
       在上述的 html 中，可以提取出两个 div 标签, class="proBar proBarB proBar2" 和 class="proBar proBar2"  
       **踩坑+1** :  
             提取第一个 div 标签的时候, soup.select('div.proBar.proBarB.proBar2')    
             提取第二个 div 标签的时候, soup.select('div.proBar.proBar2')   
             然后发现 , 提取的竟然还是 第一个 div 标签 的内容
             换一种方式  
             提取第一个 div 标签的时候, soup.find('div‘,class_=‘proBar proBarB proBar2')    
             提取第二个 div 标签的时候, soup.find('div‘,class_=‘proBar proBar2')  
             还是不可以提取到第二个 div 标签  
             恼火😫!  
             soup.select_one('.proBar:not(.proBarB)')  
             就这样给排除出去了 proBarB ,效果达到了;
    2. How to use requests  
        点击这里学习 requests 的用法 [requests](https://requests.readthedocs.io/projects/cn/zh-cn/latest/index.html "Request DOCS").
    3. How to use sqlite3  
        1. What is sqlite3 ?  
            sqlite3是一个进程内的库，实现了自给自足、无服务器、零配置、事务性的SQL数据库引擎。它是一个增长最快的数据库引擎。它不是一个独立的进程，可以按应用程序需求进行静态或动态连接，SQLite直接访问其存储文件。
        2. how to use sqlite3 ?  
           其实跟 Mysql 以及 SqlSever 一样，除了这个没 truncate 语句 ,其他个人感觉差不多 (抛开效率以及性能)
           sqlite3 的数据类型 有：
           ```
           sql
           CREATE TABLE products (
           id INTEGER PRIMARY KEY AUTOINCREMENT, -- 整数主键 ,设置自增  
           name TEXT NOT NULL,		      -- 文本字段
           price REAL NOT NULL,		      -- 浮点型
           description BLOB,		      -- 存储二进制数据，即没有特定解释的字节序列
           );
           ```
    
