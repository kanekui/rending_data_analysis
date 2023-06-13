import openpyxl
from typing import List
from dataclasses import dataclass


@dataclass
class RendingDTO:
    code: str
    outstanding_sales: int
    daily_change_sales: int
    ratio_to_listed_sales: float
    outstanding_purchases: int
    daily_change_purchases: int
    ratio_to_listed_purchases: float
    sale_purchase_ratio: float


class RendingDataSet:
    worksheet: openpyxl.worksheet.worksheet.Worksheet
    file_path: str
    stock_list = []

