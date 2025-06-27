import pandas as pd
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
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
        Membuat heatmap dari matriks biaya menggunakan matplotlib dan seaborn.
        """
        try:
            plt.figure(figsize=(10, 8))
            
            # Create heatmap
            ax = sns.heatmap(matrix, 
                           annot=True, 
                           fmt='.2f', 
                           cmap='YlOrRd',
                           xticklabels=col_labels if col_labels else [f'Task {i+1}' for i in range(matrix.shape[1])],
                           yticklabels=row_labels if row_labels else [f'Worker {i+1}' for i in range(matrix.shape[0])],
                           cbar_kws={'label': 'Cost'})
            
            # Highlight assignment if provided
            if assignment:
                for row, col in assignment:
                    ax.add_patch(plt.Rectangle((col, row), 1, 1, fill=False, edgecolor='blue', lw=3))
            
            plt.title(title, fontsize=16, fontweight='bold')
            plt.xlabel('Tasks', fontsize=12)
            plt.ylabel('Workers', fontsize=12)
            plt.tight_layout()
            
            # Save to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
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
        Membuat grafik analisis kompleksitas menggunakan matplotlib.
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Plot actual times
            plt.subplot(1, 2, 1)
            plt.plot(sizes, times, 'bo-', label='Actual Time', linewidth=2, markersize=8)
            plt.xlabel('Matrix Size (n)', fontsize=12)
            plt.ylabel('Execution Time (seconds)', fontsize=12)
            plt.title('Hungarian Algorithm\nExecution Time', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Plot theoretical O(n³) comparison
            plt.subplot(1, 2, 2)
            if len(times) > 0 and len(sizes) > 0:
                # Normalize theoretical curve to match first data point
                theoretical = [(size/sizes[0])**3 * times[0] for size in sizes]
                plt.plot(sizes, times, 'bo-', label='Actual Time', linewidth=2, markersize=8)
                plt.plot(sizes, theoretical, 'r--', label='O(n³) Theoretical', linewidth=2)
            
            plt.xlabel('Matrix Size (n)', fontsize=12)
            plt.ylabel('Execution Time (seconds)', fontsize=12)
            plt.title('Complexity Comparison\nActual vs Theoretical', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            plt.tight_layout()
            
            # Save to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            print(f"Error creating complexity chart: {e}")
            return None
        
    @staticmethod
    def create_interactive_heatmap(matrix: np.ndarray, 
                                 assignment: List[tuple] = None,
                                 title: str = "Interactive Cost Matrix") -> str:
        """
        Membuat heatmap interaktif menggunakan Plotly.
        """
        try:
            # Create hover text
            hover_text = []
            for i in range(matrix.shape[0]):
                hover_row = []
                for j in range(matrix.shape[1]):
                    hover_row.append(f'Worker {i+1}<br>Task {j+1}<br>Cost: {matrix[i][j]:.2f}')
                hover_text.append(hover_row)
            
            # Create the heatmap
            fig = go.Figure(data=go.Heatmap(
                z=matrix,
                text=matrix,
                texttemplate="%{text:.2f}",
                textfont={"size": 12},
                hovertemplate='%{customdata}<extra></extra>',
                customdata=hover_text,
                colorscale='Viridis',
                showscale=True
            ))
            
            # Add assignment highlights
            if assignment:
                for row, col in assignment:
                    fig.add_shape(
                        type="rect",
                        x0=col-0.5, y0=row-0.5,
                        x1=col+0.5, y1=row+0.5,
                        line=dict(color="red", width=3),
                        fillcolor="rgba(255,0,0,0.1)"
                    )
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="Tasks",
                yaxis_title="Workers",
                xaxis=dict(tickmode='array', tickvals=list(range(matrix.shape[1])), 
                          ticktext=[f'Task {i+1}' for i in range(matrix.shape[1])]),
                yaxis=dict(tickmode='array', tickvals=list(range(matrix.shape[0])), 
                          ticktext=[f'Worker {i+1}' for i in range(matrix.shape[0])]),
                width=600,
                height=500
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="heatmap")
            
        except Exception as e:
            print(f"Error creating interactive heatmap: {e}")
            return None

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