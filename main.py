# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 貸株+信用売り、信用買いと浮動株で比率を個別銘柄ごとに集計するスクリプト
# 手続き型でしかないため、コマンドパタンで実装。
# Factoryで各個別手続きコマンドをインスタンス化し、コマンドリストに弾込めしてもらい、
# foreachでバンバンバンとマグナム銃を撃つイメージ。
# こうすることでやりたいことが変わったときに達磨落としのようにそこだけコマンド差し替えられる。
# 変えたいところだけ新規実装で差し替えればよくてハッピー
# 引数"-a"で直近の東証の信用残と日証協の貸借のpdf,excelをダウンロードし、楽天の全銘柄の浮動株数、発行済み株数をスクレイピングして
# 各データを一つのExcelにまとめる

import sys
import datetime
import os
from Factory.jpx_daily_factory import JPXDailyFactory
from Factory.yahoo_com_data_factory import YComDataFactory
from Factory.rending_data_marge_factory import RendingDataMargeFactory
from Factory.rending_analysis_data_factory import RendingAnalysisFactory
from Factory.get_float_factory import GetFloatAndOutstandingFactory
from Factory.auto_rending_analysis_data_factory import AutoRendingAnalysisFactory
from RendingDTO import RendingDataSet


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # コマンドライン引数の解析
    mode = "default"
    pdf_file_path = None
    print("start")

    pdf_file_path = ""
    nissho_kyo_file_path = ""



    if len(sys.argv) > 1:
        if sys.argv[1] == "-Y":
            mode = "Yahoo"
            if len(sys.argv) > 2:
                pdf_file_path = sys.argv[2]

        elif sys.argv[1] == "-m":
            mode = "Marge"
            if len(sys.argv) > 3:
                pdf_file_path = sys.argv[2]
                nissho_kyo_file_path = sys.argv[3]

        elif sys.argv[1] == "-f":
            mode = "Float"
            pdf_file_path = sys.argv[2]
            nissho_kyo_file_path = sys.argv[3]

        elif sys.argv[1] == "-a":
            # 普段はこれを使う。勝手にダウンロードしてくれて一番便利だから。
            mode = "Auto"

        elif sys.argv[1] == "-s":
            mode = "SingleFloat"

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

        case "Marge" :
            print("Marge mode")
            commands = RendingDataMargeFactory.create()

        case "Float" :
            print("Float mode")
            commands = RendingAnalysisFactory.create()

        case "Auto" :
            print("Auto mode")
            # 直近の東証の信用残と日証協の貸借のpdf,excelをダウンロードし、楽天の全銘柄の浮動株数、
            # 発行済み株数をスクレイピングして各データを一つのExcelにまとめる

            # まずは本日の日付と曜日を取得してダウンロードファイルの日付を特定する
            # ここ、コマンドにしときたいなー
            today = datetime.datetime.today()
            weekday = today.weekday()  # 0: 月曜日, 1: 火曜日, 2: 水曜日, 3: 木曜日, 4: 金曜日, 5: 土曜日, 6: 日曜日
            date_str = today.strftime('%m%d')

            four_days_ago = today - datetime.timedelta(days=4)
            four_days_ago_str = four_days_ago.strftime('%m%d')
            five_days_ago = today - datetime.timedelta(days=5)
            five_days_ago_str = five_days_ago.strftime('%m%d')
            six_days_ago = today - datetime.timedelta(days=6)
            six_days_ago_str = six_days_ago.strftime('%m%d')
            eleven_days_ago = today - datetime.timedelta(days=11)
            eleven_days_ago_str = eleven_days_ago.strftime('%m%d')
            twelve_days_ago = today - datetime.timedelta(days=12)
            twelve_days_ago_str = twelve_days_ago.strftime('%m%d')


            current_folder_path = os.getcwd()
            if weekday == 1:  # 火曜日の場合
                rending_data_set.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{four_days_ago_str}00.pdf'
                rending_data_set.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{four_days_ago_str}00.pdf'
                rending_data_set.nisshokyo_file_path = current_folder_path + "\\" + f'2023{eleven_days_ago_str}z.xls'
                rending_data_set.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{eleven_days_ago_str}z.xls'
            elif weekday == 2:  # 水曜日の場合(月曜or火曜が祝日)
                rending_data_set.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{five_days_ago_str}00.pdf'
                rending_data_set.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{five_days_ago_str}00.pdf'
                rending_data_set.nisshokyo_file_path = current_folder_path + "\\" + f'2023{twelve_days_ago_str}z.xls'
                rending_data_set.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{twelve_days_ago_str}z.xls'
            elif weekday == 3:  # 木曜日の場合
                rending_data_set.pdf_file_path = current_folder_path + "\\" + f'syumatsu2023{six_days_ago_str}00.pdf'
                rending_data_set.pdf_file_url = f'https://www.jpx.co.jp/markets/statistics-equities/margin/tvdivq0000001rnl-att/syumatsu2023{six_days_ago_str}00.pdf'
                rending_data_set.nisshokyo_file_path = current_folder_path + "\\" + f'2023{six_days_ago_str}z.xls'
                rending_data_set.nisshokyo_file_url = f'https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/files/2023{six_days_ago_str}z.xls'

            commands = AutoRendingAnalysisFactory.create()

        case "SingleFloat":
            print("Single Float")
            commands = GetFloatAndOutstandingFactory.create()

        case "default":
            print("default mode")
            commands = JPXDailyFactory().create()



    for command in commands:
        rending_data_set = command.execute(rending_data_set)

    # print(rending_data_set.stock_list)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
