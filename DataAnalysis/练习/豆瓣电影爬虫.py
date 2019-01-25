'''
0.写一个爬虫，爬取豆瓣的电影信息
    -- 爬取的内容包括( 电影名称，导演姓名，演员姓名，电影类型，制片国家，日期，豆瓣评分)
    -- 并保存为“豆瓣电影数据.xlsx”输出
    提示:
'''
import requests
import random
import json
from lxml import etree
import pandas as pd
import os
import time

os.chdir(r'F:\data1')


def capture_mv_info(url):
    mov_info = {'name': '',
                'dirname': '',
                'actorname': '',
                'movietype': '',
                'country': '',
                'date': '',
                'grade': ''}
    middle_list = {}
    html_1 = requests.get(url,proxies={'https:':random.choice(proxies_list)},headers=header)
    obj_html = etree.HTML(html_1.text)

    # 定义一个清洗国家的函数
    def country_clear(path):
        country = obj_html.xpath(path)[7:10]
        ct = []
        for item in country:
            if item.strip() != '':
                ct.append(item)
        return ct

    # 定义一个循环提取信息的函数
    def data_tq(path):
        data = []
        info = obj_html.xpath(path)
        for actor in info:
            data.append(actor.text)
        return data

    dirname = data_tq(r'//div[@id="info"]//a[@rel="v:directedBy"]')
    actorname = data_tq(r'//div[@id="info"]//span[@class="actor"]//a')
    movietype = data_tq(r'//div[@id="info"]//span[@property="v:genre"]')
    country = country_clear(r'//div[@id="info"]/text()')
    date = data_tq(r'//div[@id="info"]//span[@property="v:initialReleaseDate"]')
    name = data_tq('//div[@id="content"]//span[@property="v:itemreviewed"]')
    grade = data_tq('//div[@id="interest_sectl"]//strong[@class="ll rating_num"]')

    mov_info['name'] = name
    mov_info['dirname'] = dirname
    mov_info['actorname'] = actorname
    mov_info['movietype'] = movietype
    mov_info['country'] = country
    mov_info['date'] = date
    mov_info['grade'] = grade

    return mov_info

# 设置代理
global proxies_list
global header

proxies_list = ['101.37.79.125:3128','120.92.74.189:3128','120.92.74.237:3128','119.31.210.170:7777','125.62.26.197:3128']
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}

url = r'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=2000&page_start=1'
html_response = requests.get(url,proxies={'https:':random.choice(proxies_list)},headers=header)
html_text = html_response.text
print(len(html_text))
html_json = json.loads(html_text)

movie_url = []
for item in html_json['subjects']:
    movie_url.append(item['url'])


# 自定义一个函数 遍历url 获取电影信息
def movie_infos(url_list):
    mov_info_list = []
    num = 0
    for i in url_list:
        time.sleep(2)
        mov_info = capture_mv_info(i)
        mov_info_list.append(mov_info)
        num += 1
        print('第--%s--部--OK---' %num)
    return mov_info_list


mv = movie_infos(movie_url)

'''
 存储数据
'''
data = pd.DataFrame(mv)

writer = pd.ExcelWriter('豆瓣电影数据.xlsx')
data.to_excel(writer, 'sheet1', index=False)
writer.save()

print('finish!')