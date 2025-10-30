"""
Hadoop Web Interface - Flask Application
Author: devnolife
"""

from flask import Flask, render_template, request, jsonify, send_file
from src.mysql_handler import MySQLHandler
from src.hdfs_operations import HDFSOperations
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hadoop-web-interface-2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'

# Create folders if not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Global MySQL handler
mysql_handler = None


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/mysql/connect', methods=['POST'])
def mysql_connect():
    """Connect to MySQL database"""
    global mysql_handler
    
    try:
        data = request.json
        mysql_handler = MySQLHandler(
            host=data.get('host', 'localhost'),
            port=data.get('port', 3306),
            user=data.get('user', 'root'),
            password=data.get('password', ''),
            database=data.get('database')
        )
        
        if mysql_handler.connect():
            return jsonify({
                'success': True,
                'message': 'Connected to MySQL successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to MySQL'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/databases', methods=['GET'])
def get_databases():
    """Get list of databases"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        databases = mysql_handler.get_databases()
        return jsonify({
            'success': True,
            'databases': databases
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/tables', methods=['GET'])
def get_tables():
    """Get list of tables in current database"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        tables = mysql_handler.get_tables()
        return jsonify({
            'success': True,
            'tables': tables
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/table/<table_name>/info', methods=['GET'])
def get_table_info(table_name):
    """Get table information"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        info = mysql_handler.get_table_info(table_name)
        return jsonify({
            'success': True,
            'info': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/table/<table_name>/preview', methods=['GET'])
def get_table_preview(table_name):
    """Get table data preview"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        limit = request.args.get('limit', 10, type=int)
        data = mysql_handler.get_table_preview(table_name, limit)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/table/<table_name>/export', methods=['POST'])
def export_table():
    """Export table to CSV"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        table_name = request.view_args['table_name']
        data = request.json
        limit = data.get('limit')
        
        output_file = os.path.join(
            app.config['EXPORT_FOLDER'],
            f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        csv_file = mysql_handler.export_table_to_csv(
            table_name,
            output_file,
            limit
        )
        
        if csv_file:
            return jsonify({
                'success': True,
                'message': 'Table exported successfully',
                'file': csv_file
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to export table'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mysql/query', methods=['POST'])
def execute_query():
    """Execute custom SQL query"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        data = request.json
        query = data.get('query')
        
        results = mysql_handler.execute_query(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    global mysql_handler
    
    stats = {
        'mysql_connected': mysql_handler is not None and mysql_handler.connection and mysql_handler.connection.is_connected(),
        'timestamp': datetime.now().isoformat()
    }
    
    if stats['mysql_connected']:
        stats['database'] = mysql_handler.database
        stats['tables_count'] = len(mysql_handler.get_tables())
    
    return jsonify(stats)


@app.route('/download/<path:filename>')
def download_file(filename):
    """Download exported file"""
    file_path = os.path.join(app.config['EXPORT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({
            'success': False,
            'message': 'File not found'
        }), 404


@app.route('/api/exports/list', methods=['GET'])
def list_exports():
    """List exported CSV files"""
    try:
        files = [f for f in os.listdir(app.config['EXPORT_FOLDER']) if f.endswith('.csv')]
        return jsonify({
            'success': True,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/hdfs/upload', methods=['POST'])
def hdfs_upload():
    """Upload file to HDFS"""
    try:
        data = request.json
        csv_file = data.get('csv_file')
        hdfs_path = data.get('hdfs_path')
        
        if not csv_file or not hdfs_path:
            return jsonify({
                'success': False,
                'message': 'Missing csv_file or hdfs_path'
            }), 400
        
        # Full path to CSV file
        local_path = os.path.join(app.config['EXPORT_FOLDER'], csv_file)
        
        if not os.path.exists(local_path):
            return jsonify({
                'success': False,
                'message': f'File not found: {csv_file}'
            }), 404
        
        # Upload to HDFS
        hdfs_ops = HDFSOperations()
        if hdfs_ops.put_file(local_path, hdfs_path):
            return jsonify({
                'success': True,
                'message': f'File uploaded to HDFS successfully',
                'details': f'Local: {csv_file} → HDFS: {hdfs_path}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to upload to HDFS'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/hdfs/download', methods=['POST'])
def hdfs_download():
    """Download file from HDFS"""
    try:
        data = request.json
        hdfs_path = data.get('hdfs_path')
        local_file = data.get('local_file')
        
        if not hdfs_path or not local_file:
            return jsonify({
                'success': False,
                'message': 'Missing hdfs_path or local_file'
            }), 400
        
        # Download from HDFS
        local_path = os.path.join(app.config['EXPORT_FOLDER'], local_file)
        
        hdfs_ops = HDFSOperations()
        if hdfs_ops.get_file(hdfs_path, local_path):
            return jsonify({
                'success': True,
                'message': f'File downloaded from HDFS successfully',
                'details': f'HDFS: {hdfs_path} → Local: {local_file}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to download from HDFS'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/hdfs/export-table', methods=['POST'])
def hdfs_export_table():
    """Export MySQL table directly to HDFS"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        data = request.json
        table_name = data.get('table_name')
        hdfs_path = data.get('hdfs_path')
        
        if not table_name:
            return jsonify({
                'success': False,
                'message': 'Missing table_name'
            }), 400
        
        # Export to CSV first
        csv_file = os.path.join(app.config['EXPORT_FOLDER'], f'{table_name}.csv')
        row_count = mysql_handler.export_table_to_csv(table_name, csv_file)
        
        if row_count == 0:
            return jsonify({
                'success': False,
                'message': f'Table {table_name} is empty or export failed'
            }), 400
        
        # Check if HDFS is available
        if not hdfs_path:
            hdfs_path = f'/user/data/mysql/{table_name}.csv'
        
        hdfs_ops = HDFSOperations()
        
        # Try to upload to HDFS
        try:
            upload_success = hdfs_ops.put_file(csv_file, hdfs_path)
            
            if upload_success:
                return jsonify({
                    'success': True,
                    'message': f'Table {table_name} exported to HDFS successfully',
                    'row_count': row_count,
                    'hdfs_path': hdfs_path,
                    'csv_file': f'{table_name}.csv'
                })
            else:
                # HDFS upload failed, but CSV is exported
                return jsonify({
                    'success': True,
                    'warning': True,
                    'message': f'CSV exported to exports/{table_name}.csv (HDFS not available)',
                    'row_count': row_count,
                    'csv_file': f'{table_name}.csv',
                    'note': 'HDFS tidak terinstall atau tidak berjalan. File CSV tersimpan di folder exports/.'
                })
        except Exception as hdfs_error:
            # HDFS not available, return success for CSV export
            return jsonify({
                'success': True,
                'warning': True,
                'message': f'CSV exported to exports/{table_name}.csv (HDFS not available)',
                'row_count': row_count,
                'csv_file': f'{table_name}.csv',
                'note': f'HDFS error: {str(hdfs_error)}. File CSV tersimpan di folder exports/.'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Export failed: {str(e)}'
        }), 500


@app.route('/api/hdfs/bulk-export', methods=['POST'])
def hdfs_bulk_export():
    """Export all MySQL tables to HDFS"""
    global mysql_handler
    
    if not mysql_handler:
        return jsonify({
            'success': False,
            'message': 'Not connected to MySQL'
        }), 400
    
    try:
        data = request.json
        base_path = data.get('base_path', '/user/data/mysql')
        
        tables = mysql_handler.get_tables()
        
        if not tables:
            return jsonify({
                'success': False,
                'message': 'No tables found'
            }), 400
        
        hdfs_ops = HDFSOperations()
        results = []
        successful = 0
        failed = 0
        
        for table in tables:
            try:
                # Export to CSV
                csv_file = os.path.join(app.config['EXPORT_FOLDER'], f'{table}.csv')
                row_count = mysql_handler.export_table_to_csv(table, csv_file)
                
                if row_count == 0:
                    results.append({
                        'table': table,
                        'status': 'skipped',
                        'rows': 0,
                        'hdfs_path': None,
                        'csv_file': None
                    })
                    continue
                
                # Try upload to HDFS
                hdfs_path = f'{base_path}/{table}.csv'
                
                try:
                    upload_success = hdfs_ops.put_file(csv_file, hdfs_path)
                    
                    if upload_success:
                        results.append({
                            'table': table,
                            'status': 'success',
                            'rows': row_count,
                            'hdfs_path': hdfs_path,
                            'csv_file': f'{table}.csv'
                        })
                        successful += 1
                    else:
                        # HDFS failed, but CSV exported
                        results.append({
                            'table': table,
                            'status': 'csv_only',
                            'rows': row_count,
                            'hdfs_path': None,
                            'csv_file': f'{table}.csv'
                        })
                        successful += 1  # Still count as success since CSV is created
                except Exception as hdfs_error:
                    # HDFS not available, CSV still exported
                    results.append({
                        'table': table,
                        'status': 'csv_only',
                        'rows': row_count,
                        'hdfs_path': None,
                        'csv_file': f'{table}.csv',
                        'note': 'HDFS not available'
                    })
                    successful += 1  # Count as success since CSV is created
                    
            except Exception as e:
                results.append({
                    'table': table,
                    'status': 'error',
                    'rows': None,
                    'hdfs_path': None,
                    'csv_file': None,
                    'error': str(e)
                })
                failed += 1
        
        return jsonify({
            'success': True,
            'message': f'Bulk export completed: {successful} successful, {failed} failed',
            'total': len(tables),
            'successful': successful,
            'failed': failed,
            'details': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/hdfs/list', methods=['POST'])
def hdfs_list():
    """List files in HDFS directory"""
    try:
        data = request.json
        hdfs_path = data.get('hdfs_path', '/')
        
        hdfs_ops = HDFSOperations()
        files = hdfs_ops.list_directory(hdfs_path)
        
        if files:
            return jsonify({
                'success': True,
                'files': files,
                'count': len(files)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to list HDFS directory or directory is empty'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/hdfs/command', methods=['POST'])
def hdfs_command():
    """Execute HDFS command (Interactive Learning Mode)"""
    try:
        data = request.json
        command = data.get('command')
        path = data.get('path')
        
        if not command or not path:
            return jsonify({
                'success': False,
                'message': 'Missing command or path'
            }), 400
        
        hdfs_ops = HDFSOperations()
        
        if command == 'mkdir':
            # Create directory
            cmd = f'hdfs dfs -mkdir -p {path}'
            success = hdfs_ops.create_directory(path)
            
            return jsonify({
                'success': success,
                'command': cmd,
                'message': f'Directory {path} berhasil dibuat!' if success else 'Gagal membuat directory',
                'output': None
            })
            
        elif command == 'list':
            # List directory
            cmd = f'hdfs dfs -ls {path}'
            files = hdfs_ops.list_directory(path)
            
            if files:
                return jsonify({
                    'success': True,
                    'command': cmd,
                    'files': files,
                    'output': f'Found {len(files)} items',
                    'message': f'Directory {path} berhasil dibaca!'
                })
            else:
                return jsonify({
                    'success': False,
                    'command': cmd,
                    'message': 'Directory kosong atau tidak ditemukan'
                }), 404
                
        elif command == 'cat':
            # View file content (first 10 lines)
            cmd = f'hdfs dfs -cat {path} | head -10'
            
            # Try to read file using mock or real HDFS
            try:
                # This is a mock implementation
                output = f"Isi file: {path}\n(Gunakan HDFS real untuk melihat isi file lengkap)"
                
                return jsonify({
                    'success': True,
                    'command': cmd,
                    'output': output,
                    'message': 'Perintah cat berhasil dijalankan (mock mode)'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'command': cmd,
                    'message': f'Gagal membaca file: {str(e)}'
                }), 500
                
        elif command == 'delete':
            # Delete file/directory
            cmd = f'hdfs dfs -rm -r {path}'
            success = hdfs_ops.delete_file(path)
            
            return jsonify({
                'success': success,
                'command': cmd,
                'message': f'File/directory {path} berhasil dihapus!' if success else 'Gagal menghapus file/directory',
                'output': None
            })
            
        else:
            return jsonify({
                'success': False,
                'message': f'Command tidak dikenal: {command}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Hadoop Web Interface...")
    print("📊 Access the interface at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
