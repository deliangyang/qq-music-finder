from spider.task.runner import Runner
from spider.clean import clean


def xx(message: str):
    pass


if __name__ == '__main__':
    clean()
    runner = Runner("./data/split_20190823.xlsx", 'not_found.xlsx', cb=xx, start=0, thread_num=5)
    runner.start()
