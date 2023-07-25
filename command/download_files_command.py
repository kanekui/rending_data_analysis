import pandas as pd
from IExecutable import IExecutable
from RendingDTO import RendingDataSet
import requests
import PyPDF2

#JPXのpdfファイルと日証協のexcelファイルをダウンロードしてDTOのファイルパスに格納
class DownloadFilesCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        nisshokyo_file_url = dto.nisshokyo_file_url
        jpx_file_url = dto.pdf_file_url

        # 日証協のExcelファイルをダウンロード
        nisshokyo_response = requests.get(nisshokyo_file_url)
        with open(dto.nisshokyo_file_path, 'wb') as file:
            file.write(nisshokyo_response.content)

        # JPXのPDFファイルをダウンロード
        jpx_response = requests.get(jpx_file_url)
        with open(dto.pdf_file_path, 'wb') as file:
            file.write(jpx_response.content)

        return dto

