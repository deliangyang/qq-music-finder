import os
import threading
from spider.task.claw import ClawThread
from spider.error import with_error_stack
from spider.utils.logger import logger
from spider.read_data import ReadData
from queue import Queue
from spider.export import Export


class Runner(threading.Thread):

    def __init__(self, filename: str, save_file: str, cb, start: int = 0, thread_num: int = 3):
        threading.Thread.__init__(self)
        self.filename = filename
        self.thread_num = thread_num
        self.queue = Queue(maxsize=10000)
        self.cb = cb
        self.save_file = save_file
        self.start_id = start
        self.reader = None

    def run(self) -> None:
        try:
            self.reader = ReadData(self.filename, self.start_id)
            self.print_message('start query data')
            queue_thread = threading.Thread(target=self.read_data)
            queue_thread.start()

            threads = []
            for i in range(self.thread_num):
                thread_name = 'thread-%d' % i
                claw_thread = ClawThread(thread_name, self.queue, self.callback)
                claw_thread.start()
                threads.append(claw_thread)

            queue_thread.join()
            for thread in threads:
                thread.join()

            self.print_message("处理完毕，开始导出数据，请等待...")

            export = Export()
            export.export_data(logfile='query.log', filename=self.save_file)
            self.print_message('处理完毕')
            os.system("start explorer %s" % os.path.dirname(self.save_file))
        except Exception as e:
            self.print_message('处理失败: %s' % e)
            logger.error(with_error_stack(e))

    def read_data(self):
        for data in self.reader.iter():
            self.queue.put(data)

    def callback(self):
        pass

    def print_message(self, message):
        if callable(self.cb):
            self.cb(message)
