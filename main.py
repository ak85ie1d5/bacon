#/usr/bin/env python3
import argparse
import subprocess
import os
import tarfile
from datetime import datetime

# Import the configuration
import config

from lib.nextcloud import nextcloud
from lib.upload import upload
from lib.archive import archive

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run backup script with specified runlevel.')
parser.add_argument('--runlevel', type=int, required=False, help='Runlevel for the script')
args = parser.parse_args()

pwd = os.environ["PWD"]
current_date = datetime.now().strftime('%Y-%m-%d')



# Run the backups
for site_name, site_info in config.domains.items():

    filename = f"{site_name}-{current_date}"

    if args.runlevel == None or args.runlevel == 1:
        # Backup the database
        archive.database(site_info, filename)
        # Backup the files
        archive.files(site_info, filename)

    if args.runlevel == None or args.runlevel == 2:
        # Upload files to NAS server.
        upload.rsync(filename, 'sql')
        upload.rsync(filename, 'tar.gz')

    if args.runlevel == None or args.runlevel == 3:
        # Delete previous backups locally
        archive.delete(site_name, 'sql')
        archive.delete(site_name, 'tar.gz')

        # Deletes backups older than 8 days on the NAS server
        archive.delete_remotely(site_name)
