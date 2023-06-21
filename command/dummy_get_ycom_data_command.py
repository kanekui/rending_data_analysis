import requests
from RendingDTO import RendingDataSet, RendingDTO, YApiDTO
from IExecutable import IExecutable
from datetime import datetime

YAPIurl = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=defaultKeyStatistics"
YAPIparams = {
    "formatted": "true",
    "crumb": "n5ltp3OQjEJ",
    "lang": "en-US",
    "region": "US",
    "modules": "defaultKeyStatistics",
    "corsDomain": "finance.yahoo.com",
}


class DummyGetYComDataCommand(IExecutable):
    def get_yresponse(self, symbol):
        endpoint_url = YAPIurl.format(symbol=symbol)
        response = requests.get(endpoint_url, params=YAPIparams, headers={'User-agent': 'Mozilla/5.0'})
        return response

    def get_jsondata(self, response) -> YApiDTO:
        json_data = response.json()
        try:
            float_shares = json_data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["floatShares"]["raw"]
            shares_outstanding = json_data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["sharesOutstanding"][
                "raw"]
            data = YApiDTO(float_shares=float_shares, shares_outstanding=shares_outstanding)
        except (KeyError, TypeError):
            data = YApiDTO(float_shares=0, shares_outstanding=0)
        return data

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        stock_list = dto.stock_list
        # print(dto.stock_list)

        for rending_dto in stock_list:
            code = rending_dto.code
            symbol = str(code) + ".T"
            response = self.get_yresponse(symbol)
            yapi_data = self.get_jsondata(response)

            # 取得したデータをRendingDTOに追加
            rending_dto.float_shares = yapi_data.float_shares
            rending_dto.shares_outstanding = yapi_data.shares_outstanding

            print(rending_dto.float_shares)
            print(rending_dto.shares_outstanding)

            if yapi_data.float_shares == 0:
                rending_dto.ratio_to_float_sales = 0
                rending_dto.ratio_to_float_purchases = 0
            else:
                rending_dto.ratio_to_float_sales = rending_dto.outstanding_sales / yapi_data.float_shares
                rending_dto.ratio_to_float_purchases = rending_dto.outstanding_purchases / yapi_data.float_shares

            if yapi_data.shares_outstanding == 0:
                rending_dto.ratio_to_shares_outstanding_sale = 0
                rending_dto.ratio_to_shares_outstanding_purchases = 0
            else:
                rending_dto.ratio_to_shares_outstanding_sale = rending_dto.outstanding_sales / yapi_data.shares_outstanding
                rending_dto.ratio_to_shares_outstanding_purchases = rending_dto.outstanding_purchases / yapi_data.shares_outstanding

            break

        # print("\n===\n")
        print(len(dto.stock_list))

        return dto
