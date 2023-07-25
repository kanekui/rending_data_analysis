import IExecutable
from typing import List
from command.read_from_pdf_command import ReadFromPDFCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand


class JPXDailyFactory:

    @staticmethod
    def create():
        #1.JPXの銘柄別信用取引週末残高から表部分を抜き出してデータ読み込み
        #2.xlsxで保存
        commands: List[IExecutable] = [ReadFromPDFCommand(),
                                       WriteWeeklyDataToExcelCommand()]
        return commands
