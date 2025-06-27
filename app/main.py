from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, session
import os
import json
import time
import traceback
import sys
from datetime import datetime
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import flask
from .hungarian import HungarianMethod
from .utils import DataProcessor, Visualizer, FileManager
import tempfile
import uuid
from collections import defaultdict
import logging

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging for production
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Hungarian Calculator startup')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# No database extensions needed

# Add custom Jinja2 filter
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object"""
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except (ValueError, TypeError, json.JSONDecodeError):
        return []

# Ensure directories exist (for local development)
try:
    FileManager.ensure_directory(app.config['UPLOAD_FOLDER'])
    FileManager.ensure_directory('reports')
    FileManager.ensure_directory('static/images')
except:
    # Skip directory creation in serverless environment
    pass

# No database models needed - removed all database functionality

# Helper functions
def log_activity(action, details=None, user_id=None, username=None):
    """Log user activity - simplified without database"""
    print(f"Activity: {action} - {details or 'No details'} - User: {username or 'Anonymous'}")

def get_system_info():
    """Get system information - simplified for serverless"""
    try:
        return {
            'python_version': f"{sys.version.split()[0]}",
            'flask_version': flask.__version__,
            'database_type': 'None (Serverless)',
            'uptime': 'Serverless Function',
            'memory_usage': 'Managed by Vercel',
            'db_size': 'N/A',
            'last_backup': None
        }
    except Exception as e:
        return {
            'python_version': 'Unknown',
            'flask_version': 'Unknown',
            'database_type': 'None',
            'uptime': 'Unknown',
            'memory_usage': 'Unknown',
            'db_size': 'Unknown',
            'last_backup': None
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Authentication routes removed - no database functionality

@app.route('/dashboard')
def dashboard():
    """Dashboard page - simplified without database"""
    return render_template('dashboard.html', 
                         total_calculations=0,
                         recent_calculations=[])

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/api/solve', methods=['POST'])
def solve_hungarian():
    try:
        data = request.get_json()
        matrix = data.get('matrix')
        maximize = data.get('maximize', False)
        
        if not matrix:
            return jsonify({'error': 'Matrix tidak boleh kosong'}), 400
        
        # Validasi matrix
        processor = DataProcessor()
        validation = processor.validate_matrix(matrix)
        
        if not validation['is_valid']:
            return jsonify({'error': validation['errors']}), 400
        
        # Solve Hungarian Method
        start_time = time.time()
        hungarian = HungarianMethod()
        result = hungarian.solve(matrix, maximize)
        execution_time = time.time() - start_time
        
        # Generate visualizations
        visualizer = Visualizer()
        original_heatmap = visualizer.create_heatmap(
            np.array(matrix), 
            "Original Cost Matrix",
            assignment=result['assignment']
        )
        
        # Log calculation (no database storage)
        log_activity('calculation_performed', f'Matrix size: {len(matrix)}x{len(matrix[0])}, Total cost: {result["total_cost"]}')
        calculation_id = 1  # Dummy ID for response
        
        # Format assignment untuk frontend
        formatted_assignment = []
        for row, col in result['assignment']:
            cost = matrix[row][col]
            formatted_assignment.append({
                'worker': row,
                'task': col,
                'cost': float(cost)
            })
        
        return jsonify({
            'success': True,
            'assignment': formatted_assignment,
            'total_cost': float(result['total_cost']),
            'execution_time': float(execution_time),  # Konversi ke Python float
            'heatmap': original_heatmap,
            'validation': validation,
            'calculation_id': int(calculation_id),  # Use the dummy ID instead of calculation.id
            'final_matrix': matrix,  # Tambahkan matrix untuk heatmap
            'result': result  # Tetap sertakan result lengkap untuk keperluan lain
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Read file based on extension
            processor = DataProcessor()
            if filename.endswith('.csv'):
                matrix = processor.read_csv_file(file_path)
            elif filename.endswith(('.xlsx', '.xls')):
                matrix = processor.read_excel_file(file_path)
            else:
                return jsonify({'error': 'Format file tidak didukung. Gunakan CSV atau Excel.'}), 400
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify({
                'success': True,
                'matrix': matrix,
                'filename': filename
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate HTML report from calculation data (replacing PDF to reduce bundle size)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Ensure reports directory exists
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = int(time.time())
        filename = f'hungarian_report_{timestamp}.pdf'
        output_path = os.path.join(reports_dir, filename)
        
        # Create PDF report using reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from datetime import datetime
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        title = Paragraph("LAPORAN HUNGARIAN METHOD", title_style)
        story.append(title)
        
        # Date info
        date_info = Paragraph(f"<b>Tanggal:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
        story.append(date_info)
        story.append(Spacer(1, 12))
        
        # Total cost if available
        if 'total_cost' in data:
            cost_info = Paragraph(f"<b>Total Cost:</b> {data['total_cost']}", styles['Normal'])
            story.append(cost_info)
            story.append(Spacer(1, 12))
        
        # Assignment results if available
        if 'assignment' in data and data['assignment']:
            story.append(Paragraph("HASIL PENUGASAN", styles['Heading2']))
            
            assignment_data = [['Worker', 'Task']]
            for row, col in data['assignment']:
                assignment_data.append([f'Worker {row+1}', f'Task {col+1}'])
            
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
        
        # Build PDF
        doc.build(story)
        
        # Return file for download
        return send_file(output_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"Generate report error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_steps', methods=['POST'])
def get_steps():
    try:
        data = request.get_json()
        matrix = data.get('matrix')
        is_maximization = data.get('is_maximization', False)
        
        if not matrix:
            return jsonify({'error': 'Matrix data is required'}), 400
        
        # Solve Hungarian algorithm to get steps
        hungarian = HungarianMethod()
        result = hungarian.solve(matrix, is_maximization)
        
        return jsonify({
            'success': True,
            'steps': result['steps']
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/api/step_visualization/<int:calculation_id>/<int:step_index>')
def step_visualization(calculation_id, step_index):
    """Get step-by-step visualization - simplified without database"""
    return jsonify({'error': 'Step visualization not available without database'}), 404

@app.route('/history')
def history():
    """Calculation history page - simplified without database"""
    return render_template('history.html', calculations=[])

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard - simplified without database"""
    return render_template('admin/dashboard.html',
                         total_calculations=0,
                         avg_response_time=0.0,
                         daily_usage=[])

