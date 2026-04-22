import geopandas as gpd
import json
import os

def generate_correct_json():
    print("⏳ Đang đọc file bản đồ GeoJSON...")
    gdf = gpd.read_file("data/raw/vietnam_provinces.geojson")
    
    print("🧹 Đang chuẩn hóa tên 63 tỉnh thành...")
    gdf['Clean_Name'] = gdf['TinhThanh'].str.replace('Thành phố ', '', regex=False).str.replace('Tỉnh ', '', regex=False).str.strip()
    
    adj_dict = {}
    print("⚙️ Đang dùng thuật toán không gian (Buffer + Intersects) để tìm hàng xóm...")
    for i, row in gdf.iterrows():
        # BÍ QUYẾT: Nới rộng ranh giới ra 0.005 độ để lấp các khe hở, và dùng intersects để bắt lỗi chồng lấn
        geom = row.geometry.buffer(0.005)
        neighbors = gdf[
            (gdf.geometry.buffer(0.005).intersects(geom)) & 
            (gdf['Clean_Name'] != row['Clean_Name'])
        ]['Clean_Name'].tolist()
        adj_dict[row['Clean_Name']] = neighbors
        
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/adjacency_graph.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(adj_dict, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Đã tạo thành công file {output_path} với ranh giới chính xác tuyệt đối!")

if __name__ == "__main__":
    generate_correct_json()