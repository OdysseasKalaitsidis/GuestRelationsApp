#!/bin/bash
# Quick Start Migration Script for MySQL to Supabase

set -e  # Exit on any error

echo "🚀 Starting MySQL to Supabase Migration"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check for mysqldump
    if ! command -v mysqldump &> /dev/null; then
        print_error "mysqldump not found. Please install MySQL client."
        exit 1
    fi
    
    # Check for pgloader
    if ! command -v pgloader &> /dev/null; then
        print_warning "pgloader not found. Install with:"
        echo "  Ubuntu/Debian: sudo apt-get install pgloader"
        echo "  macOS: brew install pgloader"
        echo "  Or download from: https://github.com/dimitri/pgloader"
    fi
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3."
        exit 1
    fi
    
    print_success "Dependencies check completed"
}

# Create migration directory structure
setup_migration_structure() {
    print_status "Setting up migration directory structure..."
    
    mkdir -p migration/{scripts,config,docs,backups}
    
    print_success "Migration structure created"
}

# Export MySQL schema and data
export_mysql_data() {
    print_status "Exporting MySQL data..."
    
    # Get MySQL credentials from environment or prompt
    MYSQL_USER=${MYSQL_USER:-""}
    MYSQL_PASSWORD=${MYSQL_PASSWORD:-""}
    MYSQL_HOST=${MYSQL_HOST:-""}
    MYSQL_DATABASE=${MYSQL_DATABASE:-""}
    
    if [ -z "$MYSQL_USER" ]; then
        read -p "Enter MySQL username: " MYSQL_USER
    fi
    
    if [ -z "$MYSQL_PASSWORD" ]; then
        read -s -p "Enter MySQL password: " MYSQL_PASSWORD
        echo
    fi
    
    if [ -z "$MYSQL_HOST" ]; then
        read -p "Enter MySQL host: " MYSQL_HOST
    fi
    
    if [ -z "$MYSQL_DATABASE" ]; then
        read -p "Enter MySQL database name: " MYSQL_DATABASE
    fi
    
    # Export schema only
    print_status "Exporting schema..."
    mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" \
        --no-data --routines --triggers "$MYSQL_DATABASE" \
        > migration/backups/schema_only.sql
    
    # Export data only
    print_status "Exporting data..."
    mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" \
        --no-create-info --no-create-db --no-create-table "$MYSQL_DATABASE" \
        > migration/backups/data_only.sql
    
    # Export complete backup
    print_status "Creating complete backup..."
    mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" \
        --databases "$MYSQL_DATABASE" \
        > migration/backups/complete_backup.sql
    
    print_success "MySQL data exported successfully"
}

# Setup Supabase project
setup_supabase() {
    print_status "Setting up Supabase project..."
    
    echo "Please follow these steps:"
    echo "1. Go to https://supabase.com"
    echo "2. Create a new project"
    echo "3. Note down your project details:"
    echo "   - Project URL"
    echo "   - Database password"
    echo "   - Anon key"
    echo "   - Service role key"
    echo ""
    echo "After creating the project, run the setup script:"
    echo "  migration/scripts/03_supabase_setup.sql"
    echo ""
    
    read -p "Press Enter when you've created the Supabase project..."
    
    print_success "Supabase project setup instructions provided"
}

# Update backend code
update_backend_code() {
    print_status "Updating backend code for Supabase..."
    
    # Copy updated requirements
    if [ -f "migration/requirements-supabase.txt" ]; then
        cp migration/requirements-supabase.txt backend/requirements.txt
        print_success "Updated requirements.txt"
    fi
    
    # Copy updated db.py
    if [ -f "migration/db_supabase.py" ]; then
        cp migration/db_supabase.py backend/db.py
        print_success "Updated db.py"
    fi
    
    print_success "Backend code updated"
}

# Run migration with pgloader
run_pgloader_migration() {
    print_status "Running pgloader migration..."
    
    # Get Supabase credentials
    SUPABASE_HOST=${SUPABASE_HOST:-""}
    SUPABASE_PASSWORD=${SUPABASE_PASSWORD:-""}
    
    if [ -z "$SUPABASE_HOST" ]; then
        read -p "Enter Supabase host (e.g., db.PROJECT_ID.supabase.co): " SUPABASE_HOST
    fi
    
    if [ -z "$SUPABASE_PASSWORD" ]; then
        read -s -p "Enter Supabase database password: " SUPABASE_PASSWORD
        echo
    fi
    
    # Create pgloader command file
    cat > migration/pgloader.load << EOF
LOAD DATABASE
    FROM mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST/$MYSQL_DATABASE
    INTO postgresql://postgres:$SUPABASE_PASSWORD@$SUPABASE_HOST:5432/postgres

WITH include drop, create tables, create indexes, reset sequences,
     workers = 8, concurrency = 1,
     multiple readers per thread, rows per range = 50000

SET PostgreSQL PARAMETERS
    maintenance_work_mem to '128 MB',
    work_mem to '12 MB',
    search_path to 'public'

SET MySQL PARAMETERS
    net_read_timeout = '600',
    net_write_timeout = '600'

EXCLUDING TABLE NAMES MATCHING 'migrations', 'schema_migrations'

ALTER SCHEMA 'mysql' RENAME TO 'public';
EOF
    
    # Run pgloader
    if command -v pgloader &> /dev/null; then
        print_status "Running pgloader migration..."
        pgloader migration/pgloader.load
        print_success "pgloader migration completed"
    else
        print_warning "pgloader not available. Please run migration manually:"
        echo "  pgloader migration/pgloader.load"
    fi
}

# Verify migration
verify_migration() {
    print_status "Verifying migration..."
    
    echo "Please run the verification script in Supabase SQL Editor:"
    echo "  migration/scripts/04_verify_migration.sql"
    echo ""
    echo "Or run these commands to verify:"
    echo "1. Check if all tables exist"
    echo "2. Verify row counts match"
    echo "3. Test foreign key relationships"
    echo "4. Check sequences are set correctly"
}

# Main execution
main() {
    echo "MySQL to Supabase Migration Quick Start"
    echo "======================================"
    echo ""
    
    check_dependencies
    setup_migration_structure
    export_mysql_data
    setup_supabase
    update_backend_code
    run_pgloader_migration
    verify_migration
    
    echo ""
    print_success "Migration setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Run the Supabase setup script"
    echo "2. Verify the migration"
    echo "3. Update environment variables"
    echo "4. Test the application"
    echo "5. Deploy to production"
    echo ""
    echo "For detailed instructions, see: migration/README.md"
}

# Run main function
main "$@"
