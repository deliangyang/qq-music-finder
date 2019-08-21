import xlrd


class ReadData(object):

    def __init__(self, filename: str, start_beat_id: int = 1):
        self.filename = filename
        self.start_beat_id = start_beat_id
        self.workbook = xlrd.open_workbook(self.filename)
        self.worksheet = self.workbook.sheet_by_index(0)

    def iter(self):
        for i in range(self.start_beat_id + 1, self.worksheet.nrows):
            record = self.worksheet.row_values(i)
            yield {
                'beat_id': int(record[0]),
                'beat_name': str(record[1]).replace('.0', ''),
                'singer': str(record[2]).replace('.0', ''),
                'singer1': str(record[3]).replace('.0', ''),
                'singer2': str(record[4]).replace('.0', ''),
            }
