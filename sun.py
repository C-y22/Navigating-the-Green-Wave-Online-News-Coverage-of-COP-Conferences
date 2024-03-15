import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from hashlib import md5
import json
import time

requests.DEFAULTT_RETRIES = 5
headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie" : '_pnvl_NxnLUb5i=false; pushly.user_puuid_NxnLUb5i=VkkdZKS0Gr2PBZbuRivoICOIdAsIEGL9; dnsDisplayed=undefined; ccpaApplies=false; signedLspa=undefined; nukt_sp_consent_global=NONE; _sp_su=false; ccpaUUID=9c209624-c59a-4de7-987a-7c6b3dfd68d6; nuPixelApp=j%3A%7B%22id%22%3A%2299ca5760-d52e-11ed-96d4-4d09a2f6594a%22%7D; rc_id1=01875b4064cb0022c697e865191c0506f001906700fb8; rc_id2=01875b4064cb0022c697e865191c0506f001906700fb8; _nuk_sp_id_=88bb45e2-1202-4af4-a6fc-369bb651ebef; _pnlspid_NxnLUb5i=13093; _ncg_id_=0a3d5ec2-4db6-4399-873b-65238bf7c5dd; _ncg_domain_id_=0a3d5ec2-4db6-4399-873b-65238bf7c5dd.1.1680863168.1743935168; login_event_fired=false; nukt_lv=1680870489130|||21031605|||i%20love%20picking%20up%20%E2%80%98magic%20bags%E2%80%99%20from%20shops%20and%20waitrose%20is%20the%20best%20-%20i%20paid%20%C2%A35%20for%20one%20that%E2%80%99d%20feed%20a%20family%20for%20a%20week; _pnss_NxnLUb5i=blocked; _ga_K2ECMCJBFQ=GS1.1.1680870487.2.1.1680870683.0.0.0; _ga_SQ24F7Q7YW=GS1.1.1680870487.2.1.1680870683.0.0.0; _ncg_g_id_=69fab7a0-c8cf-4b28-a3c5-18a0600c0b10.3.1680863173.1743935341; _gid=GA1.3.139046010.1703244961; _nuk_sp_ses.9caf=*; _ncg_sp_ses.6312=*; DM_SitId961=1; DM_SitId961SecId5325=1; _gcl_au=1.1.1956305099.1703244971; __qca=P0-1362502284-1703244969837; _ga=GA1.1.872627709.1680863163; DM_SitId961SecId5281=1; DM_SitId961SecId5583=1; nukt_mem=s=1703244729838; nuk_customer_country_code=US; _ncg_sp_id.6312=0a3d5ec2-4db6-4399-873b-65238bf7c5dd.1680863168.3.1703245090.1680870663.f6bf1715-f2ba-42bb-b808-fdc6a9b53470; sailthru_pageviews=6; _nuk_sp_id.9caf=.1680863163.3.1703245091.1680870662.af141572-0feb-4f22-9e17-4caa296cf4da.a47b1570-2938-43b2-ae9e-fd7acf598817.655f0fc2-eab6-4e2f-830a-95a022c7e3e1.1703244962735.28; sailthru_content=b420be78c6ab1b910aefc061f34608e0f9828cc2f4cf5f33c008fc592b2d43678312b3960d99553247ab475ee7eeed9abf409e7527338b4e8080cfe3f9054015f35c9e0c433f608ad7c48c3d4818bec4; sailthru_visitor=34f94003-0798-4470-9b26-b7c1b5b9e745; AMP_TOKEN=%24RETRIEVING; _ga_T4GNPC7D0J=GS1.1.1703244977.1.1.1703245130.0.0.0; utag_main=v_id:01875b4064cb0022c697e865191c0506f001906700fb8$_sn:3$_ss:0$_st:1703246932286$_se:1$ses_id:1703244729838%3Bexp-session$_pn:8%3Bexp-session'
}

