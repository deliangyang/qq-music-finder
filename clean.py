import os
import datetime


if __name__ == '__main__':
    for file in os.listdir('.'):
        if file.startswith('query') and file.endswith('.log'):
            new_file_name = str(datetime.datetime.now()).replace(' ', '_').replace(':', '')
            os.rename(file, new_file_name + '.' + file)
