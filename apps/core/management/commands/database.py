from datetime import datetime
from pathlib import Path
import subprocess
import logging
import os
import re

from django.core.management.base import BaseCommand

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config.settings.production import env

logger = logging.getLogger("core")


# Directories
SCRIPT_DIR = Path(__file__).resolve().parent
BACKUP_DIR = f"{SCRIPT_DIR}/backups"
CREDENTIALS_DIR = f"{BACKUP_DIR}/credentials"

# PostgreSQL configuration
PG_HOST = env.get_value("FARABIN_DB_HOST")
PG_PORT = env.get_value("FARABIN_DB_PORT")
PG_DATABASE = env.get_value("FARABIN_DB_NAME")
PG_USER = env.get_value("FARABIN_DB_USER")
PG_PASSWORD = env.get_value("FARABIN_DB_PASSWORD")


# Google Drive configuration
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = f"{CREDENTIALS_DIR}/credentials.json"
TOKEN_FILE = f"{CREDENTIALS_DIR}/token.json"
GDRIVE_FOLDER_ID = env.get_value("FARABIN_DB_BACKUP_FOLDER_ID")


class Command(BaseCommand):
    help = 'Creates a "backup" from database and uploads it to Drive/ Downloads a backup from Drive and "restore" it to database'

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["backup", "restore"],
            help='Action to perform: "backup" to create and upload a backup, "restore" to download and restore the latest backup.',
        )

    def handle(self, *args, **kwargs):
        action = kwargs["action"]
        logger.info(f"Starting {action} process...")

        os.makedirs(BACKUP_DIR, exist_ok=True)
        os.makedirs(CREDENTIALS_DIR, exist_ok=True)

        match action:
            case "backup":
                self.job()
                logger.info("Backup scheduler started. Waiting for next run...")
                self.stdout.write(
                    self.style.SUCCESS("Successfully created and uploaded a backup.")
                )
            case "restore":
                self.restore()
                logger.info("Backup downloaded and restored successfully.")
                self.stdout.write(
                    self.style.SUCCESS("Successfully downloaded and restored a backup.")
                )
            case _:
                logger.error("Invalid action. Please use 'backup' or 'restore'.")

    def job(self):
        """Main job to backup PostgreSQL database and upload to Google Drive."""
        logger.info("Starting backup job...")
        try:
            drive_service = self.setup_google_drive()
            backup_file = self.backup_postgres()
            self.upload_to_gdrive(backup_file, drive_service)
            self.cleanup_backup(backup_file)
            logger.info("Backup job completed successfully.")
        except Exception as e:
            logger.error(f"Backup job failed: {e}")

    def setup_google_drive(self):
        """Authenticate and set up Google Drive API client."""
        try:
            creds = None
            if os.path.exists(TOKEN_FILE):
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
                with open(TOKEN_FILE, "w") as token:
                    token.write(creds.to_json())
            return build("drive", "v3", credentials=creds)
        except Exception as e:
            logger.error(f"Failed to set up Google Drive: {e}")
            raise

    def backup_postgres(self):
        """Create a PostgreSQL database backup using pg_dump."""
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(
                BACKUP_DIR, f"backup_{PG_DATABASE}_{timestamp}.sql"
            )

            # Set environment variable for pg_dump password
            os.environ["PGPASSWORD"] = PG_PASSWORD

            # Run pg_dump command
            cmd = [
                "pg_dump",
                "-h",
                PG_HOST,
                "-p",
                PG_PORT,
                "-U",
                PG_USER,
                "-d",
                PG_DATABASE,
                "-f",
                backup_file,
            ]
            subprocess.run(cmd, check=True)
            logger.info(f"Backup created: {backup_file}")
            return backup_file
        except subprocess.CalledProcessError as e:
            logger.error(f"pg_dump failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
        finally:
            # Clear password from environment
            os.environ.pop("PGPASSWORD", None)

    def upload_to_gdrive(self, backup_file, drive_service):
        """Upload the backup file to Google Drive."""
        try:
            file_metadata = {
                "name": os.path.basename(backup_file),
                "parents": [GDRIVE_FOLDER_ID],
            }
            media = MediaFileUpload(backup_file)
            file = (
                drive_service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            logger.info(
                f"Uploaded to Google Drive: {backup_file}, File ID: {file.get('id')}"
            )
        except Exception as e:
            logger.error(f"Upload to Google Drive failed: {e}")
            raise

    def cleanup_backup(self, backup_file):
        """Remove the local backup file after upload."""
        try:
            os.remove(backup_file)
            logger.info(f"Deleted local backup: {backup_file}")
        except Exception as e:
            logger.error(f"Failed to delete local backup: {e}")

    def get_latest_backup(self, drive_service):
        """Find the latest backup file in Google Drive."""
        try:
            # List files in the specified Google Drive folder
            query = f"'{GDRIVE_FOLDER_ID}' in parents and mimeType='application/sql'"
            results = (
                drive_service.files()
                .list(
                    q=query,
                    fields="files(id, name, createdTime)",
                    orderBy="createdTime desc",
                )
                .execute()
            )
            files = results.get("files", [])

            if not files:
                raise Exception("No backup files found in Google Drive folder.")

            # Find the latest file based on the timestamp in the filename
            # Default to the first file (most recent by createdTime)
            latest_file = files[0]
            latest_timestamp = None
            for file in files:
                # Extract timestamp from filename (e.g., backup_<db>_20250417_123456.sql)
                match = re.search(r"(\d{8}_\d{6})\.sql$", file["name"])
                if match:
                    timestamp = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
                    if latest_timestamp is None or timestamp > latest_timestamp:
                        latest_timestamp = timestamp
                        latest_file = file

            logger.info(
                f"Latest backup found: {latest_file['name']}, File ID: {latest_file['id']}"
            )
            return latest_file
        except Exception as e:
            logger.error(f"Failed to find latest backup: {e}")
            raise

    def download_backup(self, drive_service, file_id, destination_path):
        """Download the backup file from Google Drive."""
        try:
            request = drive_service.files().get_media(fileId=file_id)
            with open(destination_path, "wb") as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    logger.info(f"Download progress: {int(status.progress() * 100)}%")
            logger.info(f"Backup downloaded to: {destination_path}")
        except Exception as e:
            logger.error(f"Failed to download backup: {e}")
            raise

    def restore_postgres(self, backup_file):
        """Restore the PostgreSQL database from the backup file."""
        try:
            # Optionally drop and recreate the database (requires superuser privileges)
            # Comment out if you only want to restore tables without dropping the database
            # logger.info(f"Dropping database {PG_DATABASE}...")
            # os.environ['PGPASSWORD'] = PG_PASSWORD
            # drop_cmd = [
            #     'dropdb',
            #     '-h', PG_HOST,
            #     '-p', PG_PORT,
            #     '-U', PG_USER,
            #     PG_DATABASE
            # ]
            # subprocess.run(drop_cmd, check=True, stderr=subprocess.PIPE)

            # logger.info(f"Creating database {PG_DATABASE}...")
            # create_cmd = [
            #     'createdb',
            #     '-h', PG_HOST,
            #     '-p', PG_PORT,
            #     '-U', PG_USER,
            #     PG_DATABASE
            # ]
            # subprocess.run(create_cmd, check=True, stderr=subprocess.PIPE)

            # Restore the database using psql
            logger.info(f"Restoring database from {backup_file}...")
            restore_cmd = [
                "psql",
                "-h",
                PG_HOST,
                "-p",
                PG_PORT,
                "-U",
                PG_USER,
                "-d",
                PG_DATABASE,
                "-f",
                backup_file,
            ]
            subprocess.run(restore_cmd, check=True, stderr=subprocess.PIPE)
            logger.info("Database restored successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {e.stderr.decode()}")
            raise
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
        finally:
            os.environ.pop("PGPASSWORD", None)

    def restore(self):
        """Main method to restore the latest backup from Google Drive."""
        logger.info("Starting restore process...")
        try:
            drive_service = self.setup_google_drive()
            latest_file = self.get_latest_backup(drive_service)

            # Download the latest backup
            local_backup_file = os.path.join(BACKUP_DIR, latest_file["name"])
            self.download_backup(drive_service, latest_file["id"], local_backup_file)

            # Restore the database
            self.restore_postgres(local_backup_file)

            # Clean up the downloaded file
            self.cleanup_backup(local_backup_file)
            logger.info("Restore process completed successfully.")
        except Exception as e:
            logger.error(f"Restore process failed: {e}")
