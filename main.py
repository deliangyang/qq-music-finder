from spider.task.runner import Runner


def xx(message: str):
    pass


if __name__ == '__main__':
    runner = Runner("./data/xxxxxxxx.xlsx", 'not_found.xlsx', cb=xx, start=0, thread_num=5)
    runner.start()
