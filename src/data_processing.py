import geopandas as gpd
import json

def process_and_build_graph(geojson_path, output_json_path):
    # 1. Đọc dữ liệu
    gdf = gpd.read_file(geojson_path)
    
    # 2. Làm sạch tên tỉnh
    gdf['Clean_Name'] = gdf['TinhThanh'].str.replace('Thành phố ', '', regex=False).str.replace('Tỉnh ', '', regex=False).str.strip()
    
    gdf.loc[(gdf['Clean_Name'] == 'Lạng Sơn') & (gdf.geometry.centroid.y < 12), 'Clean_Name'] = 'Kiên Giang'

    gdf = gdf.set_index('Clean_Name')

    # 3. Fix Invalid Geometries
    gdf['geometry'] = gdf.geometry.buffer(0)
    
    # 4. Trích xuất ma trận láng giềng
    neighbors = {}
    
    gdf_buffered = gdf.copy()
    gdf_buffered['geometry'] = gdf_buffered.geometry.buffer(0.005)

    for prov1, row1 in gdf.iterrows():
        neighbors[prov1] = []
        for prov2, row2 in gdf_buffered.iterrows():
            if prov1 != prov2:
                # Nếu ranh giới thật của tỉnh 1 chạm vào ranh giới đã mở rộng của tỉnh 2
                if row1.geometry.intersects(row2.geometry):
                    neighbors[prov1].append(prov2)
                    
    # 5. Lưu ra file JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(neighbors, f, ensure_ascii=False, indent=4)
        
    print(f"Đã xử lý xong! Tổng số tỉnh trong Graph: {len(neighbors)}")

process_and_build_graph("data/raw/vietnam_provinces.geojson", "data/processed/adjacency_graph.json")