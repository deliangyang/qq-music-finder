from spider.task.runner import Runner


if __name__ == '__main__':
    runner = Runner("./data.xlsx", 0, thread_num=5)
    runner.start()
