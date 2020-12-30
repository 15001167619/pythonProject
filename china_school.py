import requests
import os
import time
import random
import pandas as pd
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
SCHOOL_EXCEL_PATH = 'E:\school\\school.xlsx'

class SpiderChinaSchool:

    def __init__(self):
        # 新东方 高校库首页
        self.index_url = 'https://gaokao.xdf.cn/college/china/searchSchool/_____page'
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
        # columns参数用于指定生成的excel中列的顺序
        df.to_excel(excel_writer=writer, columns=['校徽', '学校名称', '院校省份', '院校性质', '院校类型', '学历层次', '院校属性', '院校详情'], index=False,
                    encoding='utf-8', sheet_name='Sheet')
        writer.save()
        writer.close()

    def spider(self):
        """
        获取首页高校
        :return:
        """
        for i in range(10):
            page_num = i+1
            self._spider_school(page_num)
            time.sleep(self.interval_time)

    def _get_school_info(self, school_info):

        data = school_info.find_all('td')
        img_url = school_info.find_all('img')[0].get('src')
        school_name = data[1].text
        province_name = data[2].text
        var3 = data[3].text
        var4 = data[4].text
        var5 = data[5].text
        var6 = data[6].text.replace('\n', ';').replace('\r', ';')
        var7 = data[7].find_all('a')[0]['href']

        school = {'校徽': img_url,
                  '学校名称': school_name,
                  '院校省份': province_name,
                  '院校性质': var3,
                  '院校类型': var4,
                  '学历层次': var5,
                  '院校属性': var6,
                  '院校详情': var7}

        return school

    def _spider_school(self, page_num):
        index_url = self.index_url.replace("page", str(page_num))
        # 抓取高校地址
        print('获取第'+str(page_num)+'页高校地址' + index_url)
        res = requests.get(index_url, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 获取第一页数据
        is_frist = 0
        schools_list = []
        for school_info in soup.find_all('tr'):
            if is_frist != 0:
                # 添高校数据
                schools_list.append(self._get_school_info(school_info))

            is_frist += 1

        self._save_excel(schools_list)


if __name__ == '__main__':
    spiderChinaSchool = SpiderChinaSchool()
    spiderChinaSchool.spider()