url_set = set()
def get_thesun(keyword):

    data = []

    if " " in keyword:
        new_keyword = keyword.replace(" ","+")
    else:
        new_keyword = keyword
    url = f"https://www.thesun.co.uk/?s={new_keyword}"

    res = requests.get(url, headers=headers)
    
    html = etree.HTML(res.text)
    
    page_num = html.xpath('//*[@id="main-content"]/div[2]/div[2]/div/ul[2]/li[15]/a/text()')[0]

    data = get_data(html, keyword)
    if page_num is not None and int(page_num) > 0:
    
        for i in range(2, int(page_num)):
            try :
                url = f"https://www.thesun.co.uk/page/{i}/?s={new_keyword}"
                res = requests.get(url, headers=headers)
                html_item = etree.HTML(res.text)
                data.extend(get_data(html_item, keyword))
            except:
                continue
    
    return data

def get_data(html, keyword):
    """Get detailed data
    """
    data = []
    items = html.xpath('//*[@id="main-content"]/div[2]/div[1]/main/div[3]/div')
    for item in items:
        try:
            a_tag = item.xpath('./div[2]/a')[0]
            if a_tag is not None:
                href_value = a_tag.get('href')
                data_headline_value = a_tag.get('data-headline')
                print('href:', href_value)
                print('data-headline:', data_headline_value)
            else:
                print('<a> tag not found')
            boby_url = f'https://www.thesun.co.uk{href_value}'
            if href_value in url_set:
                continue
            url_set.add(href_value)
            if href_value is not None:
                body, creat_date = get_news_boby(boby_url)
                if int(creat_date[:4]) < int(2015):
                    continue
                data.append(
                    {
                        "keyword":keyword,              #keywords    
                        "url":boby_url,              #link
                        "from" : 'thesun',
                        "headline": data_headline_value,   #title
                        "body": body,       #content
                        "body_word_count" : len(body.split()),   #The number of words the content contains
                        "date" : creat_date                  #Publication date
                    }
                )
        except Exception as e:
            print(e,">>>>>>>>>>>>>>>>>")
            print(e.__traceback__.tb_lineno)

    
    return data

