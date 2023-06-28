import IExecutable
from typing import List
from command.read_from_pdf_command import ReadFromPDFCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.read_nisshokyo_data_from_excel_command import ReadNisshoKyoDataFromExcelCommand
from command.write_weekly_ratio_to_excelfile import WriteWeeklyCalcDataToExcelCommand


class RendingDataMargeFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromPDFCommand(),
                                       ReadNisshoKyoDataFromExcelCommand(),
                                       WriteWeeklyDataToExcelCommand(),
                                       WriteWeeklyCalcDataToExcelCommand()]
        return commands
