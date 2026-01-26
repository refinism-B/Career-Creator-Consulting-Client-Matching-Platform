


class ClientProcessor:
    def __init__(self, service: GoogleSheetService):
        self.service = service

    def create_client(self, client_data: dict):
        """這是一個新增諮詢對象資料的函式"""
        # 從 Repo 拿到最新資料
        df = self.service.load_gsheet()
        
        # 進行邏輯修改
        df = df.append(client_data, ignore_index=True)
        
        # 將結果存回去
        self.service.save_gsheet(df)
        print(f"✅ 已成功新增諮詢對象資料！")