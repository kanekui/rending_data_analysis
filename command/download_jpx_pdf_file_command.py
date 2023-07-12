import requests
from bs4 import BeautifulSoup
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
import re
import time


#  発行済み株数、浮動株数を取得するコマンドクラス
#  dtoとして渡されるRendingDataSet内のRendingDTO毎に発行済み株数、浮動株数を値を取得し、
#  そのRendingDTOに格納する。
class GetFloatAndOutstandingCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        url = f'https://www.trkd-asia.com/rakutensec/quote.jsp?ric=7692.T&c=ja&ind=2'
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='component-file')

        target_th = soup.find('th', text='発行済株式数')

        # 見つかった<th>要素の次の<td>要素の値を取得する
        if target_th:
            next_td = target_th.find_next('td')
            value = next_td.text
            # カンマを取り除いて数値に変換
            value = re.sub(r'[^\d.]', '', value)
            print(value)

            target_th = soup.find('th', text='浮動株数')

        # 見つかった<th>要素の次の<td>要素の値を取得する
        if target_th:
            next_td = target_th.find_next('td')
            value = next_td.text
            # カンマを取り除いて数値に変換
            value = re.sub(r'[^\d.]', '', value)
            print(value)

        return dto