@app.route('/api/complexity_analysis')
def complexity_analysis():
    try:
        # Run complexity analysis
        sizes = [3, 4, 5, 6, 7, 8, 10]
        times = []
        
        for size in sizes:
            # Generate random matrix
            matrix = np.random.randint(1, 100, (size, size)).tolist()
            
            # Measure execution time
            start_time = time.time()
            hungarian = HungarianMethod()
            hungarian.solve(matrix)
            execution_time = time.time() - start_time
            times.append(execution_time)
        
        # Generate complexity chart
        visualizer = Visualizer()
        complexity_chart = visualizer.create_complexity_chart(sizes, times)
        
        return jsonify({
            'success': True,
            'chart': complexity_chart,
            'data': {
                'sizes': sizes,
                'times': times,
                'avg_time': sum(times) / len(times),
                'max_size': max(sizes)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin API endpoints
@app.route('/api/admin/add_user', methods=['POST'])
def api_add_user():
    """Admin function to add user - disabled without database"""
    return jsonify({'error': 'User management not available without database'}), 404

@app.route('/api/admin/delete_user/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    """Admin function to delete user - disabled without database"""
    return jsonify({'error': 'User management not available without database'}), 404

@app.route('/api/user/<int:user_id>')
def api_get_user(user_id):
    """Get user information - disabled without database"""
    return jsonify({'error': 'User information not available without database'}), 404

@app.route('/api/activity_logs')
def get_activity_logs():
    """Get activity logs - disabled without database"""
    return jsonify({'error': 'Activity logs not available without database'}), 404

@app.route('/api/clear_logs', methods=['DELETE'])
def clear_activity_logs():
    """Clear all activity logs - disabled without database"""
    return jsonify({'error': 'Activity logs not available without database'}), 404

@app.route('/api/backup_database', methods=['POST'])
def backup_database():
    """Create database backup - disabled without database"""
    return jsonify({'error': 'Database backup not available without database'}), 404

@app.route('/api/optimize_database', methods=['POST'])
def optimize_database():
    """Optimize database - disabled without database"""
    return jsonify({'error': 'Database optimization not available without database'}), 404

@app.route('/api/system_stats')
def get_system_stats():
    """Get system statistics - simplified without database"""
    return jsonify({
        'success': True,
        'stats': {
            'total_users': 0,
            'total_calculations': 0,
            'system_uptime': get_system_info()['uptime'],
            'database_size': 'N/A'
        }
    })

@app.route('/api/admin/export_system_report')
def export_system_report():
    """Export system report - simplified without database"""
    return jsonify({'error': 'System report export not available without database'}), 404

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # Log the error for debugging
    app.logger.error(f'Server Error: {error}')
    app.logger.error(traceback.format_exc())
    try:
        return render_template('500.html'), 500
    except:
        # Fallback if template rendering fails
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Terjadi kesalahan pada server. Silakan coba lagi.'
        }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    app.logger.error(f'Unhandled Exception: {e}')
    app.logger.error(traceback.format_exc())
    
    # Return JSON error for API requests
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Terjadi kesalahan pada server. Silakan coba lagi.'
        }), 500
    
    # Return HTML error for web requests
    try:
        return render_template('500.html'), 500
    except:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Terjadi kesalahan pada server. Silakan coba lagi.'
        }), 500

if __name__ == '__main__':
    # Database functionality has been removed from the application
    print('Starting Hungarian Method Calculator without database functionality')
    app.run(debug=True, host='0.0.0.0', port=5001)