import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from hashlib import md5
import json
import time
from selenium import webdriver
import retry


# 创建Chrome浏览器实例
options = webdriver.ChromeOptions()

# 添加header信息
options.add_argument("user-agent=Thunder Client (https://www.thunderclient.com)")
options.add_argument("Accept-Language=en-US")
options.add_argument('--headless')

def change_date(dateStr):
    input_format = '%a, %d %b %Y %H:%M:%S %z'
    output_format = '%Y-%m-%d'

    new_data = datetime.strptime( \
        dateStr, \
        input_format).strftime(output_format)

    return new_data


def encrypt_md5(str_josn):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(str_josn.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest() 


def get_cnn(keywords):
    """获取cnn数据"""

    # 保存数据
    data = []
    # id去重
    id_set = set()
    for keyword in keywords:
        print(">>>>>>>>>>", keyword)
        index = 1
        year = 2023  #开始年份
        pre_rst_md5= ""
        
        retry = 0
        while year>=2015 and retry <= 3: 
            try:
                
                url = f"https://search.api.cnn.com/content?q={keyword}&size=50&from={(index -1 )*10}&page={index}&sort=newest"
                res = requests.get(url)
                rst = res.json()['result']
                
                rst_json = json.dumps(rst)
                curr_rst_md5 = encrypt_md5(rst_json)
            except Exception as e:
                time.sleep(10)
                retry += 1
                continue

            #获取数据
            for item in rst:
                try:
                    id = item['_id']
                    if id in id_set:
                        continue
                    news_year = int(item["lastPublishDate"][:4])
                    if news_year > 2023:
                        continue
                    id_set.add(id)
                    data.append(
                        {
                            "keyword":keyword,              #关键词    
                            "url":item["url"],              #link
                            "from" : 'cnn',
                            "headline": item["headline"],   #title
                            "body": item["body"],           #内容
                            "body_word_count" : len(item["body"].split()),   #内容包含的单词数量
                            "date" : item["lastPublishDate"][:10]                   #发表日期
                        }

                    )
                    
                except Exception as e:
                    print(e)
            if curr_rst_md5 == pre_rst_md5:
                break
            pre_rst_md5 = curr_rst_md5

            if  news_year and news_year< year:
                year = news_year
            index += 1
            retry = 0
    
    print(len(data))
    return data
    

def main():
    pass

if __name__ == '__main__':
    keywords = ["climate change", "climate adaptation", "global warming", "greenhouse gases", "carbon emissions", "renewable energy", "sustainable development", "extreme weather", "sea level rise", "paris agreement", "climate policy"," climate science", "climate advocacy",
                 "environmental crisis", "biodiversity loss", "climate action", "environmental policy", "COP 15", "COP 26", "United Nations Framework Convention on Climate Change", "UNFCCC", "COP",
                 "Climate Change", "Climate Adaptation","Global Warming", "Greenhouse Gases", "Carbon Emissions", "Renewable Energy", "Sustainable Development", "Extreme Weather", "Sea Level Rise",
                 "Paris Agreement", "Climate Policy"," Climate Science", "Climate Advocacy", "Environmental Crisis", "Biodiversity Loss", "Climate Action", "Environmental Policy"
                ]

    data = []
    data.extend(get_cnn(keywords))
    df_cnn = pd.DataFrame(data)
    df_cnn.to_csv("news_cnn_1217.csv", index=False)
