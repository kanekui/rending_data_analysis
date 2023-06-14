# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from Factory.jpx_daily_factory import JPXDailyFactory
from RendingDTO import RendingDataSet

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # ファイルパスをコマンドライン引数から取得
    file_path = sys.argv[1]

    # RendingDataSetのインスタンスを作成
    rending_data_set = RendingDataSet()
    rending_data_set.file_path = file_path

    # コマンドを作成
    commands = JPXDailyFactory().create()

    for command in commands:
        rending_data_set = command.execute(rending_data_set)

    print(rending_data_set)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
