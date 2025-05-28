#!/bin/bash

files=(
    supervisord.conf
    manage.py
    config/wsgi.py
    config/asgi.py
    config/celery.py
    pytest.ini
)
BACKUP_DIR="backup"

mkdir -p "$BACKUP_DIR"

for file in "${files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "Processing file: $file"
        backup_file="$BACKUP_DIR/$(basename "$file")"
        cp "$file" "$backup_file"
        if sed -i "s/\.development/\.production/g" "$file"; then
            echo "Successfully replaced '.development' with '.production' in $file"
            # Optionally remove the backup if the operation was successful
            # rm "$backup_file"
        else
            echo "Error occurred while processing $file. Original file preserved in $backup_file"
        fi
        if sed -i "s/\development/\production/g" "$file"; then
            echo "Successfully replaced 'development' with 'production' in $file"
            # Optionally remove the backup if the operation was successful
            # rm "$backup_file"
        fi
    else
        echo "File not found: $file"
    fi
done
