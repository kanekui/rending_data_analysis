from IExecutable import IExecutable
from RendingDTO import RendingDataSet
import requests
from bs4 import BeautifulSoup
from RendingDTO import RendingDataSet
from IExecutable import IExecutable
import re

#JPXのpdfファイルと日証協のexcelファイルのInput/Outputファイル名を曜日から決めるコマンド
#火曜、木曜、金曜のいずれかが祝日だとファイル名の日付部分がずれる。
#その場合は後段のコマンドでエラーとなる。


class NisshokyoUrlCreateCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/index.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='component-file')

        # ページのHTMLを取得
        response = requests.get(url)
        html = response.text

        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(html, 'html.parser')

        # リンクを抽出する
        links = soup.find_all('a', href=True)

        # "AAA"が最大のリンクを見つける
        max_link = None
        max_value = 0

        for link in soup.find_all('a', href=re.compile(r'./files/.*\.xls')):
            match = re.search(r'/files/(\d+)z\.xls', link['href'])
            if match:
                aaa_value = int(match.group(1))
                if aaa_value > max_value:
                    max_value = aaa_value
                    max_link = link['href']

        dto.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/' + max_link.replace("./files/", "files/")
        print(dto.nisshokyo_file_url)
        return dto

