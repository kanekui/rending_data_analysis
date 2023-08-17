from IExecutable import IExecutable
from RendingDTO import RendingDataSet
import datetime
import os

#JPXのpdfファイルと日証協のexcelファイルのInput/Outputファイル名を曜日から決めるコマンド
#火曜、木曜、金曜のいずれかが祝日だとファイル名の日付部分がずれる。
#その場合は公団のコマンドでエラーとなる。


class IOfilenameCreateCommand(IExecutable):
    def execute(self, dto: RendingDataSet) -> RendingDataSet:

        # まずは本日の日付と曜日を取得してダウンロードファイルの日付を特定する
        today = datetime.datetime.today()
        weekday = today.weekday()  # 0: 月曜日, 1: 火曜日, 2: 水曜日, 3: 木曜日, 4: 金曜日, 5: 土曜日, 6: 日曜日
        date_str = today.strftime('%m%d')

        four_days_ago = today - datetime.timedelta(days=4)
        four_days_ago_str = four_days_ago.strftime('%m%d')
        five_days_ago = today - datetime.timedelta(days=5)
        five_days_ago_str = five_days_ago.strftime('%m%d')
        six_days_ago = today - datetime.timedelta(days=6)
        six_days_ago_str = six_days_ago.strftime('%m%d')
        eleven_days_ago = today - datetime.timedelta(days=11)
        eleven_days_ago_str = eleven_days_ago.strftime('%m%d')
        twelve_days_ago = today - datetime.timedelta(days=12)
        twelve_days_ago_str = twelve_days_ago.strftime('%m%d')

        current_folder_path = os.getcwd()
        if weekday == 1:  # 火曜日の場合
            dto.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{four_days_ago_str}00.pdf'
            dto.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{four_days_ago_str}00.pdf'
            dto.nisshokyo_file_path = current_folder_path + "\\" + f'2023{eleven_days_ago_str}z.xls'
            dto.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{eleven_days_ago_str}z.xls'
        elif weekday == 2:  # 水曜日の場合(月曜or火曜が祝日)
            dto.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{five_days_ago_str}00.pdf'
            dto.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{five_days_ago_str}00.pdf'
            dto.nisshokyo_file_path = current_folder_path + "\\" + f'2023{twelve_days_ago_str}z.xls'
            dto.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{twelve_days_ago_str}z.xls'
        elif weekday == 3:  # 木曜日の場合
            dto.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{six_days_ago_str}00.pdf'
            dto.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{six_days_ago_str}00.pdf'
            dto.nisshokyo_file_path = current_folder_path + "\\" + f'2023{six_days_ago_str}z.xls'
            dto.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{six_days_ago_str}z.xls'

        return dto

