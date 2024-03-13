import pandas as pd
from IExecutable import IExecutable
from RendingDTO import RendingDataSet
import requests
import os

#JPXのpdfファイルと日証協のexcelファイルをダウンロードしてDTOのファイルパスに格納
class DownloadFilesCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        nisshokyo_file_url = dto.nisshokyo_file_url
        jpx_file_url = dto.pdf_file_url

        print(jpx_file_url)

        current_folder_path = os.getcwd()
        dto.nisshokyo_file_path = current_folder_path + "//" + nisshokyo_file_url.split("/")[-1]
        dto.pdf_file_path = current_folder_path + "//" + jpx_file_url.split("/")[-1]

        # 日証協のExcelファイルをダウンロード
        nisshokyo_response = requests.get(nisshokyo_file_url)
        with open(dto.nisshokyo_file_path, 'wb') as file:
            file.write(nisshokyo_response.content)

        # JPXのPDFファイルをダウンロード
        jpx_response = requests.get(jpx_file_url)
        with open(dto.pdf_file_path, 'wb') as file:
            file.write(jpx_response.content)

        return dto

