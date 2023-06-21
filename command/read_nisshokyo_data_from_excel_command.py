import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable


class ReadNisshoKyoDataFromExcelCommand(IExecutable):

    DEFAULT_SHEET_NAME = "残高（株券等（上場））"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        workbook = openpyxl.load_workbook(dto.nisshoukyo_file_path)
        dto.jpx_worksheet = workbook[self.DEFAULT_SHEET_NAME]
        print(dto.nisshoukyo_worksheet)
        return dto
