import openpyxl
import win32com.client

from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

#
#
#


class ExecuteDescendCommand(IExecutable):

    SHEET_NAME = "Rending Ratio"
    # TARGET_COLUMN = "D"
    TARGET_WIDTH = 17.73

    def execute(self, dto: RendingDataSet) -> RendingDataSet:

        excel = win32com.client.Dispatch("Excel.Application")

        # DisplayAlertsを無効化する方法
        excel.Visible = False
        excel.Application.DisplayAlerts = False  # 修正: 正しい方法でプロパティを設定

        filename = "E:\\Finance\\rendinganalysis\\" + dto.out_filepath
        wb = excel.Workbooks.Open(filename)
        sheet = wb.Worksheets(1)

        sheet.Columns("A:X").Sort(Key1=sheet.Range("H2"), Order1=2, Header=1)

        # ワークブックを保存
        wb.Save()
        excel.quit()
        return dto
