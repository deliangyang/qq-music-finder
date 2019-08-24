import openpyxl
import xlrd


def read_data(filename: str, index: int):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(index)
    for i in range(sheet.nrows):
        yield sheet.row_values(i)


if __name__ == '__main__':
    filenames = [('data/split_20190823.xlsx', 1), ('123123123123xxxxxxsadasd.xlsx', 0), ]
    new_workbook = openpyxl.Workbook()
    new_sheet = new_workbook.create_sheet('伴奏列表', 0)

    for (fn, index) in filenames:
        for item in read_data(fn, index):
            new_sheet.append(item)

    new_workbook.save("伴奏列表2.xlsx")


