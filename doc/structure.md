# 專案結構說明

本文件記錄 `Career-Creator-Consulting-Client-Matching-Platform` 專案的程式結構與檔案用途。專案採用前後端分離架構，前端使用 Streamlit 構建，後端邏輯位於 `/src` 目錄中，負責處理資料模型、資料庫連結及業務邏輯。

## 目錄結構

```text
/
├── app.py          # 前端應用程式入口 (Streamlit)
└── src
    ├── client.py       # 客戶資料模型定義 (Pydantic)
    ├── config.py       # 專案環境與路徑設定
    ├── database.py     # Google Sheets 資料庫串接
    ├── general.py      # 通用工具函式
    └── manage.py       # 核心業務邏輯管理器
```

## 檔案詳細說明

### 1. app.py (前端應用程式)
專案的入口點，使用 `streamlit` 框架建構網頁介面。
*   **功能**:
    *   **頁面路由**: 負責 `Home` (首頁), `AddClient` (新增), `SearchClient` (查詢) 的頁面切換。
    *   **Session State 管理**: 維護 `manager` (後端控制器) 實例與 `search_results` (查詢結果快取)。
    *   **UI 呈現**: 包含 CSS 樣式優化、表單輸入、資料編輯器 (`data_editor`) 與互動邏輯。

### 2. src/client.py (資料模型)
定義了單筆客戶資料的實體類別 `Client`，使用 `pydantic` 進行強型別資料驗證。

*   **類別 `Client`**:
    *   **屬性**:
        *   `name` (名稱): 客戶姓名或暱稱 (1-15字)。
        *   `gender` (性別): "男", "女"。
        *   `age` (年紀): "18-30歲", "31-40歲" 等區間。
        *   `area` (地區): "北部（北北基桃竹）" 等台灣分區。
        *   `location` (地點): 詳細地點描述 (3-10字)。
        *   `mode` (可接受諮詢方式): "線上諮詢", "實體面談" 等。
        *   `member` (所屬學員): 關聯的學員名稱。
        *   `status` (預約狀態): "待預約", "已預約", "已取消"。
        *   `remark` (備註): 補充說明。
        *   `update_time` (更新時間): 自動記錄最後修改時間，支援字串與 datetime 互轉。
    *   **方法**:
        *   `touch()`: 更新 `update_time` 為當前時間。

### 3. src/config.py (設定檔)
負責管理專案的全域設定與路徑。

*   **變數**:
    *   `ROOT_PATH`: 專案根目錄路徑。
    *   `DATA_PATH`: 指向 `data/consulting_client.xlsx` (開發測試用)。
    *   `CREDENTIAL_PATH`: 指向 `key/dirve.json` (Google API 金鑰)。

### 4. src/database.py (資料庫介面)
負責與 Google Sheets API 進行互動 (使用 `gspread` 套件)。

*   **類別 `GoogleSheetService`**:
    *   **初始化**: 讀取金鑰並建立連線。
    *   **方法**:
        *   `load_gsheet()`: 讀取 `consulting_client` 下的 `client` 分頁，回傳 `pandas.DataFrame`。
        *   `save_gsheet(df)`: 將 DataFrame 全量覆蓋寫回 `client` 分頁。
        *   `append_row(row_data)`: 將單列資料附加到分頁末端，並強制設定 `USER_ENTERED` 模式以正確解析日期。

### 5. src/general.py (通用工具)
提供路徑處理等輔助函式。

*   **函式**:
    *   `get_project_root()`: 回傳專案根目錄的 `Path` 物件。

### 6. src/manage.py (業務邏輯)
後端的核心控制器，協調 `Client` 模型與 `GoogleSheetService`。

*   **類別 `ClientManager`**:
    *   **快取機制**: 維護 `_clients_cache` (List[Client]) 以減少 API 呼叫。
    *   **狀態管理**: 使用 `_is_initialized` 標記是否已從雲端載入資料。
    *   **方法**:
        *   `load()`: 從雲端讀取資料並轉換為物件列表存入快取。
        *   `create_client(client_data)`: 驗證資料 -> 呼叫 `append_row` 寫入雲端 -> 更新本地快取。
        *   `filter_clients(...)`: 針對記憶體快取進行多條件篩選 (性別、地區、模式、年齡)。
        *   `update_client(client_id, updated_data)`: 建立資料副本 -> 產生新的完整列表 -> 呼叫 `save_gsheet` 全量同步 -> 更新快取。
