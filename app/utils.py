import pandas as pd
import os
import pandas as pd
import numpy as np
# PDF generation removed to reduce bundle size
# Alternative: Use HTML to PDF conversion or client-side PDF generation
import io
import base64
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

class DataProcessor:
    """
    Kelas untuk memproses data input dan output.
    """
    
    @staticmethod
    def read_csv_file(file_path: str) -> List[List[float]]:
        """
        Membaca file CSV dan mengkonversi ke matriks.
        """
        try:
            df = pd.read_csv(file_path, header=None)
            return df.values.tolist()
        except Exception as e:
            raise ValueError(f"Error membaca file CSV: {str(e)}")
            
    @staticmethod
    def read_excel_file(file_path: str, sheet_name: str = None) -> List[List[float]]:
        """
        Membaca file Excel dan mengkonversi ke matriks.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            return df.values.tolist()
        except Exception as e:
            raise ValueError(f"Error membaca file Excel: {str(e)}")
            
    @staticmethod
    def validate_matrix(matrix: List[List[float]]) -> Dict[str, Any]:
        """
        Validasi matriks input.
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        if not matrix or not matrix[0]:
            result['is_valid'] = False
            result['errors'].append("Matriks kosong")
            return result
            
        rows = len(matrix)
        cols = len(matrix[0])
        
        # Cek konsistensi kolom
        for i, row in enumerate(matrix):
            if len(row) != cols:
                result['is_valid'] = False
                result['errors'].append(f"Baris {i+1} memiliki {len(row)} kolom, seharusnya {cols}")
                
        # Cek tipe data
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                try:
                    float(val)
                except (ValueError, TypeError):
                    result['is_valid'] = False
                    result['errors'].append(f"Nilai di baris {i+1}, kolom {j+1} bukan angka: {val}")
                    
        # Info tambahan
        result['info'] = {
            'rows': rows,
            'cols': cols,
            'is_square': rows == cols,
            'is_balanced': rows == cols
        }
        
        # Warning untuk matriks tidak seimbang
        if rows != cols:
            result['warnings'].append(f"Matriks tidak seimbang ({rows}x{cols}). Akan ditambahkan dummy rows/columns.")
            
        return result
        
    @staticmethod
    def matrix_to_dataframe(matrix: List[List[float]], 
                          row_labels: List[str] = None, 
                          col_labels: List[str] = None) -> pd.DataFrame:
        """
        Konversi matriks ke DataFrame dengan label.
        """
        df = pd.DataFrame(matrix)
        
        if row_labels:
            df.index = row_labels
        else:
            df.index = [f"Worker {i+1}" for i in range(len(matrix))]
            
        if col_labels:
            df.columns = col_labels
        else:
            df.columns = [f"Task {i+1}" for i in range(len(matrix[0]))]
            
        return df

