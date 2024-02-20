import IExecutable
from typing import List
from command.read_from_pdf_command import ReadFromPDFCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.get_yahoo_com_data_command import GetYComDataCommand


class YComDataFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [IRBKConnectCommand(),
                                       ChechIRBKConnectCommand(),
                                       GetYComDataCommand()]
        return commands
