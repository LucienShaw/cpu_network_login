import requests
import re
import json
import warnings

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
}

def get_ip_local():
    import socket
    ip = '127.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_ip_remote():
    params = {
        'callback': 'dr1002',
    }
    try:
        response = requests.get('http://192.168.199.21/drcom/chkstatus', params=params, headers=HEADERS, verify=False)
        response.encoding = 'gbk'
        re_obj = re.search('dr1002\((.*)\)', response.text)
        if re_obj is None:
            warnings.warn(f'Failed to get remote ip address, using local ip address instead.\n Cause:\nInvalid response', RuntimeWarning)
            ip = get_ip_local()
        else:
            ip = json.loads(re_obj.group(1))['ss5']
    except Exception as e:
        warnings.warn(f'Failed to get remote ip address, using local ip address instead.\n Cause:\n{str(e)}', RuntimeWarning)
        ip = get_ip_local()
    return ip

def login(ip, username, password):
    params = (
        ('c', 'Portal'),
        ('a', 'login'),
        ('login_method', '1'),
        ('user_account', username),
        ('user_password', password),
        ('wlan_user_ip', ip),
    )
    response = requests.get('http://192.168.199.21:801/eportal/', headers=HEADERS, params=params, verify=False)
    response.encoding = 'utf-8'
    re_obj = re.search('\((.*)\)', response.text)
    if re_obj is None:
        raise RuntimeError('Invalid response')
    res = json.loads(re_obj.group(1))
    if res['ret_code'] == 2 or res['result'] == '1':
        return f"Success: ip={ip}; user={username}"
    else:
        return f"Failure: ip={ip}; user={username}\nDetail:\n{response.text}"
