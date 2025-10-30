// Hadoop Data Manager - Frontend JavaScript
// Author: devnolife

let currentDatabase = null;
let exportCount = 0;

// Show loading indicator
function showLoading() {
  document.getElementById('loadingIndicator').style.display = 'block';
}

// Hide loading indicator
function hideLoading() {
  document.getElementById('loadingIndicator').style.display = 'none';
}

// Show alert message
function showAlert(message, type = 'info') {
  const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

  const container = document.querySelector('.main-container');
  container.insertAdjacentHTML('afterbegin', alertHtml);

  // Auto dismiss after 5 seconds
  setTimeout(() => {
    const alert = container.querySelector('.alert');
    if (alert) {
      alert.remove();
    }
  }, 5000);
}

// Connect to MySQL
async function connectMySQL() {
  const host = document.getElementById('mysqlHost').value;
  const port = document.getElementById('mysqlPort').value;
  const user = document.getElementById('mysqlUser').value;
  const password = document.getElementById('mysqlPassword').value;
  const database = document.getElementById('mysqlDatabase').value;

  showLoading();

  try {
    const response = await fetch('/api/mysql/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        host,
        port: parseInt(port) || 3306,
        user,
        password,
        database: database || null
      })
    });

    const data = await response.json();

    if (data.success) {
      showAlert('✅ ' + data.message, 'success');
      currentDatabase = database;
      updateStatus(true);
      loadDatabases();
      loadTables();
      document.getElementById('tablesCard').style.display = 'block';
      document.getElementById('queryCard').style.display = 'block';
      document.getElementById('hdfsOpsCard').style.display = 'block';
      loadExportedFiles();
    } else {
      showAlert('❌ ' + data.message, 'danger');
      updateStatus(false);
    }
  } catch (error) {
    showAlert('❌ Connection error: ' + error.message, 'danger');
    updateStatus(false);
  } finally {
    hideLoading();
  }
}

// Update connection status
function updateStatus(connected) {
  const statusText = document.getElementById('statusText');
  const statusIcon = document.getElementById('statusIcon');

  if (connected) {
    statusText.textContent = 'Connected';
    statusText.className = 'text-success';
    statusIcon.className = 'bi bi-check-circle-fill text-success';
  } else {
    statusText.textContent = 'Disconnected';
    statusText.className = 'text-danger';
    statusIcon.className = 'bi bi-x-circle-fill text-danger';
  }
}

// Load databases
async function loadDatabases() {
  try {
    const response = await fetch('/api/mysql/databases');
    const data = await response.json();

    if (data.success) {
      document.getElementById('dbCount').textContent = data.databases.length;
    }
  } catch (error) {
    console.error('Error loading databases:', error);
  }
}

