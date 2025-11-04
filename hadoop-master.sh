#!/bin/bash

# ============================================================================
# HADOOP MASTER CONTROL SCRIPT
# All-in-one script for Hadoop installation, configuration, and management
# ============================================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m'
BOLD='\033[1m'
BLINK='\033[5m'

# Background colors
BG_GREEN='\033[42m'
BG_BLUE='\033[44m'

# Unicode
CHECK="✓"
CROSS="✗"
ARROW="➜"
STAR="★"
ROCKET="🚀"
FIRE="🔥"
GEAR="⚙"
DISK="💾"
NETWORK="🌐"
DATABASE="🗄"
LOCK="🔒"
CHART="📊"
FILE="📁"
SERVER="🖥"
CLUSTER="☁"

# Paths
BASE_DIR="/home/devnolife/hdoop"
HADOOP_ARCHIVE="$BASE_DIR/hadoop/hadoop-3.3.6.tar.gz"
HADOOP_DIR="$BASE_DIR/hadoop/hadoop-3.3.6"
CONFIG_DIR="$BASE_DIR/hadoop/config"
DB_CONFIG="$CONFIG_DIR/database-config.conf"

# Terminal width
TERM_WIDTH=$(tput cols)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

print_banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ██╗  ██╗ █████╗ ████████╗ ██████╗  ██████╗  ██████╗ ██████╗   ║
    ║   ██║  ██║██╔══██╗██╔═════╝██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗  ║
    ║   ███████║███████║██║  ███╗██║   ██║██║   ██║██████╔╝██████╔╝  ║
    ║   ██╔══██║██╔══██║██║   ██║██║   ██║██║   ██║██╔═══╝ ██╔═══╝   ║
    ║   ██║  ██║██║  ██║╚████████║╚██████╔╝╚██████╔╝██║     ██║       ║
    ║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝       ║
    ║                                                                   ║
    ║              ${YELLOW}MASTER CONTROL & MANAGEMENT${CYAN}                      ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo -e "${MAGENTA}${BOLD}           ╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}${BOLD}           ║  ${STAR}${FIRE} Created by: ${WHITE}DevNoLife${MAGENTA} ${FIRE}${STAR}             ║${NC}"
    echo -e "${MAGENTA}${BOLD}           ╔═══════════════════════════════════════════════╝${NC}"
    echo -e "${GRAY}              Big Data Processing Framework - v3.3.6${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}${BOLD}  ${CHECK} ${1}${NC}"; }
print_error() { echo -e "${RED}${BOLD}  ${CROSS} ${1}${NC}"; }
print_warning() { echo -e "${YELLOW}${BOLD}  ⚠ ${1}${NC}"; }
print_info() { echo -e "${CYAN}${BOLD}  ${ARROW} ${1}${NC}"; }
print_divider() { printf "${GRAY}%0.s${1:-═}${NC}" $(seq 1 $TERM_WIDTH); echo ""; }
print_step() { echo -e "${CYAN}${BOLD}[${1}]${NC} ${WHITE}${2}${NC}"; }

check_service() {
    if jps | grep -q "$1"; then
        return 0
    else
        return 1
    fi
}

