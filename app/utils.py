import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
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
        Membuat heatmap dari matriks.
        """
        plt.figure(figsize=(10, 8))
        
        # Buat mask untuk assignment jika ada
        mask = None
        if assignment:
            mask = np.zeros_like(matrix, dtype=bool)
            for row, col in assignment:
                if row < matrix.shape[0] and col < matrix.shape[1]:
                    mask[row, col] = True
                    
        # Buat heatmap
        ax = sns.heatmap(matrix, 
                        annot=True, 
                        fmt='.2f', 
                        cmap='YlOrRd',
                        xticklabels=col_labels or [f"T{i+1}" for i in range(matrix.shape[1])],
                        yticklabels=row_labels or [f"W{i+1}" for i in range(matrix.shape[0])],
                        cbar_kws={'label': 'Cost'})
        
        # Highlight assignment
        if assignment:
            for row, col in assignment:
                if row < matrix.shape[0] and col < matrix.shape[1]:
                    ax.add_patch(plt.Rectangle((col, row), 1, 1, 
                                             fill=False, edgecolor='blue', lw=3))
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Tasks', fontsize=12)
        plt.ylabel('Workers', fontsize=12)
        plt.tight_layout()
        
        # Simpan ke base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
        
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
        Membuat grafik kompleksitas waktu.
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8, label='Actual Time')
        
        # Tambahkan trendline O(n³)
        if len(sizes) > 1:
            # Fit polynomial degree 3
            z = np.polyfit(sizes, times, 3)
            p = np.poly1d(z)
            x_smooth = np.linspace(min(sizes), max(sizes), 100)
            plt.plot(x_smooth, p(x_smooth), 'r--', alpha=0.7, label='O(n³) Trend')
        
        plt.xlabel('Matrix Size (n)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.title('Hungarian Algorithm Complexity Analysis', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Simpan ke base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
        
    @staticmethod
    def create_interactive_heatmap(matrix: np.ndarray, 
                                 assignment: List[tuple] = None,
                                 title: str = "Interactive Cost Matrix") -> str:
        """
        Membuat heatmap interaktif dengan Plotly.
        """
        # Buat annotations untuk assignment
        annotations = []
        if assignment:
            for row, col in assignment:
                if row < matrix.shape[0] and col < matrix.shape[1]:
                    annotations.append(
                        dict(
                            x=col, y=row,
                            text="★",
                            showarrow=False,
                            font=dict(color="blue", size=20)
                        )
                    )
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            colorscale='YlOrRd',
            showscale=True,
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Tasks",
            yaxis_title="Workers",
            annotations=annotations
        )
        
        return fig.to_html(include_plotlyjs='cdn')

class ReportGenerator:
    """
    Kelas untuk generate laporan PDF.
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        
    def generate_report(self, result: Dict[str, Any], 
                       output_path: str,
                       complexity_data: Dict = None) -> str:
        """
        Generate laporan PDF lengkap.
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("LAPORAN HUNGARIAN METHOD ASSIGNMENT", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Info umum
        info_data = [
            ['Tanggal', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
            ['Tipe Problem', 'Maksimisasi' if result['is_maximization'] else 'Minimisasi'],
            ['Ukuran Matrix', f"{len(result['original_matrix'])}x{len(result['original_matrix'][0])}"],
            ['Total Cost/Benefit', f"{result['total_cost']:.2f}"]
        ]
        
        info_table = Table(info_data)
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Original Matrix
        story.append(Paragraph("MATRIKS INPUT ASLI", self.styles['Heading2']))
        original_matrix = result['original_matrix']
        matrix_data = [[''] + [f'Task {i+1}' for i in range(len(original_matrix[0]))]]
        for i, row in enumerate(original_matrix):
            matrix_data.append([f'Worker {i+1}'] + [f'{val:.2f}' for val in row])
            
        matrix_table = Table(matrix_data)
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(matrix_table)
        story.append(Spacer(1, 20))
        
        # Assignment Results
        story.append(Paragraph("HASIL PENUGASAN OPTIMAL", self.styles['Heading2']))
        assignment_data = [['Worker', 'Task', 'Cost']]
        for i, (row, col) in enumerate(result['assignment']):
            cost = original_matrix[row][col]
            assignment_data.append([f'Worker {row+1}', f'Task {col+1}', f'{cost:.2f}'])
            
        assignment_table = Table(assignment_data)
        assignment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(assignment_table)
        story.append(Spacer(1, 20))
        
        # Complexity Analysis jika ada
        if complexity_data:
            story.append(Paragraph("ANALISIS KOMPLEKSITAS", self.styles['Heading2']))
            complexity_info = [
                ['Kompleksitas Teoritis', 'O(n³)'],
                ['Waktu Eksekusi Rata-rata', f"{complexity_data.get('avg_time', 0):.4f} detik"],
                ['Ukuran Matrix Terbesar Diuji', f"{complexity_data.get('max_size', 0)}x{complexity_data.get('max_size', 0)}"],
                ['Cyclomatic Complexity', f"{complexity_data.get('cyclomatic', 'N/A')}"]
            ]
            
            complexity_table = Table(complexity_info)
            complexity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(complexity_table)
            
        # Build PDF
        doc.build(story)
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