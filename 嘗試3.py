# %%
import streamlit as st
import random
import pandas as pd
import os

# --- 1. 頁面基本設定 (必須放在最上方) ---
st.set_page_config(page_title="成大美食導航", page_icon="🍱")

# 設定檔案名稱
DATA_FILE = "restaurants_v2.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict('records')
    return [
        {"name": "元味屋", "price": 150, "rating": 4.5},
        {"name": "成大館", "price": 100, "rating": 4.0},
        {"name": "麥當勞", "price": 120, "rating": 4.2},
        {"name": "活力小廚", "price": 80, "rating": 4.3}
    ]

def save_data(data):
    pd.DataFrame(data).to_csv(DATA_FILE, index=False)

if 'restaurant_db' not in st.session_state:
    st.session_state.restaurant_db = load_data()

# --- 2. 側邊欄優化 (Sidebar) ---
with st.sidebar:
    st.header("⚙️ 搜尋設定")
    # 將預算和評分篩選移到這裡
    budget = st.slider("💰 預算上限", 0, 1000, 200, 10)
    min_rating = st.slider("⭐ 最低評分", 0.0, 5.0, 3.5, 0.1)
    
    st.divider()
    with st.expander("🛠️ 進階管理"):
        if st.button("🗑️ 清空所有餐廳資料"):
            st.session_state.restaurant_db = []
            save_data([])
            st.rerun()

# --- 3. 主頁面標題 ---
st.title("🍴 成大專業級挑選器")
st.write("利用側邊欄設定預算，抽出一頓完美的晚餐！")

# --- 4. 抽選功能區 ---
st.divider()
if st.button("🎯 符合條件，抽一個！", type="primary"):
    # 同時過濾預算與評分
    filtered_list = [
        res for res in st.session_state.restaurant_db 
        if int(res['price']) <= budget and float(res['rating']) >= min_rating
    ]
    
    if filtered_list:
        selected = random.choice(filtered_list)
        st.balloons()
        
        with st.container():
            st.markdown(f"### 🎊 推薦結果：**{selected['name']}**")
            col1, col2 = st.columns(2)
            col1.metric("預估價格", f"${selected['price']}")
            col2.metric("網友評價", f"⭐️ {selected['rating']}")
            
            map_url = f"https://www.google.com/maps/search/?api=1&query={selected['name']}"
            st.markdown(f"[📍 點我開啟 Google 地圖]({map_url})")
    else:
        st.warning(f"找不到符合 ${budget} 元且高於 {min_rating} 顆星的餐廳，請調整篩選條件！")

# --- 5. 新增餐廳表單 ---
st.divider()
st.header("📝 新增美食口袋名單")
with st.form("add_form", clear_on_submit=True):
    new_name = st.text_input("餐廳名稱")
    c1, c2 = st.columns(2)
    new_price = c1.number_input("平均消費 ($)", min_value=0, step=10, value=100)
    new_rating = c2.slider("推薦評分 (0.0-5.0)", 0.0, 5.0, 4.0, 0.1)
    
    submitted = st.form_submit_button("新增至資料庫")
    if submitted and new_name:
        new_data = {"name": new_name, "price": int(new_price), "rating": float(new_rating)}
        st.session_state.restaurant_db.append(new_data)
        save_data(st.session_state.restaurant_db)
        st.success(f"✅ 已成功加入 {new_name}！")
        st.rerun()

# --- 6. 統計數據與表格展示 ---
st.divider()
st.header("📊 美食資料庫統計")
if st.session_state.restaurant_db:
    df = pd.DataFrame(st.session_state.restaurant_db)
    
    # 顯示三個小指標
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("總餐廳數", len(df))
    stat2.metric("平均價格", f"${int(df['price'].astype(int).mean())}")
    stat3.metric("平均評分", f"⭐ {df['rating'].astype(float).mean():.1f}")
    
    # 展示精美表格
    with st.expander("📂 查看完整清單"):
        st.dataframe(df, use_container_width=True, hide_index=True)


