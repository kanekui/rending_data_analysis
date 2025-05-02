import openpyxl
import win32com.client
import os

from RendingDTO import RendingDataSet
from IExecutable import IExecutable
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

#
#
#


class GetFilepathCommand(IExecutable):

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        current_folder_path = os.getcwd()



        return dto
