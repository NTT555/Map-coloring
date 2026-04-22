def mrv_degree_heuristic(assignment, graph, colors):
    """
    Kết hợp MRV và Degree Heuristic:
    1. Tìm (các) tỉnh có số lượng màu hợp lệ còn lại ít nhất (MRV).
    2. Nếu có nhiều hơn 1 tỉnh hòa nhau, chọn tỉnh có nhiều hàng xóm CHƯA TÔ MÀU nhất (Degree).
    """
    unassigned_nodes = [node for node in graph.keys() if node not in assignment]
    
    if not unassigned_nodes:
        return None

    # --- BƯỚC 1: LỌC BẰNG MRV ---
    def count_valid_colors(node):
        valid_colors = 0
        for color in colors:
            neighbor_colors = [assignment.get(neighbor) for neighbor in graph.get(node, []) if neighbor in assignment]
            if color not in neighbor_colors:
                valid_colors += 1
        return valid_colors

    # Tính số màu khả dụng cho tất cả các tỉnh chưa tô
    mrv_counts = {node: count_valid_colors(node) for node in unassigned_nodes}
    min_mrv_value = min(mrv_counts.values())
    
    # Lấy danh sách TẤT CẢ các tỉnh có cùng số màu ít nhất (những tỉnh bị hòa)
    mrv_candidates = [node for node, count in mrv_counts.items() if count == min_mrv_value]

    # Nếu chỉ có 1 tỉnh thỏa mãn, trả về luôn không cần xét tiếp
    if len(mrv_candidates) == 1:
        return mrv_candidates[0]

    # --- BƯỚC 2: GIẢI QUYẾT HÒA BẰNG DEGREE HEURISTIC ---
    def count_unassigned_neighbors(node):
        # Đếm số lượng hàng xóm của tỉnh này mà CŨNG CHƯA ĐƯỢC TÔ MÀU
        return sum(1 for neighbor in graph.get(node, []) if neighbor not in assignment)

    # Trong số các ứng viên bị hòa, chọn ra tỉnh có nhiều hàng xóm chưa tô nhất
    best_node = max(mrv_candidates, key=count_unassigned_neighbors)
    
    return best_node