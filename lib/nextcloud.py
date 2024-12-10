import config
import json
import base64
import urllib2

class nextcloud:
    # NextCloud send notifications
    @staticmethod
    def notification(message):
        data = json.dumps({'message': message}).encode('utf-8')
        auth = base64.b64encode('{}:{}'.format(config.nc_username, config.nc_password).encode('utf-8')).decode('utf-8')
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'OCS-APIRequest': 'true',
            'Authorization': 'Basic {}'.format(auth)
        }

        nc_req = urllib2.Request(config.nc_url, data=data, headers=headers)

        try:
            response = urllib2.urlopen(nc_req)
            print(response.getcode())
            print(response.read().decode('utf-8'))
        except urllib2.HTTPError as e:
            print(e.code, e.reason)