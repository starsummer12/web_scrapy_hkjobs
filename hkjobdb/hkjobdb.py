# -*- coding:utf-8 _*-
"""
@author: Leo Yang
@license: Apache Licence
@file: UCSDPoliScien.py
@createtime: 2020-07-03 21:40
@contact: leoyang@ucsd.edu
@site: www.leoyang.org
"""

import requests
import json
import logging
import csv
from lxml import etree


class hkjobdb:
    def __init__(self,page):
        logging.basicConfig(filename='HKJobs.log', level=logging.INFO)
        self.page = page
        # fill in your url
        self.url = 'https://hk.jobsdb.com/hk/en/Search/FindJobs?JSRV=1&page='+str(page)
        print('Working on page ' + str(page))
        self.headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept - encoding': 'gzip, deflate, br',
            'accept - language': 'zh - CN, zh;q = 0.9',
            'cache - control': 'max - age = 0',
            'sec-fetch - dest':'document',
            'sec-fetch - mode':'navigate',
            'sec-fetch - site':'none',
            'sec-fetch - user':'?1',
            'upgrade-insecure-requests': '1',
            'user-agent':'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_14_5) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.135 Safari / 537.36'
        }

    def send_get_request(self, url):
        r = requests.get(url,headers=self.headers)
        if r.text:
            response=r.text
            #html_result = r.text
            print('get result success')
            return response
        else:
            print('get result fail')
            return ''

    # Todo #1: add a function called extract_info_urls() to extract job urls list
    def extract_info_urls(self,response):
        raw_tree=etree.HTML(response)
        job_urls=raw_tree.xpath(
            '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div/div/div/div/article/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/h1/a/@href')
        return job_urls

    def extract_information(self, response):
        raw_tree = etree.HTML(response)
        dic_result={}
        dic_result['jobname']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/h1/text()')[0]
        dic_result['comname']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/span/text()')[0]
        try:
            dic_result['img']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div/img/@src')[0]
        except IndexError:
            dic_result['img']=''
        # try:
        #     dic_result['icon']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div/img/@src')[0]
        # except IndexError:
        #     dic_result['icon'] = ''
        try:
            dic_result['place']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[1]/div/a/span/text()')[0]
        except IndexError:
            dic_result['place'] = ''
        try:
            dic_result['salary']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[2]/span/text()')[0]
        except IndexError:
            dic_result['salary']=''
        dic_result['posttime']=raw_tree.xpath('//*[@id="contentContainer"]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/div[3]/span/text()')[0]
        dic_result['job_detail']='\n'.join(raw_tree.xpath('//*[@id="contentContainer"]/div/div[2]/div/descendant::*/text()'))
        dic_result['page']=self.page
        return dic_result

    # Todo #2: add a function save_information( ) to save the extracted information in csv format.
    def save_information(self, raw_json):
        with open('hkjobs3.csv', 'a+') as out_f:
            out_f.write(json.dumps(raw_json, ensure_ascii=False) + '\n')
            # out_f.write(json.dumps(raw_json, ensure_ascii=False) + '\n')
            # csv_writer = csv.DictWriter(out_f, raw_json.keys())
            # What's this? Why do we need it?
            # if out_f.tell() == 0:
            #     csv_writer.writeheader()
            #
            # csv_writer.writerow(raw_json)

    # Put all the things together
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
        runner = hkjobdb(page=page)
        runner.run()
