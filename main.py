# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Factory.jpx_daily_factory import JPXDailyFactory
from RendingDTO import RendingDataSet

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    commands: JPXDailyFactory().create()

    for command in commands:
        RendingDataSet = command.execute(RendingDataSet)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
