import xlrd
from spider.reg import replace


class ReadData(object):

    def __init__(self, filename: str, start_beat_id: int = 1):
        self.filename = filename
        self.start_beat_id = start_beat_id
        self.workbook = xlrd.open_workbook(self.filename)
        self.worksheet = self.workbook.sheet_by_index(0)

    def iter(self):
        for i in range(0, self.worksheet.nrows):
            record = self.worksheet.row_values(i)
            try:
                beat_id = int(record[0])
            except Exception as _:
                beat_id = 0
            if beat_id > self.start_beat_id:
                yield {
                    'beat_id': int(record[0]),
                    'beat_name': replace(record[1]),
                    'singer': replace(record[2]),
                    'singer1': replace(record[3]),
                    'singer2': replace(record[4]),
                }
