import config
from lib.nextcloud import nextcloud
import os
import subprocess
import time

class upload:
    # Upload files to the remote server with `rsync`.
    @staticmethod
    def rsync(filename, extension):
        pwd = os.environ["PWD"]

        commande_rsync = 'rsync -av -e "ssh -p {}" {}/{}.{} {}@{}:{}'.format(config.ssh_port, pwd, filename, extension, config.ssh_username, config.ssh_hostname, config.ssh_path)
        result = subprocess.call(commande_rsync, shell=True)

        nextcloud.notification('Upload {}.{} status: {}'.format(filename, extension, result))
