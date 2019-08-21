import requests
from spider.header import headers
from spider.utils.logger import logger


params = {
    'ct': 24,
    'qqmusic_ver': 1298,
    'new_json': 1,
    'remoteplace': 'txt.yqq.center',
    'searchid': '41528322314210299',
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


def search(keyword) -> iter:
    """
    查询 歌名和歌手相关信息
    :param keyword:
    :return:
    """
    resp = requests.get(
        url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp',
        params=get_params(keyword),
        headers=headers)
    content = resp.json()
    for item in content['data']['song']['list']:
        data = {
            'name': item['name'],
            'singer': [],
            'mid': item['mid'],
            'music_id': item['id'],
        }
        for singer in item['singer']:
            data['singer'].append(singer['name'])
        yield data


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
    origin_singers = list(filter(lambda x: len(x) > 0, origin_singers))
    if search_src['name'] == origin['beat_name']:
        count = 0
        for singer in origin_singers:
            for s in search_src['singer']:
                if singer == s:
                    count += 1
        if count > 0 and count == len(search_src['singer']):
            return search_src['mid'], search_src['music_id'], True
    return None, 0, False

