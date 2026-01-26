import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from src.config import DATA_PATH, CREDENTIAL_PATH


def get_consulting_clients():
    """
    從 data/consulting_client.xlsx 讀取 client 分頁並回傳為 DataFrame。
    """
    file_path = DATA_PATH
    df = pd.read_excel(file_path, sheet_name='client')
    return df


class GoogleSheetService:
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.creds = Credentials.from_service_account_file(CREDENTIAL_PATH, scopes=self.scopes)
        self.client = gspread.authorize(self.creds)


    def load_gsheet(self):
        """
        從 Google 雲端試算表讀取 consulting_client 的 client 分頁，並回傳為 DataFrame。
        """
        # 開啟試算表並選取指定分頁
        spreadsheet = self.client.open('consulting_client')
        worksheet = spreadsheet.worksheet('client')

        # 讀取所有內容並轉換為 DataFrame
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        return df


    def save_gsheet(self, df: pd.DataFrame):
        """
        將輸入的 DataFrame 更新至 Google 雲端試算表 consulting_client 中的 client 分頁。
        """
        spreadsheet = self.client.open('consulting_client')
        worksheet = spreadsheet.worksheet('client')

        # 直接使用 update 覆蓋現有內容，避免先清除導致更新失敗時資料遺失
        data = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data)
