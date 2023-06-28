import os
import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from datetime import datetime


class SaveToExcelCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        extracted_lines = dto.weekly_outstanding_data

        # ファイル名に年月日を追加
        current_date = datetime.now().strftime("%Y%m%d")
        output_file_path = f'weekly_data_{current_date}.xlsx'

        # 既に同名のファイルが存在する場合、別名で保存する
        counter = 1
        while os.path.exists(output_file_path):
            output_file_name = f'weekly_data_{current_date}_{counter}.xlsx'
            output_file_path = output_file_name
            counter += 1

        workbook = openpyxl.Workbook()
        workbook.copy_worksheet(dto.rending_ratio_worksheet)
        workbook.copy_worksheet(dto.nisshokyo_worksheet)
        workbook.copy_worksheet(dto.jpx_worksheet)

        # ファイルを保存する前にデフォルトの "Sheet" シートを削除する
        if 'Sheet' in workbook.sheetnames:
            workbook.remove(workbook['Sheet'])

        workbook.save(output_file_path)

        return dto
