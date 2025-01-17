import unittest
from spider.detail.lyric import find_content, query_lyric
from spider.detail.info import query_info
from spider.search.song_list import *
import json


class TestCase(unittest.TestCase):

    def test_query_lyric(self):
        result = query_lyric('004IUrvw1Sm2Mp', 4929707)
        print(result)
        self.assertEqual(result['lyric'], '余光中')
        self.assertEqual(result['song'], 'Cheon Seong Ill')
        self.assertEqual(result['arranging'], '')

    @classmethod
    def find_content(cls, content: str):
        return find_content(content)

    def test_query_page(self):
        data = query_info('0039BM8G2UmFvZ')
        self.assertEqual(data['company'], '金牌大风')
        self.assertEqual(data['genre'], 'Pop')
        self.assertEqual(data['lan'], '国语')

    def test_search(self):
        result, _ = search('屋顶 周杰伦 温岚')
        d = {
            'beat_name': '屋顶',
            'singer': '周杰伦',
            'singer1': '温岚',
            'singer2': '',
        }
        print(result)
        for i, res in enumerate(result):
            t = compare(res, d, 0)
            print(t)

    def test_search23(self):
        result, _ = search('屋顶 温岚 周杰伦')
        d = {
            'beat_name': '屋顶',
            'singer': '温岚',
            'singer1': '周杰伦',
            'singer2': '',
        }
        print(result)
        for i, res in enumerate(result):
            t = compare(res, d, 1)
            print(t)

    def test_search2(self):
        result, _ = search('点烟 china blue 伍佰')
        print(json.dumps(result))
        d = {
            'beat_name': '点烟',
            'singer': 'china blue',
            'singer1': '伍佰',
            'singer2': '',
        }
        print(result)
        for res in result:
            t = compare(res, d)
            print(t)

    def test_compare(self):
        info = {
            'name': '妙妙妙', 'singer': ['徐怀钰'], 'mid': '004IUrvw1Sm2Mp', 'music_id': 4929707
        }
        data = {'beat_id': 1, 'beat_name': '妙妙妙', 'singer': '徐怀钰', 'singer1': '', 'singer2': ''}
        mid, music_id, ok = compare(info, data)
        self.assertEqual(mid, '004IUrvw1Sm2Mp')
        self.assertEqual(music_id, 4929707)
        self.assertEqual(ok, True)

    def test_query_info(self):
        info = query_info('001rvKQX16P0mO')
        print(info)

    def test_compare2(self):
        data = {'beat_id': 1, 'beat_name': 'cheers', 'singer': 'rihanna', 'singer1': '', 'singer2': ''}
        result = {}
        print(get_keywords(data))
        for infos in get_keywords(data):
            search_result, ok = search(' '.join(infos))
            print((' '.join(infos), search_result, ok))
            if not ok:
                continue
            for items in search_result:
                print(items)
                mid, music_id, ok = compare(items, parse_singer(infos))
                if not ok:
                    continue
                logger.info('=' * 20)
                for k, v in query_info(mid).items():
                    if k in result and len(result[k]) > 0:
                        result[k] += '#' + v
                    else:
                        result[k] = v
                break
        print(result)
