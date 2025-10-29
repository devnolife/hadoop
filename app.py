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


@app.route('/api/hdfs/list', methods=['GET'])
def hdfs_list():
    """List HDFS directory"""
    try:
        path = request.args.get('path', '/')
        hdfs = HDFSOperations()
        files = hdfs.list_directory(path)
        
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
        local_file = data.get('local_file')
        hdfs_path = data.get('hdfs_path')
        
        hdfs = HDFSOperations()
        success = hdfs.upload_file(local_file, hdfs_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'File uploaded to HDFS successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to upload file to HDFS'
            }), 400
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


if __name__ == '__main__':
    print("🚀 Starting Hadoop Web Interface...")
    print("📊 Access the interface at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
