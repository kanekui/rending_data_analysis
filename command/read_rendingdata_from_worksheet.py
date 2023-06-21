import openpyxl
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from RendingDTO import RendingDTO


class ReadFromRendingDataFromWorksheetCommand(IExecutable):

    def execute(self, dto: RendingDataSet) -> RendingDataSet:

        # ヘッダー行を取得
        #print(dto.worksheet[1])
        # headers = [cell.value for cell in dto.jpx_worksheet[1]]

        headers = ["銘柄名", "コード", "売り残高＋貸株残高", "貸付残高", "売残高", "貸株残高", "売残高前週比", "貸株残高前週比", "買残高", "買残高前週比", "一般信用売残高", "一般信用売残高前週比", "制度信用売残高", "制度信用売残高前週比", "一般信用買残高", "一般信用買残高前週比", "制度信用買残高", "一般信用買残高前週比"]
        print(headers)

        # データを格納するリストを作成
        data_list = []

        # データ行を取得
        for row in dto.jpx_worksheet.iter_rows(min_row=2, values_only=True):
            print(row)
            code = row[2][:4]
            # print(code)
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
