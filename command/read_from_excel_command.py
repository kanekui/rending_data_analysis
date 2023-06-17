import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable


class ReadFromExcelCommand(IExecutable):

    DEFAULT_SHEET_NAME = "個別銘柄信用取引残高"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        workbook = openpyxl.load_workbook(dto.pdf_file_path)
        dto.worksheet = workbook[self.DEFAULT_SHEET_NAME]
        print(dto.worksheet)
        return dto
