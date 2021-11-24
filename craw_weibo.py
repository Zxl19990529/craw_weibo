import enum
from time import sleep
import random
from requests.api import head
from utils import get_ua,get_status,del_mblog
import pandas as pd
import numpy as np
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup 
from tqdm import tqdm 

if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active
    # wb_path = 'result.xlsx'
    wb_head = ['Time','containerid','weiboid','text','attitudes','comments_count','reposts_count']
    ws.append(wb_head)

    header = {
        'User-Agent': 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
    }
    cookie ={'cookie':r'SUB=_2A25MlOYYDeRhGeVP7lEV9SvKyDiIHXVsdopQrDV6PUJbktB-LWfykW1NTREUym7WTSSNWfoQDkZH8Ey9TQnzM7FZ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFjTyIC5AQPFXQdO-ixvSIv5NHD95Q0eK-0Sh-fSoeXWs4DqcjxgJyydJURIg4jIg8V90z7eKet; _T_WM=99297551269; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=c729a3; M_WEIBOCN_PARAMS=fid%3D100103type%253D1%2526q%253D%25E6%25B5%2599%25E6%25B1%259F%25E5%25A4%25A7%25E5%25AD%25A6%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%25B5%2599%25E6%25B1%259F%25E5%25A4%25A7%25E5%25AD%25A6%26uicode%3D10000011'} 

    # uid = '1871729063' # 天津大学
    # uid = '1880883723' #  山东大学
    # uid = '1703010470' # 东南大学
    # uid = '1825107551' # 中国海洋大学
    uid_dict = {
        # '3082822153':'大连理工',
        # '5396134858':'北京航空航天大学',
        # '1875088617':'北京师范大学',
        # '1823887605':'中国科学技术大学',
        # '7127745503':'国防科技大学',
        # '1844770327':'中央民族大学',
        # '1851766841':'中国农业大学',
        # '1688511087':'华东师范大学',
        '1851755225':'浙江大学'
    }
    for uid,university_name in uid_dict.items():

        main_url = "https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s" %(uid,uid)
        response = requests.get(url=main_url, headers=header,cookies=cookie, timeout=10)
        json_data = response.json()['data']
        json_file = uid+'.json'
        
        tabs = json_data['tabsInfo']['tabs']
        weibo_container_id = 0
        for tab in tabs:
            # print(tab['tabKey'])
            if tab['tabKey'] == 'weibo':
                # weibo_container_id = 
                # print(tab['containerid'])
                weibo_container_id = tab['containerid']# str
            else:
                continue
        # print(weibo_container_id)

        max_pages = 200
        

        start_page = 1 # 从第几页中断了，从第几页开始接着爬虫
        try:
            for page_id in range(start_page,max_pages):
                rand_base = random.randint(6,10)
                rand_i = 0.1*random.randint(1,10)
        
                page_url = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s&containerid=%s&page=%d'%(uid,uid,weibo_container_id,page_id)
                page_response = requests.get(page_url,headers=header,cookies=cookie)
                page_jsondata = page_response.json()['data']
                cards_data = page_jsondata['cards']
                save_path = '%s_page_%03d_%03d.xlsx'%(uid,start_page,page_id)
                for idx,card in enumerate(cards_data):
                    print('正在爬取{0}第{1}页，第{2}条微博,uid={3}'.format(university_name,page_id,idx,uid))
                    if str(card['card_type']) == '9':
                        item_id = card['itemid']
                        container_id ,weibo_id = item_id.split('_-_')
                        weibo_url = card['scheme']
                        mblog = card['mblog']

                        raw_time,context = del_mblog(mblog)
                        # attitudes,comments_count,reposts_count = get_status(weibo_id,header,cookie)
                        attitudes,comments_count,reposts_count = mblog['attitudes_count'],mblog['comments_count'],mblog['reposts_count']
                        ws.append([raw_time,container_id,weibo_id,context,attitudes,comments_count,reposts_count])
                # pbar.update(1)
                    sleep(rand_base+rand_i)
        except Exception as e:
            print(e)
            print('pageid:%d,idx:%d'%(page_id,idx))
            wb.save(save_path)
        wb.save(save_path)