import openpyxl
from typing import List
from dataclasses import dataclass


@dataclass
class RendingDTO:
    name: str                                       # 銘柄名
    code: int                                       # 証券コード
    outstanding_sales: int                          # 売り残高
    weekly_change_sales: int                        # 売り残高増減
    outstanding_purchases: int                      # 買い残高
    weekly_change_purchases: int                    # 買い残高増減
    yahoo_com_float: int                            # 浮動株数
    yahoo_com_shares_outstanding: int               # 発行済み株数
    sale_purchase_ratio: float                      # 売り残高/買い残高
    ratio_to_float_sales: float                     # 売り残高/浮動株
    ratio_to_float_purchases: float                 # 買い残高/浮動株
    ratio_to_shares_outstanding_sale: float         # 売り残高/発行済み株数
    ratio_to_shares_outstanding_purchases: float    # 買い残高/発行済み株数


class RendingDataSet:
    jpx_worksheet: openpyxl.worksheet.worksheet.Worksheet
    nisshokyo_worksheet: openpyxl.worksheet.worksheet.Worksheet
    rending_ratio_worksheet: openpyxl.worksheet.worksheet.Worksheet
    pdf_file_path: str
    nisshokyo_file_path: str
    weekly_outstanding_data: List[List[str]]
    stock_list = []


class YApiDTO:
    float_shares: int
    shares_outstanding: int

    def __init__(self, float_shares, shares_outstanding):
        self.float_shares = float_shares
        self.shares_outstanding = shares_outstanding



