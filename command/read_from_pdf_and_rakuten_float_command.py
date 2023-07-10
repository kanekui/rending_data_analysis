import PyPDF2
from RendingDTO import RendingDataSet, RendingDTO
from IExecutable import IExecutable
import requests
from bs4 import BeautifulSoup
import re
import time


class ReadFromPDFAndRakutenCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        file_path = dto.pdf_file_path

        # PDFファイルを読み込む
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text_content = ''
            for page in reader.pages:
                text_content += page.extract_text()

        # "B"で始まる行の抽出とカンマとスペースの置き換え
        lines = text_content.split('\n')
        extracted_lines = []
        extracter_lines_for_rendingdto = []
        header_line = '銘柄名,コード,新証券コード,売残高,売残高前週比,買残高,買残高前週比,一般信用売残高,一般信用売残高前週比,制度信用売残高,制度信用売残高前週比,一般信用買残高,一般信用買残高前週比,制度信用買残高,一般信用買残高前週比'
        extracted_lines.append(header_line)


        for line in lines:
            if '普通株式' in line:
                line = line.replace(',', '').replace(' ', ',')
                line = line.replace('▲,', '-')
                if '銘柄別信用取引週末残高' in line:
                    start_index = line.index('銘柄別信用取引週末残高')
                    line = line[:start_index] + line[start_index:].replace(line[start_index:], '')
                extracter_lines_for_rendingdto.append(line.split(','))
                # print(extracter_lines_for_rendingdto)
                #print(extracter_lines_for_rendingdto[0])
                extracted_lines.append(','.join(line.split(',')))  # 行をカンマで結合して格納する

        # RendingDTOの作成とRendingDataSetへの格納
        stock_list = []

        for line in extracter_lines_for_rendingdto:
            if len(line) < 7:
                continue
            if str(line[1])[-1] == '0':
                code = int(line[1][0:4])
            else:
                code = None

            print(f'code = {code}')

            if code is not None:
                if line[5] == '0':
                    sale_purchase_ratio = 0
                else:
                    sale_purchase_ratio = int(line[3]) / int(line[5])

                rendingdto = RendingDTO(
                    # Bを削除し、全角スペースを除去して銘柄名を取得する
                    name=line[0].replace("B", "").replace("　", "").split("普通株式")[0],
                    code=code,
                    outstanding_sales=int(line[3]),
                    weekly_change_sales=line[4],
                    outstanding_purchases=int(line[5]),
                    weekly_change_purchases=line[6],
                    sale_purchase_ratio=sale_purchase_ratio,
                    stock_float=0,
                    stock_shares_outstanding=0,
                    ratio_to_float_sales=0.0,
                    ratio_to_float_purchases=0.0,
                    ratio_to_shares_outstanding_purchases=0.0,
                    ratio_to_shares_outstanding_sale=0.0
                )
                get_rakten_float_and_outstanding(rendingdto)
                print(rendingdto.code)
                dto.stock_list[int(rendingdto.code)] = rendingdto
                # print(dto.stock_list[int(rendingdto.code)])

        dto.weekly_outstanding_data = extracted_lines
        # print(dto.stock_list)

        return dto


def get_rakten_float_and_outstanding(dto: RendingDTO) -> RendingDTO:
    print(dto.code)
    url = f'https://www.trkd-asia.com/rakutensec/quote.jsp?ric={dto.code}.T&c=ja&ind=2'
    print(url)
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', class_='js-table-values')

            target_th = soup.find('th', text='発行済株式数')

            # 見つかった<th>要素の次の<td>要素の値を取得する
            if target_th:
                next_td = target_th.find_next('td')
                value = next_td.text
                # カンマを取り除いて数値に変換
                value = re.sub(r'[^\d.]', '', value)
                value = value[:-2]  # ".0"を削除
                dto.stock_shares_outstanding = int(value)  # 整数に変換して格納
                if dto.code == "7692":
                    print(dto.stock_shares_outstanding)

            target_th = soup.find('th', text='浮動株数')

            # 見つかった<th>要素の次の<td>要素の値を取得する
            if target_th:
                next_td = target_th.find_next('td')
                value = next_td.text
                # カンマを取り除いて数値に変換
                value = re.sub(r'[^\d.]', '', value)
                value = value[:-2]  # ".0"を削除
                dto.stock_float = int(value)  # 整数に変換して格納
                if dto.code == "7692":
                    print(dto.stock_float)

            # time.sleep(1)  # 3秒待機
            return dto
        except requests.Timeout:
            print(f'Request timed out. Retrying ({retry_count+1}/{max_retries})...')
            retry_count += 1
            time.sleep(10)  # 1秒待機してからリトライ
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return dto
    print(f'Retries exceeded ({max_retries}). Unable to retrieve data.')
    return dto
