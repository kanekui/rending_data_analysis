import os
import pandas as pd
from IExecutable import IExecutable
from RendingDTO import RendingDataSet

#日証協のexcelファイル(xls)をxlsxファイルに変換するコマンドクラス
#openpyxlがxlsxファイルしか読めないため、そのためだけにpandasで変換…
class ConvertXLSCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        file_path = dto.nisshokyo_file_path

        # ファイル名と拡張子を取得
        file_name, extension = os.path.splitext(file_path)

        # 新しいファイルパスを生成
        new_file_path = file_name + ".xlsx"

        # XLSファイルを読み込んでDataFrameに変換
        df = pd.read_excel(file_path, sheet_name=None)

        # DataFrameを新しいExcelファイルに書き込む
        with pd.ExcelWriter(new_file_path) as writer:
            for sheet_name, sheet_data in df.items():
                sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

        # RendingDataSetのファイルパスを更新
        dto.nisshokyo_file_path = new_file_path

        return dto