import IExecutable
from typing import List
from command.read_from_pdf_and_rakuten_float_command import ReadFromPDFAndRakutenCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.read_nisshokyo_data_from_excel_command import ReadNisshoKyoDataFromExcelCommand
from command.write_weekly_float_ratio_to_excelfile import WriteWeeklyRatioDataToExcelCommand
from command.convert_xls_to_xlsx_command import ConvertXLSCommand
from command.check_file_exist_command import CheckFileExistCommand


class RendingAnalysisFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [CheckFileExistCommand(),
                                       ReadFromPDFAndRakutenCommand(),
                                       ConvertXLSCommand(),
                                       ReadNisshoKyoDataFromExcelCommand(),
                                       WriteWeeklyDataToExcelCommand(),
                                       WriteWeeklyRatioDataToExcelCommand()]
        return commands
