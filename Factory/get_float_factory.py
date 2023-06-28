import IExecutable
from typing import List
from command.read_from_pdf_command import ReadFromPDFCommand
from command.get_float_and_outstanding_command import GetFloatAndOutstandingCommand

class GetFloatAndOutstandingFactory:

    @staticmethod
    def create():
        commands: List[IExecutable] = [ReadFromPDFCommand(),
                                       GetFloatAndOutstandingCommand()]
        return commands
