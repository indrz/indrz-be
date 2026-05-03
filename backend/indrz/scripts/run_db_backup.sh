#!/bin/bash

##############################
# Nightly Backup Script
##############################

# ----------------------------
# Configuration Variables
# ----------------------------

# Docker container name running PostgreSQL
CONTAINER_NAME="indrz_db"  # <-- Replace with your container name

# Name of the PostgreSQL database to back up
DB_NAME="indrzwu"

# Directory inside the Docker container where backups will be stored
CONTAINER_BACKUP_DIR="/scripts/backup"

# Directory on the host machine where you want to store the backups
HOST_BACKUP_DIR="/srv/data/backup"    # <-- Replace with your desired host backup directory

# GeoServer data directory on the host machine
GEOSERVER_DATA_DIR="/srv/data/geoserver-data"

# Log file path
LOG_FILE="/srv/data/logs/postgres_geoserver_backup.log"

# Number of days to keep backups
RETENTION_DAYS=7

# ----------------------------
# Derived Variables
# ----------------------------

# Current date in YYYY_MM_DD format
CURRENT_DATE=$(date +%Y_%m_%d)

# Backup file name
BACKUP_FILE="indrz_${DB_NAME}_backup_${CURRENT_DATE}.backup"

# Full path for the backup file inside the container
CONTAINER_BACKUP_PATH="${CONTAINER_BACKUP_DIR}/${BACKUP_FILE}"

# Full path for the backup file on the host
HOST_BACKUP_PATH="${HOST_BACKUP_DIR}/${BACKUP_FILE}"

# GeoServer backup file name
GEOSERVER_BACKUP_FILE="geoserver-data_backup_${CURRENT_DATE}.tar.gz"

# Full path for the GeoServer backup file on the host
GEOSERVER_BACKUP_PATH="${HOST_BACKUP_DIR}/${GEOSERVER_BACKUP_FILE}"

# ----------------------------
# Logging Function
# ----------------------------

log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') : $1" >> "$LOG_FILE"
}

cleanup_old_backups() {
    local pattern="$1"
    local label="$2"

    if find "$HOST_BACKUP_DIR" -type f -name "$pattern" -mtime +"$RETENTION_DAYS" -exec rm {} \;; then
        log_message "Old ${label} backups older than $RETENTION_DAYS days have been removed."
    else
        log_message "WARNING: Failed to remove old ${label} backups."
    fi
}

# ----------------------------
# Start Backup Process
# ----------------------------

log_message "Starting backup for database '$DB_NAME' in container '$CONTAINER_NAME'."

# Ensure the host backup directory exists
if [ ! -d "$HOST_BACKUP_DIR" ]; then
    mkdir -p "$HOST_BACKUP_DIR"
    if [ $? -ne 0 ]; then
        log_message "ERROR: Failed to create host backup directory '$HOST_BACKUP_DIR'."
        exit 1
    fi
    log_message "Created host backup directory '$HOST_BACKUP_DIR'."
fi

# Ensure the backup directory exists inside the container and is owned by postgres
docker exec "$CONTAINER_NAME" bash -c "mkdir -p '$CONTAINER_BACKUP_DIR' && chown postgres:postgres '$CONTAINER_BACKUP_DIR'"
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to ensure backup directory '$CONTAINER_BACKUP_DIR' inside container."
    exit 1
fi

# Perform the backup using pg_dump as the postgres user
docker exec -u postgres "$CONTAINER_NAME" bash -c "pg_dump -Fc -f '$CONTAINER_BACKUP_PATH' -d '$DB_NAME'"
if [ $? -ne 0 ]; then
    log_message "ERROR: pg_dump failed for database '$DB_NAME'."
    exit 1
fi

log_message "pg_dump completed successfully for database '$DB_NAME'."

# Copy the backup file from the container to the host
docker cp "${CONTAINER_NAME}:${CONTAINER_BACKUP_PATH}" "${HOST_BACKUP_DIR}/"
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to copy backup file from container to host."
    exit 1
fi

log_message "Backup file copied to host at '$HOST_BACKUP_PATH'."

# Optionally, remove the backup file from the container to save space
docker exec "$CONTAINER_NAME" rm -f "$CONTAINER_BACKUP_PATH"
if [ $? -ne 0 ]; then
    log_message "WARNING: Failed to remove backup file from container."
else
    log_message "Backup file removed from container."
fi

# Create a compressed archive of the GeoServer data directory
if [ ! -d "$GEOSERVER_DATA_DIR" ]; then
    log_message "ERROR: GeoServer data directory '$GEOSERVER_DATA_DIR' does not exist."
    exit 1
fi

tar -czf "$GEOSERVER_BACKUP_PATH" -C "$(dirname "$GEOSERVER_DATA_DIR")" "$(basename "$GEOSERVER_DATA_DIR")"
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to create GeoServer backup archive '$GEOSERVER_BACKUP_PATH'."
    exit 1
fi

log_message "GeoServer data backup created at '$GEOSERVER_BACKUP_PATH'."

# Clean up old backups on the host
cleanup_old_backups "indrz_db_backup_*.backup" "database"
cleanup_old_backups "geoserver-data_backup_*.tar.gz" "GeoServer data"

log_message "Backup process completed successfully."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -f "${SCRIPT_DIR}/backup.env" ]; then
    log_message "ERROR: ${SCRIPT_DIR}/backup.env not found."
    exit 1
fi
# shellcheck source=backup.env
source "${SCRIPT_DIR}/backup.env"

LOCAL_FILE="$BACKUP_FILE"
REMOTE_DIR="backups"
LOG_FILE="/srv/log/ftps_upload.log"

echo "Starting FTP upload of backup file '${BACKUP_FILE}'..."

lftp <<EOF
set net:max-retries 3
set net:timeout 20
set ftp:passive-mode true
set ssl:verify-certificate false
set ftp:ssl-allow true
set ftp:ssl-force true
set ftp:ssl-protect-data yes
open -u "${FTP_USER}","${FTP_PASS}" -p 21 ${FTP_HOST}
put -O ${REMOTE_DIR} ${HOST_BACKUP_PATH}
bye
EOF

if [ $? -ne 0 ]; then
    log_message "ERROR: FTP upload of '${BACKUP_FILE}' failed."
    exit 1
fi

log_message "FTP upload of '${BACKUP_FILE}' to '${FTP_HOST}:${REMOTE_DIR}' completed successfully."

