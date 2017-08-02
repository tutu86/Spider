import threading
from Queue import Queue
from spyder import Spider
from domain import *
from general import *

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://thenewboston.com/index.php'
DOMAIN_NAME = get_domain_name(HOMEPAGE)

QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWL_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 2
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


#do the next job in the queue

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


#each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()




#check if there are items in the queue if so crawl it
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(queued_links) + ' links in the queue')
        create_jobs()


create_workers()
crawl()


when i run, it says;

/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7 /Users/tutumac/PycharmProjects/untitled9/Crawler/main.py
Creating directory thenewboston
First Spider not crawling https://thenewboston.com/index.php
Queue 1 | Crawled 0
addinfourl instance has no attribute 'getheader'

Process finished with exit code 0
