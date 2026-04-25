import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd
import json
from src.csp_core import MapColoringCSP

# Tối ưu hóa không gian hiển thị ngay từ cấu hình trang
st.set_page_config(page_title="Map Coloring N11", layout="wide", initial_sidebar_state="collapsed")

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
st.markdown("<div class='main-title'>🗺️ ĐỒ ÁN MAP COLORING NHÓM 11</div>", unsafe_allow_html=True)

# --- CẤU HÌNH DỮ LIỆU ---
COLOR_DICT = {"#E74C3C": "Đỏ", "#3498DB": "Xanh Dương", "#2ECC71": "Xanh Lá", "#F1C40F": "Vàng"}
selected_colors = list(COLOR_DICT.keys())
GRAPH_PATH = "data/processed/adjacency_graph.json"

@st.cache_data
def load_map_data():
    gdf = gpd.read_file("data/raw/vietnam_provinces.geojson")
    name_col = 'TinhThanh'
    #Làm sạch chuỗi tên tỉnh
    gdf['Clean_Name'] = gdf[name_col].str.replace('Thành phố ', '', regex=False).str.replace('Tỉnh ', '', regex=False).str.strip()
    gdf = gdf.set_index('Clean_Name')
    gdf['geometry'] = gdf.geometry.buffer(0)
    return gdf

@st.cache_data
def load_graph_data():
    with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

gdf_base = load_map_data()
full_graph = load_graph_data()

# --- SIDEBAR ---
st.sidebar.markdown("---")
# Thêm nút chọn để demo sự bá đạo của AC-3 cho thầy cô xem
use_ac3 = st.sidebar.checkbox("🚀 Kích hoạt thuật toán AC-3", value=True)

if st.sidebar.button("🚀 KHỞI CHẠY AI", use_container_width=True):
    # Truyền đúng 3 tham số cho thuật toán lõi mới
    variables = list(full_graph.keys())
    csp = MapColoringCSP(variables, full_graph, selected_colors)
    
    # Chạy thuật toán solve mới
    csp.solve(use_ac3=use_ac3)
    st.session_state['history'] = csp.history

# --- GIAO DIỆN CHÍNH (Đã tối ưu diện tích) ---
if 'history' in st.session_state and len(st.session_state['history']) > 0:
    history = st.session_state['history']
    
    # Đưa slider lên cùng một hàng với label để tiết kiệm chỗ
    step = st.slider("🕹️ Timeline:", 0, len(history)-1, len(history)-1)
    
    # Xử lý tương thích với cấu trúc history mới của csp_core.py
    current_assignment = history[step]
    
    # Tự động suy luận hành động (Tỉnh nào vừa được tô màu)
    # Vì Python giữ nguyên thứ tự thêm vào dict, tỉnh cuối cùng chính là tỉnh vừa thao tác
    current_province = list(current_assignment.keys())[-1] if current_assignment else "N/A"
    
    if current_province != "N/A":
        color_hex = current_assignment[current_province]
        action_text = f"Tô màu {COLOR_DICT.get(color_hex, 'Mới')} cho {current_province}"
    else:
        action_text = "Đang khởi tạo thuật toán..."

    # --- THANH CHI TIẾT (EXPANDER) NHỎ GỌN ---
    with st.expander("🔍 HÀNH ĐỘNG CHI TIẾT", expanded=True):
        # Sử dụng 3 cột nhỏ để dàn hàng ngang thông tin trong expander
        c1, c2, c3 = st.columns([1, 1.5, 2])
        with c1:
            st.markdown(f"<div class='compact-label'>📍 Vị trí: <span style='color: #3498DB;'>{current_province}</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='compact-label'>📝: <span style='font-size: 16px; color: #5D6D7E;'>{action_text}</span></div>", unsafe_allow_html=True)
        with c3:
            # TỰ ĐỘNG TÍNH MIỀN GIÁ TRỊ (Domain thu hẹp do Forward Checking/AC-3)
            if current_province != "N/A":
                neighbors = full_graph.get(current_province, [])
                used_colors = {current_assignment[n] for n in neighbors if n in current_assignment}
                available_names = [COLOR_DICT[c] for c in selected_colors if c not in used_colors]
                
                color_html = "".join([f"<span class='color-tag-small'>{name}</span>" for name in available_names])
                st.markdown(f"<div class='compact-label'>🎨 Còn lại: {color_html if color_html else '❌ Hết màu'}</div>", unsafe_allow_html=True)

    # --- BẢN ĐỒ CHIẾM DIỆN TÍCH CÒN LẠI ---
    gdf_step = gdf_base.copy()
    gdf_step['Màu_AI'] = gdf_step.index.map(current_assignment).fillna("#EBEDEF")

    gdf_display = gdf_step.reset_index()
    # 1. Định nghĩa bản đồ
    fig = px.choropleth_mapbox(
        gdf_display, 
        geojson=gdf_display.geometry.__geo_interface__, 
        locations=gdf_display.index, 
        color="Màu_AI", 
        color_discrete_map="identity",
        hover_name="Clean_Name", 
        hover_data={
            "Màu_AI": False,    
        },
        mapbox_style="carto-positron", 
        zoom=5.2, 
        center={"lat": 16.2, "lon": 106.0},
        opacity=0.9
    )

    fig.update_traces(hovertemplate="<b style='font-size: 16px;'>%{hovertext}</b><extra></extra>")
    
    # 2. Cấu hình khung nhìn và HIỂN THỊ (Cần có 2 dòng này)
    fig.update_layout(height=580, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.info("👈 Bấm nút ở thanh bên trái để bắt đầu.")