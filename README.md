# 🗺️ Vietnam Map Coloring - AI Constraint Satisfaction Problem

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![GeoPandas](https://img.shields.io/badge/GeoPandas-0.10+-green.svg)

## 📌 Giới thiệu dự án (Nhóm 06)
Dự án ứng dụng Trí tuệ Nhân tạo (AI) để giải quyết bài toán **Tô màu bản đồ (Map Coloring)** cho 63 tỉnh thành Việt Nam. Mục tiêu là sử dụng tối đa 4 màu sao cho không có 2 tỉnh nào giáp ranh bị trùng màu, tuân thủ chặt chẽ Định lý 4 màu (Four Color Theorem).

🌍 **Link Demo Trực Tuyến:** 
[Bấm vào đây để xem dự án trên Streamlit](https://map-coloring-ery7uo22beomelatmh62um.streamlit.app/)
## 🚀 Các tính năng cốt lõi
1. **Làm sạch Dữ liệu Không gian (GIS Data Processing):**
   - Tự động phát hiện và sửa các lỗi ranh giới bản đồ (overlap/gap) từ file GeoJSON thô bằng thuật toán `buffer` và `intersects` của thư viện GeoPandas.
   - Trích xuất thành công ma trận kề (Adjacency Graph) chuẩn xác cho 63 tỉnh thành.
2. **Thuật toán Thông minh (AI Core):** - Tích hợp thuật toán Backtracking kết hợp với Heuristics nâng cao: **MRV (Minimum Remaining Values)** và **Degree Heuristic**.
   - Giúp AI ưu tiên xử lý các khu vực khó, cắt tỉa không gian tìm kiếm và giải quyết bài toán cực kỳ tối ưu.
3. **UI/UX Tương tác Trực quan:** - Giao diện Web Step-by-step cho phép người dùng kéo Timeline để xem AI "suy nghĩ", thử màu, và quay lui ở từng bước.
   - Tự động zoom cận cảnh (Bounding Box) và tản chữ (adjustText) chống đè rập cho các khu vực diện tích nhỏ.
## 🛠️ Công nghệ sử dụng (Tech Stack)
- **Ngôn ngữ:** Python
- **Xử lý Dữ liệu Không gian:** Pandas, GeoPandas, Shapely
- **Đồ thị & Trực quan hóa:** NetworkX, Matplotlib, adjustText
- **Giao diện Web:** Streamlit

