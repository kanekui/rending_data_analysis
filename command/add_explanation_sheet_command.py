#IExecutableインターフェイスを継承し、dto.excel_workbookの末尾に「この表の説明」シートを追加するクラス

import openpyxl
import win32com.client

from RendingDTO import RendingDataSet
from IExecutable import IExecutable


class AddExplanationSheetCommand(IExecutable):
    SHEET_NAME = "この需給表の説明"

    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        # Excelファイルを開く
        workbook = dto.excel_workbook
        # 新しいシートを追加
        explanation_sheet = workbook.create_sheet(title=self.SHEET_NAME)
        # 説明文を追加        
        explanation_sheet["A1"] = """この表は、"""
        explanation_sheet["A2"] = """   ・毎週火曜発表JPXの銘柄別信用取引週末残高(https://www.jpx.co.jp/markets/statistics-equities/margin/05.html)"""
        explanation_sheet["A3"] = """   ・毎週木曜発表日証協の銘柄別株券等貸借週末残高 (https://www.jsda.or.jp/shiryoshitsu/toukei/kabu-taiw/index.html)"""
        explanation_sheet["A4"] = """をベースに各銘柄ごとの数値を収集し、そこに浮動株データ他のいくつかのWeb上から拾ったデータを反映させた表です。"""
        explanation_sheet["A5"] = """(信用売り残高+貸株残高)/浮動株数について降順(高い方から順番に低い方へ)並べています。"""
        explanation_sheet["A6"] = """【補足】"""
        explanation_sheet["A7"] = """JPXの銘柄別信用取引週末残高はpdfで配布されているため、ソート他表計算ができない悩みがありました。なのでExcelに変換し、"""
        explanation_sheet["A8"] = """JPX Dataシートとして保存しています。"""

        # ワークブックを保存
        workbook.save(dto.out_filepath)
        
        return dto