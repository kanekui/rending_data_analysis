import requests
from bs4 import BeautifulSoup
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
import re
import time

class GetFloatAndOutstandingCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        for stock in dto.stock_list:
            print(stock.code)
            url = f'https://www.trkd-asia.com/rakutensec/quote.jsp?ric={stock.code}.T&c=ja&ind=2'
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', class_='js-table-values')

            target_th = soup.find('th', text='発行済株式数')

            # 見つかった<th>要素の次の<td>要素の値を取得する
            if target_th:
                next_td = target_th.find_next('td')
                value = next_td.text
                # カンマを取り除いて数値に変換
                value = re.sub(r'[^\d.]', '', value)
                stock.stock_shares_outstanding = value
                print(stock.stock_shares_outstanding)

            target_th = soup.find('th', text='浮動株数')

            # 見つかった<th>要素の次の<td>要素の値を取得する
            if target_th:
                next_td = target_th.find_next('td')
                value = next_td.text
                # カンマを取り除いて数値に変換
                value = re.sub(r'[^\d.]', '', value)
                stock.stock_float = value
                print(stock.stock_float)

            time.sleep(3)  # 3秒待機

        return dto
