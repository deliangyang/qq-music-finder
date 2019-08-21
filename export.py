import json
import re
import xlwt


def parse_data(data: str) -> str:
    items = list(set(filter(lambda x: len(x) > 0, data.split('#'))))
    return '#'.join(items).strip()


def parse_content(content: str) -> str:
    count = 0
    _content = ''
    for s in content:
        if s == '\"' and count > 0:
            count -= 1
        elif s == '\"':
            count += 1
        if count > 0 and s == "\'":
            _content += '^'
        else:
            _content += s
    return _content.replace('\'', '"').replace('\\xa0', ' ').replace('^', '')


def parse_cols(ct: {}) -> (list, bool):
    record = ct['record']
    company = parse_data(record['company'])
    lan = parse_data(record['lan'])
    pub_time = parse_data(record['pub_time'])
    lyric = parse_data(record['lyric'])
    genre = parse_data(record['genre'])
    song = parse_data(record['song'])
    arranging = parse_data(record['arranging'])
    message = parse_data(record['message'])

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
    has_fail = False
    if len(company) <= 0 and len(genre) <= 0 and len(lan) <= 0 and len(pub_time) <= 0:
        has_fail = True
    return _cols, has_fail


if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding='utf-8')
    work_sheet = workbook.add_sheet('伴奏数据')
    work_sheet2 = workbook.add_sheet('需要重新跑的')

    alignment = xlwt.Alignment()
    alignment.wrap = 1
    alignment.horz = 0x02
    style2 = xlwt.XFStyle()
    style2.alignment = alignment

    cols = ['伴奏ID', '伴奏名称', '歌手', '歌手1', '歌手2', '唱片公司', '流派', '语种', '发行时间', '词', '曲', '编曲', '失败原因']
    for index, col in enumerate(cols):
        work_sheet.write(0, index, col)
        work_sheet2.write(0, index, col)

    re_tag = re.compile(r'\w(")[\w\s]')
    total = 0
    total2 = 0
    with open('query.log', 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            if line.find("'target': 'records'") > 0:
                try:
                    content = parse_content(line[55:])
                    content = json.loads(content)
                    if 'record' in content:
                        cols, has_fail = parse_cols(content)
                        if has_fail:
                            total2 += 1
                            for index, col in enumerate(cols):
                                work_sheet2.write(total2, index, col)
                        total += 1
                        for index, col in enumerate(cols):
                            work_sheet.write(total, index, col)
                except Exception as e:
                    print('xx' * 20)
                    print(line[55:])
                    print(content)
                    raise e
        workbook.save("data.xls")
