import openpyxl
import xlrd


def read_data(filename: str):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name('伴奏数据')
    for i in range(sheet.nrows):
        yield sheet.row_values(i)


if __name__ == '__main__':
    filenames = ['data/xxxxxxxx.xlsx', '123123123123xxxxxxsadasd.xlsx', ]
    new_workbook = openpyxl.Workbook()
    new_sheet = new_workbook.create_sheet('伴奏列表', 0)

    for fn in filenames:
        for item in read_data(fn):
            new_sheet.append(item)

    new_workbook.save("伴奏列表2.xlsx")


