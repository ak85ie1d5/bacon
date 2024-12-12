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
                subprocess.call(command, stdout=backup_file)
            nextcloud.notification("Dump {}.sql: OK.".format(filename))
        except subprocess.CalledProcessError as e:
            nextcloud.notification("Erreur lors de la sauvegarde de {}.sql: {}".format(filename, e))

    @staticmethod
    def files(site_info, filename):
        try:
            with tarfile.open(filename+'.tar.gz', 'w:gz') as archive_file:
                archive_file.add(site_info['file_path'], arcname=filename)
            nextcloud.notification("Archive {}.tar.gz: OK.".format(filename))
        except Exception as e:
            nextcloud.notification("Une erreur s'est produite : {}".format(e))

    @staticmethod
    def delete(site_name, extension):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        formatted_previous_date = previous_date.strftime('%Y-%m-%d')
        filename = "{}-{}.{}".format(site_name, formatted_previous_date, extension)

        if os.path.exists(filename):
            os.remove(filename)
            nextcloud.notification("Deleted {}: OK".format(filename))
        else:
            nextcloud.notification("{} does not exist".format(filename))

    @staticmethod
    def delete_remotely(site_name):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=8)
        formatted_previous_date = previous_date.strftime('%Y-%m-%d')
        filename = "{}-{}.*".format(site_name, formatted_previous_date)
        remote_path = "{}{}".format(config.ssh_path, filename)

        # Command to list files
        command_ls = 'ssh -p {} {}@{} "ls {}"'.format(config.ssh_port, config.ssh_username, config.ssh_hostname, remote_path)

        try:
            result = subprocess.call(command_ls, shell=True)

            if result == 0:
                # Files exist, proceed to delete
                command_rm = 'ssh -p {} {}@{} "rm {}"'.format(config.ssh_port, config.ssh_username, config.ssh_hostname, remote_path)
                subprocess.call(command_rm, shell=True)
                nextcloud.notification("Delete remotely {}: OK.".format(remote_path))
            else:
                nextcloud.notification("No files to delete for {}.".format(filename))
        except subprocess.CalledProcessError as e:
            nextcloud.notification("Error checking or deleting files: {}".format(e))