def get_news_boby(boby_url):
    boby_text = []
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cookie" : '_pnvl_NxnLUb5i=false; pushly.user_puuid_NxnLUb5i=VkkdZKS0Gr2PBZbuRivoICOIdAsIEGL9; dnsDisplayed=undefined; ccpaApplies=false; signedLspa=undefined; nukt_sp_consent_global=NONE; _sp_su=false; ccpaUUID=9c209624-c59a-4de7-987a-7c6b3dfd68d6; nuPixelApp=j%3A%7B%22id%22%3A%2299ca5760-d52e-11ed-96d4-4d09a2f6594a%22%7D; rc_id1=01875b4064cb0022c697e865191c0506f001906700fb8; rc_id2=01875b4064cb0022c697e865191c0506f001906700fb8; _nuk_sp_id_=88bb45e2-1202-4af4-a6fc-369bb651ebef; _pnlspid_NxnLUb5i=13093; _ncg_id_=0a3d5ec2-4db6-4399-873b-65238bf7c5dd; _ncg_domain_id_=0a3d5ec2-4db6-4399-873b-65238bf7c5dd.1.1680863168.1743935168; login_event_fired=false; _pnss_NxnLUb5i=blocked; _ga_K2ECMCJBFQ=GS1.1.1680870487.2.1.1680870683.0.0.0; _ga_SQ24F7Q7YW=GS1.1.1680870487.2.1.1680870683.0.0.0; _ncg_g_id_=69fab7a0-c8cf-4b28-a3c5-18a0600c0b10.3.1680863173.1743935341; _gid=GA1.3.139046010.1703244961; _nuk_sp_ses.9caf=*; _ncg_sp_ses.6312=*; DM_SitId961=1; DM_SitId961SecId5325=1; _gcl_au=1.1.1956305099.1703244971; __qca=P0-1362502284-1703244969837; DM_SitId961SecId5281=1; DM_SitId961SecId5583=1; nukt_lv=1703244729838|||23547827|||18%20best%20flower%20subscription%20services%202023%20uk%20for%20fresh%20regular%20flower%20delivery; nukt_mem=s=1703244729838|ppn=article%3A18%20best%20flower%20subscription%20services%202023%20uk%20for%20fresh%20regular%20flower%20delivery|ppt=article|pps=shopping; AMP_TOKEN=%24RETRIEVING; _ga=GA1.1.872627709.1680863163; sailthru_pageviews=8; _ncg_sp_id.6312=0a3d5ec2-4db6-4399-873b-65238bf7c5dd.1680863168.3.1703245291.1680870663.f6bf1715-f2ba-42bb-b808-fdc6a9b53470; sailthru_content=b420be78c6ab1b910aefc061f34608e0f9828cc2f4cf5f33c008fc592b2d43678312b3960d99553247ab475ee7eeed9abf409e7527338b4e8080cfe3f9054015f35c9e0c433f608ad7c48c3d4818bec479fec55200b0a06d0cc4f49c27dce8c7347ccb4e6564102c4b51e519c8894f2b; sailthru_visitor=34f94003-0798-4470-9b26-b7c1b5b9e745; nuk_customer_country_code=CA; _ga_T4GNPC7D0J=GS1.1.1703244977.1.1.1703245297.0.0.0; utag_main=v_id:01875b4064cb0022c697e865191c0506f001906700fb8$_sn:3$_ss:0$_st:1703247097229$_se:1$ses_id:1703244729838%3Bexp-session$_pn:10%3Bexp-session; _nuk_sp_id.9caf=.1680863163.3.1703245297.1680870662.af141572-0feb-4f22-9e17-4caa296cf4da.a47b1570-2938-43b2-ae9e-fd7acf598817.655f0fc2-eab6-4e2f-830a-95a022c7e3e1.1703244962735.41'
    }
    res = requests.get(boby_url, headers=headers)
    html = etree.HTML(res.text)
    data_1 = html.xpath('//*[@id="main-content"]/section/div/main/article/div[1]/div[2]/div/div/ul/li[2]/time')
    if len(data_1) > 0:
        date = data_1[0].get("datetime")
    else:
        date = html.xpath('//*[@id="main-content"]/section/div/main/article/div[1]/div[2]/div/div/ul/li/time')[0].get("datetime")
    tag_p = html.xpath('//*[@id="main-content"]/section/div/main/article/div[3]/p')
    for p in tag_p:
        boby_text.extend(p.xpath('./text()'))
    
    return "\n".join(boby_text).replace('\n', ' '), date[:10]
if __name__ == '__main__':
    keywords = ["climate change", "climate adaptation", "global warming", "greenhouse gases", "carbon emissions", "renewable energy", "sustainable development", "extreme weather", "sea level rise", "paris agreement", "climate policy"," climate science", "climate advocacy",
                 "environmental crisis", "biodiversity loss", "climate action", "environmental policy", "COP 15", "COP 26", "United Nations Framework Convention on Climate Change", "UNFCCC", "COP",
                 "Climate Change", "Climate Adaptation","Global Warming", "Greenhouse Gases", "Carbon Emissions", "Renewable Energy", "Sustainable Development", "Extreme Weather", "Sea Level Rise",
                 "Paris Agreement", "Climate Policy"," Climate Science", "Climate Advocacy", "Environmental Crisis", "Biodiversity Loss", "Climate Action", "Environmental Policy"
                ]

    data = []
    for keyword in keywords:
        try:
            print(">>>>>>>>>>>>>>>>>>>>", keyword, len(data))
            data.extend(get_thesun(keyword))
        except:
            continue
    
    df = pd.DataFrame(data)
    df.to_csv("thesun.csv", index=False)
    
