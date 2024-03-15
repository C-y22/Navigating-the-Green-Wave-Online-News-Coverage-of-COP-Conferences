import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from hashlib import md5
import json
import time
from selenium import webdriver
import retry


# Create a Chrome browser instance
options = webdriver.ChromeOptions()

# Add header information
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
    # Create md5 object
    new_md5 = md5()
    # Here one must use the encode() function to encode the string, otherwise an error will be reported. TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(str_josn.encode(encoding='utf-8'))
    # encryption
    return new_md5.hexdigest() 


def get_cnn(keywords):
    """获取cnn数据"""

    # save data
    data = []
    # id deduplication
    id_set = set()
    for keyword in keywords:
        print(">>>>>>>>>>", keyword)
        index = 1
        year = 2023  #start year
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

            #retrieve data
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
                            "keyword":keyword,              #keywords    
                            "url":item["url"],              #link
                            "from" : 'cnn',
                            "headline": item["headline"],   #title
                            "body": item["body"],           #content
                            "body_word_count" : len(item["body"].split()),   #The number of words the content contains
                            "date" : item["lastPublishDate"][:10]                   #Publication date
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
