# 專案流程文件 (Project Workflow)

本文件描述 **Career-Creator-Consulting-Client-Matching-Platform** 的系統運作流程，包含前端互動與後端資料處理邏輯。

## 前端 (Frontend)

前端使用 **Streamlit** 框架構建 (`app.py`)，採用 Single Page Application (SPA) 模式，透過 Session State 管理狀態。

### 1. 頁面架構與導航
系統透過 `st.session_state.current_page` 控制頁面顯示：
*   **首頁 (Home)**: 系統入口，提供功能簡介與快速導航按鈕（新增/查詢）。
*   **新增諮詢對象 (AddClient)**: 提供資料輸入表單。
*   **查詢諮詢對象 (SearchClient)**: 提供多條件篩選與資料編輯功能。

### 2. 互動邏輯詳解
*   **新增資料**:
    1.  使用者填寫表單（包含名稱、性別、地區、年紀等必填欄位）。
    2.  點擊「送出資料」後，前端進行基本欄位檢查（非空檢查）。
    3.  若檢查通過，呼叫後端 `manager.create_client()`。
    4.  接收後端回傳結果，顯示成功訊息或錯誤提示 (例如名稱重複)。

*   **查詢與編輯**:
    1.  **篩選**: 使用者設定性別、地區、狀態、年紀 (複選)、諮詢方式等條件。
    2.  **查詢觸發**: 點擊「查詢」按鈕或首次進入頁面時，呼叫後端 `manager.filter_clients()`。結果暫存於 `session_state.search_results`。
    3.  **列表顯示**: 使用 `st.data_editor` 顯示查詢結果，允許直接修改部分欄位。
    4.  **變更偵測**: 當使用者修改表格內容並點擊「儲存修改」：
        *   系統逐列比對修改後的資料與原始資料。
        *   若偵測到差異，呼叫後端 `manager.update_client()` 進行單筆資料更新。
        *   更新完成後，自動重新執行查詢以刷新畫面。

---

## 後端 (Backend)

後端邏輯由 `ClientManager` (`src/manage.py`) 統籌，透過 `GoogleSheetService` (`src/database.py`) 確保資料與 Google Sheets 同步。

### 1. 系統初始化與資料載入 (Initialization)
當 `app.py` 啟動且 Session State 中無 `manager` 時執行：
1.  **實例化**: 建立 `GoogleSheetService` (API 連線) 與 `ClientManager`。
2.  **載入資料 (`load`)**:
    *   呼叫 `service.load_gsheet()` 讀取雲端資料 (DataFrame)。
    *   將每一列轉換為 `Client` 物件 (Pydantic Model)，存入記憶體快取 `_clients_cache`。
    *   設定 `_is_initialized = True`。

### 2. 新增客戶流程 (Create Client Workflow)
1.  **接收資料**: 前端傳入 Dictionary。
2.  **重複性檢查**: 比對 `name` 是否已存在於快取中。
3.  **資料驗證**: 使用 `Client` Model 驗證型別與限制。
4.  **雲端寫入 (Append)**:
    *   格式化資料順序。
    *   呼叫 `service.append_row()` 將單筆資料附加至 Google Sheets 末端。
5.  **快取更新**: 雲端寫入成功後，將新 `Client` 物件加入本地快取。

### 3. 查詢與篩選流程 (Query & Filter Workflow)
所有查詢皆針對 **記憶體快取** 進行，速度快且節省 API 配額。
1.  **呼叫篩選**: `filter_clients()`。
2.  **條件比對**: 支援性別、地區、模式、年齡區間等多條件過濾。
3.  **回傳結果**: 回傳符合條件的 `Client` 物件列表。

### 4. 更新客戶資料流程 (Update Client Workflow)
採用「單筆更新，全量同步」策略 (因 Google Sheets API 特性與資料一致性考量)。
1.  **鎖定目標**: 根據 `client_id` (名稱) 鎖定快取中的物件。
2.  **建立副本**: 複製物件並套用變更 (`model_copy`)，自動更新 `update_time`。
3.  **準備同步列表**: 建立一份包含「已更新物件」的完整列表副本。
4.  **雲端同步 (Override)**:
    *   將新列表轉換為 DataFrame。
    *   呼叫 `service.save_gsheet()` 覆寫 Google Sheets 該分頁所有內容。
5.  **快取確認**: 雲端寫入成功後，才更新本地 `_clients_cache`。
