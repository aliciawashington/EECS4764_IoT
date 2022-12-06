import urequests as requests
from uconfig import API_KEY, MAC_ADDRESS

def data_post(field, data):
    if not isinstance(data, str):
        data = str(data)
    if not isinstance(field, str):
        field = str(field)
    # http://192.168.1.160:4999/machine/update/API_key=ASNIOENFIH/mac=40:91:51:4e:f7:6c/field=1/data=72
    base_url = 'http://192.168.1.160:4999/machine/update'
    api_key_url = '/API_key='  + API_KEY
    mac_url = '/mac=' + MAC_ADDRESS
    field_url = '/field=' + field
    data_url = '/data=' + data
    url = base_url + api_key_url + mac_url + field_url + data_url 
    print(f'URL: {url}')
    response = requests.get(url)
    print(response.text)
