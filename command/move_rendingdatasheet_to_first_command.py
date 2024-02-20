import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable

#
#
#
class MoveRendingDataSheetToFirstCommand(IExecutable):

    SHEET_NAME = "JPX Data"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        #workbook = openpyxl.load_workbook(dto.out_filepath)
        #print(workbook.worksheets)
        #print(workbook.index(workbook.get_sheet_by_name(self.SHEET_NAME)))
        dto.excel_workbook.move_sheet(self.SHEET_NAME, offset=+2)
        dto.excel_workbook.save(dto.out_filepath)
        return dto
