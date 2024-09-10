from queue import Queue
import threading
import time

def get_detail_html(queue):
    """爬取文章信息"""
    while True:
        url = queue.get()
        print("get detail html start")
        time.sleep(2)
        print("get detail html start")

def get_detail_url(queue):
    """爬取文章url列表"""
    while True:
        print("get detail url start")
        time.sleep(4)
        for i in range(20):
            queue.put(f"http://projectsedu.com/id={i}")
        print("get detail url start")

def main():
    detail_url_queue = Queue(maxsize = 1000)
    thread_detail_url = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_html, args=(detail_url_queue,))
        html_thread.start()

    start_time = time.time()
    detail_url_queue.task_done()
    detail_url_queue.join()
    
if __name__ == '__main__':
    main()