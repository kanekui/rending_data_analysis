# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 貸株+信用売り、信用買いと浮動株で比率を個別銘柄ごとに集計するスクリプト
# 手続き型でしかないため、コマンドパタンで実装。
# Factoryで各個別手続きコマンドをインスタンス化し、コマンドリストに弾込めしてもらい、
# foreachでバンバンバンとマグナム銃を撃つイメージ。
# こうすることでやりたいことが変わったときに達磨落としのようにそこだけコマンド差し替えられる。
# 変えたいところだけ新規実装で差し替えればよくてハッピー

import sys
from Factory.jpx_daily_factory import JPXDailyFactory
from Factory.yahoo_com_data_factory import YComDataFactory
from Factory.dummy_yahoo_com_data_factory import DummyYComDataFactory
from RendingDTO import RendingDataSet

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # コマンドライン引数の解析
    mode = "default"
    pdf_file_path = None
    print("start")

    if len(sys.argv) > 1:
        if sys.argv[1] == "-Y":
            mode = "Yahoo"
            if len(sys.argv) > 2:
                pdf_file_path = sys.argv[2]
        elif sys.argv[1] == "-dY":
            mode = "DummyYahoo"
            if len(sys.argv) > 2:
                pdf_file_path = sys.argv[2]

        elis sys.argv[1] == "-m":
            mode = "Marge"
            if len(sys.argv) > 3:
                pdf_file_path = sys.argv[2]
                nissho_kyo_file_path = sys.argv[3]

        else:
            mode = "default"
            pdf_file_path = sys.argv[1]

    # RendingDataSetのインスタンスを作成
    rending_data_set = RendingDataSet()
    rending_data_set.pdf_file_path = pdf_file_path
    rending_data_set.nisshokyo_file_path = nissho_kyo_file_path

    # コマンドを作成
    commands = []
    print(mode)

    match mode:
        case "Yahoo" :
            print("yahoo mode")
            commands = YComDataFactory().create()

        case "DummyYahoo" :
            print("Dummyyahoo mode")
            commands = DummyYComDataFactory.create()

        case "Marge" :
            print("Marge mode")
            commands = RendingDataMargeFactory.create()

        case "default":
            print("default mode")
            commands = JPXDailyFactory().create()



    for command in commands:
        rending_data_set = command.execute(rending_data_set)

    # print(rending_data_set.stock_list)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
