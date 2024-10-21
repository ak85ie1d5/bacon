import config
import json
import base64
import urllib.request
import urllib.error

class nextcloud:
    # NextCloud send notifications
    @staticmethod
    def notification(message):
        data = json.dumps({'message':message}).encode('utf-8')
        auth = base64.b64encode(f'{config.nc_username}:{config.nc_password}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'OCS-APIRequest': 'true',
            'Authorization': f'Basic {auth}'
        }

        nc_req = urllib.request.Request(config.nc_url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(nc_req) as response:
                print(response.status)
                print(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(e.code, e.reason)