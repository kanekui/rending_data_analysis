import openpyxl
from RendingDTO import RendingDataSet
import IExecutable
import RendingDTO


class ReadFromExcelCommand(IExecutable):

    def execute(self, dto: RendingDataSet) -> RendingDataSet:

        # ヘッダー行を取得
        headers = [cell.value for cell in dto.worksheet]

        # データを格納するリストを作成
        data_list = []

        # データ行を取得
        for row in dto.worksheet.iter_rows(min_row=2, values_only=True):
            code = row[0][:4]
            existing_data = next((data for data in data_list if data.code == code), None)

            if existing_data:
                existing_data.outstanding_sales += row[1]
                existing_data.outstanding_purchases += row[4]
            else:
                data = RendingDTO(
                    code=code,
                    outstanding_sales=row[1],
                    daily_change_sales=row[2],
                    ratio_to_listed_sales=row[3],
                    outstanding_purchases=row[4],
                    daily_change_purchases=row[5],
                    ratio_to_listed_purchases=row[6],
                    sale_purchase_ratio=row[7]
                )
                data_list.append(data)



        return dto
