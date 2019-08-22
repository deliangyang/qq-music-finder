import json
import requests
from spider.reg import *
from spider.header import headers
from spider.error import ERROR_MESSAGE_OFF_LINE
from spider.utils.logger import logger


def query_info(mid: str) -> {}:
    """
    查询 发行公司/流派/语种/发行时间
    :param mid:
    :return:
    """
    resp = requests.get('https://y.qq.com/n/yqq/song/%s.html' % mid, headers=headers)
    _content = resp.content.decode('utf-8')
    result = re_info.findall(_content)
    logger.debug(result)
    data = {
        'company': '',
        'genre': '',
        'lan': '',
        'pub_time': '',
        'message': '',
    }
    if len(result) <= 0:
        logger.debug(_content)
        return data
    content = json.loads(result[0])
    for key in data:
        if key in content and 'content' in content[key]:
            for datum in content[key]['content']:
                if len(data[key]) > 0:
                    data[key] += '#'
                data[key] += datum['value']

    song_data = re_song_data.findall(_content)
    if len(song_data) <= 0:
        return data
    logger.debug(song_data)
    song_data = json.loads(song_data[0])
    if 'disabled' in song_data and song_data['disabled'] == 1:
        data['message'] = ERROR_MESSAGE_OFF_LINE
    return data
