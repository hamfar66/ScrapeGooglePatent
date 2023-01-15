import general
import spider
import os
import shutil
import time
import pandas as pd
import multiprocessing as mp
import threading


def my_scraper (thread_number):
    stop = False
    while not stop:
        worker = spider.Spider()
        remain_link = worker.read_links(thread_number)
        # print(remain_link)
        worker.read_url(thread_number)
        worker.html_parser(thread_number)
        worker.find_title(thread_number)
        worker.find_abstract(thread_number)
        worker.find_inventor(thread_number)
        worker.find_download_link(thread_number)
        worker.collect_data(thread_number)
        if remain_link == 0:
            stop = True


def main():
    if os.path.exists('./files/'):
        shutil.rmtree('./files')

    coordinator = general.General()
    total_num_links = coordinator.make_crawl_queued_file("I:/PythonProjects/1ScrapGooglePatentt/Links/test.csv")

    num_applied_thread = 20
    general.General.splitter(num_applied_thread)

    list_threads = []

    start = time.time()

    for i in range(0, num_applied_thread):
        t = threading.Thread(target=my_scraper, args=(i,))
        list_threads.append(t)

    for i in range(0, num_applied_thread):
        list_threads[i].start()

    for i in range(0,num_applied_thread):
        list_threads[i].join()

    print(time.time() - start)
    #
    # start = time.time()
    #
    # file_queue = pd.read_csv('./files/queue.csv')
    # file_crawled = pd.read_csv('./files/crawled.csv')
    #
    #
    #
    # spider.Spider.collected_data.to_csv('./files/CollectedData.csv')
    #
    # print(time.time() - start)


if __name__ == '__main__':
    main()

