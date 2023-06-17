import PyPDF2
from RendingDTO import RendingDataSet
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
        header_line = '銘柄名,コード,新証券コード,売残高,売残高前週比,買残高,買残高前週比,一般信用売残高,一般信用売残高前週比,制度信用売残高,制度信用売残高前週比,一般信用買残高,一般信用買残高前週比,制度信用買残高,一般信用買残高前週比'
        extracted_lines.append(header_line)
        for line in lines:
            if line.startswith('B'):
                line = line.replace(',', '').replace(' ', ',')
                line = line.replace('▲,', '-')
                if '銘柄別信用取引週末残高' in line:
                    start_index = line.index('銘柄別信用取引週末残高')
                    line = line[:start_index] + line[start_index:].replace(line[start_index:], '')
                extracted_lines.append(line)

        # 抽出された行の表示
        # for line in extracted_lines:
        #    print(line)
        dto.weekly_outstanding_data = extracted_lines

        return dto







