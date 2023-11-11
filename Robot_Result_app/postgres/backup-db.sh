#!/bin/bash
# Backup script for PostgreSQL

# Timestamp for backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create a backup
pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > /backups/db_backup_$TIMESTAMP.sql
