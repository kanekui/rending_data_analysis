import IExecutable
from typing import List
from command.read_from_excel_command import ReadFromExcelCommand
from command.read_rendingdata_from_worksheet import ReadFromRendingDataFromWorksheetCommand
from command.read_from_pdf_command import ReadFromPDFCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.get_yahoo_com_data_command import GetYComDataCommand
from command.read_nisshokyo_data_from_excel_command import ReadNisshoKyoDataFromExcelCommand
from command.write_weekly_ratio_to_excelfile import WriteWeeklyCalcDataToExcelCommand
from command.save_excel_file import SaveToExcelCommand
from command.get_float_and_outstanding_command import GetFloatAndOutstandingCommand

class GetFloatAndOutstandingFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromPDFCommand(),
                                       GetFloatAndOutstandingCommand()]
        return commands
