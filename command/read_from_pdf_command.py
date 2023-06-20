import PyPDF2
from RendingDTO import RendingDataSet, RendingDTO
from IExecutable import IExecutable

class ReadFromPDFCommand(IExecutable):
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
        extracter_lines_for_rendingdt = []
        header_line = '銘柄名,コード,新証券コード,売残高,売残高前週比,買残高,買残高前週比,一般信用売残高,一般信用売残高前週比,制度信用売残高,制度信用売残高前週比,一般信用買残高,一般信用買残高前週比,制度信用買残高,一般信用買残高前週比'
        extracted_lines.append(header_line)
        for line in lines:
            if line.startswith('B'):
                line = line.replace(',', '').replace(' ', ',')
                line = line.replace('▲,', '-')
                if '銘柄別信用取引週末残高' in line:
                    start_index = line.index('銘柄別信用取引週末残高')
                    line = line[:start_index] + line[start_index:].replace(line[start_index:], '')
                extracted_lines.append(','.join(line.split(',')))  # 行をカンマで結合して格納する
                extracter_lines_for_rendingdt.append(line.split(','))

        # RendingDTOの作成とRendingDataSetへの格納
        stock_list = []
        for line in extracter_lines_for_rendingdt[1:]:
            if len(line) < 7:
                continue
            if str(line[1])[-1] == '0':
                code = int(line[1][0:4])
            else:
                code = None

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
                    yahoo_com_float=0,
                    yahoo_com_shares_outstanding=0,
                    ratio_to_float_sales=0.0,
                    ratio_to_float_purchases=0.0,
                    ratio_to_shares_outstanding_purchases=0.0,
                    ratio_to_shares_outstanding_sale=0.0
                )
                stock_list.append(rendingdto)

        dto.weekly_outstanding_data = extracted_lines
        dto.stock_list = stock_list
        # print(dto.stock_list)

        return dto
