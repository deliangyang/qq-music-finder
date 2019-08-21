from spider.task.runner import Runner


if __name__ == '__main__':
    runner = Runner("./data/伴奏列表.xlsx", 0, thread_num=3)
    runner.start()
