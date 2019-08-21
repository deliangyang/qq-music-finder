import requests
from spider.reg import *
from spider.header import headers
from spider.utils.logger import logger


params = {
    'nobase64': 1,
    'musicid': 7365,
    '-': 'jsonp1',
    'g_tk': 5381,
    'loginUin': 0,
    'format': 'json',
    'inCharset': 'utf8',
    'outCharset': 'utf8',
    'notice': 0,
    'platform': 'yqq.json',
    'needNewCode': 0,
}


def query_lyric(mid: str, music_id: int) -> {}:
    """
    查找歌词
    :param mid:
    :param music_id:
    :return: {}
    """
    headers['Referer'] = 'https://y.qq.com/n/yqq/song/%s.html' % mid
    req = requests.get(
        url='https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg',
        params=get_params(music_id),
        headers=headers)
    logger.debug('url: %s' % req.url)
    content = req.json()
    result = find_content(content['lyric'])
    return result


def get_params(music_id: int) -> object:
    params['musicid'] = music_id
    return params


def find_content(content: str):
    data = {
        'lyric': '',
        'song': '',
        'arranging': '',
    }
    for item in re_split_brackets.split(content):
        if item.startswith('词：'):
            data['lyric'] = re_tag.sub(' ', item.replace('词：', '')).strip()
        elif item.startswith('曲：'):
            data['song'] = re_tag.sub(' ', item.replace('曲：', '')).strip()
        elif item.startswith('编曲：'):
            data['arranging'] = re_tag.sub(' ', item.replace('编曲：', '')).strip()
    return data
