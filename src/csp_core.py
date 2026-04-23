import copy

class MapColoringCSP:
    def __init__(self, variables, neighbors, colors):
        self.variables = variables  # Danh sách tỉnh
        self.neighbors = neighbors  # Dict hàng xóm
        self.colors = colors        # Danh sách mã màu
        # Khởi tạo Domain: mỗi tỉnh ban đầu đều có thể chọn tất cả các màu
        self.domains = {v: list(colors) for v in variables}

    def is_consistent(self, var, color, assignment):
        """Kiểm tra màu có bị trùng với hàng xóm đã tô không"""
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    def forward_checking(self, var, color, domains):
        """Kỹ thuật Forward Checking: Xóa màu khỏi domain của hàng xóm"""
        new_domains = copy.deepcopy(domains)
        for neighbor in self.neighbors.get(var, []):
            if neighbor not in self.assignment: # Chỉ xét hàng xóm chưa tô
                if color in new_domains[neighbor]:
                    new_domains[neighbor].remove(color)
                    # Nếu một hàng xóm hết màu để chọn -> Thất bại
                    if not new_domains[neighbor]:
                        return None
        return new_domains

    def ac3(self, domains):
        """Thuật toán AC-3 để duy trì Arc Consistency"""
        queue = [(u, v) for u in self.variables for v in self.neighbors.get(u, [])]
        new_domains = copy.deepcopy(domains)

        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj, new_domains):
                if not new_domains[xi]:
                    return None
                for xk in self.neighbors.get(xi, []):
                    if xk != xj:
                        queue.append((xk, xi))
        return new_domains

    def revise(self, xi, xj, domains):
        """Hỗ trợ AC-3: Xóa các giá trị không thỏa mãn ràng buộc"""
        revised = False
        for x in domains[xi][:]:
            # Nếu không có màu nào ở xj khác với màu x ở xi -> Vi phạm
            if all(x == y for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    def solve(self, use_ac3=False):
        self.assignment = {}
        self.history = []
        # Nếu dùng AC-3, chạy bước lọc domain ban đầu
        current_domains = self.ac3(self.domains) if use_ac3 else self.domains
        return self.backtrack(self.assignment, current_domains, use_ac3)

    def backtrack(self, assignment, domains, use_ac3):
        if len(assignment) == len(self.variables):
            return assignment

        # 1. Heuristic chọn biến (MRV + Degree)
        var = self.select_unassigned_variable(assignment, domains)
        
        # 2. Thử từng màu cho tỉnh đã chọn
        for color in domains[var]:
            if self.is_consistent(var, color, assignment):
                assignment[var] = color
                self.assignment = assignment
                
                # Lưu lịch sử để hiển thị Timeline trên Streamlit
                self.history.append(copy.deepcopy(assignment))

                # 3. Sử dụng Forward Checking hoặc AC-3 để cắt tỉa Domain
                if use_ac3:
                    # Gán cứng màu đã chọn cho biến hiện tại trước khi chạy AC-3
                    local_domains = copy.deepcopy(domains)
                    local_domains[var] = [color]
                    new_domains = self.ac3(local_domains)
                else:
                    new_domains = self.forward_checking(var, color, domains)

                if new_domains is not None:
                    result = self.backtrack(assignment, new_domains, use_ac3)
                    if result: return result

                # Quay lui
                del assignment[var]
                self.assignment = assignment
        
        return None

    def select_unassigned_variable(self, assignment, domains):
        """MRV + Degree Heuristic"""
        unassigned = [v for v in self.variables if v not in assignment]
        # Sắp xếp theo số lượng màu còn lại (MRV), nếu bằng nhau thì chọn tỉnh nhiều hàng xóm nhất
        return min(unassigned, key=lambda v: (len(domains[v]), -len(self.neighbors.get(v, []))))