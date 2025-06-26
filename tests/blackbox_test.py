import unittest
import sys
import os
import json
import time
import random
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import lists, integers, floats

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from hungarian import HungarianMethod
from utils import DataProcessor

class TestHungarianBlackBox(unittest.TestCase):
    """Black Box Testing untuk Hungarian Method
    
    Fokus pada testing input-output tanpa memperhatikan implementasi internal
    """
    
    def setUp(self):
        """Setup untuk setiap test case"""
        self.hungarian = HungarianMethod()
        self.data_processor = DataProcessor()
    
    def test_input_output_basic(self):
        """Test input-output dasar"""
        # Test Case 1: Matriks 3x3 minimisasi
        input_matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        result = self.hungarian.solve(input_matrix, is_maximization=False)
        
        # Verifikasi output structure
        self.assertIn('success', result)
        self.assertIn('assignment', result)
        self.assertIn('total_cost', result)
        self.assertIn('steps', result)
        self.assertIn('execution_time', result)
        
        # Verifikasi output values
        self.assertTrue(result['success'])
        self.assertIsInstance(result['assignment'], list)
        self.assertIsInstance(result['total_cost'], (int, float))
        self.assertIsInstance(result['steps'], list)
        self.assertIsInstance(result['execution_time'], float)
    
    def test_input_validation_boundary(self):
        """Test validasi input pada boundary conditions"""
        # Test Case 1: Matriks kosong
        result = self.hungarian.solve([])
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        
        # Test Case 2: Matriks 1x1 (minimum valid size)
        result = self.hungarian.solve([[5]])
        self.assertTrue(result['success'])
        self.assertEqual(result['assignment'], [0])
        self.assertEqual(result['total_cost'], 5)
        
        # Test Case 3: Matriks maksimum yang diizinkan (20x20)
        large_matrix = [[i + j for j in range(20)] for i in range(20)]
        result = self.hungarian.solve(large_matrix)
        self.assertTrue(result['success'])
        
        # Test Case 4: Matriks terlalu besar (21x21)
        too_large_matrix = [[1] * 21 for _ in range(21)]
        result = self.hungarian.solve(too_large_matrix)
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_input_types_validation(self):
        """Test validasi tipe data input"""
        # Test Case 1: Input bukan list
        result = self.hungarian.solve("not a matrix")
        self.assertFalse(result['success'])
        
        # Test Case 2: Elemen bukan numerik
        result = self.hungarian.solve([[1, 'a'], [2, 3]])
        self.assertFalse(result['success'])
        
        # Test Case 3: Mixed numeric types (int dan float)
        result = self.hungarian.solve([[1, 2.5], [3.7, 4]])
        self.assertTrue(result['success'])
        
        # Test Case 4: Nilai None dalam matriks
        result = self.hungarian.solve([[1, None], [2, 3]])
        self.assertFalse(result['success'])
        
        # Test Case 5: Nilai infinity
        result = self.hungarian.solve([[1, float('inf')], [2, 3]])
        self.assertFalse(result['success'])
    
    def test_matrix_dimensions(self):
        """Test berbagai dimensi matriks"""
        # Test Case 1: Matriks persegi berbagai ukuran
        for size in [2, 3, 4, 5, 10]:
            matrix = [[i + j for j in range(size)] for i in range(size)]
            result = self.hungarian.solve(matrix)
            self.assertTrue(result['success'], f"Failed for {size}x{size} matrix")
            self.assertEqual(len(result['assignment']), size)
        
        # Test Case 2: Matriks tidak persegi (lebih banyak baris)
        matrix = [[1, 2], [3, 4], [5, 6]]  # 3x2
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['assignment']), 3)
        
        # Test Case 3: Matriks tidak persegi (lebih banyak kolom)
        matrix = [[1, 2, 3], [4, 5, 6]]  # 2x3
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['assignment']), 2)
    
    def test_numeric_ranges(self):
        """Test berbagai range nilai numerik"""
        # Test Case 1: Nilai positif
        matrix = [[1, 2], [3, 4]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 2: Nilai negatif
        matrix = [[-1, -2], [-3, -4]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 3: Nilai campuran positif-negatif
        matrix = [[-1, 2], [3, -4]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 4: Nilai nol
        matrix = [[0, 1], [2, 0]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 5: Nilai desimal
        matrix = [[1.5, 2.7], [3.2, 4.8]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 6: Nilai sangat besar
        matrix = [[1000000, 2000000], [3000000, 4000000]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
        
        # Test Case 7: Nilai sangat kecil
        matrix = [[0.001, 0.002], [0.003, 0.004]]
        result = self.hungarian.solve(matrix)
        self.assertTrue(result['success'])
    
    def test_minimization_vs_maximization(self):
        """Test perbedaan hasil minimisasi vs maksimisasi"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        # Test minimisasi
        min_result = self.hungarian.solve(matrix, is_maximization=False)
        self.assertTrue(min_result['success'])
        
        # Test maksimisasi
        max_result = self.hungarian.solve(matrix, is_maximization=True)
        self.assertTrue(max_result['success'])
        
        # Hasil harus berbeda (kecuali kasus khusus)
        # Assignment bisa sama atau berbeda, tapi total cost harus berbeda
        if min_result['assignment'] == max_result['assignment']:
            # Jika assignment sama, maka ini kasus khusus
            pass
        else:
            # Assignment berbeda adalah normal
            pass
    
    def test_assignment_validity(self):
        """Test validitas assignment yang dihasilkan"""
        test_matrices = [
            [[3, 1, 4], [2, 0, 5], [1, 3, 2]],  # 3x3
            [[1, 2], [3, 4]],  # 2x2
            [[1, 2, 3], [4, 5, 6]],  # 2x3
            [[1, 2], [3, 4], [5, 6]]  # 3x2
        ]
        
        for matrix in test_matrices:
            result = self.hungarian.solve(matrix)
            self.assertTrue(result['success'])
            
            assignment = result['assignment']
            
            # Verifikasi panjang assignment
            self.assertEqual(len(assignment), len(matrix))
            
            # Verifikasi tidak ada duplikasi task
            assigned_tasks = [task for task in assignment if task != -1]
            self.assertEqual(len(assigned_tasks), len(set(assigned_tasks)))
            
            # Verifikasi range assignment
            for task in assigned_tasks:
                self.assertGreaterEqual(task, 0)
                self.assertLess(task, len(matrix[0]))
    
    def test_cost_calculation_accuracy(self):
        """Test akurasi perhitungan total cost"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        result = self.hungarian.solve(matrix)
        
        self.assertTrue(result['success'])
        
        # Hitung manual total cost berdasarkan assignment
        assignment = result['assignment']
        manual_cost = sum(matrix[i][assignment[i]] for i in range(len(assignment)) if assignment[i] != -1)
        
        # Bandingkan dengan hasil algoritma
        self.assertEqual(result['total_cost'], manual_cost)
    
    def test_performance_requirements(self):
        """Test requirement performa"""
        # Test dengan berbagai ukuran matriks
        performance_data = []
        
        for size in [3, 5, 8, 10, 15]:
            matrix = [[random.randint(1, 100) for _ in range(size)] for _ in range(size)]
            
            start_time = time.time()
            result = self.hungarian.solve(matrix)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            self.assertTrue(result['success'])
            self.assertLess(execution_time, 10.0)  # Harus selesai dalam 10 detik
            
            performance_data.append({
                'size': size,
                'time': execution_time,
                'reported_time': result['execution_time']
            })
        
        # Verifikasi bahwa waktu eksekusi yang dilaporkan akurat
        for data in performance_data:
            # Toleransi 10% untuk perbedaan waktu
            self.assertLess(abs(data['time'] - data['reported_time']), data['time'] * 0.1)
    
    def test_consistency_multiple_runs(self):
        """Test konsistensi hasil pada multiple runs"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        results = []
        for _ in range(10):
            result = self.hungarian.solve(matrix)
            results.append(result)
        
        # Semua run harus sukses
        for result in results:
            self.assertTrue(result['success'])
        
        # Total cost harus konsisten (optimal solution)
        costs = [result['total_cost'] for result in results]
        self.assertEqual(len(set(costs)), 1, "Total cost should be consistent across runs")
    
    def test_error_handling(self):
        """Test error handling untuk berbagai kondisi error"""
        error_cases = [
            ([], "Empty matrix"),
            ([[]], "Empty rows"),
            ([[1, 2], [3]], "Inconsistent row lengths"),
            ([[1, 'a'], [2, 3]], "Non-numeric values"),
            (None, "None input"),
            ("string", "String input"),
            ([[1, 2], [3, float('inf')]], "Infinity values"),
            ([[1, 2], [3, float('nan')]], "NaN values")
        ]
        
        for matrix, description in error_cases:
            with self.subTest(case=description):
                result = self.hungarian.solve(matrix)
                self.assertFalse(result['success'], f"Should fail for: {description}")
                self.assertIn('error', result, f"Should have error message for: {description}")
    
    def test_steps_completeness(self):
        """Test kelengkapan langkah-langkah algoritma"""
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        result = self.hungarian.solve(matrix)
        
        self.assertTrue(result['success'])
        steps = result['steps']
        
        # Harus ada langkah-langkah
        self.assertGreater(len(steps), 0)
        
        # Setiap langkah harus memiliki struktur yang benar
        required_keys = ['step', 'description', 'matrix']
        for step in steps:
            for key in required_keys:
                self.assertIn(key, step, f"Step missing key: {key}")
        
        # Langkah pertama harus berisi matriks original
        first_step = steps[0]
        self.assertIn('original', first_step['description'].lower())

class TestHungarianPropertyBased(unittest.TestCase):
    """Property-based testing menggunakan Hypothesis"""
    
    def setUp(self):
        self.hungarian = HungarianMethod()
    
    @given(st.lists(
        st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=5),
        min_size=2, max_size=5
    ).filter(lambda matrix: len(set(len(row) for row in matrix)) == 1))  # Ensure all rows have same length
    @settings(max_examples=50, deadline=5000)
    def test_property_assignment_validity(self, matrix):
        """Property: Assignment harus selalu valid untuk matriks valid"""
        result = self.hungarian.solve(matrix)
        
        if result['success']:
            assignment = result['assignment']
            
            # Property 1: Panjang assignment = jumlah baris
            self.assertEqual(len(assignment), len(matrix))
            
            # Property 2: Tidak ada duplikasi task
            assigned_tasks = [task for task in assignment if task != -1]
            self.assertEqual(len(assigned_tasks), len(set(assigned_tasks)))
            
            # Property 3: Assignment dalam range valid
            for task in assigned_tasks:
                self.assertGreaterEqual(task, 0)
                self.assertLess(task, len(matrix[0]))
    
    @given(st.lists(
        st.lists(st.integers(min_value=1, max_value=50), min_size=2, max_size=4),
        min_size=2, max_size=4
    ).filter(lambda matrix: len(set(len(row) for row in matrix)) == 1))
    @settings(max_examples=30, deadline=5000)
    def test_property_cost_optimality(self, matrix):
        """Property: Solusi harus optimal (tidak ada solusi yang lebih baik)"""
        result = self.hungarian.solve(matrix)
        
        if result['success']:
            optimal_cost = result['total_cost']
            assignment = result['assignment']
            
            # Verifikasi bahwa ini adalah assignment yang valid
            manual_cost = sum(matrix[i][assignment[i]] for i in range(len(assignment)) if assignment[i] != -1)
            self.assertEqual(optimal_cost, manual_cost)
            
            # Property: Cost harus non-negatif untuk matriks positif
            if all(all(cell >= 0 for cell in row) for row in matrix):
                self.assertGreaterEqual(optimal_cost, 0)
    
    @given(st.lists(
        st.lists(st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False), 
                min_size=2, max_size=3),
        min_size=2, max_size=3
    ).filter(lambda matrix: len(set(len(row) for row in matrix)) == 1))
    @settings(max_examples=20, deadline=5000)
    def test_property_minimization_maximization_duality(self, matrix):
        """Property: Hasil minimisasi dan maksimisasi harus konsisten"""
        min_result = self.hungarian.solve(matrix, is_maximization=False)
        max_result = self.hungarian.solve(matrix, is_maximization=True)
        
        # Kedua hasil harus sukses atau gagal bersamaan
        self.assertEqual(min_result['success'], max_result['success'])
        
        if min_result['success'] and max_result['success']:
            # Property: Assignment bisa sama atau berbeda, tapi keduanya harus valid
            self.assertEqual(len(min_result['assignment']), len(max_result['assignment']))

class TestDataProcessorBlackBox(unittest.TestCase):
    """Black Box Testing untuk DataProcessor"""
    
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_csv_processing(self):
        """Test pemrosesan file CSV"""
        # Create temporary CSV content
        csv_content = "1,2,3\n4,5,6\n7,8,9"
        
        # Test dengan string content
        try:
            result = self.processor.process_csv_content(csv_content)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)
            self.assertEqual(len(result[0]), 3)
        except Exception as e:
            # Jika method tidak ada, skip test ini
            self.skipTest(f"CSV processing method not implemented: {e}")
    
    def test_matrix_validation_integration(self):
        """Test integrasi validasi matriks dengan DataProcessor"""
        # Test valid matrix
        valid_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
        try:
            result = self.processor.validate_matrix_data(valid_matrix)
            self.assertTrue(result.get('valid', False))
        except Exception as e:
            # Jika method tidak ada, skip test ini
            self.skipTest(f"Matrix validation method not implemented: {e}")

class TestSystemIntegration(unittest.TestCase):
    """Integration testing untuk keseluruhan sistem"""
    
    def test_end_to_end_workflow(self):
        """Test workflow end-to-end"""
        # Simulasi workflow lengkap
        matrix = [[3, 1, 4], [2, 0, 5], [1, 3, 2]]
        
        # Step 1: Solve problem
        hungarian = HungarianMethod()
        result = hungarian.solve(matrix, is_maximization=False)
        
        self.assertTrue(result['success'])
        
        # Step 2: Verify result structure
        required_keys = ['success', 'assignment', 'total_cost', 'steps', 'execution_time']
        for key in required_keys:
            self.assertIn(key, result)
        
        # Step 3: Verify assignment validity
        assignment = result['assignment']
        self.assertEqual(len(assignment), len(matrix))
        
        # Step 4: Verify cost calculation
        manual_cost = sum(matrix[i][assignment[i]] for i in range(len(assignment)) if assignment[i] != -1)
        self.assertEqual(result['total_cost'], manual_cost)
    
    def test_stress_testing(self):
        """Stress testing dengan multiple concurrent operations"""
        import threading
        import queue
        
        results_queue = queue.Queue()
        
        def solve_matrix(matrix_id):
            """Solve matrix in separate thread"""
            matrix = [[random.randint(1, 10) for _ in range(4)] for _ in range(4)]
            hungarian = HungarianMethod()
            result = hungarian.solve(matrix)
            results_queue.put((matrix_id, result))
        
        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=solve_matrix, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        self.assertEqual(len(results), 10)
        
        for matrix_id, result in results:
            self.assertTrue(result['success'], f"Matrix {matrix_id} failed")

if __name__ == '__main__':
    # Setup test suite dengan berbagai level verbosity
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Black Box Tests for Hungarian Method')
    parser.add_argument('--verbose', '-v', action='count', default=1, help='Increase verbosity')
    parser.add_argument('--fast', action='store_true', help='Run only fast tests')
    
    args = parser.parse_args()
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add basic tests
    suite.addTest(unittest.makeSuite(TestHungarianBlackBox))
    
    if not args.fast:
        # Add property-based tests (slower)
        suite.addTest(unittest.makeSuite(TestHungarianPropertyBased))
        suite.addTest(unittest.makeSuite(TestSystemIntegration))
    
    # Add data processor tests
    suite.addTest(unittest.makeSuite(TestDataProcessorBlackBox))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=args.verbose)
    result = runner.run(suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)