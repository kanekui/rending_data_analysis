import openpyxl
import win32com.client

from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

#
#
#


class ReSaveCommand(IExecutable):

    SHEET_NAME = "Rending Ratio"
    TARGET_COLUMN = "D"
    TARGET_WIDTH = 17.73

    def execute(self, dto: RendingDataSet) -> RendingDataSet:

        filepath = "E:\\Finance\\rendinganalysis\\" + dto.out_filepath
        wb = openpyxl.load_workbook(filepath)

        new_file_path = filepath + "_temp"
        wb.save(new_file_path)

        import os
        os.remove(filepath)
        os.rename(new_file_path, filepath)

        return dto
