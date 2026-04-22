import json
from src.heuristics import mrv_degree_heuristic

class MapColoringCSP:
    def __init__(self, graph_file, colors):
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph = json.load(f)
        self.colors = colors
        self.history = [] # Cuốn sổ ghi chép lịch sử chạy

    def is_safe(self, node, color, assignment):
        for neighbor in self.graph.get(node, []):
            if assignment.get(neighbor) == color:
                return False
        return True

    def get_domains(self, assignment):
        """Hàm tính toán Miền giá trị (màu còn lại hợp lệ) cho từng tỉnh"""
        domains = {}
        for node in self.graph:
            if node in assignment:
                domains[node] = [assignment[node]] # Đã tô thì chỉ còn 1 màu
            else:
                valid = [c for c in self.colors if self.is_safe(node, c, assignment)]
                domains[node] = valid
        return domains

    def backtrack(self, assignment={}, use_mrv=False):
        # Điều kiện dừng
        if len(assignment) == len(self.graph):
            return assignment

        # Chọn tỉnh tiếp theo
        if use_mrv:
            # Gọi hàm kết hợp mới thay vì hàm mrv cũ
            node = mrv_degree_heuristic(assignment, self.graph, self.colors) 
        else:
            unassigned = [n for n in self.graph.keys() if n not in assignment]
            node = unassigned[0]

        for color in self.colors:
            if self.is_safe(node, color, assignment):
                assignment[node] = color
                
                # --- THÊM ĐOẠN NÀY ĐỂ DỊCH MÃ HEX SANG TÊN MÀU ---
                color_names = {
                    "#E74C3C": "đỏ", 
                    "#3498DB": "xanh dương", 
                    "#2ECC71": "xanh lá", 
                    "#F1C40F": "vàng"
                }
                ten_mau = color_names.get(color, color) # Nếu không tìm thấy trong từ điển thì giữ nguyên mã
                
                # [LƯU LỊCH SỬ] - Ghi lại hành động (Sử dụng biến ten_mau)
                self.history.append({
                    "action": f"🖌️ Tô màu {ten_mau} cho {node}",
                    "assignment": assignment.copy(),
                    "domains": self.get_domains(assignment)
                })
                
                result = self.backtrack(assignment, use_mrv)
                if result:
                    return result
                
                # [LƯU LỊCH SỬ] - Nếu sai thì Xóa màu (Backtrack)
                del assignment[node]
                self.history.append({
                    "action": f"❌ Xung đột! Xóa màu {ten_mau} tại {node} và quay lui",
                    "assignment": assignment.copy(),
                    "domains": self.get_domains(assignment)
                })

        return None