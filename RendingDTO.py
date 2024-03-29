import openpyxl
from typing import List
from dataclasses import dataclass
from typing import Dict

@dataclass
class RendingDTO:
    name: str                                       # 銘柄名
    code: int                                       # 証券コード
    outstanding_sales: int                          # 売り残高
    weekly_change_sales: int                        # 売り残高増減
    outstanding_purchases: int                      # 買い残高
    weekly_change_purchases: int                    # 買い残高増減
    stock_float: int                            # 浮動株数
    stock_shares_outstanding: int               # 発行済み株数
    sale_purchase_ratio: float                      # 売り残高/買い残高
    ratio_to_float_sales: float                     # 売り残高/浮動株
    ratio_to_float_purchases: float                 # 買い残高/浮動株
    ratio_to_shares_outstanding_sale: float         # 売り残高/発行済み株数
    ratio_to_shares_outstanding_purchases: float    # 買い残高/発行済み株数
    market: str                                     # 上場市場
    stock_price: int                                # 本日株価
    vwap: float                                     # vwap


class RendingDataSet:
    excel_workbook: openpyxl.Workbook
    jpx_worksheet: openpyxl.worksheet.worksheet.Worksheet
    nisshokyo_worksheet: openpyxl.worksheet.worksheet.Worksheet
    rending_ratio_worksheet: openpyxl.worksheet.worksheet.Worksheet
    pdf_file_path: str
    nisshokyo_file_path: str
    pdf_file_url: str
    nisshokyo_file_url: str
    out_filepath: str
    weekly_outstanding_data: List[List[str]]
    stock_list: Dict[str, RendingDTO] = {}


class YApiDTO:
    float_shares: int
    shares_outstanding: int

    def __init__(self, float_shares, shares_outstanding):
        self.float_shares = float_shares
        self.shares_outstanding = shares_outstanding



