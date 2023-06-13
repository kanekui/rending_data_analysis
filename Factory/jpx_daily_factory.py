import IExecutable
from typing import List
from command.read_from_excel_command import ReadFromExcelCommand


class JPXDailyFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromExcelCommand()]
        return commands
