import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
	
print("\033c")
PROJECT_NAME = input("Please enter Project name: ")
print("\033c")
HOMEPAGE = input("Please enter the url to crawl: ")
print("\033c")
print("Please enter the directory path where the queue and crawled txt files will be store. For example, /../../Desktop/Container. The queue and crawled files would be located at the Desktop and it will be stored inside a folder called Container: ", end="")
PATH = str(input())
if not PATH.endswith("/"):
	PATH += "/"
PROJECT_NAME = PATH +PROJECT_NAME
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PATH+PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        create_jobs()


create_workers()
crawl()
