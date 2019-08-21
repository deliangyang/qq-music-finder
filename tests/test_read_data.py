import unittest
from spider.read_data import ReadData


class ReadDataTestCase(unittest.TestCase):

    def test_read_data(self):
        beat_id = 4
        read_data = ReadData("../data/伴奏列表.xlsx", beat_id)
        for item in read_data.iter():
            self.assertEqual(beat_id + 1, item['beat_id'])
            break
