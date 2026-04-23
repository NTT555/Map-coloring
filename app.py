import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd
import json
from src.csp_core import MapColoringCSP

# Tối ưu hóa không gian hiển thị ngay từ cấu hình trang
st.set_page_config(page_title="Map Coloring N6", layout="wide", initial_sidebar_state="collapsed")

# --- CSS TỐI ƯU HÓA KHÔNG GIAN (Compact UI) ---
st.markdown("""
    <style>
    /* Loại bỏ khoảng trống thừa ở đầu trang của Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Thu nhỏ tiêu đề chính */
    .main-title {
        font-size: 32px !important;
        font-weight: 800;
        text-align: center;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }

    /* Thu nhỏ Expander và các thành phần bên trong */
    .stExpander {
        border: 2px solid #3498DB !important;
        border-radius: 10px !important;
    }
    .st-expanderHeader {
        font-size: 18px !important; /* Nhỏ lại để tiết kiệm diện tích */
        color: #1A5276 !important;
        font-weight: bold !important;
        padding: 5px 15px !important;
    }
    .compact-label {
        font-size: 20px !important;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 2px;
    }
    .color-tag-small {
        font-size: 18px !important;
        color: #E67E22;
        font-weight: bold;
        background: #FEF5E7;
        padding: 2px 10px;
        border-radius: 6px;
        border: 1px solid #F39C12;
        display: inline-block;
        margin-right: 5px;
    }
    
    /* Thu nhỏ Slider */
    .stSlider { padding-top: 0rem !important; padding-bottom: 1rem !important; }
    
    /* Ẩn bớt padding không cần thiết giữa các phần tử */
    div[data-testid="stVerticalBlock"] > div {
        margin-top: -0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Hiển thị tiêu đề đã thu nhỏ
st.markdown("<div class='main-title'>🗺️ ĐỒ ÁN MAP COLORING - NHÓM 11</div>", unsafe_allow_html=True)

# --- CẤU HÌNH DỮ LIỆU ---
COLOR_DICT = {"#E74C3C": "Đỏ", "#3498DB": "Xanh Dương", "#2ECC71": "Xanh Lá", "#F1C40F": "Vàng"}
selected_colors = list(COLOR_DICT.keys())
GRAPH_PATH = "data/processed/adjacency_graph.json"

@st.cache_data
def load_map_data():
    gdf = gpd.read_file("data/raw/vietnam_provinces.geojson")
    name_col = 'TinhThanh'
    gdf['Clean_Name'] = gdf[name_col].str.replace('Thành phố ', '', regex=False).str.replace('Tỉnh ', '', regex=False).str.strip()
    gdf = gdf.set_index('Clean_Name')
    return gdf

@st.cache_data
def load_graph_data():
    with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

gdf_base = load_map_data()
full_graph = load_graph_data()

# --- SIDEBAR (Ẩn bớt để tập trung màn hình chính) ---
if st.sidebar.button("🚀 KHỞI CHẠY AI", use_container_width=True):
    csp = MapColoringCSP(GRAPH_PATH, selected_colors)
    csp.history.append({"action": "Bắt đầu", "assignment": {}, "domains": csp.get_domains({})})
    csp.backtrack(assignment={}, use_mrv=True)
    st.session_state['history'] = csp.history

# --- GIAO DIỆN CHÍNH (Đã tối ưu diện tích) ---
if 'history' in st.session_state:
    history = st.session_state['history']
    
    # Đưa slider lên cùng một hàng với label để tiết kiệm chỗ
    step = st.slider("🕹️ Timeline:", 0, len(history)-1, len(history)-1)
    
    curr = history[step]
    action_text = curr['action']
    current_assignment = curr['assignment']

    # --- THANH CHI TIẾT (EXPANDER) NHỎ GỌN ---
    with st.expander("🔍 HÀNH ĐỘNG CHI TIÊT", expanded=True):
        current_province = "N/A"
        for prov in gdf_base.index:
            if prov in action_text:
                current_province = prov
                break
        
        # Sử dụng 3 cột nhỏ để dàn hàng ngang thông tin trong expander
        c1, c2, c3 = st.columns([1, 1.5, 2])
        with c1:
            st.markdown(f"<div class='compact-label'>📍 Vị trí: <span style='color: #3498DB;'>{current_province}</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='compact-label'>📝: <span style='font-size: 16px; color: #5D6D7E;'>{action_text}</span></div>", unsafe_allow_html=True)
        with c3:
            # TỰ ĐỘNG TÍNH MIỀN GIÁ TRỊ 
            if current_province != "N/A":
                neighbors = full_graph.get(current_province, [])
                used_colors = {current_assignment[n] for n in neighbors if n in current_assignment and n != current_province}
                available_names = [COLOR_DICT[c] for c in selected_colors if c not in used_colors]
                
                color_html = "".join([f"<span class='color-tag-small'>{name}</span>" for name in available_names])
                st.markdown(f"<div class='compact-label'>🎨 Miền giá trị: {color_html if color_html else '❌'}</div>", unsafe_allow_html=True)

    # --- BẢN ĐỒ CHIẾM DIỆN TÍCH CÒN LẠI ---
    gdf_step = gdf_base.copy()
    gdf_step['Màu_AI'] = gdf_step.index.map(current_assignment).fillna("#EBEDEF")
    
    fig = px.choropleth_mapbox(
        gdf_step, geojson=gdf_step.geometry.__geo_interface__, locations=gdf_step.index,
        color="Màu_AI", color_discrete_map="identity",
        mapbox_style="carto-positron", zoom=5.2, center={"lat": 16.2, "lon": 106.0},
        opacity=0.9
    )
    # Giảm height xuống khoảng 550-600 để vừa vặn một màn hình laptop
    fig.update_layout(height=580, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Bấm nút bên trái để bắt đầu.")