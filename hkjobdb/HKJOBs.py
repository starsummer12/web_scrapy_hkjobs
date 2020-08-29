# -*- coding:utf-8 _*-
"""
@author: Leo Yang
@license: Apache Licence
@file: HKJob.py
@createtime: 2020-07-04 21:23
@contact: leoyang@ucsd.edu
@site: www.leoyang.org
"""

import requests
import json
import logging
import csv
from lxml import etree


class HKJob(object):
    def __init__(self, page):
        # init logging
        logging.basicConfig(filename='HKJob.log', level=logging.INFO)
        self.page = page
        self.url = 'https://hk.jobsdb.com/hk/en/Search/FindJobs?JSRV=1&page=' + str(page)
        print('Working on page ' + str(page))
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            # 'cookie': '__cfduid=d4a5e5025c307a0899cfb595f591de2321591411627; __cfduid=d4a5e5025c307a0899cfb595f591de2321591411627; azTest=j%3A%7B%22id%22%3A%22af644b3a-7e57-4b74-a6ac-7081d2f3c78e%22%2C%22createdAt%22%3A%222020-06-06T00%3A46%3A43.809Z%22%7D; ABNEWHP=1607; showNewHomePage=B; isSmartSearch=A; sol_id=74034b65-7d37-43de-94e1-ea2caf21d6dc; s_fid=47BC437B5DDD3E34-38816260845AF8DB; _gcl_au=1.1.3255028.1591411635; s_vi=[CS]v1|2F6D81D905159C2C-60000A22221F80DA[CE]; intercom-id-o7zrfpg6=489c6e71-c371-4a82-9478-26f4afa57525; _fbp=fb.1.1591411666764.1130609656; s_cc=true; _hjid=533d3b03-b258-4c44-b361-6b35adae2f01; RecentSearch=%7B%22Keyword%22%3A%5B%22data%22%5D%7D; ABSSRPGroup=B; ABHPGroup=B; ABJDGroup=B; NSC_wjq_kpctec.dpn_ttm=30dfa3dbcdc234aa83959421623161a99f20596b3402b72e8d156af38c20a8f9e3dee830; ABIDPGroup=1; sol_id_pre_stored=74034b65-7d37-43de-94e1-ea2caf21d6dc; _gid=GA1.2.818155812.1593870501; intercom-session-o7zrfpg6=; ASP.NET_SessionId=rronrppqvou1gjrlcpebyl5g; s_sq=%5B%5BB%5D%5D; ABSSRP=1659; sol_id=74034b65-7d37-43de-94e1-ea2caf21d6dc; utag_main=v_id:017287866ed70010221858819c4c03078007207000bd0$_sn:5$_se:2$_ss:0$_st:1593915998514$ses_id:1593914193762%3Bexp-session$_pn:1%3Bexp-session; _ga=GA1.1.960239391.1591411635; _ga_88RH71GXX9=GS1.1.1593914191.5.1.1593914314.0',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    def send_get_request(self, url):
        # 3. Receive Response
        r = requests.get(url, headers=self.headers)
        if r.text:
            response = r.text
            # print('get response success')
            return response
        else:
            print('get response fail')
            return ''

    def extract_info_urls(self, response):
        # The response is not json this time. We need to extract information from html file.
        # Therefore, we need to import a new module -- lxml
        # Please review how to install new module using conda, we discussed it in the first session.
        raw_tree = etree.HTML(response)
        # Here we first extract the urls of the detailed info pages
        job_urls = raw_tree.xpath(
            '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div/div/div/div/article/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/h1/a/@href')
        return job_urls

    # 4. Extract Information
    def extract_information(self, response):
        raw_tree = etree.HTML(response)
        dict_result = {}
        dict_result['job_name'] = raw_tree.xpath(
            '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/h1/text()')[
            0]
        dict_result['company_name'] = raw_tree.xpath(
            '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/span/text()')[
            0]
        try:
            dict_result['company_img'] = raw_tree.xpath(
                '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div/img/@src')[0]
        except IndexError:
            dict_result['company_img'] = ''
        try:
            dict_result['work_place'] = raw_tree.xpath(
                '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[1]/div/a/span/text()')[
                0]
        except IndexError:
            dict_result['work_place'] = ''
        try:
            dict_result['salary'] = raw_tree.xpath(
                '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[2]/span/text()')[0]
        except IndexError:
            dict_result['salary'] = ''
        dict_result['posted_time'] = raw_tree.xpath(
            '//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[3]/span/text()')[0]

        dict_result['job_details'] = '\n'.join(
            raw_tree.xpath('//*[@id="contentContainer"]/div/div[2]/div/descendant::*/text()'))
        dict_result['page'] = self.page
        return dict_result

    def save_information(self, raw_json):
        with open('HKJob_result3.json', 'a+') as out_f:
            out_f.write(json.dumps(raw_json, ensure_ascii=False) + '\n')

    def run(self):
        response = self.send_get_request(self.url)
        job_urls = self.extract_info_urls(response)
        for url in job_urls:
            try:
                print('Scraping url ' + url)
                info_response = self.send_get_request(url)
                raw_json = self.extract_information(info_response)
                raw_json['job_url'] = url
                # self.save_information_json(raw_json)
                self.save_information(raw_json)
            except IndexError as e:
                print('There are something wrong when phrasing ' + url)
                logging.info(str(e) + ' ' + url)


if __name__ == '__main__':
    for page in range(10,11):
        runner = HKJob(page=page)
        runner.run()
