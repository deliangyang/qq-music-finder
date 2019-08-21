import threading
from spider.task.claw import ClawThread
from spider.utils.logger import logger
from spider.read_data import ReadData
from queue import Queue


class Runner(threading.Thread):

    def __init__(self, filename: str, start: int = 0, thread_num: int = 3):
        threading.Thread.__init__(self)
        self.filename = filename
        self.thread_num = thread_num
        self.container = []
        self.reader = ReadData(self.filename, start)
        self.queue = Queue(maxsize=10000)

    def run(self) -> None:
        logger.info('start query data')
        queue_thread = threading.Thread(target=self.read_data)
        queue_thread.start()

        threads = []
        for i in range(self.thread_num):
            thread_name = 'thread-%d' % i
            claw_thread = ClawThread(thread_name, self.queue, self.container, self.callback)
            claw_thread.start()
            threads.append(claw_thread)

        queue_thread.join()
        for thread in threads:
            thread.join()

    def read_data(self):
        for data in self.reader.iter():
            self.queue.put(data)

    def callback(self):
        self.container = []
