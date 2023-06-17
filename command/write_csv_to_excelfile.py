import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from datetime import datetime


class WriteToExcelCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        extracted_lines = dto.weekly_outstanding_data

        # ファイル名に年月日を追加
        current_date = datetime.now().strftime("%Y%m%d")
        output_file_path = f'weekly_data_{current_date}.xlsx'

        # Excelファイルにデータを書き込む
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        for line in extracted_lines:
            worksheet.append(line.split(","))
        workbook.save(output_file_path)

        return dto
