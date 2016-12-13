import scrapy
import os
import csv
from time import sleep
from datetime import datetime



class NewsSpider(scrapy.Spider):
    name = "bing_news"

    def start_requests(self, url_list=None):
        #TODO: Make this less blunt.
        if not url_list:
            indexes_and_urls = link_list_from_bing_csv(os.path.realpath('bing_spiders/data/queries/bing_link_list2016-12-12.csv'))
        else:
            assert type(url_list) is list
            indexes_and_urls = url_list
            for index, url in indexes_and_urls[-10:10]:
                assert type(url) is str
        cnt = 0
        for indx, url in indexes_and_urls:
            cnt += 1
            # Let's take our time.
            sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, save_local=True, root_save_dir=os.path.realpath('tutorial/data/bing/webpages')):
        page = response.url.split("/")[-2]
        if not page:
            page = str(datetime.now()).replace(' ', '_').replace(':', '-').replace('.', '_')
        filename = '{}.html'.format(page)
        if os.path.exists(os.path.join(root_save_dir, filename)):
            copy_num = 1
            while True:
                copy_name = filename[:-5] + '({})'.format(copy_num) + filename[-5:]
                if os.path.exists(os.path.join(root_save_dir, copy_name)):
                    copy_num += 1
                elif copy_num > 300:
                    raise IOError('more than 300 copies of docname present in dir. Please specify new name.')
                else:
                    filename = copy_name
                    break
        if save_local:
            if root_save_dir != 'cwd':
                if os.path.exists(root_save_dir):
                    filename = os.path.join(root_save_dir, filename)
                else:
                    raise ValueError('path to root_save_dir does not exist.')
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file {}'.format(filename))
        else:
            return response.body


def link_list_from_bing_csv(csv_file):
    with open(csv_file, 'rb') as csvfile:
        link_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            link_list.append((row['index'], row['url']))
        return link_list
