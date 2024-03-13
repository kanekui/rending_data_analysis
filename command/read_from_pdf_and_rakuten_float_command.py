import PyPDF2
from RendingDTO import RendingDataSet, RendingDTO
from IExecutable import IExecutable
import requests
from bs4 import BeautifulSoup
import re
import time

# JPX週末信用残高の値を取得し、Excelファイル化する。かつ、楽天証券から浮動株数、発行済み株数、上場市場を取得する。
# 実装が大きくなってきたのでリファクタリングしたい
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
                code = line[1][0:4]
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
                    ratio_to_shares_outstanding_sale=0.0,
                    market="",
                    stock_price=0,
                    vwap=0
                )
                get_rakten_float_and_outstanding_and_Market(rendingdto)
                # print(rendingdto.code)
                #get_matsui_stockvalue_and_vwap(rendingdto)
                get_sbi_stockvalue_and_vwap(rendingdto)

                print(rendingdto.stock_price)
                print(rendingdto.vwap)

                dto.stock_list[str(rendingdto.code)] = rendingdto
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

def get_rakten_float_and_outstanding_and_Market(dto: RendingDTO) -> RendingDTO:
    # print(dto.code)
    url = f'https://www.trkd-asia.com/rakutensec/quote.jsp?ric={dto.code}.T&c=ja&ind=2'
    # print(url)
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

            target_th = soup.find('th', text='上場市場')

            # 見つかった<th>要素の次の<td>要素の値を取得する
            if target_th:
                next_td = target_th.find_next('td')
                value = next_td.text

                dto.market = value  # 上場市場はそのままの値を格納:"東証P"、"東証G"等
                if dto.code == "7692":
                    print(dto.market)

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


def get_matsui_stockvalue_and_vwap(dto: RendingDTO) -> RendingDTO:
    # print(dto.code)
    url = f'https://finance.matsui.co.jp/stock/{dto.code}/index'
    headers = {'User-agent': 'Mozilla/5.0'}
    # print(url)
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')

            # table = soup.find('table', class_='js-table-values')
            # print(table)

            # 特定のクラス内の要素を取得
            stock_price_element = soup.select_one('.m-stock-price strong')
            # print(stock_price_element.text.strip())

            # 要素が存在するか確認してからテキストを取得
            if stock_price_element:
                stock_price = stock_price_element.text.strip()
            else:
                stock_price = 0
                print(response.text)

            # VWAPの要素を取得
            vwap_element = soup.select_one('th:contains("VWAP") + td')

            # 要素が存在するか確認してからテキストを取得
            if vwap_element:
                vwap_value = vwap_element.text.strip()
            else:
                vwap_value = 0

            # dto.stock_price = int(stock_price)
            dto.stock_price = int(float(stock_price.replace(',', '')))
            dto.vwap = vwap_value

            print(dto.stock_price)

            time.sleep(3)

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

def get_sbi_stockvalue_and_vwap(dto: RendingDTO) -> RendingDTO:
    # print(dto.code)
    url = f'https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control&_PageID=WPLETsiR001Idtl10&_DataStoreID=DSWPLETsiR001Control&_ActionID=stockDetail&s_rkbn=2&s_btype=&i_stock_sec=3133&i_dom_flg=1&i_exchange_code=JPN&i_output_type=0&exchange_code=TKY&stock_sec_code_mul={dto.code}&ref_from=1&ref_to=20&wstm4130_sort_id=&wstm4130_sort_kbn=&qr_keyword=1&qr_suggest=1&qr_sort=1'
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
               'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'}

    # print(url)
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers,  timeout=10)
            # print(response.text)
            # BeautifulSoupを使用してHTMLを解析
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)
            # 特定の位置の要素を取得
            current_value = soup.find('div', class_='kabuNowStatus').find('span', class_='fxx01').text
            dto.stock_price = int(float(current_value.replace(',', '')))

            # VWAPの値を取得
            vwap_value = soup.find('th', text='VWAP').find_next('td').find('span', class_='fm01').text
            dto.vwap = float(vwap_value.replace(',', ''))

            return dto

        except requests.Timeout:
            print(f'Request timed out. Retrying ({retry_count+1}/{max_retries})...')
            retry_count += 1
            time.sleep(10)  # 1秒待機してからリトライ
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return dto
    print(f'Retries exceeded ({max_retries}). Unable to retrieve data.')

