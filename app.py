import streamlit as st
import pandas as pd
from typing import Optional
from src.database import GoogleSheetService
from src.manage import ClientManager
from src.client import Client

# --- 設定頁面 ---
st.set_page_config(
    page_title="職游－諮詢對象媒合平台",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS 樣式優化 ---
st.markdown("""
<style>
    div[data-testid="stInputInstructions"] {
        display: none;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E86C1;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        color: #566573;
        margin-bottom: 2rem;
    }
    .intro-box {
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .big-button {
        font-size: 1.0rem !important;
    }
</style>
""", unsafe_allow_html=True)


# --- 初始化 Session State ---
if 'manager' not in st.session_state:
    try:
        with st.spinner('正在連接系統資料庫，請稍候...'):
            service = GoogleSheetService()
            manager = ClientManager(service)
            manager.load()
            st.session_state.manager = manager
    except Exception as e:
        st.error(f"系統初始化失敗: {e}")
        st.stop()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# --- 導航函式 ---


def navigate_to(page_name):
    st.session_state.current_page = page_name


# --- 側邊欄 ---
with st.sidebar:
    st.header("功能選單")
    if st.button("🏠 首頁", use_container_width=True):
        navigate_to("Home")
    if st.button("🙋 新增諮詢對象", use_container_width=True):
        navigate_to("AddClient")
    if st.button("🔍 查詢諮詢對象", use_container_width=True):
        navigate_to("SearchClient")

    st.markdown("---")
    st.header("系統操作")
    if st.button("🔄 手動更新資料", help="重新從雲端讀取最新資料"):
        with st.spinner("資料讀取中..."):
            st.session_state.manager.load()
        st.success("資料已更新！")

# --- 頁面內容 ---


def page_home():
    st.markdown('<div class="main-title">職游：專業職涯諮詢師培訓</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sub-title">實習諮詢對象媒合平台</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="intro-box">
        這是一個開放平台，由於課程建議不要尋找太親近的對象作為練習對象，故建立此系統，讓大家可以提供自己身邊適合/需要諮詢的人選，同時也可以查詢是否有適合自己練習的諮詢對象。<br><br>
        <ul>
            <li>選擇「<b>新增諮詢對象</b>」將自己認識、適合的諮詢對象資料新增進列表。</li>
            <li>選擇「<b>查詢諮詢對象</b>」尋找列表中符合條件的諮詢對象。</li>
        </ul>
        <br>
        <em>本系統僅處理資訊交換與查詢，恕不承擔後續媒合及諮詢過程所發生之事件。提醒各位同學在媒合、尋找諮詢對象時仍務必謹慎。</em>
        <br>
        <br>
        <span style="color: #E74C3C; font-weight: bold;">注意：</span>資料表中不會存取個人資料（如電話、email等聯絡資料）如欲建立諮詢關係，請聯絡所屬學員，由對方進行轉介紹。
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2.1, 1, 1, 2])

    with col2:
        if st.button("🙋 新增諮詢對象", key="home_add_btn"):
            navigate_to("AddClient")
            st.rerun()
    with col3:
        if st.button("🔍 查詢諮詢對象", key="home_search_btn"):
            navigate_to("SearchClient")
            st.rerun()


def page_add_client():
    st.markdown("## 新增諮詢對象")

    # 注意：clear_on_submit=True 有時會導致變數重置問題，先設False，成功後再手動清空如果需要，或者直接提示成功
    with st.form("add_client_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            member = st.text_input(
                "你的名字 (必填)", max_chars=15, placeholder="請入填自己的LINE名稱（或辨識度高的稱呼）", help="本平台不存取任何聯絡方式，有諮詢意願的同學會聯絡你取得諮詢對象的聯繫方式")
            gender = st.selectbox(
                "性別 (必填)", ["男", "女"], index=None, placeholder="點擊選擇性別")
            area = st.selectbox(
                "地區 (必填)", ["北部（北北基桃竹）", "中部（苗中彰雲投）", "南部（嘉南高屏）", "東部（宜花東）", "離島"], index=None, placeholder="點擊選擇地區")
            mode = st.selectbox(
                "可接受諮詢方式 (必填)", ["線上諮詢", "實體面談", "線上及實體皆可", "其他"], index=None, placeholder="點擊選擇可接受諮詢的方式")

        with col2:
            name = st.text_input("來訪者暱稱 (必填)", max_chars=15,
                                 placeholder="填寫來訪者名稱或暱稱")
            age = st.selectbox("年紀 (必填)", [
                               "18-30歲", "31-40歲", "41-50歲", "51-60歲", "61-70歲"], index=None, placeholder="點擊選擇年紀區間")
            location = st.text_input(
                "地點 (必填)", max_chars=10, placeholder="填寫更細部的地點，例如：台北市中正區")
            remark = st.text_input("備註", max_chars=30)

        submitted = st.form_submit_button("送出資料")

        if submitted:
            # 基本檢查
            errors = []
            if not name:
                errors.append("請輸入暱稱")
            if not location:
                errors.append("請輸入地點")
            if not member:
                errors.append("請輸入所屬學員")
            if not age:
                errors.append("請選擇年紀區間")
            if not gender:
                errors.append("請選擇性別")
            if not area:
                errors.append("請選擇地區")
            if not mode:
                errors.append("請選擇可接受諮詢方式")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                client_data = {
                    "名稱": name,
                    "性別": gender,
                    "年紀": age,
                    "地區": area,
                    "地點": location,
                    "可接受諮詢方式": mode,
                    "所屬學員": member,
                    "備註": remark if remark else "",
                    "預約狀態": "待預約"  # 預設狀態
                }

                try:
                    with st.spinner("正在新增資料..."):
                        st.session_state.manager.create_client(client_data)
                    st.success(f"✅ 成功新增諮詢對象：{name}")
                    # 可以在這裡加入重置表單的邏輯，或者導向回列表
                except ValueError as ve:
                    st.error(str(ve))
                except Exception as e:
                    st.error(f"新增失敗: {e}")


