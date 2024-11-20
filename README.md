# MySQL Backup and Restore UI 

This service allows you to easily and efficiently back up and restore MySQL databases. It can be used to create backups of MySQL databases and restore them from backup files.

## Key Features

1. **MySQL Database Backup**:
   - Perform a full backup of a MySQL database in SQL format.
   - Specify the source host (localhost or custom host).
   - Includes a separate SQL configuration file for backup.
   
2. **MySQL Database Restore**:
   - Restore a MySQL database from a backup SQL file.
   - Specify the destination host (localhost or remote host).
   
3. **Select Backup File**:
   - Upload the SQL backup file to restore through a web interface.

4. **Web Interface**:
   - A simple HTML user interface that allows you to easily perform backup and restore operations.

## Prerequisites

- **MySQL** or **MariaDB** must be installed and running on the server.
- Database access with sufficient permissions to perform backups and restores.
- **docker** (https://docs.docker.com/engine/install/) and **docker-compose** (https://docs.docker.com/compose/install/) installed on your system

## How to Use

1. **Backup Configuration**:
   - Choose the host from which to perform the backup (localhost or custom host).
   - Provide the MySQL username and password.
   - Specify the backup filename (default: `backup-alldb.sql`) and the configuration file (default: `backup-alldb-config.sql`).
   - Click the "Backup" button to perform the backup. 
   - Your backup will be in /data dir 

2. **Restore Backup**:
   - Choose the destination host (localhost or remote host).
   - Provide the MySQL username and password.
   - Select the backup file to restore from /data dir 
   - Click the "Restore" button to perform the restore. 

3. **View Available Backups**:
   - Existing backups plced in /data dir can be viewed in the "Available Backups" section.

## Endpoints

The service exposes the following endpoints for backup and restore operations:

- **POST /backup**: Perform a MySQL database backup.
- **POST /restore**: Restore a MySQL database from a backup file.
- **GET /list-backups**: Retrieve the list of available backups.


## How to Run the Service
1. Clone the repository
```bash
git clone https://github.com/lm2git/mysql-backup-restore-ui.git
cd mysql-backup-restore-ui
docker-compose up --build -d 
```
## How to remove Service 
```bash
docker-compose down -v
```