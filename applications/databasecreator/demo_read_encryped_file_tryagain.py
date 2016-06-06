# coding=UTF-8

import win32com.client
import xlrd

excel = win32com.client.Dispatch('Excel.Application')
book = excel.Workbooks.open(r'E:\data\exceltest\m10.xls')
print(book)
print(book.Sheets.Count)
print(book.Sheets[0].Cells(7,2).Value)
#sht = book.Worksheets('1-8')
sht = book.Sheets[7]
print(sht.Cells(8,2).Value)
row_number = sht.UsedRange.Rows.Count
column_number = sht.UsedRange.Columns.Count
print(row_number)
print(column_number)
mdata = sht.Range(sht.Cells(1,1),sht.Cells(row_number,column_number)).Value
print(type(mdata))
print(list(mdata))
#book.SaveAs(r'E:\data\exceltest\m5.xlsx')

#xlrd.open_workbook(r'E:\data\exceltest\m5.xlsx')