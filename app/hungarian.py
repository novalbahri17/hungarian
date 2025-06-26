import numpy as np
import copy
from typing import List, Tuple, Optional, Dict, Any

class HungarianMethod:
    """
    Implementasi manual Hungarian Method untuk menyelesaikan assignment problem.
    Mendukung minimisasi, maksimisasi, dan kasus tidak seimbang.
    """
    
    def __init__(self):
        self.original_matrix = None
        self.cost_matrix = None
        self.assignment = None
        self.total_cost = 0
        self.steps = []
        self.is_maximization = False
        self.dummy_rows = 0
        self.dummy_cols = 0
        
    def solve(self, matrix: List[List[float]], maximize: bool = False) -> Dict[str, Any]:
        """
        Menyelesaikan assignment problem menggunakan Hungarian Method.
        
        Args:
            matrix: Matriks biaya (list of lists)
            maximize: True untuk maksimisasi, False untuk minimisasi
            
        Returns:
            Dictionary berisi hasil dan langkah-langkah
        """
        self.original_matrix = copy.deepcopy(matrix)
        self.is_maximization = maximize
        self.steps = []
        
        # Validasi input
        if not self._validate_input(matrix):
            raise ValueError("Input matrix tidak valid")
            
        # Konversi ke numpy array
        self.cost_matrix = np.array(matrix, dtype=float)
        
        # Log langkah awal
        self._log_step("Input Matrix", self.cost_matrix.copy())
        
        # Jika maksimisasi, konversi ke minimisasi
        if maximize:
            max_val = np.max(self.cost_matrix)
            self.cost_matrix = max_val - self.cost_matrix
            self._log_step("Konversi Maksimisasi ke Minimisasi", self.cost_matrix.copy())
            
        # Buat matriks seimbang jika perlu
        self._balance_matrix()
        
        # Langkah 1: Reduksi baris
        self._reduce_rows()
        
        # Langkah 2: Reduksi kolom
        self._reduce_columns()
        
        # Langkah 3-5: Iterasi hingga solusi optimal
        while True:
            # Langkah 3: Cari assignment dengan nol
            assignment = self._find_assignment()
            
            if len(assignment) == min(self.cost_matrix.shape):
                # Solusi ditemukan
                self.assignment = assignment
                break
                
            # Langkah 4: Cari minimum covering lines
            lines = self._find_minimum_lines(assignment)
            
            # Langkah 5: Update matriks
            self._update_matrix(lines)
            
        # Hitung total biaya
        self._calculate_total_cost()
        
        return self._prepare_result()
        
    def _validate_input(self, matrix: List[List[float]]) -> bool:
        """
        Validasi input matrix.
        """
        if not matrix or not matrix[0]:
            return False
            
        rows = len(matrix)
        cols = len(matrix[0])
        
        # Cek konsistensi kolom
        for row in matrix:
            if len(row) != cols:
                return False
                
        # Cek apakah semua elemen adalah angka
        try:
            for row in matrix:
                for val in row:
                    float(val)
        except (ValueError, TypeError):
            return False
            
        return True
        
    def _balance_matrix(self):
        """
        Membuat matriks seimbang dengan menambah dummy rows/columns.
        """
        rows, cols = self.cost_matrix.shape
        
        if rows == cols:
            return
            
        if rows < cols:
            # Tambah dummy rows
            self.dummy_rows = cols - rows
            dummy = np.zeros((self.dummy_rows, cols))
            self.cost_matrix = np.vstack([self.cost_matrix, dummy])
            self._log_step(f"Menambah {self.dummy_rows} dummy rows", self.cost_matrix.copy())
            
        elif cols < rows:
            # Tambah dummy columns
            self.dummy_cols = rows - cols
            dummy = np.zeros((rows, self.dummy_cols))
            self.cost_matrix = np.hstack([self.cost_matrix, dummy])
            self._log_step(f"Menambah {self.dummy_cols} dummy columns", self.cost_matrix.copy())
            
    def _reduce_rows(self):
        """
        Langkah 1: Reduksi baris - kurangi setiap baris dengan nilai minimum baris tersebut.
        """
        for i in range(self.cost_matrix.shape[0]):
            min_val = np.min(self.cost_matrix[i, :])
            if min_val > 0:
                self.cost_matrix[i, :] -= min_val
                
        self._log_step("Reduksi Baris", self.cost_matrix.copy())
        
    def _reduce_columns(self):
        """
        Langkah 2: Reduksi kolom - kurangi setiap kolom dengan nilai minimum kolom tersebut.
        """
        for j in range(self.cost_matrix.shape[1]):
            min_val = np.min(self.cost_matrix[:, j])
            if min_val > 0:
                self.cost_matrix[:, j] -= min_val
                
        self._log_step("Reduksi Kolom", self.cost_matrix.copy())
        
    def _find_assignment(self) -> List[Tuple[int, int]]:
        """
        Langkah 3: Cari assignment menggunakan nol dalam matriks.
        """
        assignment = []
        matrix_copy = self.cost_matrix.copy()
        
        # Cari nol dan buat assignment
        while True:
            # Cari baris dengan nol paling sedikit
            zero_counts = []
            for i in range(matrix_copy.shape[0]):
                zeros_in_row = np.sum(matrix_copy[i, :] == 0)
                if zeros_in_row > 0:
                    zero_counts.append((zeros_in_row, i))
                    
            if not zero_counts:
                break
                
            # Pilih baris dengan nol paling sedikit
            zero_counts.sort()
            _, row = zero_counts[0]
            
            # Cari kolom dengan nol di baris ini
            zero_cols = np.where(matrix_copy[row, :] == 0)[0]
            if len(zero_cols) == 0:
                break
                
            col = int(zero_cols[0])  # Konversi numpy int64 ke Python int
            assignment.append((int(row), col))  # Pastikan row juga Python int
            
            # Hapus baris dan kolom yang sudah diassign
            matrix_copy[row, :] = float('inf')
            matrix_copy[:, col] = float('inf')
            
        return assignment
        
    def _find_minimum_lines(self, assignment: List[Tuple[int, int]]) -> Dict[str, List[int]]:
        """
        Langkah 4: Cari minimum number of lines untuk cover semua nol.
        """
        n = self.cost_matrix.shape[0]
        
        # Buat graf bipartit
        unassigned_rows = set(range(n))
        assigned_cols = set()
        
        for row, col in assignment:
            unassigned_rows.discard(row)
            assigned_cols.add(col)
            
        # Marking algorithm
        marked_rows = set(unassigned_rows)
        marked_cols = set()
        
        changed = True
        while changed:
            changed = False
            
            # Mark columns yang memiliki nol di marked rows
            for row in marked_rows:
                for col in range(n):
                    if self.cost_matrix[row, col] == 0 and col not in marked_cols:
                        marked_cols.add(col)
                        changed = True
                        
            # Mark rows yang memiliki assignment di marked columns
            for row, col in assignment:
                if col in marked_cols and row not in marked_rows:
                    marked_rows.add(row)
                    changed = True
                    
        # Lines: unmarked rows + marked columns
        covering_rows = [i for i in range(n) if i not in marked_rows]
        covering_cols = list(marked_cols)
        
        return {'rows': covering_rows, 'cols': covering_cols}
        
    def _update_matrix(self, lines: Dict[str, List[int]]):
        """
        Langkah 5: Update matriks dengan mengurangi nilai minimum dari uncovered elements.
        """
        n = self.cost_matrix.shape[0]
        
        # Cari uncovered elements
        uncovered_elements = []
        for i in range(n):
            for j in range(n):
                if i not in lines['rows'] and j not in lines['cols']:
                    uncovered_elements.append(self.cost_matrix[i, j])
                    
        if not uncovered_elements:
            return
            
        min_uncovered = min(uncovered_elements)
        
        # Update matriks
        for i in range(n):
            for j in range(n):
                if i not in lines['rows'] and j not in lines['cols']:
                    # Uncovered: kurangi dengan minimum
                    self.cost_matrix[i, j] -= min_uncovered
                elif i in lines['rows'] and j in lines['cols']:
                    # Intersection: tambah dengan minimum
                    self.cost_matrix[i, j] += min_uncovered
                    
        self._log_step(f"Update Matrix (min uncovered: {min_uncovered})", self.cost_matrix.copy())
        
    def _calculate_total_cost(self):
        """
        Hitung total biaya dari assignment yang ditemukan.
        """
        original = np.array(self.original_matrix)
        
        # Jika ada dummy rows/cols, sesuaikan assignment
        valid_assignment = []
        for row, col in self.assignment:
            if (row < len(self.original_matrix) and 
                col < len(self.original_matrix[0])):
                valid_assignment.append((row, col))
                
        self.assignment = valid_assignment
        
        # Hitung total cost
        self.total_cost = 0
        for row, col in self.assignment:
            self.total_cost += original[row, col]
            
    def _log_step(self, description: str, matrix: np.ndarray):
        """
        Log langkah-langkah algoritma.
        """
        self.steps.append({
            'description': description,
            'matrix': matrix.copy()
        })
        
    def _prepare_result(self) -> Dict[str, Any]:
        """
        Siapkan hasil akhir.
        """
        # Konversi numpy types ke Python native types untuk JSON serialization
        return {
            'assignment': self.assignment,
            'total_cost': float(self.total_cost),  # Konversi ke Python float
            'steps': self._convert_steps_to_json_serializable(),
            'original_matrix': self.original_matrix,
            'is_maximization': self.is_maximization,
            'optimal_value': float(self.total_cost)  # Konversi ke Python float
        }
        
    def get_assignment_matrix(self) -> np.ndarray:
        """
        Buat matriks assignment (1 untuk assigned, 0 untuk tidak).
        """
        if not self.assignment:
            return None
            
        rows = len(self.original_matrix)
        cols = len(self.original_matrix[0])
        assignment_matrix = np.zeros((rows, cols))
        
        for row, col in self.assignment:
            if row < rows and col < cols:
                assignment_matrix[row, col] = 1
                
        return assignment_matrix
    
    def _convert_steps_to_json_serializable(self) -> List[Dict[str, Any]]:
        """
        Konversi steps yang mengandung numpy arrays ke format yang bisa di-serialize ke JSON.
        """
        json_steps = []
        for step in self.steps:
            json_step = {
                'description': step['description'],
                'matrix': step['matrix'].tolist() if isinstance(step['matrix'], np.ndarray) else step['matrix']
            }
            json_steps.append(json_step)
        return json_steps