class Visualizer:
    """
    Kelas untuk membuat visualisasi.
    """
    
    @staticmethod
    def create_heatmap(matrix: np.ndarray, 
                      title: str = "Cost Matrix",
                      row_labels: List[str] = None,
                      col_labels: List[str] = None,
                      assignment: List[tuple] = None) -> str:
        """
        Membuat representasi sederhana dari matriks biaya (tanpa visualisasi grafis).
        """
        try:
            # Return simple HTML table representation instead of image
            html = f"<h3>{title}</h3><table border='1' style='border-collapse: collapse;'>"
            
            # Header row
            html += "<tr><th></th>"
            for i in range(matrix.shape[1]):
                label = col_labels[i] if col_labels else f"T{i+1}"
                html += f"<th style='padding: 5px; background-color: #f0f0f0;'>{label}</th>"
            html += "</tr>"
            
            # Data rows
            for i, row in enumerate(matrix):
                row_label = row_labels[i] if row_labels else f"W{i+1}"
                html += f"<tr><th style='padding: 5px; background-color: #f0f0f0;'>{row_label}</th>"
                for j, val in enumerate(row):
                    style = "background-color: #ffcccc;" if assignment and (i, j) in assignment else ""
                    html += f"<td style='padding: 5px; text-align: center; {style}'>{val:.2f}</td>"
                html += "</tr>"
            html += "</table>"
            return html
            
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            return None
        
    @staticmethod
    def create_step_visualization(steps: List[Dict], step_index: int) -> str:
        """
        Membuat visualisasi untuk langkah tertentu.
        """
        if step_index >= len(steps):
            return None
            
        step = steps[step_index]
        matrix = step['matrix']
        title = f"Step {step_index + 1}: {step['description']}"
        
        return Visualizer.create_heatmap(matrix, title)
        
    @staticmethod
    def create_complexity_chart(sizes: List[int], times: List[float]) -> str:
        """
        Membuat tabel analisis kompleksitas sederhana.
        """
        try:
            html = "<h3>Hungarian Algorithm Complexity Analysis</h3>"
            html += "<table border='1' style='border-collapse: collapse; margin: 10px 0;'>"
            html += "<tr><th style='padding: 8px; background-color: #f0f0f0;'>Matrix Size (n)</th>"
            html += "<th style='padding: 8px; background-color: #f0f0f0;'>Execution Time (seconds)</th>"
            html += "<th style='padding: 8px; background-color: #f0f0f0;'>Time per Element (ms)</th></tr>"
            
            for size, time in zip(sizes, times):
                time_per_element = (time * 1000) / (size * size) if size > 0 else 0
                html += f"<tr>"
                html += f"<td style='padding: 8px; text-align: center;'>{size}</td>"
                html += f"<td style='padding: 8px; text-align: center;'>{time:.4f}</td>"
                html += f"<td style='padding: 8px; text-align: center;'>{time_per_element:.2f}</td>"
                html += f"</tr>"
            
            html += "</table>"
            html += "<p><em>Note: Hungarian Algorithm has O(n³) time complexity</em></p>"
            return html
            
        except Exception as e:
            print(f"Error creating complexity chart: {e}")
            return None
        
    @staticmethod
    def create_interactive_heatmap(matrix: np.ndarray, 
                                 assignment: List[tuple] = None,
                                 title: str = "Interactive Cost Matrix") -> str:
        """
        Membuat heatmap sederhana dengan HTML/CSS.
        """
        try:
            html = f"<h3>{title}</h3>"
            html += "<table border='1' style='border-collapse: collapse; margin: 10px 0;'>"
            
            # Header row
            html += "<tr><th style='padding: 8px; background-color: #f0f0f0;'></th>"
            for j in range(matrix.shape[1]):
                html += f"<th style='padding: 8px; background-color: #f0f0f0;'>T{j+1}</th>"
            html += "</tr>"
            
            # Data rows
            for i, row in enumerate(matrix):
                html += f"<tr><th style='padding: 8px; background-color: #f0f0f0;'>W{i+1}</th>"
                for j, val in enumerate(row):
                    # Color coding based on value (simple heatmap effect)
                    max_val = np.max(matrix)
                    min_val = np.min(matrix)
                    normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
                    red_intensity = int(255 * normalized)
                    bg_color = f"rgb({red_intensity}, {255-red_intensity//2}, {255-red_intensity//2})"
                    
                    # Highlight assignment
                    if assignment and (i, j) in assignment:
                        bg_color = "#4CAF50"  # Green for assignment
                        val_text = f"★ {val:.2f}"
                    else:
                        val_text = f"{val:.2f}"
                    
                    html += f"<td style='padding: 8px; text-align: center; background-color: {bg_color};'>{val_text}</td>"
                html += "</tr>"
            
            html += "</table>"
            return html
            
        except Exception as e:
            print(f"Error creating interactive heatmap: {e}")
            return None

