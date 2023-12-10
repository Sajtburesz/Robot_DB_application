#!/bin/bash

# Start PostgreSQL server in the background
if [ -d /db_base/base.sql ]; then
    echo "/db_base/base.sql is a directory, expected a file. Creating a new file."
    rm -rf /db_base/base.sql
    touch /db_base/base.sql
fi
echo "Starting PostgreSQL server..."
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h localhost -U "$POSTGRES_USER"; do
  sleep 1
done

# Check for existing backup and load it
if [ -f /db_base/base.sql ]; then
    echo "Loading previous state of the database."
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f /db_base/base.sql
else
    echo "No backup found. Starting with a fresh database."

    # Setup user
    psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
        CREATE DATABASE "$POSTGRES_DB";
        CREATE USER "$POSTGRES_USER" WITH PASSWORD '$POSTGRES_PASSWORD';
        GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
        \c "$POSTGRES_DB";
        GRANT USAGE ON SCHEMA public TO "$POSTGRES_USER";
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$POSTGRES_USER";
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "$POSTGRES_USER";
        GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO "$POSTGRES_USER";
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "$POSTGRES_USER";
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "$POSTGRES_USER";
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO "$POSTGRES_USER";
        GRANT CREATE ON SCHEMA public TO "$POSTGRES_USER";
EOSQL
fi

backup_db() {
    # Create a backup
    pg_dump -U $POSTGRES_USER $POSTGRES_DB > /db_backup/backup.sql 2>/db_backup/backup.log

    if [ $? -eq 0 ]; then
        echo "Backup successful."
        exit 0
    else
        echo "Backup failed. Check /db_backup/backup.log for errors."
        exit 1
    fi

}


trap 'backup_db' SIGTERM

wait
