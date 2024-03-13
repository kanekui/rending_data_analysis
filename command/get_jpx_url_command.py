import requests
from bs4 import BeautifulSoup
from RendingDTO import RendingDataSet
from IExecutable import IExecutable

#JPXのpdfファイルと日証協のexcelファイルのInput/Outputファイル名を曜日から決めるコマンド
#火曜、木曜、金曜のいずれかが祝日だとファイル名の日付部分がずれる。
#その場合は後段のコマンドでエラーとなる。


class JPXUrlCreateCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/05.html'
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

        for link in links:
            href = link['href']
            # リンクが特定のパターンを満たす場合に処理
            if "/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu" in href:
                # リンク内の"AAA"の値を取得
                aaa_value = href.split("syumatsu")[1].split(".pdf")[0]
                # "AAA"の値が数値であるか確認
                if aaa_value.isdigit():
                    # 数値に変換して比較
                    aaa_value = int(aaa_value)
                    if aaa_value > max_value:
                        max_value = aaa_value
                        max_link = href


        dto.pdf_file_url = f'https://www.jpx.co.jp' + max_link

        return dto

