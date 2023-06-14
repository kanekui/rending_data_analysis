import IExecutable
from typing import List
from command.read_from_excel_command import ReadFromExcelCommand
from command.read_rendingdata_from_worksheet import ReadFromRendingDataFromWorksheetCommand


class JPXDailyFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromExcelCommand(),
                                       ReadFromRendingDataFromWorksheetCommand()]
        return commands
