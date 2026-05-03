#!/bin/bash

##############################
# PostgreSQL Docker Backup Script
##############################

# ----------------------------
# Configuration Variables
# ----------------------------

# Docker container name running PostgreSQL
CONTAINER_NAME="indrz_db"  # <-- Replace with your container name

# Name of the PostgreSQL database to back up
DB_NAME="indrzaau"

# Directory inside the Docker container where backups will be stored
CONTAINER_BACKUP_DIR="/scripts/backup"

# Directory on the host machine where you want to store the backups
HOST_BACKUP_DIR="/srv/data/backup"    # <-- Replace with your desired host backup directory

# Log file path
LOG_FILE="/var/log/postgres_backup.log"

# Number of days to keep backups
RETENTION_DAYS=7

# ----------------------------
# Derived Variables
# ----------------------------

# Current date in YYYY_MM_DD format
CURRENT_DATE=$(date +%Y_%m_%d)

# Backup file name
BACKUP_FILE="indrz_db_backup_${CURRENT_DATE}.backup"

# Full path for the backup file inside the container
CONTAINER_BACKUP_PATH="${CONTAINER_BACKUP_DIR}/${BACKUP_FILE}"

# Full path for the backup file on the host
HOST_BACKUP_PATH="${HOST_BACKup_DIR}/${BACKUP_FILE}"

# ----------------------------
# Logging Function
# ----------------------------

log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') : $1" >> "$LOG_FILE"
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

# Clean up old backups on the host
find "$HOST_BACKUP_DIR" -type f -name "indrz_db_backup_*.backup" -mtime +$RETENTION_DAYS -exec rm {} \;
if [ $? -eq 0 ]; then
    log_message "Old backups older than $RETENTION_DAYS days have been removed."
else
    log_message "WARNING: Failed to remove old backups."
fi

log_message "Backup process completed successfully."

exit 0