spinner() {
    local pid=$1
    local message=$2
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    echo -n " "
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "${CYAN}[%c] ${message}${NC}" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# ============================================================================
# INSTALLATION MODULE
# ============================================================================

install_hadoop() {
    print_banner
    echo -e "${GREEN}${BOLD}${BLINK}  ${ROCKET} HADOOP INSTALLATION MODULE ${ROCKET}${NC}"
    echo ""
    print_divider
    sleep 1

    # Check download
    print_step "1/9" "${DISK} Checking Hadoop Download"
    print_divider "─"
    if [ ! -f "$HADOOP_ARCHIVE" ]; then
        print_error "Hadoop archive not found at: $HADOOP_ARCHIVE"
        echo -e "${YELLOW}  Download is still in progress or failed.${NC}"
        read -p "  Press Enter to return to menu..."
        return 1
    fi
    print_success "Hadoop archive found!"
    echo ""
    sleep 1

    # Extract
    print_step "2/9" "${DISK} Extracting Hadoop"
    print_divider "─"
    cd "$BASE_DIR/hadoop"
    if [ -d "hadoop-3.3.6" ]; then
        print_warning "Hadoop already extracted. Skipping."
    else
        print_info "Extracting 696MB archive..."
        (tar -xzf hadoop-3.3.6.tar.gz) &
        pid=$!
        spinner $pid "Extracting files"
        wait $pid
        print_success "Extraction complete!"
    fi
    cd "$BASE_DIR"
    echo ""
    sleep 1

    # Copy configs
    print_step "3/9" "${GEAR} Configuring Hadoop"
    print_divider "─"
    cp "$CONFIG_DIR"/*.xml "$HADOOP_DIR/etc/hadoop/" 2>/dev/null
    cp "$CONFIG_DIR/workers" "$HADOOP_DIR/etc/hadoop/" 2>/dev/null
    if ! grep -q "JAVA_HOME=/home/devnolife/hdoop/jdk-11.0.2" "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"; then
        echo "export JAVA_HOME=/home/devnolife/hdoop/jdk-11.0.2" >> "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"
    fi
    print_success "Configuration complete!"
    echo ""
    sleep 1

    # Setup environment
    print_step "4/9" "${GEAR} Environment Variables"
    print_divider "─"
    source "$BASE_DIR/scripts/env-setup.sh"
    print_success "Environment loaded!"
    echo ""
    sleep 1

    # Verify Java
    print_step "5/9" "${GEAR} Verifying Java"
    print_divider "─"
    java_version=$(java -version 2>&1 | head -n 1)
    print_success "${java_version}"
    echo ""
    sleep 1

    # SSH
    print_step "6/9" "${LOCK} SSH Configuration"
    print_divider "─"
    if [ ! -f ~/.ssh/id_rsa ]; then
        ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa -q
        print_success "SSH key generated!"
    else
        print_info "SSH key exists"
    fi
    if ! grep -q "$(cat ~/.ssh/id_rsa.pub)" ~/.ssh/authorized_keys 2>/dev/null; then
        cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 2>/dev/null
        chmod 0600 ~/.ssh/authorized_keys
    fi
    print_success "SSH configured!"
    echo ""
    sleep 1

    # Create directories
    print_step "7/9" "${DISK} Creating Directories"
    print_divider "─"
    mkdir -p "$BASE_DIR/hadoop/data/namenode"
    mkdir -p "$BASE_DIR/hadoop/data/datanode"
    mkdir -p "$BASE_DIR/hadoop/tmp"
    print_success "Directories created!"
    echo ""
    sleep 1

    # Format NameNode
    print_step "8/9" "${DISK} Formatting NameNode"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  Format NameNode? (y/n): ${NC}"
    read -r format_choice
    if [[ $format_choice =~ ^[Yy]$ ]]; then
        hdfs namenode -format -force > /dev/null 2>&1
        print_success "NameNode formatted!"
    else
        print_warning "Skipped formatting"
    fi
    echo ""
    sleep 1

    # Start services
    print_step "9/9" "${ROCKET} Starting Services"
    print_divider "─"
    print_info "Starting HDFS..."
    $HADOOP_HOME/sbin/start-dfs.sh > /dev/null 2>&1
    sleep 3
    print_success "HDFS started!"
    print_info "Starting YARN..."
    $HADOOP_HOME/sbin/start-yarn.sh > /dev/null 2>&1
    sleep 3
    print_success "YARN started!"
    echo ""

    print_divider
    echo ""
    echo -e "${BG_GREEN}${WHITE}${BOLD}  ${ROCKET} INSTALLATION COMPLETE! ${ROCKET}  ${NC}"
    echo ""
    echo -e "${CYAN}${BOLD}  Running Processes:${NC}"
    jps | while read line; do
        echo -e "${GREEN}    ${CHECK} ${line}${NC}"
    done
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

# ============================================================================
# DATABASE SETUP MODULE
# ============================================================================

setup_database() {
    print_banner
    echo -e "${MAGENTA}${BOLD}  ${DATABASE} DATABASE INTEGRATION WIZARD${NC}"
    echo ""
    print_divider
    sleep 1

    # Database type selection
    print_step "1/7" "Select Database Type"
    print_divider "─"
    echo ""
    echo -e "${CYAN}${BOLD}  Available Databases:${NC}"
    echo -e "${WHITE}     1) MySQL${NC}"
    echo -e "${WHITE}     2) PostgreSQL${NC}"
    echo -e "${WHITE}     3) Oracle${NC}"
    echo -e "${WHITE}     4) SQL Server${NC}"
    echo ""
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Select (1-4): ${NC}"
    read -r db_choice

    case $db_choice in
        1) DB_TYPE="mysql"; DB_PORT_DEFAULT="3306"; JDBC_PREFIX="jdbc:mysql" ;;
        2) DB_TYPE="postgresql"; DB_PORT_DEFAULT="5432"; JDBC_PREFIX="jdbc:postgresql" ;;
        3) DB_TYPE="oracle"; DB_PORT_DEFAULT="1521"; JDBC_PREFIX="jdbc:oracle:thin" ;;
        4) DB_TYPE="sqlserver"; DB_PORT_DEFAULT="1433"; JDBC_PREFIX="jdbc:sqlserver" ;;
        *) print_error "Invalid choice!"; read -p "Press Enter..."; return 1 ;;
    esac
    print_success "${DB_TYPE} selected!"
    echo ""
    sleep 1

    # Get connection details
    print_step "2/7" "Database Host"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Host (default: localhost): ${NC}"
    read -r DB_HOST
    DB_HOST=${DB_HOST:-localhost}
    print_success "Host: ${DB_HOST}"
    echo ""

    print_step "3/7" "Database Port"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Port (default: ${DB_PORT_DEFAULT}): ${NC}"
    read -r DB_PORT
    DB_PORT=${DB_PORT:-$DB_PORT_DEFAULT}
    print_success "Port: ${DB_PORT}"
    echo ""

    print_step "4/7" "Database Name"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Database name: ${NC}"
    read -r DB_NAME
    [ -z "$DB_NAME" ] && { print_error "Required!"; read -p "Press Enter..."; return 1; }
    print_success "Database: ${DB_NAME}"
    echo ""

    print_step "5/7" "Username"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Username: ${NC}"
    read -r DB_USER
    [ -z "$DB_USER" ] && { print_error "Required!"; read -p "Press Enter..."; return 1; }
    print_success "Username: ${DB_USER}"
    echo ""

    print_step "6/7" "Password"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${LOCK} Password: ${NC}"
    read -s DB_PASSWORD
    echo ""
    print_success "Password received!"
    echo ""

    print_step "7/7" "Table Selection"
    print_divider "─"
    echo -ne "${YELLOW}${BOLD}  ${ARROW} Table (or 'ALL'): ${NC}"
    read -r DB_TABLE
    DB_TABLE=${DB_TABLE:-ALL}
    print_success "Table: ${DB_TABLE}"
    echo ""

    # Build JDBC URL
    if [ "$DB_TYPE" == "mysql" ] || [ "$DB_TYPE" == "postgresql" ]; then
        JDBC_URL="${JDBC_PREFIX}://${DB_HOST}:${DB_PORT}/${DB_NAME}"
    elif [ "$DB_TYPE" == "oracle" ]; then
        JDBC_URL="${JDBC_PREFIX}:@${DB_HOST}:${DB_PORT}:${DB_NAME}"
    elif [ "$DB_TYPE" == "sqlserver" ]; then
        JDBC_URL="${JDBC_PREFIX}://${DB_HOST}:${DB_PORT};databaseName=${DB_NAME}"
    fi

    # Summary
    print_divider
    echo ""
    echo -e "${GREEN}${BOLD}  ${CHECK} Configuration Summary:${NC}"
    echo -e "${CYAN}${BOLD}  ════════════════════════════════════════${NC}"
    echo -e "${WHITE}     Database:  ${CYAN}${DB_TYPE}${NC}"
    echo -e "${WHITE}     Host:      ${CYAN}${DB_HOST}:${DB_PORT}${NC}"
    echo -e "${WHITE}     Database:  ${CYAN}${DB_NAME}${NC}"
    echo -e "${WHITE}     Username:  ${CYAN}${DB_USER}${NC}"
    echo -e "${WHITE}     Table:     ${CYAN}${DB_TABLE}${NC}"
    echo -e "${CYAN}${BOLD}  ════════════════════════════════════════${NC}"
    echo ""

    # Save config
    mkdir -p "$CONFIG_DIR"
    cat > "$DB_CONFIG" << EOF
DB_TYPE="${DB_TYPE}"
DB_HOST="${DB_HOST}"
DB_PORT="${DB_PORT}"
DB_NAME="${DB_NAME}"
DB_USER="${DB_USER}"
DB_PASSWORD="${DB_PASSWORD}"
DB_TABLE="${DB_TABLE}"
JDBC_URL="${JDBC_URL}"
EOF
    chmod 600 "$DB_CONFIG"
    print_success "Configuration saved!"

    # Generate Sqoop script
    SQOOP_SCRIPT="$BASE_DIR/scripts/sqoop-import.sh"
    cat > "$SQOOP_SCRIPT" << EOF
#!/bin/bash
source ${DB_CONFIG}

# Import table to HDFS
sqoop import \\
  --connect "\${JDBC_URL}" \\
  --username "\${DB_USER}" \\
  --password "\${DB_PASSWORD}" \\
  --table "\${DB_TABLE}" \\
  --target-dir "/user/hadoop/sqoop/\${DB_TABLE}" \\
  --m 1

# Verify
hdfs dfs -ls /user/hadoop/sqoop/\${DB_TABLE}/
EOF
    chmod +x "$SQOOP_SCRIPT"
    print_success "Sqoop script created: $SQOOP_SCRIPT"
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

# ============================================================================
# WEB DASHBOARD MODULE
# ============================================================================

show_web_dashboard() {
    while true; do
        print_banner
        echo -e "${BLUE}${BOLD}  ${NETWORK} WEB INTERFACES GUIDE${NC}"
        echo ""
        print_divider

        # Check services
        echo ""
        echo -e "${CYAN}${BOLD}  ${SERVER} Service Status:${NC}"
        print_divider "─"
        check_service "NameNode" && print_success "NameNode running" || echo -e "${RED}  ${CROSS} NameNode not running${NC}"
        check_service "DataNode" && print_success "DataNode running" || echo -e "${RED}  ${CROSS} DataNode not running${NC}"
        check_service "ResourceManager" && print_success "ResourceManager running" || echo -e "${RED}  ${CROSS} ResourceManager not running${NC}"
        check_service "NodeManager" && print_success "NodeManager running" || echo -e "${RED}  ${CROSS} NodeManager not running${NC}"

        echo ""
        print_divider
        echo ""
        echo -e "${YELLOW}${BOLD}  ${NETWORK} Available Interfaces:${NC}"
        echo ""
        echo -e "${WHITE}  1) ${BOLD}NameNode UI${NC}          ${GRAY}(http://localhost:9870)${NC}"
        echo -e "${GRAY}     └─ HDFS metadata, file browser, cluster status${NC}"
        echo ""
        echo -e "${WHITE}  2) ${BOLD}ResourceManager UI${NC}   ${GRAY}(http://localhost:8088)${NC}"
        echo -e "${GRAY}     └─ YARN jobs, applications, resource monitoring${NC}"
        echo ""
        echo -e "${WHITE}  3) ${BOLD}DataNode UI${NC}          ${GRAY}(http://localhost:9864)${NC}"
        echo -e "${GRAY}     └─ DataNode storage, blocks, health status${NC}"
        echo ""
        echo -e "${WHITE}  4) ${BOLD}Architecture Guide${NC}"
        echo -e "${GRAY}     └─ How HDFS & YARN work together${NC}"
        echo ""
        echo -e "${WHITE}  5) ${BOLD}Open All in Browser${NC}"
        echo ""
        echo -e "${WHITE}  0) ${BOLD}Back to Main Menu${NC}"
        echo ""
        echo -ne "${CYAN}${BOLD}  ${ARROW} Select option: ${NC}"
        read -r web_choice

        case $web_choice in
            1) show_namenode_guide ;;
            2) show_resourcemanager_guide ;;
            3) show_datanode_guide ;;
            4) show_architecture ;;
            5)
                if command -v xdg-open &> /dev/null; then
                    xdg-open "http://localhost:9870" &
                    xdg-open "http://localhost:8088" &
                    xdg-open "http://localhost:9864" &
                    print_success "Browsers opened!"
                else
                    print_warning "Manual open required:"
                    echo -e "${CYAN}  http://localhost:9870${NC}"
                    echo -e "${CYAN}  http://localhost:8088${NC}"
                    echo -e "${CYAN}  http://localhost:9864${NC}"
                fi
                sleep 3
                ;;
            0) return ;;
            *) print_error "Invalid option!"; sleep 2 ;;
        esac
    done
}

show_namenode_guide() {
    clear
    print_banner
    echo -e "${GREEN}${BOLD}  ${FILE} NAMENODE WEB UI - PORT 9870${NC}"
    print_divider
    echo ""
    echo -e "${CYAN}${BOLD}  ${NETWORK} URL: ${WHITE}http://localhost:9870${NC}"
    echo ""
    echo -e "${YELLOW}${BOLD}  📋 Key Features:${NC}"
    echo -e "${WHITE}  1. Overview Tab${NC} - Cluster capacity, live/dead nodes"
    echo -e "${WHITE}  2. Datanodes Tab${NC} - Individual node health & storage"
    echo -e "${WHITE}  3. Browse Filesystem${NC} - Navigate HDFS like file explorer"
    echo -e "${WHITE}  4. Logs${NC} - Debug issues & errors"
    echo ""
    echo -e "${CYAN}${BOLD}  ⚙ How NameNode Works:${NC}"
    echo -e "${GRAY}  Step 1: Client requests file → NameNode returns block locations${NC}"
    echo -e "${GRAY}  Step 2: Client reads/writes directly to DataNodes${NC}"
    echo -e "${GRAY}  Step 3: NameNode tracks metadata (not actual data)${NC}"
    echo -e "${GRAY}  Step 4: Heartbeat monitoring ensures node health${NC}"
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

show_resourcemanager_guide() {
    clear
    print_banner
    echo -e "${GREEN}${BOLD}  ${CLUSTER} RESOURCEMANAGER UI - PORT 8088${NC}"
    print_divider
    echo ""
    echo -e "${CYAN}${BOLD}  ${NETWORK} URL: ${WHITE}http://localhost:8088${NC}"
    echo ""
    echo -e "${YELLOW}${BOLD}  📋 Key Features:${NC}"
    echo -e "${WHITE}  1. Cluster Metrics${NC} - CPU, Memory, Containers"
    echo -e "${WHITE}  2. Applications${NC} - Running/finished jobs with progress"
    echo -e "${WHITE}  3. Nodes${NC} - NodeManager status & resources"
    echo -e "${WHITE}  4. Scheduler${NC} - Queue configuration & allocation"
    echo ""
    echo -e "${CYAN}${BOLD}  ⚙ How YARN Works:${NC}"
    echo -e "${GRAY}  Step 1: Client submits app → ResourceManager schedules${NC}"
    echo -e "${GRAY}  Step 2: ApplicationMaster launches in container${NC}"
    echo -e "${GRAY}  Step 3: AppMaster requests resources for tasks${NC}"
    echo -e "${GRAY}  Step 4: Tasks run in containers on NodeManagers${NC}"
    echo -e "${GRAY}  Step 5: Progress reported → Resources released when done${NC}"
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

show_datanode_guide() {
    clear
    print_banner
    echo -e "${GREEN}${BOLD}  ${SERVER} DATANODE UI - PORT 9864${NC}"
    print_divider
    echo ""
    echo -e "${CYAN}${BOLD}  ${NETWORK} URL: ${WHITE}http://localhost:9864${NC}"
    echo ""
    echo -e "${YELLOW}${BOLD}  📋 Key Features:${NC}"
    echo -e "${WHITE}  1. Storage Info${NC} - Capacity, usage, volumes"
    echo -e "${WHITE}  2. Blocks${NC} - Number of blocks stored"
    echo -e "${WHITE}  3. Logs${NC} - DataNode operations"
    echo ""
    echo -e "${CYAN}${BOLD}  ⚙ How DataNode Works:${NC}"
    echo -e "${GRAY}  Step 1: Registers with NameNode on startup${NC}"
    echo -e "${GRAY}  Step 2: Stores actual data blocks (128MB each)${NC}"
    echo -e "${GRAY}  Step 3: Sends heartbeat every 3 seconds${NC}"
    echo -e "${GRAY}  Step 4: Block report every 6 hours${NC}"
    echo -e "${GRAY}  Step 5: Handles read/write from clients${NC}"
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

show_architecture() {
    clear
    print_banner
    echo -e "${GREEN}${BOLD}  ${CLUSTER} HADOOP ARCHITECTURE${NC}"
    print_divider
    echo ""
    echo -e "${YELLOW}HDFS Architecture:${NC}"
    cat << "EOF"
    Client
      │
      ├─[metadata]──→ NameNode (master)
      │                   └─ manages file system
      │
      └─[data]──────→ DataNode (workers)
                          └─ store actual blocks
EOF
    echo ""
    echo -e "${YELLOW}YARN Architecture:${NC}"
    cat << "EOF"
    Client
      │
      └→ ResourceManager (master)
           ├→ ApplicationMaster
           │    └→ Task coordination
           │
           └→ NodeManager (workers)
                └→ Run containers
EOF
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

# ============================================================================
# SERVICE MANAGEMENT
# ============================================================================

start_services() {
    print_banner
    echo -e "${GREEN}${BOLD}  ${ROCKET} STARTING HADOOP SERVICES${NC}"
    echo ""
    print_divider

    source "$BASE_DIR/scripts/env-setup.sh"

    echo ""
    print_info "Starting HDFS..."
    $HADOOP_HOME/sbin/start-dfs.sh
    sleep 2

    print_info "Starting YARN..."
    $HADOOP_HOME/sbin/start-yarn.sh
    sleep 2

    echo ""
    print_success "Services started!"
    echo ""
    echo -e "${CYAN}${BOLD}  Running processes:${NC}"
    jps
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

stop_services() {
    print_banner
    echo -e "${RED}${BOLD}  ⏹ STOPPING HADOOP SERVICES${NC}"
    echo ""
    print_divider

    source "$BASE_DIR/scripts/env-setup.sh"

    echo ""
    print_info "Stopping YARN..."
    $HADOOP_HOME/sbin/stop-yarn.sh
    sleep 2

    print_info "Stopping HDFS..."
    $HADOOP_HOME/sbin/stop-dfs.sh
    sleep 2

    echo ""
    print_success "Services stopped!"
    echo ""
    jps
    echo ""
    print_divider
    read -p "  Press Enter to continue..."
}

# ============================================================================
# EXAMPLES MODULE
# ============================================================================

run_examples() {
    while true; do
        print_banner
        echo -e "${MAGENTA}${BOLD}  ${FIRE} HADOOP EXAMPLES${NC}"
        echo ""
        print_divider
        echo ""
        echo -e "${YELLOW}${BOLD}  Available Examples:${NC}"
        echo ""
        echo -e "${WHITE}  1) HDFS Basic Commands${NC}"
        echo -e "${GRAY}     └─ mkdir, put, get, ls, cat, rm${NC}"
        echo ""
        echo -e "${WHITE}  2) WordCount MapReduce${NC}"
        echo -e "${GRAY}     └─ Classic MapReduce example${NC}"
        echo ""
        echo -e "${WHITE}  3) Custom HDFS Operations${NC}"
        echo -e "${GRAY}     └─ Interactive HDFS playground${NC}"
        echo ""
        echo -e "${WHITE}  0) Back to Main Menu${NC}"
        echo ""
        echo -ne "${CYAN}${BOLD}  ${ARROW} Select: ${NC}"
        read -r ex_choice

        case $ex_choice in
            1) run_hdfs_examples ;;
            2) run_wordcount ;;
            3) custom_hdfs_ops ;;
            0) return ;;
            *) print_error "Invalid!"; sleep 2 ;;
        esac
    done
}

run_hdfs_examples() {
    clear
    print_banner
    echo -e "${CYAN}${BOLD}  ${FILE} HDFS BASIC COMMANDS${NC}"
    print_divider
    echo ""

    source "$BASE_DIR/scripts/env-setup.sh"

    echo -e "${YELLOW}Running HDFS examples...${NC}"
    echo ""

    echo -e "${CYAN}1. Creating directories${NC}"
    hdfs dfs -mkdir -p /user/hadoop/input
    hdfs dfs -mkdir -p /user/hadoop/output
    print_success "Directories created"
    echo ""

    echo -e "${CYAN}2. Uploading file${NC}"
    hdfs dfs -put "$BASE_DIR/data/input/sample-data.txt" /user/hadoop/input/
    print_success "File uploaded"
    echo ""

    echo -e "${CYAN}3. Listing files${NC}"
    hdfs dfs -ls /user/hadoop/input/
    echo ""

    echo -e "${CYAN}4. Viewing file content${NC}"
    hdfs dfs -cat /user/hadoop/input/sample-data.txt | head -n 5
    echo ""

    echo -e "${CYAN}5. Checking storage${NC}"
    hdfs dfs -du -h /user/hadoop/input/
    echo ""

    print_success "Examples completed!"
    print_divider
    read -p "  Press Enter to continue..."
}

run_wordcount() {
    clear
    print_banner
    echo -e "${CYAN}${BOLD}  ${CHART} WORDCOUNT MAPREDUCE${NC}"
    print_divider
    echo ""

    source "$BASE_DIR/scripts/env-setup.sh"

    echo -e "${YELLOW}Running WordCount...${NC}"
    echo ""

    # Prepare input
    hdfs dfs -mkdir -p /user/hadoop/wordcount/input
    hdfs dfs -put "$BASE_DIR/data/input/word-count-input.txt" /user/hadoop/wordcount/input/ 2>/dev/null

    # Run MapReduce
    echo -e "${CYAN}Executing MapReduce job...${NC}"
    hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
        wordcount /user/hadoop/wordcount/input /user/hadoop/wordcount/output

    echo ""
    echo -e "${CYAN}Results:${NC}"
    hdfs dfs -cat /user/hadoop/wordcount/output/part-r-00000
    echo ""

    print_success "WordCount completed!"
    print_divider
    read -p "  Press Enter to continue..."
}

custom_hdfs_ops() {
    clear
    print_banner
    echo -e "${CYAN}${BOLD}  ${GEAR} CUSTOM HDFS OPERATIONS${NC}"
    print_divider
    echo ""

    source "$BASE_DIR/scripts/env-setup.sh"

    echo -ne "${YELLOW}Enter HDFS command (e.g., ls /): ${NC}"
    read -r hdfs_cmd

    echo ""
    hdfs dfs -${hdfs_cmd}
    echo ""

    print_divider
    read -p "  Press Enter to continue..."
}

# ============================================================================
# MAIN MENU
# ============================================================================

main_menu() {
    while true; do
        print_banner

        echo -e "${YELLOW}${BOLD}  ${ROCKET} MAIN MENU${NC}"
        echo ""
        print_divider
        echo ""
        echo -e "${WHITE}  ${BOLD}[SETUP]${NC}"
        echo -e "${WHITE}  1) ${GEAR} Install & Configure Hadoop${NC}"
        echo -e "${WHITE}  2) ${DATABASE} Setup Database Integration${NC}"
        echo ""
        echo -e "${WHITE}  ${BOLD}[SERVICES]${NC}"
        echo -e "${WHITE}  3) ${ROCKET} Start Hadoop Services${NC}"
        echo -e "${WHITE}  4) ⏹  Stop Hadoop Services${NC}"
        echo ""
        echo -e "${WHITE}  ${BOLD}[MONITORING]${NC}"
        echo -e "${WHITE}  5) ${NETWORK} Web Dashboard Guide${NC}"
        echo -e "${WHITE}  6) ${CHART} Service Status${NC}"
        echo ""
        echo -e "${WHITE}  ${BOLD}[EXAMPLES]${NC}"
        echo -e "${WHITE}  7) ${FIRE} Run HDFS & MapReduce Examples${NC}"
        echo ""
        echo -e "${WHITE}  0) ${CROSS} Exit${NC}"
        echo ""
        print_divider
        echo ""
        echo -ne "${CYAN}${BOLD}  ${ARROW} Select option: ${NC}"

        read -r choice

        case $choice in
            1) install_hadoop ;;
            2) setup_database ;;
            3) start_services ;;
            4) stop_services ;;
            5) show_web_dashboard ;;
            6)
                clear
                print_banner
                echo -e "${CYAN}${BOLD}Service Status:${NC}"
                echo ""
                jps
                echo ""
                print_divider
                read -p "Press Enter to continue..."
                ;;
            7) run_examples ;;
            0)
                clear
                echo ""
                echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
                echo -e "${CYAN}${BOLD}║                                                            ║${NC}"
                echo -e "${CYAN}${BOLD}║  ${GREEN}${ROCKET} Thank you for using Hadoop Master Control! ${ROCKET}${CYAN}     ║${NC}"
                echo -e "${CYAN}${BOLD}║                                                            ║${NC}"
                echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
                echo ""
                echo -e "${MAGENTA}${BOLD}       ╔═══════════════════════════════════════════════╗${NC}"
                echo -e "${MAGENTA}${BOLD}       ║  ${STAR}${FIRE} Crafted with ${RED}♥${MAGENTA} by ${WHITE}DevNoLife${MAGENTA} ${FIRE}${STAR}    ║${NC}"
                echo -e "${MAGENTA}${BOLD}       ║  ${GRAY}github.com/devnolife                  ${MAGENTA}║${NC}"
                echo -e "${MAGENTA}${BOLD}       ╚═══════════════════════════════════════════════╝${NC}"
                echo ""
                echo -e "${GRAY}  Big Data never sleeps... Keep Hadooping! ${ROCKET}${NC}"
                echo ""
                exit 0
                ;;
            *)
                print_error "Invalid option!"
                sleep 2
                ;;
        esac
    done
}

# ============================================================================
# ENTRY POINT
# ============================================================================

trap 'echo -e "\n${RED}${BOLD}Interrupted!${NC}"; exit 1' INT

main_menu
