import xlrd
import openpyxl


if __name__ == '__main__':
    filename = 'test12312312313.xlsx'
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name('伴奏数据')

    new_workbook = openpyxl.Workbook()
    new_worksheet = new_workbook.create_sheet('伴奏数据', 0)
    new_worksheet2 = new_workbook.create_sheet('伴奏数据2', 1)

    for i in range(sheet.nrows):
        records = sheet.row_values(i)
        if str(records[12]).find('QQ音乐搜索不到该伴奏') >= 0:
            new_worksheet.append(records)
        else:
            new_worksheet2.append(records)
    new_workbook.save('./data/xxxxxxxx.xlsx')
