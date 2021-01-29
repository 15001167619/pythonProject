import requests
import os
import random
import pandas as pd
import time
from bs4 import BeautifulSoup

headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
]

# 高校存储excel
SCHOOL_EXCEL_PATH = 'E:\school\\abroad_school_temp.xlsx'


class SpiderAbroadSchool:

    def __init__(self):
        # 请求头 headers
        self.header = {'User-Agent': random.choice(headers)}
        # 请求间隔时长 interval_time
        self.interval_time = 10

    def _save_excel(self, school_list):
        if os.path.exists(SCHOOL_EXCEL_PATH):
            df = pd.read_excel(SCHOOL_EXCEL_PATH)
            df = df.append(school_list)
        else:
            df = pd.DataFrame(school_list)
        writer = pd.ExcelWriter(SCHOOL_EXCEL_PATH)
        df.to_excel(excel_writer=writer, columns=['学校名称（中文）', '学校名称（英文）', '国家', '州', '城市'],
                    index=False,
                    encoding='utf-8', sheet_name='Sheet')
        writer.save()
        writer.close()

    def spider(self):
        """
        获取首页高校
        :return:
        """

        # abroad_school_list = [
        #                       '奥地利', '爱尔兰', '比利时', '保加利亚', '波兰', '丹麦', '俄罗斯', '芬兰', '荷兰', '葡萄牙', '罗马尼亚', '喀麦隆', '白俄罗斯',
        #                       '阿尔及利亚', '毛里求斯',
        #                       '斯里兰卡', '吉尔吉斯斯坦', '拉脱维亚', '列支敦士登', '以色列', '卢森堡', '马耳他', '其他']
        abroad_school_url = 'https://www.xuanxiaodi.com/schools/226-0-0-0-0-0-XXX.html'
        for i in range(281):
            spider_abroad_school_url = abroad_school_url.replace("XXX", str(i+1))
            print(spider_abroad_school_url)
            res = requests.get(spider_abroad_school_url, headers=self.header)
            # 返回网页中文数据乱码
            soup = BeautifulSoup(res.text, 'html.parser')
            schools_list = []
            for k in soup.find_all('div', class_='component-school-item'):
                school_zh_name = k.find(name="a", attrs={"class": "school-zh-name"})
                school_en_name = k.find(name="div", attrs={"class": "school-en-name"})
                location_text = k.find(name="span", attrs={"class": "location-text"})
                locations = location_text.text.split('-')
                country_name = ''
                zhou_name = ''
                cs_name = ''
                try:
                    if len(locations)==3:
                        country_name = locations[0]
                        zhou_name = locations[1]
                        cs_name = locations[2]
                    elif len(locations)==2:
                        country_name = locations[0]
                        zhou_name = locations[1]
                    else:
                        country_name = locations[0]
                except IOError as e:
                    print("IOE ERROR")
                except Exception as e:
                    print("Exception")

                school = {'学校名称（中文）': school_zh_name.text,
                          '学校名称（英文）': school_en_name.text,
                          '国家': country_name,
                          '州': zhou_name,
                          '城市': cs_name}
                schools_list.append(school)

            self._save_excel(schools_list)
            time.sleep(self.interval_time)





if __name__ == '__main__':
    spiderAbroadSchool = SpiderAbroadSchool()
    spiderAbroadSchool.spider()
