from queue import Queue
import time
import os
import requests
import random
import threading
import shutil
class DownloadThread(threading.Thread):
    def __init__(self, bytes_queue: Queue, url):
        super().__init__(daemon=True)
        self.bytes_queue = bytes_queue
        self.url = url

    def run(self):
        while not self.bytes_queue.empty():
            bytes_range = self.bytes_queue.get()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
                "Range": "bytes={}".format(bytes_range[1])
            }
            response = requests.get(self.url, headers=headers)
            with open("temp/{}.tmp".format(bytes_range[0]), "wb") as f:
                f.write(response.content)

def get_file_size(url) -> int:
    response = requests.head(url)
    file_length = int(response.headers['Content-Length'])

    return file_length

def get_thread_download(file_length) -> list:
    bytes = Queue(20)

    start_bytes = -1
    for i in range(20):
        bytes_size = int(file_length/20)*i
        
        if i == 20-1: bytes_size = file_length
        bytes_length = "{}-{}".format(start_bytes+1, bytes_size)
        
        bytes.put([i, bytes_length])
        start_bytes = bytes_size

    return bytes

def create_threading(bytes_queue,url):
    thread_list = []
    for i in range(8):
        thread = DownloadThread(bytes_queue, url)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

def composite_file():
    if os.path.isfile("spigot.jar"): os.remove("spigot.jar")
    with open("spigot.jar", "ab") as f:
        for i in range(20):
            with open("temp/{}.tmp".format(i), "rb") as bytes_f:
                f.write(bytes_f.read())

def main(url):
    file_length = get_file_size(url)
    copies_queue = get_thread_download(file_length)
    create_threading(copies_queue,url)
    composite_file()
    
def download(url,version):
    try:
        os.mkdir('temp')
        os.mkdir(version)
    except:
        time.sleep(1)

    if __name__ == '__main__':
        main(url)

    shutil.rmtree('temp')
    shutil.move('spigot.jar',version + '/spigot.jar')
