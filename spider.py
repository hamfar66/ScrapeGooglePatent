import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from tabulate import tabulate
from os import system



class Spider:

    db_print = pd.DataFrame([], columns=[['links remain', 'links done', 'parser', 'title', 'abstract', 'inventor', 'download link']])

    # def __init__(self):
    #     self.link = Spider.read_links(file_queue, file_crawl)


    def read_links(self, thrd_num):
        db_queue = pd.read_csv('./files/split/queue'+str(thrd_num)+'.csv')
        db_crawled = pd.read_csv('./files/split/crawled'+str(thrd_num)+'.csv')
        l = db_queue['result link'][0]
        db_queue = db_queue.iloc[1:, :]
        db_queue['result link'].to_csv('./files/split/queue'+str(thrd_num)+'.csv')
        db_crawled.loc[len(db_crawled)] = l
        db_crawled['result link'].to_csv('./files/split/crawled'+str(thrd_num)+'.csv')
        self.link = l
        Spider.db_print.loc[thrd_num,'links remain'] = len(db_queue)
        print('thread ' + str(thrd_num) + ' got url:' + str(l))
        return len(db_queue)


    def read_url(self, thrd_num):
        # print('thread number '+ str(thrd_num) + ' is reading:' + str(self.link))
        fp = urllib.request.urlopen(self.link)
        mybytes = fp.read()
        self.html_result = mybytes.decode("utf8")
        # print(self.html_result)
        fp.close()
        print('thread ' + str(thrd_num) + ' read url')


    def html_parser(self, thrd_num):
        self.soup = BeautifulSoup(self.html_result, 'html.parser')
        Spider.db_print.loc[thrd_num, 'parser'] = 1
        print('thread ' + str(thrd_num) + ' parsed url')


    def find_title(self, thrd_num):
        self.temp = self.soup.findAll('title')
        self.title = self.temp[0].get_text()
        self.position_ = self.title.find("-")
        self.title = self.title[self.position_ + 2:]
        self.position_ = self.title.find("-")
        self.title = self.title[:self.position_]
        if not self.title:
            self.title = 'empty'
        Spider.db_print.loc[thrd_num,'title'] = 1
        print('thread ' + str(thrd_num) + ' found title')

    def find_abstract(self, thrd_num):
        self.temp = self.soup.findAll('meta' )
        # print(self.temp)
        self.abstract = 'empty'
        for i in self.temp:
            if i.get('name') == 'description':
                self.abstract = i.get('content')
        first = self.abstract.find(next(filter(str.isalpha, self.abstract)))
        self.abstract = self.abstract[first:]
        Spider.db_print.loc[thrd_num, 'abstract'] = 1
        print('thread ' + str(thrd_num) + ' found abstract')


    def find_inventor(self,thrd_num):
        self.temp = self.soup.findAll('meta' )
        lst = []
        for i in self.temp:
            if i.get('scheme') == 'inventor':
                lst.append(i.get('content'))
        self.inventor = lst
        if not self.inventor:
            self.inventor = 'empty'
        Spider.db_print.loc[thrd_num, 'inventor'] = 1
        print('thread ' + str(thrd_num) + ' found inventor')


    def find_download_link(self, thrd_num):
        self.temp = self.soup.findAll('a' )
        # print(type(self.temp[0]))
        self.download_link = 'empty'
        for i in self.temp:
            # print(str(i.get('itemprop')).find('pdf') )
            if str(i.get('itemprop')).find('pdf') == 0:
                self.download_link = i['href']
                # print(i['href'])
        Spider.db_print.loc[thrd_num, 'download link'] = 1
        print('thread ' + str(thrd_num) + ' found download link')


    def collect_data(self, thrd_num):
        collected_data = pd.read_csv('./files/split/collectedData'+str(thrd_num)+'.csv')
        n = len(collected_data.index)
        collected_data.loc[n,'title'] = self.title
        collected_data.loc[n,'abstract'] = self.abstract
        # print(type(self.inventor))
        collected_data.loc[n,'DownloadLink'] = self.download_link
        collected_data.loc[n,'Inventors'] = [[self.inventor]]
        collected_data.iloc[:,-4:].to_csv('./files/split/collectedData'+str(thrd_num)+'.csv')
        Spider.db_print.loc[thrd_num, 'parser'] = 0
        Spider.db_print.loc[thrd_num,'title'] = 0
        Spider.db_print.loc[thrd_num, 'abstract'] = 0
        Spider.db_print.loc[thrd_num, 'inventor'] = 0
        Spider.db_print.loc[thrd_num, 'download link'] = 0
        Spider.db_print.loc[thrd_num, 'links done'] = n+1

        Spider.print_table()

    @staticmethod
    def print_table():
        print(tabulate(Spider.db_print.loc[:,['links remain','links done']], headers='keys', tablefmt='psql'))

