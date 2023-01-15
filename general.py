import pandas as pd
import os
import numpy as np


class General:
    @staticmethod
    def make_crawl_queued_file(file_links):
        db = pd.read_csv(file_links)
        db_links = db['result link']
        num_of_links = len(db_links)
        if os.path.exists('./files/'):
            pass
        else:
            os.makedirs('./files/')
            db_links.to_csv('./files/queue.csv')
            pd.DataFrame([], columns=['result link']).to_csv('./files/crawled.csv')
            pd.DataFrame([], columns=[['title',
                                       'abstract',
                                       'Inventors',
                                       'DownloadLink'
                                       ]]).to_csv('./files/CollectedData.csv')
        return num_of_links

    @staticmethod
    def splitter (num_thrd):
        list_queue_db = np.array_split(pd.read_csv('./files/queue.csv'), num_thrd)

        if os.path.exists('./files/split/'):
            pass
        else:
            os.makedirs('./files/split/')

        for i in range(0, num_thrd):
            list_queue_db[i]['result link'].to_csv('./files/split/queue'+str(i)+'.csv')
            pd.DataFrame([], columns=['result link']).to_csv('./files/split/crawled'+str(i)+'.csv')
            pd.DataFrame([], columns=[['title',
                                       'abstract',
                                       'Inventors',
                                       'DownloadLink']]).to_csv('./files/split/collectedData'+str(i)+'.csv')
