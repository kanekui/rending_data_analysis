# commands/fetch_volume_5d_stooq.py
from IExecutable import IExecutable
from models.dto import RendingDataSet
from fetchers.stooq_batch import five_day_avg_volume

class FetchVolume5dStooqCommand(IExecutable):
    """RendingDataSet.stock_list 内の全 DTO に
       volume_5days_average を埋めるコマンド"""

    def __init__(self, batch_size=25):
        self.batch_size = batch_size

    def execute(self, ds: RendingDataSet) -> RendingDataSet:
        # --- 1. 取得対象コードをリストアップ
        codes = list(ds.stock_list.keys())          # '3133' など

        # --- 2. バッチで一括取得
        vol_map = {}
        for i in range(0, len(codes), self.batch_size):
            chunk = codes[i : i + self.batch_size]
            vol_map.update(five_day_avg_volume(chunk))

        # --- 3. DTO に反映
        for code, dto in ds.stock_list.items():
            dto.volume_5days_average = vol_map.get(code)  # 無ければ None

        return ds