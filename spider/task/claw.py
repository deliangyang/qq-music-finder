import threading
from queue import Queue
from spider.utils.logger import logger
from spider.error import with_error_stack
from spider.detail.info import query_info
from spider.detail.lyric import query_lyric
from spider.search.song_list import search, compare
from spider.error import ERROR_MESSAGE_NOT_FOUND, ERROR_MESSAGE_NOT_COMPANY_INFO, ERROR_MESSAGE_UNKNOWN


class ClawThread(threading.Thread):

    def __init__(self, thread_name: str, queue: Queue, container: [], callback):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_name = thread_name
        self.container = container
        self.callback = callback

    @classmethod
    def get_keywords(cls, data: {}):
        singers = [data['singer'], data['singer1'], data['singer2']]
        singers = list(filter(lambda x: len(str(x)) > 0, singers))
        if len(singers) == 2:
            yield ' '.join([data['beat_name'], singers[0], singers[1]])
            yield ' '.join([data['beat_name'], singers[1], singers[0]])
        else:
            singers.insert(0, data['beat_name'])
            yield ' '.join(singers)

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
                            if len(result[k]) > 0:
                                result[k] += '#'
                            result[k] += v
                    except Exception as e:
                        logger.error(with_error_stack(e))

                    try:
                        for k, v in query_lyric(mid, music_id).items():
                            if len(result[k]) > 0:
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
        finally:
            logger.info({
                'thread': self.thread_name,
                'record': result,
            })
            if callable(self.callback):
                self.callback()

    def detail_info(self, mid: str):
        pass

    def lyric_info(self, mid: str, music_id: int):
        pass

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
