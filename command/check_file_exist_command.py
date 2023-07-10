import pandas as pd
from IExecutable import IExecutable
from RendingDTO import RendingDataSet
import PyPDF2

#JPXのpdfファイルと日証協のexcelファイルが存在していることを確認する
class CheckFileExistCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        nisshokyo_file_path = dto.nisshokyo_file_path
        jpx_file_path = dto.pdf_file_path

        # XLSファイルを読み込んでDataFrameに変換
        df = pd.read_excel(nisshokyo_file_path, sheet_name=None)

        # PDFファイルを読み込む
        with open(jpx_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

        return dto

