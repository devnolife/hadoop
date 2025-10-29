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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 Hadoop Data Manager initialized');
  console.log('Created by devnolife');
});
