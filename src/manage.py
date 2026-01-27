from src.database import GoogleSheetService
from src.client import Client
import pandas as pd
from typing import Optional


class ClientManager:
    def __init__(self, service: GoogleSheetService):
        self.service = service
        self._clients_cache: list[Client] = []  # 記憶體快取
        self._columns: list[str] = [] # 儲存資料表欄位順序
        self._is_initialized = False  # 標記位：判斷是否需要重新從雲端讀取

    def _ensure_data_loaded(self):
        """私有方法：確保快取中有資料"""
        if not self._is_initialized:
            self.load()

    def load(self):
        """一次性讀取所有資料並快取"""
        df = self.service.load_gsheet()
        # 確保我們先取得欄位順序，即使資料是空的，至少要有 Header
        # 如果 df 是空的，可能會有問題，但假設至少有 Header
        if not df.empty:
            self._columns = df.columns.tolist()
        elif hasattr(df, 'columns'):
             self._columns = df.columns.tolist()
        
        self._clients_cache = []
        for index, row in enumerate(df.to_dict('records')):
            try:
                self._clients_cache.append(Client(**row))
            except Exception as e:
                print(f"⚠️ 跳過無效資料 (第 {index + 1} 筆): {e}")

        self._is_initialized = True
        print("🌐 已完成雲端資料同步")

    def _sync_to_cloud(self):
        """將記憶體中的資料批次寫回 Google Sheets"""
        # 利用 model_dump 搭配 by_alias=True，確保寫回的是「性別」而不是 "gender"
        data_to_save = [c.model_dump(by_alias=True)
                        for c in self._clients_cache]
        df_to_save = pd.DataFrame(data_to_save)
        self.service.save_gsheet(df_to_save)

    def create_client(self, client_data: dict) -> Client:
        """根據前端輸入的資料，建立新的Client資料"""
        self._ensure_data_loaded()

        target_name = client_data.get("名稱") or client_data.get("name")
        if any(c.name == target_name for c in self._clients_cache):
            raise ValueError(f"❌ 錯誤：客戶名稱 '{target_name}' 已存在，不可重複。")

        try:
            # 1. 驗證資料正確性
            new_client = Client(**client_data)

            # 2. 先更新至雲端
            # 使用 self._columns 確保順序與 Google Sheets 一致
            dumped_data = new_client.model_dump(by_alias=True)
            
            # 使用明確的欄位順序清單，確保與 Google Sheet 欄位對應
            # 這樣無論 self._columns 如何變化，新增的資料都能正確對應
            expected_columns = ["名稱", "性別", "年紀", "地區", "地點", "可接受諮詢方式", "所屬學員", "預約狀態", "備註", "更新時間"]
            row_values = [dumped_data.get(col, "") for col in expected_columns]
                
            self.service.append_row(row_values)

            # 3. 再更新進快取
            self._clients_cache.append(new_client)
            print(f"✅ 成功新增客戶：{new_client.name}")

        except Exception as e:
            print(f"❌ 新增失敗：{e}")
            raise e

    def filter_clients(
        self,
        gender: Optional[str] = None,
        area: Optional[str] = None,
        mode: Optional[str] = None,
        age_options: Optional[list[str]] = None
    ) -> list[Client]:
        """根據條件進行篩選
        
        Args:
            gender: 性別篩選（單選）
            area: 地區篩選（單選）
            mode: 可接受諮詢方式篩選（單選）
            age_options: 年紀區間篩選（複選列表，如 ["18-30歲", "31-40歲"]）
        """
        self._ensure_data_loaded()

        results = []
        for client in self._clients_cache:
            # 使用條件列表，增加可讀性
            criteria = [
                (gender is None) or (client.gender == gender),
                (area is None) or (client.area == area),
                (mode is None) or (client.mode == mode),
                (age_options is None) or (len(age_options) == 0) or (client.age in age_options),
            ]

            if all(criteria):
                results.append(client)

        return results

    def update_client(self, client_id: str, updated_data: dict) -> bool:
        """根據唯一 ID 更新客戶資料 (確保雲端先成功)"""
        self._ensure_data_loaded()

        target_client = next(
            (c for c in self._clients_cache if c.name == client_id), None)
        if not target_client:
            print(f"⚠️ 找不到客戶：{client_id}")
            return False

        try:
            # 1. 產生更新後的物件（區域變數）
            updated_client = target_client.model_copy(update=updated_data)

            # 2. 建立一份「預計更新後」的清單，用來同步
            # 我們不直接動 self._clients_cache，而是先做一份副本
            temp_cache = self._clients_cache.copy()
            idx = temp_cache.index(target_client)
            temp_cache[idx] = updated_client

            # 3. 將這份「新的清單」同步回雲端
            # 注意：這裡我們需要稍微修改 _sync_to_cloud 的彈性，或者直接寫同步邏輯
            data_to_save = [c.model_dump(by_alias=True) for c in temp_cache]
            df_to_save = pd.DataFrame(data_to_save)

            # 直接呼叫 service 寫入，確保寫入的是 temp_cache 的內容
            self.service.save_gsheet(df_to_save)

            # 4. 雲端成功後，才正式把快取換成新的
            self._clients_cache = temp_cache

            print(f"✅ 已成功更新並同步：{client_id}")
            return True

        except Exception as e:
            print(f"❌ 更新失敗（雲端未同步）：{e}")
            raise e
