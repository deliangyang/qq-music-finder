import xlrd


if __name__ == '__main__':
    work = xlrd.open_workbook('伴奏列表2.xlsx')
    sheet = work.sheet_by_index(0)
    print(sheet.nrows)
    print(sheet.row_values(0))
    print(sheet.row_values(1))
    print(sheet.row_values(sheet.nrows - 1))
