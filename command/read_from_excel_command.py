import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable

#
# JPXの銘柄別信用取引週末残高のpdfファイルの表部分をExcel化する
#
class ReadFromExcelCommand(IExecutable):

    DEFAULT_SHEET_NAME = "個別銘柄信用取引残高"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        workbook = openpyxl.load_workbook(dto.pdf_file_path)
        dto.jpx_worksheet = workbook[self.DEFAULT_SHEET_NAME]
        print(dto.jpx_worksheet)
        return dto
