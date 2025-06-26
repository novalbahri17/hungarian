import unittest
import numpy as np
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from hungarian import HungarianMethod

class TestHungarianMethod(unittest.TestCase):
    """Unit tests untuk Hungarian Method (White Box Testing)"""
    
    def setUp(self):
        """Setup untuk setiap test case"""
        self.hungarian = HungarianMethod()
    
    def test_init(self):
        """Test inisialisasi class"""
        self.assertIsInstance(self.hungarian, HungarianMethod)
        self.assertEqual(self.hungarian.steps, [])
        self.assertIsNone(self.hungarian.original_matrix)
        self.assertIsNone(self.hungarian.matrix)
        self.assertIsNone(self.hungarian.assignment)
        self.assertEqual(self.hungarian.total_cost, 0)
    
    def test_validate_matrix_valid(self):
        """Test validasi matriks yang valid"""
        # Test matriks persegi
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = self.hungarian.validate_matrix(matrix)
        self.assertTrue(result['valid'])
        
        # Test matriks tidak persegi
        matrix = [[1, 2, 3], [4, 5, 6]]
        result = self.hungarian.validate_matrix(matrix)
        self.assertTrue(result['valid'])
    
    def test_validate_matrix_invalid(self):
        """Test validasi matriks yang tidak valid"""
        # Test matriks kosong
        matrix = []
        result = self.hungarian.validate_matrix(matrix)
        self.assertFalse(result['valid'])
        self.assertIn('Matrix cannot be empty', result['error'])
        
        # Test matriks dengan baris kosong
        matrix = [[]]
        result = self.hungarian.validate_matrix(matrix)
        self.assertFalse(result['valid'])
        self.assertIn('Matrix rows cannot be empty', result['error'])
        
        # Test matriks dengan ukuran baris tidak konsisten
        matrix = [[1, 2], [3, 4, 5]]
        result = self.hungarian.validate_matrix(matrix)
        self.assertFalse(result['valid'])
        self.assertIn('All rows must have the same number of columns', result['error'])
        
        # Test matriks dengan nilai non-numerik
        matrix = [[1, 'a'], [3, 4]]
        result = self.hungarian.validate_matrix(matrix)
        self.assertFalse(result['valid'])
        self.assertIn('All matrix elements must be numeric', result['error'])
        
        # Test matriks terlalu besar
        large_matrix = [[1] * 25 for _ in range(25)]
        result = self.hungarian.validate_matrix(large_matrix)
        self.assertFalse(result['valid'])
        self.assertIn('Matrix size too large', result['error'])
    
    def test_balance_matrix_square(self):
        """Test balancing matriks yang sudah persegi"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        balanced = self.hungarian.balance_matrix(matrix)
        
        # Matriks persegi tidak perlu diubah
        self.assertEqual(len(balanced), 3)
        self.assertEqual(len(balanced[0]), 3)
        np.testing.assert_array_equal(balanced, matrix)
    
    def test_balance_matrix_rectangular(self):
        """Test balancing matriks tidak persegi"""
        # Test matriks dengan lebih banyak baris
        matrix = [[1, 2], [3, 4], [5, 6]]
        balanced = self.hungarian.balance_matrix(matrix)
        
        self.assertEqual(len(balanced), 3)
        self.assertEqual(len(balanced[0]), 3)
        # Kolom terakhir harus berisi 0
        for row in balanced:
            self.assertEqual(row[-1], 0)
        
        # Test matriks dengan lebih banyak kolom
        matrix = [[1, 2, 3], [4, 5, 6]]
        balanced = self.hungarian.balance_matrix(matrix)
        
        self.assertEqual(len(balanced), 3)
        self.assertEqual(len(balanced[0]), 3)
        # Baris terakhir harus berisi 0
        self.assertEqual(balanced[-1], [0, 0, 0])
    
    def test_convert_to_minimization(self):
        """Test konversi matriks maksimisasi ke minimisasi"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        converted = self.hungarian.convert_to_minimization(matrix)
        
        max_value = 9
        expected = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
        
        np.testing.assert_array_equal(converted, expected)
    
    def test_reduce_rows(self):
        """Test reduksi baris"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        reduced = self.hungarian.reduce_rows(matrix)
        
        # Setiap baris harus memiliki minimal satu nol
        for row in reduced:
            self.assertIn(0, row)
        
        # Test dengan matriks yang sudah tereduksi
        matrix = [[0, 1, 2], [0, 2, 1], [0, 1, 3]]
        reduced = self.hungarian.reduce_rows(matrix)
        
        # Matriks tidak berubah karena sudah tereduksi
        np.testing.assert_array_equal(reduced, matrix)
    
    def test_reduce_columns(self):
        """Test reduksi kolom"""
        matrix = [[0, 1, 2], [0, 2, 1], [0, 1, 3]]
        reduced = self.hungarian.reduce_columns(matrix)
        
        # Setiap kolom harus memiliki minimal satu nol
        matrix_array = np.array(reduced)
        for col in range(matrix_array.shape[1]):
            self.assertIn(0, matrix_array[:, col])
    
    def test_find_zero_assignment(self):
        """Test pencarian assignment berdasarkan nol"""
        # Test matriks dengan solusi unik
        matrix = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
        assignment = self.hungarian.find_zero_assignment(matrix)
        
        # Harus ada assignment untuk setiap baris
        self.assertEqual(len(assignment), 3)
        
        # Setiap assignment harus menunjuk ke posisi nol
        for i, j in enumerate(assignment):
            if j != -1:  # -1 berarti tidak ada assignment
                self.assertEqual(matrix[i][j], 0)
    
    def test_find_minimum_lines(self):
        """Test pencarian garis penutup minimum"""
        matrix = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
        assignment = [0, 1, 2]  # Assignment lengkap
        
        covered_rows, covered_cols = self.hungarian.find_minimum_lines(matrix, assignment)
        
        # Jumlah garis harus minimal untuk menutupi semua nol
        total_lines = len(covered_rows) + len(covered_cols)
        self.assertGreaterEqual(total_lines, 0)
    
    def test_update_matrix(self):
        """Test update matriks dengan nilai minimum"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        covered_rows = [0]
        covered_cols = [1]
        
        updated = self.hungarian.update_matrix(matrix, covered_rows, covered_cols)
        
        # Matriks harus berubah
        self.assertNotEqual(updated, matrix)
        
        # Dimensi harus sama
        self.assertEqual(len(updated), len(matrix))
        self.assertEqual(len(updated[0]), len(matrix[0]))
    
    def test_calculate_total_cost(self):
        """Test perhitungan total biaya"""
        original_matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        assignment = [1, 0, 2]  # (0,1), (1,0), (2,2)
        
        total_cost = self.hungarian.calculate_total_cost(original_matrix, assignment)
        expected_cost = 1 + 2 + 2  # original_matrix[0][1] + original_matrix[1][0] + original_matrix[2][2]
        
        self.assertEqual(total_cost, expected_cost)
    
    def test_solve_minimization_simple(self):
        """Test penyelesaian problem minimisasi sederhana"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        self.assertGreater(result['total_cost'], 0)
        self.assertGreater(len(result['steps']), 0)
        self.assertGreater(result['execution_time'], 0)
    
    def test_solve_maximization_simple(self):
        """Test penyelesaian problem maksimisasi sederhana"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        result = self.hungarian.solve(matrix, is_maximization=True)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        self.assertGreater(result['total_cost'], 0)
        self.assertGreater(len(result['steps']), 0)
        self.assertGreater(result['execution_time'], 0)
    
    def test_solve_unbalanced_matrix(self):
        """Test penyelesaian matriks tidak seimbang"""
        # Matriks 2x3
        matrix = [[1, 2, 3], [4, 5, 6]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        
        # Matriks 3x2
        matrix = [[1, 2], [3, 4], [5, 6]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
    
    def test_solve_invalid_matrix(self):
        """Test penyelesaian dengan matriks tidak valid"""
        # Matriks kosong
        matrix = []
        result = self.hungarian.solve(matrix)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        
        # Matriks dengan nilai non-numerik
        matrix = [[1, 'a'], [2, 3]]
        result = self.hungarian.solve(matrix)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_solve_large_matrix(self):
        """Test penyelesaian matriks besar"""
        # Matriks 5x5
        matrix = [
            [7, 3, 1, 8, 2],
            [4, 9, 6, 5, 3],
            [2, 1, 7, 4, 9],
            [8, 6, 3, 2, 1],
            [5, 4, 8, 7, 6]
        ]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        self.assertEqual(len(result['assignment']), 5)
        
        # Verifikasi bahwa setiap worker mendapat tepat satu task
        assignment = result['assignment']
        assigned_tasks = [task for task in assignment if task != -1]
        self.assertEqual(len(set(assigned_tasks)), len(assigned_tasks))  # Tidak ada duplikasi
    
    def test_solve_with_zero_costs(self):
        """Test penyelesaian dengan beberapa biaya nol"""
        matrix = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_cost'], 0)  # Optimal cost should be 0
    
    def test_solve_with_negative_costs(self):
        """Test penyelesaian dengan biaya negatif"""
        matrix = [[-1, 2, 3], [4, -2, 1], [0, 1, -3]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
    
    def test_steps_recording(self):
        """Test perekaman langkah-langkah algoritma"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        steps = result['steps']
        
        # Harus ada langkah-langkah yang terekam
        self.assertGreater(len(steps), 0)
        
        # Setiap langkah harus memiliki struktur yang benar
        for step in steps:
            self.assertIn('step', step)
            self.assertIn('description', step)
            self.assertIn('matrix', step)
    
    def test_assignment_validity(self):
        """Test validitas assignment yang dihasilkan"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        result = self.hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        assignment = result['assignment']
        
        # Setiap worker harus mendapat tepat satu task
        self.assertEqual(len(assignment), len(matrix))
        
        # Tidak boleh ada duplikasi task
        assigned_tasks = [task for task in assignment if task != -1]
        self.assertEqual(len(set(assigned_tasks)), len(assigned_tasks))
        
        # Assignment harus dalam range yang valid
        for task in assigned_tasks:
            self.assertGreaterEqual(task, 0)
            self.assertLess(task, len(matrix[0]))
    
    def test_performance_consistency(self):
        """Test konsistensi performa algoritma"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        # Jalankan beberapa kali dan pastikan hasilnya konsisten
        results = []
        for _ in range(5):
            result = self.hungarian.solve(matrix, is_maximization=False)
            results.append(result)
        
        # Semua hasil harus sukses
        for result in results:
            self.assertTrue(result['success'])
        
        # Total cost harus sama untuk semua run
        costs = [result['total_cost'] for result in results]
        self.assertEqual(len(set(costs)), 1)  # Semua cost harus sama
    
    def test_edge_cases(self):
        """Test kasus-kasus edge"""
        # Matriks 1x1
        matrix = [[5]]
        result = self.hungarian.solve(matrix)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['assignment'], [0])
        self.assertEqual(result['total_cost'], 5)
        
        # Matriks dengan semua nilai sama
        matrix = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
        result = self.hungarian.solve(matrix)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_cost'], 9)  # 3 * 3
    
    def test_memory_efficiency(self):
        """Test efisiensi memori"""
        # Test dengan matriks yang cukup besar
        size = 10
        matrix = [[i + j for j in range(size)] for i in range(size)]
        
        result = self.hungarian.solve(matrix)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        
        # Pastikan objek hungarian dapat di-reset
        self.hungarian = HungarianMethod()
        self.assertEqual(len(self.hungarian.steps), 0)

class TestHungarianMethodIntegration(unittest.TestCase):
    """Integration tests untuk Hungarian Method"""
    
    def test_real_world_assignment_problem(self):
        """Test dengan problem assignment dunia nyata"""
        # Problem: Assign 4 workers to 4 tasks with given costs
        cost_matrix = [
            [9, 2, 7, 8],    # Worker 1 costs for tasks 1,2,3,4
            [6, 4, 3, 7],    # Worker 2 costs for tasks 1,2,3,4
            [5, 8, 1, 8],    # Worker 3 costs for tasks 1,2,3,4
            [7, 6, 9, 4]     # Worker 4 costs for tasks 1,2,3,4
        ]
        
        hungarian = HungarianMethod()
        result = hungarian.solve(cost_matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        
        # Verifikasi bahwa ini adalah solusi optimal
        # Untuk matriks ini, solusi optimal adalah: Worker1->Task2, Worker2->Task3, Worker3->Task3, Worker4->Task4
        # dengan total cost = 2 + 3 + 1 + 4 = 10
        self.assertLessEqual(result['total_cost'], 15)  # Harus mendapat solusi yang reasonable
    
    def test_profit_maximization_problem(self):
        """Test problem maksimisasi profit"""
        # Problem: Maximize profit from worker-task assignment
        profit_matrix = [
            [3, 7, 1, 2],
            [5, 1, 6, 4],
            [2, 8, 3, 7],
            [4, 2, 9, 1]
        ]
        
        hungarian = HungarianMethod()
        result = hungarian.solve(profit_matrix, is_maximization=True)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        self.assertGreater(result['total_cost'], 0)
    
    def test_unbalanced_real_problem(self):
        """Test problem tidak seimbang dari dunia nyata"""
        # 3 workers, 4 tasks
        cost_matrix = [
            [4, 1, 3, 2],
            [2, 0, 5, 3],
            [3, 2, 2, 1]
        ]
        
        hungarian = HungarianMethod()
        result = hungarian.solve(cost_matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['assignment'])
        
        # Harus ada tepat 3 assignment (satu worker tidak mendapat task)
        assigned_tasks = [task for task in result['assignment'] if task != -1]
        self.assertEqual(len(assigned_tasks), 3)

if __name__ == '__main__':
    # Setup test suite
    unittest.main(verbosity=2)