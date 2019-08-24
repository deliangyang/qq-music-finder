import xlrd
import openpyxl


if __name__ == '__main__':
    filename = './data/伴奏列表2.xlsx'
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name('伴奏列表')

    count = 0
    for i in range(sheet.nrows):
        records = sheet.row_values(i)
        if str(records[12]).find('QQ音乐搜索不到该伴奏') >= 0:
            count += 1
    print('count: %d', count)
