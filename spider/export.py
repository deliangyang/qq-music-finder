import re
import openpyxl
import json


class Export(object):

    def __init__(self):
        self.re_escape = re.compile(r'\\x[a-z0-9]{2}', re.I)
        self.re_tag = re.compile(r'\w(")[\w\s]')

    def export_data(self, logfile: str, filename: str):
        workbook = openpyxl.Workbook()
        work_sheet = workbook.create_sheet('伴奏数据', 0)
        cols = ['伴奏ID', '伴奏名称', '歌手', '歌手1', '歌手2', '唱片公司',
                '流派', '语种', '发行时间', '词', '曲', '编曲', '失败原因']
        work_sheet.append(cols)

        total = 0
        with open(logfile, 'rb') as f:
            for line in f.readlines():
                line = line.decode('utf-8')
                if line.find("'target': 'records'") > 0:
                    try:
                        content = self.convert(line[55:])
                        content = json.loads(content)
                        if 'record' in content:
                            cols, _has_fail = self.parse_cols(content)
                            if not _has_fail:
                                total += 1
                                work_sheet.append(cols)
                    except Exception as e:
                        raise e
            workbook.save(filename)

    @classmethod
    def parse_data(cls, data: str) -> str:
        items = list(set(filter(lambda x: len(x) > 0, data.split('#'))))
        return '#'.join(items).strip()

    def convert(self, ct: str) -> str:
        src = self.re_escape.sub('', ct).replace('""', '')
        print(src)
        src = src.replace('Cat\'t', 'Cat"t')
        ll = len(src)
        new_src = ''
        start = 0
        for i, s in enumerate(src):
            if s == '\'' and start > 0:
                s = '^'
            if i > 1 and src[i-1] == ' ' and src[i - 2] == ':' and s == '"' and start == 0:
                start += 1
                s = "'"
            elif i < ll - 2 and src[i+1] == ',' and src[i+2] == ' ' and s == '"' and start > 0:
                start -= 1
                s = "'"
            elif s == '"':
                s = "'"

            if 0 < i < ll-3 and s == '\'':
                if src[i-1] == '{':
                    new_src += '"'
                elif i > 2 and src[i-1] == ' ' and (src[i-2] == ':' or src[i-2] == ','):
                    new_src += '"'
                elif src[i+1] == '}':
                    new_src += '"'
                elif (src[i+1] == ':' or src[i+1] == ',') and src[i+2] == ' ':
                    new_src += '"'
                else:
                    new_src += s
            else:
                new_src += s
        new_src = new_src.replace("\\'", "'")
        print(new_src)
        return new_src.replace('^', '')

    def parse_cols(self, ct: {}) -> (list, bool):
        record = ct['record']
        company = self.parse_data(record['company'])
        lan = self.parse_data(record['lan'])
        pub_time = self.parse_data(record['pub_time'])
        lyric = self.parse_data(record['lyric'])
        genre = self.parse_data(record['genre'])
        song = self.parse_data(record['song'])
        arranging = self.parse_data(record['arranging'])
        message = self.parse_data(record['message'])

        if message == 'QQ音乐无唱片公司信息#QQ音乐已下架' \
                or message == 'QQ音乐无唱片公司信息#因QQ音乐无版权下架' \
                or message == 'QQ音乐已下架#QQ音乐无唱片公司信息':
            message = '因QQ音乐无版权下架'

        _cols = [
            record['beat_id'],
            record['beat_name'],
            record['singer'],
            record['singer1'],
            record['singer2'],
            company, genre, lan, pub_time, lyric, song, arranging, message,
        ]
        _has_fail = False
        if len(company) <= 0 and len(genre) <= 0 and len(lan) <= 0 and len(pub_time) <= 0:
            _has_fail = True
        return _cols, _has_fail
