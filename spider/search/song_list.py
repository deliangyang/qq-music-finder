import requests
from spider.header import headers
from spider.utils.logger import logger
from urllib.parse import urlencode
from spider.error import with_error_stack
from spider.reg import replace_tag


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
    :param search_src: 搜索结构的数据 { name: 'xx', singer: [] }
    :param origin: 输入数据，excel { beat_name: 'xx', singer: [] }
    :return: (str, int, bool)
    """
    logger.debug({
        'search_src': search_src,
        'origin': origin,
    })
    origin['singer'] = list(map(replace_tag, origin['singer']))
    search_src['singer'] = list(map(replace_tag, search_src['singer']))
    search_name = replace_tag(search_src['name'])
    beat_name = replace_tag(origin['beat_name'])
    # logger.error({
    #     'type': 'name',
    #     'origin': beat_name,
    #     'search': search_name,
    # })
    if search_name == beat_name:
        if _compare_singer(origin['singer'], search_src['singer']):
            return search_src['mid'], search_src['music_id'], True
    return None, 0, False


def _compare_singer(origin_singers: list, search_singers: list) -> bool:
    # logger.error({
    #     'type': 'singer',
    #     'origin': '#'.join(origin_singers),
    #     'search': '#'.join(search_singers),
    # })
    if len(origin_singers) == len(search_singers) and len(origin_singers) <= 2:
        return origin_singers == search_singers
    else:
        count = 0
        for singer in origin_singers:
            for s in search_singers:
                if singer == s:
                    count += 1
        if count > 0 and count == len(origin_singers):
            return True
    return False


def get_keywords(data: {}) -> list:
    singers = [data['singer'], data['singer1'], data['singer2']]
    result = []
    try:
        singers = list(filter(lambda x: x and len(x) > 0, singers))
        if len(singers) == 2:
            result = [
                [data['beat_name'], singers[0], singers[1]],
                [data['beat_name'], singers[1], singers[0]],
            ]
        else:
            singers.insert(0, data['beat_name'])
            result = [singers]
    except Exception as e:
        print(e, singers, data)
    return result


def parse_singer(data: list):
    try:
        return {
            'beat_name': data[0],
            'singer': data[1:],
        }
    except Exception as e:
        print(e, data)