// Load tables
async function loadTables() {
  showLoading();

  try {
    const response = await fetch('/api/mysql/tables');
    const data = await response.json();

    if (data.success) {
      const tbody = document.getElementById('tablesTableBody');
      tbody.innerHTML = '';

      document.getElementById('tableCount').textContent = data.tables.length;

      if (data.tables.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No tables found</td></tr>';
        return;
      }

      // Load info for each table
      for (const table of data.tables) {
        const infoResponse = await fetch(`/api/mysql/table/${table}/info`);
        const infoData = await infoResponse.json();

        const row = document.createElement('tr');
        row.innerHTML = `
                    <td><i class="bi bi-table"></i> ${table}</td>
                    <td>${infoData.success ? infoData.info.row_count.toLocaleString() : 'N/A'}</td>
                    <td>${infoData.success ? infoData.info.columns.length : 'N/A'}</td>
                    <td class="table-actions">
                        <button class="btn btn-sm btn-primary" onclick="previewTable('${table}')">
                            <i class="bi bi-eye"></i> Preview
                        </button>
                        <button class="btn btn-sm btn-success" onclick="exportTable('${table}')">
                            <i class="bi bi-download"></i> Export
                        </button>
                    </td>
                `;
        tbody.appendChild(row);
      }

      // Populate HDFS table selects
      populateHDFSTableSelects(data.tables);
    }
  } catch (error) {
    showAlert('❌ Error loading tables: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Refresh tables
function refreshTables() {
  loadTables();
}

// Preview table data
async function previewTable(tableName) {
  showLoading();

  try {
    const response = await fetch(`/api/mysql/table/${tableName}/preview?limit=50`);
    const data = await response.json();

    if (data.success) {
      document.getElementById('previewTableName').textContent = tableName;

      const previewContent = document.getElementById('previewContent');

      if (data.data.length === 0) {
        previewContent.innerHTML = '<p class="text-muted">No data found</p>';
      } else {
        // Create table
        const columns = Object.keys(data.data[0]);
        let tableHtml = '<div class="table-responsive"><table class="table table-striped table-bordered">';

        // Header
        tableHtml += '<thead><tr>';
        columns.forEach(col => {
          tableHtml += `<th>${col}</th>`;
        });
        tableHtml += '</tr></thead>';

        // Body
        tableHtml += '<tbody>';
        data.data.forEach(row => {
          tableHtml += '<tr>';
          columns.forEach(col => {
            tableHtml += `<td>${row[col] !== null ? row[col] : '<em>NULL</em>'}</td>`;
          });
          tableHtml += '</tr>';
        });
        tableHtml += '</tbody></table></div>';

        previewContent.innerHTML = tableHtml;
      }

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('previewModal'));
      modal.show();
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error previewing table: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Export table to CSV
async function exportTable(tableName) {
  showLoading();

  try {
    const response = await fetch(`/api/mysql/table/${tableName}/export`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    });

    const data = await response.json();

    if (data.success) {
      showAlert(`✅ Table ${tableName} exported successfully!`, 'success');
      exportCount++;
      document.getElementById('exportCount').textContent = exportCount;

      // Download file
      const fileName = data.file.split('/').pop();
      window.location.href = `/download/${fileName}`;
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error exporting table: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Execute SQL query
async function executeQuery() {
  const query = document.getElementById('sqlQuery').value.trim();

  if (!query) {
    showAlert('⚠️ Please enter a SQL query', 'warning');
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/mysql/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query })
    });

    const data = await response.json();

    const resultsDiv = document.getElementById('queryResults');

    if (data.success) {
      if (data.results.length === 0) {
        resultsDiv.innerHTML = '<div class="alert alert-info">Query executed successfully. No results returned.</div>';
      } else {
        // Create table
        const columns = Object.keys(data.results[0]);
        let tableHtml = '<div class="alert alert-success">Query executed successfully. ' + data.count + ' rows returned.</div>';
        tableHtml += '<div class="table-responsive"><table class="table table-striped table-bordered">';

        // Header
        tableHtml += '<thead><tr>';
        columns.forEach(col => {
          tableHtml += `<th>${col}</th>`;
        });
        tableHtml += '</tr></thead>';

        // Body
        tableHtml += '<tbody>';
        data.results.forEach(row => {
          tableHtml += '<tr>';
          columns.forEach(col => {
            tableHtml += `<td>${row[col] !== null ? row[col] : '<em>NULL</em>'}</td>`;
          });
          tableHtml += '</tr>';
        });
        tableHtml += '</tbody></table></div>';

        resultsDiv.innerHTML = tableHtml;
      }
    } else {
      resultsDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${data.message}</div>`;
    }
  } catch (error) {
    document.getElementById('queryResults').innerHTML = `<div class="alert alert-danger">❌ Error: ${error.message}</div>`;
  } finally {
    hideLoading();
  }
}

// Upload file to HDFS
async function uploadToHDFS() {
  const csvFile = document.getElementById('uploadCsvFile').value;
  const hdfsPath = document.getElementById('hdfsUploadPath').value;

  if (!csvFile || !hdfsPath) {
    showAlert('⚠️ Please select file and specify HDFS path', 'warning');
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/hdfs/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        csv_file: csvFile,
        hdfs_path: hdfsPath
      })
    });

    const data = await response.json();

    if (data.success) {
      showAlert('✅ ' + data.message, 'success');
      document.getElementById('hdfsResults').innerHTML = `
        <div class="alert alert-success">
          <strong>✅ Upload Successful!</strong><br>
          File: ${csvFile}<br>
          HDFS Path: ${hdfsPath}<br>
          ${data.details || ''}
        </div>`;
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Download file from HDFS
async function downloadFromHDFS() {
  const hdfsPath = document.getElementById('hdfsDownloadPath').value;
  const localFile = document.getElementById('localFilename').value;

  if (!hdfsPath || !localFile) {
    showAlert('⚠️ Please specify HDFS path and local filename', 'warning');
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/hdfs/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        hdfs_path: hdfsPath,
        local_file: localFile
      })
    });

    const data = await response.json();

    if (data.success) {
      showAlert('✅ ' + data.message, 'success');
      document.getElementById('hdfsResults').innerHTML = `
        <div class="alert alert-success">
          <strong>✅ Download Successful!</strong><br>
          HDFS Path: ${hdfsPath}<br>
          Local File: ${localFile}<br>
          ${data.details || ''}
        </div>`;
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Export MySQL table to HDFS
async function exportTableToHDFS() {
  const tableName = document.getElementById('exportTableToHDFS').value;
  const hdfsPath = document.getElementById('hdfsExportPath').value;

  if (!tableName) {
    showAlert('⚠️ Please select a table', 'warning');
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/hdfs/export-table', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        table_name: tableName,
        hdfs_path: hdfsPath || `/user/data/mysql/${tableName}.csv`
      })
    });

    const data = await response.json();

    if (data.success) {
      const alertType = data.warning ? 'warning' : 'success';
      const icon = data.warning ? '⚠️' : '✅';

      showAlert(icon + ' ' + data.message, alertType);

      let resultHTML = `<div class="alert alert-${alertType}">
        <strong>${icon} Export Successful!</strong><br>
        Table: ${tableName}<br>
        Rows Exported: ${data.row_count || 'N/A'}<br>`;

      if (data.hdfs_path) {
        resultHTML += `HDFS Path: ${data.hdfs_path}<br>`;
      }

      resultHTML += `CSV File: exports/${data.csv_file || 'N/A'}`;

      if (data.note) {
        resultHTML += `<br><small class="text-muted">ℹ️ ${data.note}</small>`;
      }

      resultHTML += `</div>`;

      document.getElementById('hdfsResults').innerHTML = resultHTML;
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// Bulk export all tables to HDFS
async function bulkExportToHDFS() {
  const basePath = document.getElementById('hdfsBulkPath').value;

  if (!confirm('⚠️ This will export ALL tables to HDFS. Continue?')) {
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/hdfs/bulk-export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        base_path: basePath
      })
    });

    const data = await response.json();

    if (data.success) {
      showAlert('✅ ' + data.message, 'success');

      let resultsHtml = `
        <div class="alert alert-success">
          <strong>✅ Bulk Export Completed!</strong><br>
          <strong>Summary:</strong><br>
          Total Tables: ${data.total}<br>
          Successful: ${data.successful}<br>
          Failed: ${data.failed}<br>
          HDFS Base Path: ${basePath}
        </div>`;

      if (data.details && data.details.length > 0) {
        resultsHtml += '<div class="table-responsive mt-3"><table class="table table-sm table-striped">';
        resultsHtml += '<thead><tr><th>Table</th><th>Status</th><th>Rows</th><th>HDFS Path / CSV File</th></tr></thead><tbody>';

        data.details.forEach((item) => {
          let statusClass, statusIcon, statusText;

          if (item.status === 'success') {
            statusClass = 'success';
            statusIcon = '✅';
            statusText = 'Success';
          } else if (item.status === 'csv_only') {
            statusClass = 'warning';
            statusIcon = '⚠️';
            statusText = 'CSV Only';
          } else if (item.status === 'skipped') {
            statusClass = 'secondary';
            statusIcon = '⏭️';
            statusText = 'Skipped';
          } else {
            statusClass = 'danger';
            statusIcon = '❌';
            statusText = 'Failed';
          }

          const pathInfo = item.hdfs_path || (item.csv_file ? `exports/${item.csv_file}` : 'N/A');

          resultsHtml += `
            <tr class="table-${statusClass}">
              <td>${item.table}</td>
              <td>${statusIcon} ${statusText}</td>
              <td>${item.rows || 'N/A'}</td>
              <td><small>${pathInfo}</small>${item.note ? '<br><small class="text-muted">' + item.note + '</small>' : ''}</td>
            </tr>`;
        });

        resultsHtml += '</tbody></table></div>';
      }

      document.getElementById('hdfsResults').innerHTML = resultsHtml;
    } else {
      showAlert('❌ ' + data.message, 'danger');
    }
  } catch (error) {
    showAlert('❌ Error: ' + error.message, 'danger');
  } finally {
    hideLoading();
  }
}

// List HDFS files
async function listHDFSFiles() {
  const hdfsPath = document.getElementById('hdfsListPath').value;

  if (!hdfsPath) {
    showAlert('⚠️ Please specify HDFS path', 'warning');
    return;
  }

  showLoading();

  try {
    const response = await fetch('/api/hdfs/list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        hdfs_path: hdfsPath
      })
    });

    const data = await response.json();

    if (data.success && data.files) {
      let tableHtml = '<table class="table table-hover">';
      tableHtml += '<thead><tr><th>Name</th><th>Type</th><th>Size</th><th>Modified</th></tr></thead><tbody>';

      data.files.forEach((file) => {
        const icon = file.type === 'directory' ? '📁' : '📄';
        tableHtml += `
          <tr>
            <td>${icon} ${file.name}</td>
            <td>${file.type}</td>
            <td>${file.size || 'N/A'}</td>
            <td>${file.modified || 'N/A'}</td>
          </tr>`;
      });

      tableHtml += '</tbody></table>';
      document.getElementById('hdfsFileList').innerHTML = tableHtml;
    } else {
      document.getElementById('hdfsFileList').innerHTML = `<div class="alert alert-warning">${data.message || 'No files found'}</div>`;
    }
  } catch (error) {
    document.getElementById('hdfsFileList').innerHTML = `<div class="alert alert-danger">❌ Error: ${error.message}</div>`;
  } finally {
    hideLoading();
  }
}

// Load exported CSV files for HDFS upload
async function loadExportedFiles() {
  try {
    const response = await fetch('/api/exports/list');
    const data = await response.json();

    if (data.success && data.files) {
      const select = document.getElementById('uploadCsvFile');
      select.innerHTML = '<option value="">-- Select File --</option>';

      data.files.forEach((file) => {
        const option = document.createElement('option');
        option.value = file;
        option.textContent = file;
        select.appendChild(option);
      });
    }
  } catch (error) {
    console.error('Error loading exported files:', error);
  }
}

// Populate table selects for HDFS operations
function populateHDFSTableSelects(tables) {
  const exportSelect = document.getElementById('exportTableToHDFS');
  if (exportSelect) {
    exportSelect.innerHTML = '<option value="">-- Select Table --</option>';
    tables.forEach((table) => {
      const option = document.createElement('option');
      option.value = table;
      option.textContent = table;
      exportSelect.appendChild(option);
    });
  }
}

// Run HDFS commands (Interactive Learning Mode)
async function runHDFSCommand(command, pathInputId) {
  const path = document.getElementById(pathInputId).value;
  const resultDiv = document.getElementById(`result-${command}`);

  if (!path) {
    resultDiv.innerHTML = '<div class="alert alert-warning">⚠️ Mohon isi path terlebih dahulu</div>';
    return;
  }

  resultDiv.innerHTML = '<div class="alert alert-info"><i class="bi bi-hourglass-split"></i> Menjalankan perintah...</div>';

  try {
    const response = await fetch('/api/hdfs/command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        command: command,
        path: path
      })
    });

    const data = await response.json();

    if (data.success) {
      let html = '<div class="alert alert-success"><strong>✅ Berhasil!</strong><br>';
      html += `<strong>Perintah:</strong> <code>${data.command}</code><br>`;

      if (data.output) {
        if (command === 'list') {
          // Format list output as table
          html += '<div class="mt-2"><strong>Files/Directories:</strong>';
          html += '<div class="table-responsive mt-2"><table class="table table-sm table-striped">';
          html += '<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead><tbody>';

          if (Array.isArray(data.files)) {
            data.files.forEach((file) => {
              const icon = file.type === 'directory' ? '📁' : '📄';
              html += `<tr><td>${icon} ${file.name}</td><td>${file.type}</td><td>${file.size || 'N/A'}</td></tr>`;
            });
          }

          html += '</tbody></table></div></div>';
        } else if (command === 'cat') {
          // Format cat output
          html += '<div class="mt-2"><strong>Isi File (10 baris pertama):</strong>';
          html += `<pre class="bg-dark text-light p-2 mt-2" style="max-height: 300px; overflow-y: auto;">${data.output}</pre></div>`;
        } else {
          html += `<div class="mt-2"><pre class="bg-light p-2">${data.output}</pre></div>`;
        }
      }

      if (data.message) {
        html += `<div class="mt-2">${data.message}</div>`;
      }

      html += '</div>';
      resultDiv.innerHTML = html;
    } else {
      resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Error!</strong><br>${data.message}</div>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Error!</strong><br>${error.message}</div>`;
  }
}

// Run HDFS Upload (Interactive)
async function runHDFSUpload() {
  const file = document.getElementById('hdfsUploadFile').value;
  const dest = document.getElementById('hdfsUploadDest').value;
  const resultDiv = document.getElementById('result-upload');

  if (!file || !dest) {
    resultDiv.innerHTML = '<div class="alert alert-warning">⚠️ Mohon pilih file dan isi destination path</div>';
    return;
  }

  resultDiv.innerHTML = '<div class="alert alert-info"><i class="bi bi-hourglass-split"></i> Uploading...</div>';

  try {
    const response = await fetch('/api/hdfs/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        csv_file: file,
        hdfs_path: dest
      })
    });

    const data = await response.json();

    if (data.success) {
      resultDiv.innerHTML = `
        <div class="alert alert-success">
          <strong>✅ Upload Berhasil!</strong><br>
          File: ${file}<br>
          HDFS Path: ${dest}<br>
          <small>Perintah: <code>hdfs dfs -put exports/${file} ${dest}</code></small>
        </div>`;
    } else {
      resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Upload Gagal!</strong><br>${data.message}</div>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Error!</strong><br>${error.message}</div>`;
  }
}

// Run HDFS Download (Interactive)
async function runHDFSDownload() {
  const src = document.getElementById('hdfsDownloadSrc').value;
  const dest = document.getElementById('hdfsDownloadDest').value;
  const resultDiv = document.getElementById('result-download');

  if (!src || !dest) {
    resultDiv.innerHTML = '<div class="alert alert-warning">⚠️ Mohon isi source dan destination path</div>';
    return;
  }

  resultDiv.innerHTML = '<div class="alert alert-info"><i class="bi bi-hourglass-split"></i> Downloading...</div>';

  try {
    const response = await fetch('/api/hdfs/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        hdfs_path: src,
        local_file: dest
      })
    });

    const data = await response.json();

    if (data.success) {
      resultDiv.innerHTML = `
        <div class="alert alert-success">
          <strong>✅ Download Berhasil!</strong><br>
          HDFS Path: ${src}<br>
          Local File: exports/${dest}<br>
          <small>Perintah: <code>hdfs dfs -get ${src} exports/${dest}</code></small>
        </div>`;
    } else {
      resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Download Gagal!</strong><br>${data.message}</div>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="alert alert-danger"><strong>❌ Error!</strong><br>${error.message}</div>`;
  }
}

// Load files for interactive HDFS upload selector
async function loadFilesForHDFSUpload() {
  try {
    const response = await fetch('/api/exports/list');
    const data = await response.json();

    if (data.success && data.files) {
      const select = document.getElementById('hdfsUploadFile');
      if (select) {
        select.innerHTML = '<option value="">-- Pilih file dari exports/ --</option>';
        data.files.forEach((file) => {
          const option = document.createElement('option');
          option.value = file;
          option.textContent = file;
          select.appendChild(option);
        });
      }
    }
  } catch (error) {
    console.error('Error loading files for HDFS upload:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 Hadoop Data Manager initialized');
  console.log('Created by devnolife');

  // Load exported CSV files
  loadExportedFiles();
  loadFilesForHDFSUpload();
});
