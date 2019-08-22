import threading
from queue import Queue
from spider.utils.logger import logger
from spider.detail.info import query_info
from spider.detail.lyric import query_lyric
from spider.search.song_list import search, compare
from spider.error import *


class ClawThread(threading.Thread):

    def __init__(self, thread_name: str, queue: Queue, callback):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_name = thread_name
        self.callback = callback

    def run(self) -> None:
        while True:
            try:
                data = self.queue.get(block=True, timeout=20)
                self.start_deal_with(data)
            except Exception as e:
                logger.error(with_error_stack(e))
                break

    def start_deal_with(self, data: {}):
        result = self.__init_data(data)
        try:
            for keyword in self.get_keywords(data):
                logger.info({
                    'thread': self.thread_name,
                    'keyword': keyword,
                    'beat_id': data['beat_id'],
                })
                count = 0
                for items in search(keyword):
                    mid, music_id, ok = compare(items, data)
                    logger.debug({
                        'mid': mid,
                        'music_id': music_id,
                        'ok': ok,
                    })
                    if not ok:
                        continue
                    logger.info(items)

                    try:
                        for k, v in query_info(mid).items():
                            if k in result and len(result[k]) > 0:
                                result[k] += '#'
                            result[k] += v
                    except Exception as e:
                        logger.error(with_error_stack(e))

                    if result['message'] != ERROR_MESSAGE_OFF_LINE:
                        try:
                            for k, v in query_lyric(mid, music_id).items():
                                if k in result and len(result[k]) > 0:
                                    result[k] += '#'
                                result[k] += v
                        except Exception as e:
                            logger.error(with_error_stack(e))

                    if len(result['company']) <= 0:
                        result = self.update_message(result, ERROR_MESSAGE_NOT_COMPANY_INFO)
                    count += 1
                    break
                if count <= 0:
                    result = self.update_message(result, ERROR_MESSAGE_NOT_FOUND)
        except Exception as e:
            result = self.update_message(result, ERROR_MESSAGE_UNKNOWN)
            logger.error(with_error_stack(e))
            logger.error({
                'message': 'ERROR_MESSAGE_UNKNOWN',
                'result': result,
            })
            print(self.get_keywords(data))
        finally:
            logger.info({
                'target': 'records',
                'thread': self.thread_name,
                'record': result,
            })
            if callable(self.callback):
                self.callback()

    @classmethod
    def update_message(cls, result, message: str):
        if len(result['message']) > 0:
            result['message'] += '#'
        result['message'] += message
        return result

    @classmethod
    def __init_data(cls, data: {}):
        return {
            'beat_id': data['beat_id'],
            'beat_name': data['beat_name'],
            'singer': data['singer'],
            'singer1': data['singer1'],
            'singer2': data['singer2'],
            'company': '',
            'genre': '',
            'lan': '',
            'pub_time': '',
            'lyric': '',
            'song': '',
            'arranging': '',
            'message': '',
        }

    @classmethod
    def get_keywords(cls, data: {}):
        singers = [data['singer'], data['singer1'], data['singer2']]
        try:
            singers = list(filter(lambda x: x and len(x) > 0, singers))
            if len(singers) == 2:
                yield ' '.join([data['beat_name'], singers[0], singers[1]])
                yield ' '.join([data['beat_name'], singers[1], singers[0]])
            else:
                singers.insert(0, data['beat_name'])
                yield ' '.join(singers)
        except Exception as e:
            print(e, singers, data)
