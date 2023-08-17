# 貸株+信用売り、信用買いと浮動株で比率を個別銘柄ごとに集計するスクリプト
# 手続き型でしかないため、コマンドパタンで実装。
# Factoryで各個別手続きコマンドをインスタンス化し、コマンドリストに弾込めしてもらい、
# foreachでバンバンバンとマグナム銃を撃つイメージ。
# こうすることでやりたいことが変わったときに達磨落としのようにそこだけコマンド差し替えられる。
# 変えたいところだけ新規実装で差し替えればよくてハッピー
# コマンドクラスはIExecutableを継承し、Executeメソッドで自分の責務を実行する。
# マグナム撃つ方はようわからんけど、Executeしといて、という感じ

# 引数"-a"で直近の東証の信用残と日証協の貸借のpdf,excelをダウンロードし、楽天の全銘柄の浮動株数、発行済み株数をスクレイピングして
# 各データを一つのExcelにまとめる

import sys
from Factory.jpx_daily_factory import JPXDailyFactory
from Factory.yahoo_com_data_factory import YComDataFactory
from Factory.rending_data_marge_factory import RendingDataMargeFactory
from Factory.rending_analysis_data_factory import RendingAnalysisFactory
from Factory.get_float_factory import GetFloatAndOutstandingFactory
from Factory.auto_rending_analysis_data_factory import AutoRendingAnalysisFactory
from Factory.auto_friday_holiday_rending_analysis_data_factory import AutoFridayHolidayRendingAnalysisFactory
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

        elif sys.argv[1] == "-af":
            mode = "AutoFridayHoliday"

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

            commands = AutoRendingAnalysisFactory.create()

        case "AutoFridayHoliday" :
            print("Auto Friday Holiday")
            commands = AutoFridayHolidayRendingAnalysisFactory.create()

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
