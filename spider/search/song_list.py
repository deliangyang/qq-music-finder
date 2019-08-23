import requests
import json
from spider.header import headers
from spider.utils.logger import logger
from urllib.parse import urlencode
from spider.error import with_error_stack
from spider.error import ERROR_MESSAGE_FORBIDDEN

params = {
    'ct': 24,
    'qqmusic_ver': 1298,
    'new_json': 1,
    'remoteplace': 'txt.yqq.center',
    'searchid': '52946548694911179',
    't': 0,
    'aggr': 1,
    'cr': 1,
    'catZhida': 1,
    'lossless': 0,
    'flag_qc': 0,
    'p': 1,
    'n': 10,
    'w': '',
    'g_tk': 5381,
    'loginUin': 0,
    'hostUin': 0,
    'format': 'json',
    'inCharset': 'utf8',
    'outCharset': 'utf8',
    'notice': 0,
    'platform': 'yqq.json',
    'needNewCode': 0,
}


def get_params(keyword: str) -> {}:
    params['w'] = keyword
    return params


def search(keyword) -> (list, bool):
    """
    查询 歌名和歌手相关信息
    :param keyword:
    :return:
    """
    resp = requests.get(
        url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp',
        params=urlencode(get_params(keyword)),
        headers=headers)
    try:
        content = resp.json()
    except Exception as e:
        logger.error(with_error_stack(e))
        logger.debug("keyword: %s, content: %", resp.content.decode('utf-8'))
        return []
    result = []

    if 'message' in content and content['message'] == 'query forbid':
        return [], False

    try:
        for item in content['data']['song']['list']:
            data = {
                'name': item['name'],
                'singer': [],
                'mid': item['mid'],
                'music_id': item['id'],
            }
            for singer in item['singer']:
                data['singer'].append(singer['name'])
            result.append(data)
    except Exception as e:
        logger.error(with_error_stack(e))
        return [], True
    logger.debug(result)
    return result, True


def compare(search_src: {}, origin: {}) -> (str, int, bool):
    """
    比较搜索结果
    :param search_src: 搜索结构的数据
    :param origin: 输入数据，excel
    :return: (str, int, bool)
    """
    logger.debug({
        'search_src': search_src,
        'origin': origin,
    })
    origin_singers = [origin['singer'], origin['singer1'], origin['singer2']]
    origin_singers = list(map(lambda x: str(x).lower().strip(), filter(lambda x: len(x) > 0, origin_singers)))
    search_src['singer'] = list(map(lambda x: str(x).lower().strip(), search_src['singer']))
    if str(search_src['name']).replace(' ', '').lower() == str(origin['beat_name']).replace(' ', ''):
        count = 0
        for singer in origin_singers:
            for s in search_src['singer']:
                if singer == s:
                    count += 1
        if count > 0 and count == len(origin_singers):
            return search_src['mid'], search_src['music_id'], True
    return None, 0, False

