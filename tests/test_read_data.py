import unittest
from spider.read_data import ReadData
from spider.export import Export


class ReadDataTestCase(unittest.TestCase):

    def test_read_data(self):
        beat_id = 4
        read_data = ReadData("../data.xlsx", beat_id)
        for item in read_data.iter():
            self.assertEqual(beat_id + 1, item['beat_id'])
            break

    def test_convert2(self):
        export = Export()
        res = export.convert("{'target': 'records', 'thread': 'thread-1', 'record': {'beat_id': 977160, "
                             "'beat_name': 'They Just Can\\'t Stop It The ', 'singer': 'The Spinners', 'singer1': "
                             "'', 'singer2': '', "
                             "'company': '', 'genre': '', 'lan': '', 'pub_time': '', 'lyric': '', 'song': '',"
                             " 'arranging': "
                             "'', 'message': 'QQ音乐搜索不到该伴奏'}}")
        print(res)
