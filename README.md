# 🗺️ Vietnam Map Coloring

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![AI](https://img.shields.io/badge/Algorithm-AC--3%20%7C%20Backtracking-orange.svg)

## 📌 Giới thiệu dự án (Nhóm 11)
Dự án ứng dụng Trí tuệ Nhân tạo để giải quyết bài toán **Tô màu bản đồ (Map Coloring)** cho 63 tỉnh thành Việt Nam. Đây là một bài toán điển hình về Ràng buộc (Constraint Satisfaction Problem - CSP) với mục tiêu sử dụng tối đa 4 màu sao cho không có 2 tỉnh giáp ranh nào trùng màu nhau.

🌍 **Link Demo Trực Tuyến:** [Bấm vào đây để xem dự án trên Streamlit](https://map-coloring-ery7uo22beomelatmh62um.streamlit.app/)

## 🚀 Các tính năng & Thuật toán cốt lõi
### 1. Tiền xử lý dữ liệu Không gian (GIS Processing)
- **Làm sạch dữ liệu:** Sử dụng `GeoPandas` và thuật toán `buffer(0)` kết hợp `intersects` để xử lý các lỗi hình học (Gap/Overlap) giữa ranh giới các tỉnh từ file GeoJSON thô.
- **Trích xuất Đồ thị kề (Adjacency Graph):** Chuyển đổi dữ liệu bản đồ thành cấu trúc dữ liệu Graph (Nodes & Edges) chuẩn xác làm đầu vào cho bộ giải AI.
### 2. Bộ giải AI nâng cao (Advanced AI Solver)
Dự án không chỉ sử dụng tìm kiếm đơn thuần mà tích hợp các kỹ thuật suy luận mạnh mẽ nhất trong CSP:
- **Thuật toán Tìm kiếm:** **Backtracking Search** tối ưu hóa.
- **Kỹ thuật Suy luận & Duy trì tính nhất quán:**
    - **Forward Checking (FC):** Nhìn trước một bước để loại bỏ sớm các màu không khả thi ở các tỉnh lân cận ngay khi một tỉnh vừa được tô.
    - **AC-3 Algorithm (Arc Consistency):** Duy trì tính nhất quán cung trên toàn bộ đồ thị, giúp phát hiện sớm các xung đột dây chuyền và cắt tỉa không gian tìm kiếm cực kỳ hiệu quả.
- **Chiến lược Chọn biến (Heuristics):**
    - **MRV (Minimum Remaining Values):** Ưu tiên tô màu cho các tỉnh đang có ít lựa chọn nhất.
    - **Degree Heuristic:** Ưu tiên các tỉnh có nhiều láng giềng nhất (các nút có bậc cao trong đồ thị).
### 3. Trực quan hóa & UX chuyên sâu
- **Timeline Step-by-step:** Cho phép theo dõi quá trình "suy luận" và "thử-sai" của AI theo thời gian thực.
- **Smart Viewport:** Tự động tính toán khung bao (**Bounding Box**) để zoom cận cảnh vào khu vực đang xử lý.
- **Labeling Optimization:** Tích hợp thư viện `adjustText` để tự động sắp xếp tên các tỉnh, tránh chồng chéo tại các khu vực có diện tích nhỏ (như Đồng bằng sông Hồng).

## 🛠️ Công nghệ sử dụng
- **AI Core:** Python, NetworkX (Graph theory)
- **GIS:** GeoPandas, Shapely, Fiona
- **Visuals:** Plotly Express, Matplotlib, adjustText
- **Web App:** Streamlit

## ⚙️ Cài đặt nhanh (Local)
1. Clone dự án: `git clone https://github.com/NTT555/Map-coloring.git`
2. Cài đặt thư viện: `pip install -r requirements.txt`
3. Chạy ứng dụng: `streamlit run app.py`
