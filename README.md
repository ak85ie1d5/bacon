# Bacon

A script written in Python to automate website backup.

## Features
The script make backup of websites one by one as follows:

1. export of the database and make .sql file
2. make tar.gz archive of the website
3. upload the database on the remote server
4. upload the archive on the remote server
5. remove the next archive and the database from the webserver
6. remove the older than 7 days archives and databases from the remote server

A notification is sent on Nextcloud Talk after each step.

## Requirements

- Python 3.*
- dumpsql
- SQL credentials of the website(s) you want to backup
- Nextcloud Talk credentials to send notifications
- (optional) FTP/SFTP credentials of the remote server to store history backups

## Installation

1. Clone this project in your webserver 
2. Rename `config.sample.py` file into `config.py` and complete the file with your credentials.
3. Run the following command:

```shell
python3 bacon/main.py
```

## Parameters

Is it possible to run partially the script by passing `--runlevel` parameter. 

`--runlevel 1`, run only step 1 and 2
`--runlevel 2`, run only step 3 and 4
`--runlevel 3`, run only step 5 and 6

## License

This project is licensed under the MIT License - see the LICENSE file for details.