from datetime import datetime, timedelta
from lib.nextcloud import nextcloud
import os
import config
import subprocess
import tarfile

class archive:

    @staticmethod
    def database(site_info, filename):

        command = [
            'mysqldump',
            '--host=' + site_info['db_hostname'],
            '--user=' + site_info['db_username'],
            '--password=' + site_info['db_password'],
            site_info['db_name']
        ]

        try:
            with open(filename + '.sql', 'w') as backup_file:
                subprocess.run(command, stdout=backup_file, check=True)
            nextcloud.notification(f"Dump {filename}.sql: OK.")
        except subprocess.CalledProcessError as e:
            nextcloud.notification(f"Erreur lors de la sauvegarde de {filename}.sql: {e}")

    @staticmethod
    def files(site_info, filename):
        try:
            with tarfile.open(filename+'.tar.gz', 'w:gz') as archive_file:
                archive_file.add(site_info['file_path'], arcname=filename)
            nextcloud.notification(f"Archive {filename}.tar.gz: OK.")
        except Exception as e:
            nextcloud.notification(f"Une erreur s'est produite : {e}")

    @staticmethod
    def delete(site_name, extension):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        formatted_previous_date = previous_date.strftime('%Y-%m-%d')
        filename = f"{site_name}-{formatted_previous_date}.{extension}"

        if os.path.exists(filename):
            os.remove(filename)
            nextcloud.notification(f"Deleted {filename}: OK")
        else:
            nextcloud.notification(f"{filename} does not exist")

    @staticmethod
    def delete_remotely(site_name):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=8)
        formatted_previous_date = previous_date.strftime('%Y-%m-%d')
        filename = f"{site_name}-{formatted_previous_date}.*"
        remote_path = f"{config.ssh_path}{filename}"

        # Command to list files
        command_ls = f'ssh -p {config.ssh_port} {config.ssh_username}@{config.ssh_hostname} "ls {remote_path}"'

        try:
            result = subprocess.run(command_ls, shell=True)

            if result.returncode == 0:
                # Files exist, proceed to delete
                command_rm = f'ssh -p {config.ssh_port} {config.ssh_username}@{config.ssh_hostname} "rm {remote_path}"'
                subprocess.run(command_rm, shell=True, check=True)
                nextcloud.notification(f"Delete remotely {remote_path}: OK.")
            else:
                nextcloud.notification(f"No files to delete for {filename}.")
        except subprocess.CalledProcessError as e:
            nextcloud.notification(f"Error checking or deleting files: {e}")
