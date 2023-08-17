import IExecutable
from typing import List
from command.read_from_pdf_and_rakuten_float_command import ReadFromPDFAndRakutenCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.read_nisshokyo_data_from_excel_command import ReadNisshoKyoDataFromExcelCommand
from command.write_weekly_float_ratio_to_excelfile import WriteWeeklyRatioDataToExcelCommand
from command.convert_xls_to_xlsx_command import ConvertXLSCommand
from command.download_files_command import DownloadFilesCommand
from command.friday_holiday_iofilename_create_command import FridayHolidayIOfilenameCreateCommand


class AutoFridayHolidayRendingAnalysisFactory:

    @staticmethod
    def create():
        #1.JPXから銘柄別信用取引週末残高、日証協から銘柄別株券等貸借週末残高をダウンロード
        #2.JPXの銘柄別信用取引週末残高から表部分を抜き出してデータ読み込み、ついでに楽天から浮動株数と発行済み株数を一銘柄ずつ取得
        #  →設計的には浮動株数と発行済み株数取得を別コマンドとしたいが、ループが倍になるので同時にやって高速化
        #3.日証協の銘柄別株券等貸借週末残高がxlsでopenpyxlで解釈できないのでxlsx化
        #4.3でxlsx化した銘柄別株券等貸借週末残高のデータを読み込み
        #5.2のデータをxlsxで保存
        #6.信用売り+貸株を合計してから対浮動株数、対発行済み株数で比を取ってからxlsxに保存
        commands: List[IExecutable] = [FridayHolidayIOfilenameCreateCommand(),
                                       DownloadFilesCommand(),
                                       ReadFromPDFAndRakutenCommand(),
                                       ConvertXLSCommand(),
                                       ReadNisshoKyoDataFromExcelCommand(),
                                       WriteWeeklyDataToExcelCommand(),
                                       WriteWeeklyRatioDataToExcelCommand()]
        return commands
