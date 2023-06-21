import IExecutable
from typing import List
from command.read_from_excel_command import ReadFromExcelCommand
from command.read_rendingdata_from_worksheet import ReadFromRendingDataFromWorksheetCommand
from command.read_from_pdf_command import ReadFromPDFCommand
from command.write_weekly_to_excelfile import WriteWeeklyDataToExcelCommand
from command.dummy_get_ycom_data_command import DummyGetYComDataCommand


class DummyYComDataFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromPDFCommand(),
                                       WriteWeeklyDataToExcelCommand(),
                                       DummyGetYComDataCommand()]
        return commands
