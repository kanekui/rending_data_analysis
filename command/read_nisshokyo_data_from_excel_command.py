import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable


class ReadNisshoKyoDataFromExcelCommand(IExecutable):

    DEFAULT_SHEET_NAME = "残高（株券等（上場））"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        dto.excel_workbook = openpyxl.load_workbook(dto.nisshokyo_file_path)
        dto.nisshokyo_worksheet = dto.excel_workbook[self.DEFAULT_SHEET_NAME]
        print(dto.nisshokyo_worksheet)
        return dto
