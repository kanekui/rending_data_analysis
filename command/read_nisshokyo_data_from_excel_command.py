import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable


class ReadNisshoKyoDataFromExcelCommand(IExecutable):

    DEFAULT_SHEET_NAME = "残高（株券等（上場））"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        workbook = openpyxl.load_workbook(dto.nisshokyo_file_path)
        dto.nisshokyo_worksheet = workbook[self.DEFAULT_SHEET_NAME]
        print(dto.nisshokyo_worksheet)
        return dto
