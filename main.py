from spider.task.runner import Runner


def xx(message: str):
    pass


if __name__ == '__main__':
    runner = Runner("./data/伴奏列表.xlsx", 'test12312312313.xlsx', cb=xx, start=0, thread_num=5)
    runner.start()