def page_search_client():
    st.markdown("## 查詢諮詢對象")

    # --- 篩選區塊 ---
    with st.expander("查詢條件", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_gender = st.selectbox("性別", ["全部", "男", "女"])
        with col2:
            filter_area = st.selectbox(
                "地區", ["全部", "北部（北北基桃竹）", "中部（苗中彰雲投）", "南部（嘉南高屏）", "東部（宜花東）", "離島"])
        with col3:
            filter_status = st.selectbox("預約狀態", ["全部", "待預約", "已預約"])
        
        col4, col5 = st.columns(2)
        with col4:
            filter_age_options = st.multiselect(
                "年紀區間（可複選）",
                options=["18-30歲", "31-40歲", "41-50歲", "51-60歲", "61-70歲"],
                default=None,
                placeholder="選擇年紀區間"
            )
        with col5:
            filter_mode = st.selectbox(
                "可接受諮詢方式",
                ["全部", "線上諮詢", "實體面談", "線上及實體皆可", "其他"]
            )

        search_clicked = st.button("查詢")

    # 處理篩選邏輯
    # 這裡我們使用 session_state 來暫存查詢結果，避免每次互動都重查，但需求說點擊查詢才查
    if 'search_results' not in st.session_state or search_clicked:
        # 轉換 "全部" 為 None，並存入 session_state 供儲存後重新查詢使用
        st.session_state.filter_gender = filter_gender if filter_gender != "全部" else None
        st.session_state.filter_area = filter_area if filter_area != "全部" else None
        st.session_state.filter_status = filter_status
        st.session_state.filter_age_options = filter_age_options if filter_age_options else None
        st.session_state.filter_mode = filter_mode if filter_mode != "全部" else None

        with st.spinner("查詢中..."):
            initial_results = st.session_state.manager.filter_clients(
                gender=st.session_state.filter_gender,
                area=st.session_state.filter_area,
                mode=st.session_state.filter_mode,
                age_options=st.session_state.filter_age_options
            )

            # 二次篩選 Status
            if st.session_state.filter_status != "全部":
                initial_results = [
                    c for c in initial_results if c.status == st.session_state.filter_status]

            st.session_state.search_results = initial_results

    # --- 顯示結果與編輯 ---
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        st.info(f"搜尋結果：共 {len(results)} 筆資料")

        if results:
            # 將 Pydantic 物件轉為 DataFrame 供 DataEditor 使用
            # 使用 by_alias=True 來顯示中文欄位名稱，這樣對使用者比較友善
            data_list = [c.model_dump(by_alias=True) for c in results]
            df = pd.DataFrame(data_list)

            # 設定 DataEditor 的欄位組態
            column_config = {
                # 名稱是 ID，不給改
                "名稱": st.column_config.TextColumn("名稱", disabled=True, help="名稱不可修改"),
                "性別": st.column_config.SelectboxColumn("性別", options=["男", "女"], required=True),
                "地區": st.column_config.SelectboxColumn("地區", options=["北部（北北基桃竹）", "中部（苗中彰雲投）", "南部（嘉南高屏）", "東部（宜花東）", "離島"], required=True),
                "預約狀態": st.column_config.SelectboxColumn("預約狀態", options=["待預約", "已預約"], required=True),
                "年紀": st.column_config.SelectboxColumn("年紀", options=["18-30歲", "31-40歲", "41-50歲", "51-60歲", "61-70歲"], required=True),
                "可接受諮詢方式": st.column_config.SelectboxColumn("可接受諮詢方式", options=["線上諮詢", "實體面談", "線上及實體皆可", "其他"]),
                "更新時間": st.column_config.DatetimeColumn("更新時間", disabled=True, format="Yb-MM-DD HH:mm:ss"),
            }

            edited_df = st.data_editor(
                df,
                key="client_editor",
                column_config=column_config,
                use_container_width=True,
                num_rows="fixed",  # 不允許在表格直接新增/刪除列，需透過新增頁面
                hide_index=True
            )

            # 儲存按鈕
            if st.button("💾 儲存修改"):
                # 比對差異並更新
                # 由於 data_editor 回傳的是整個 df，我們需要找出哪一列變了
                # 或者比較簡單暴力的做法：逐列檢查與原始資料的差異

                updated_count = 0
                error_count = 0

                with st.status("正在更新資料...", expanded=True) as status:
                    for index, row in edited_df.iterrows():
                        client_name = row["名稱"]
                        # 找到原始物件
                        original_client = next(
                            (c for c in st.session_state.search_results if c.name == client_name), None)

                        if original_client:
                            # 檢查是否有變更
                            # 將 row 轉回 dict，注意可能有的欄位型別差異
                            # Pydantic dump 出來的是原值，row 也是原值，應該可以直接比

                            # 建立一個變更後的資料 dict
                            # 注意：這裡 row 是 Series，轉 dict
                            new_data = row.to_dict()

                            # 簡單比對：嘗試用新資料 update
                            # 由於 update_client 會做 model_copy，我們只需要傳入差異或全部

                            # 為了效能，我們可以先檢查有沒有變，但 update_client 本身也算快
                            # 這裡直接呼叫 update_client，讓後端去處理同步
                            # 不過 update_client 是一次一筆寫入雲端 (save_gsheet 全量覆蓋)
                            # 如果改多筆，會導致多次全量覆蓋，效率極差且有 Race Condition 風險
                            # 但目前 manage.py 的 update_client 實作確實是單筆更新就 save_gsheet
                            # 考慮到併發與效能，理想是批次更新，但題目沒要求改 manage.py 架構
                            # 我們先用簡單邏輯：如果有變更才呼叫 update

                            has_changed = False
                            old_data = original_client.model_dump(
                                by_alias=True)

                            # 比對關鍵欄位（使用字串轉換確保類型一致）
                            relevant_keys = [
                                "性別", "年紀", "地區", "地點", "可接受諮詢方式", "所屬學員", "預約狀態", "備註"]
                            for k in relevant_keys:
                                old_val = str(old_data.get(k, ""))
                                new_val = str(new_data.get(k, ""))
                                if old_val != new_val:
                                    has_changed = True
                                    break

                            if has_changed:
                                st.write(f"正在更新：{client_name} ...")
                                try:
                                    # 使用 Client.model_validate 解析 alias-based 資料
                                    # 這會正確處理中文欄位名稱並驗證資料
                                    temp_obj = Client.model_validate(new_data)
                                    # 自動更新 update_time
                                    temp_obj.touch()

                                    # 轉回 field name based dict（model_copy 需要 field name）
                                    update_payload = temp_obj.model_dump(
                                        by_alias=False)

                                    if st.session_state.manager.update_client(client_name, update_payload):
                                        updated_count += 1
                                    else:
                                        error_count += 1
                                        st.write(f"❌ 更新 {client_name} 失敗")
                                except Exception as e:
                                    error_count += 1
                                    st.write(f"❌ 更新 {client_name} 發生錯誤: {e}")

                    # 根據錯誤狀態顯示不同的訊息
                    if error_count > 0:
                        status.update(
                            label=f"更新過程中發生 {error_count} 個錯誤", state="error", expanded=True)
                    else:
                        status.update(
                            label="更新完成", state="complete", expanded=False)

                if updated_count > 0 and error_count == 0:
                    st.success(f"成功更新 {updated_count} 筆資料！")
                    # 重新整理結果
                    # 從 session_state 讀取篩選條件進行重新查詢
                    st.session_state.search_results = st.session_state.manager.filter_clients(
                        gender=st.session_state.get('filter_gender'),
                        area=st.session_state.get('filter_area'),
                        mode=st.session_state.get('filter_mode'),
                        age_options=st.session_state.get('filter_age_options')
                    )
                    # 再次過濾 status
                    if st.session_state.get('filter_status', '全部') != "全部":
                        st.session_state.search_results = [
                            c for c in st.session_state.search_results if c.status == st.session_state.filter_status]

                    st.rerun()
                elif error_count > 0:
                    st.error(f"更新過程中發生 {error_count} 個錯誤，請檢查資料格式後重試。")
                elif updated_count == 0 and error_count == 0:
                    st.info("沒有偵測到資料變更。")

# --- 路由控制 ---


if st.session_state.current_page == "Home":
    page_home()
elif st.session_state.current_page == "AddClient":
    page_add_client()
elif st.session_state.current_page == "SearchClient":
    page_search_client()