class ReportGenerator:
    """
    Kelas untuk generate laporan HTML (menggantikan PDF untuk mengurangi ukuran bundle).
    """
    
    def __init__(self):
        pass  # No complex initialization needed for HTML generation
        
    def generate_report(self, result: Dict[str, Any], 
                       output_path: str,
                       complexity_data: Dict = None) -> str:
        """
        Generate laporan HTML (menggantikan PDF untuk mengurangi ukuran bundle).
        """
        from datetime import datetime
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Laporan Hungarian Method Assignment</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; color: #333; }}
                h2 {{ color: #666; border-bottom: 2px solid #ddd; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
                .info-table {{ max-width: 500px; }}
            </style>
        </head>
        <body>
            <h1>LAPORAN HUNGARIAN METHOD ASSIGNMENT</h1>
            
            <h2>Informasi Umum</h2>
            <table class="info-table">
                <tr><th>Tanggal</th><td>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td></tr>
                <tr><th>Tipe Problem</th><td>{'Maksimisasi' if result['is_maximization'] else 'Minimisasi'}</td></tr>
                <tr><th>Ukuran Matrix</th><td>{len(result['original_matrix'])}x{len(result['original_matrix'][0])}</td></tr>
                <tr><th>Total Cost/Benefit</th><td>{result['total_cost']:.2f}</td></tr>
            </table>
            
            <h2>Matriks Input Asli</h2>
            <table>
                <tr><th></th>{''.join([f'<th>Task {i+1}</th>' for i in range(len(result['original_matrix'][0]))])}</tr>
                {''.join([f'<tr><th>Worker {i+1}</th>{"".join([f"<td>{val:.2f}</td>" for val in row])}</tr>' for i, row in enumerate(result['original_matrix'])])}
            </table>
            
            <h2>Hasil Penugasan Optimal</h2>
            <table>
                <tr><th>Worker</th><th>Task</th><th>Cost</th></tr>
                {''.join([f'<tr><td>Worker {row+1}</td><td>Task {col+1}</td><td>{result["original_matrix"][row][col]:.2f}</td></tr>' for row, col in result['assignment']])}
            </table>
            
            {f'''
            <h2>Analisis Kompleksitas</h2>
            <table class="info-table">
                <tr><th>Kompleksitas Teoritis</th><td>O(n³)</td></tr>
                <tr><th>Waktu Eksekusi Rata-rata</th><td>{complexity_data.get('avg_time', 0):.4f} detik</td></tr>
                <tr><th>Ukuran Matrix Terbesar Diuji</th><td>{complexity_data.get('max_size', 0)}x{complexity_data.get('max_size', 0)}</td></tr>
                <tr><th>Cyclomatic Complexity</th><td>{complexity_data.get('cyclomatic', 'N/A')}</td></tr>
            </table>
            ''' if complexity_data else ''}
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
        
class FileManager:
    """
    Kelas untuk manajemen file.
    """
    
    @staticmethod
    def ensure_directory(path: str):
        """
        Pastikan direktori ada.
        """
        os.makedirs(path, exist_ok=True)
        
    @staticmethod
    def save_matrix_to_csv(matrix: List[List[float]], file_path: str):
        """
        Simpan matriks ke file CSV.
        """
        df = pd.DataFrame(matrix)
        df.to_csv(file_path, index=False, header=False)
        
    @staticmethod
    def save_results_to_json(result: Dict[str, Any], file_path: str):
        """
        Simpan hasil ke file JSON.
        """
        import json
        
        # Convert numpy arrays to lists for JSON serialization
        json_result = {}
        for key, value in result.items():
            if isinstance(value, np.ndarray):
                json_result[key] = value.tolist()
            elif key == 'steps':
                json_result[key] = []
                for step in value:
                    step_copy = step.copy()
                    step_copy['matrix'] = step_copy['matrix'].tolist()
                    json_result[key].append(step_copy)
            else:
                json_result[key] = value
                
        with open(file_path, 'w') as f:
            json.dump(json_result, f, indent=2)