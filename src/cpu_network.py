import requests
import re
import json
import base64


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
        'callback': '',
    }
    response = requests.get('http://192.168.199.21/drcom/chkstatus', params=params, headers=HEADERS, verify=False)
    response.encoding = 'utf-8'
    re_obj = re.search('\((.*)\)', response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("获取IP地址失败，请检查网络连接状态")
    else:
        ip = json.loads(re_obj.group(1))['ss5']
    return ip

def get_status(ip):
    status = {
        'is_online': False,
        'message': '',
        'ip': str(ip),
        'mac': '',
        'username': '',
    }
    params = {
        'c': 'Portal',
        'a': 'find_mac',
        'login_method': '1',
        'wlan_user_ip': str(ip),
    }
    response = requests.get('http://192.168.199.21:801/eportal/', params=params, headers=HEADERS, verify=False)
    response.encoding = 'utf-8'
    re_obj = re.search('\((.*)\)', response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("获取IP地址关联设备状态失败，请检查网络连接状态")
    res = json.loads(re_obj.group(1))
    status['message'] = res['msg']
    if res['result'] == '0':
        return status
    else:
        status['is_online'] = True
        status['mac'] = res['list'][0]['online_mac']
        status['username'] = res['list'][0]['user_account']
    return status

def login(ip, username, password):
    status = {
        'success': False,
        'msg': '',
        'ip': str(ip),
        'username': str(username),
    }
    cur_status = get_status(str(ip))
    if cur_status['is_online']:
        status['success'] = True
        status['msg'] = f"已经上线，无需重复登录"
        status['username'] = cur_status['username'][:]
        return status
    params = {
        'c': 'Portal',
        'a': 'login',
        'login_method': '1',
        'user_account': str(username),
        'user_password': str(password),
        'wlan_user_ip': str(ip),
    }
    response = requests.get('http://192.168.199.21:801/eportal/', headers=HEADERS, params=params, verify=False)
    response.encoding = 'utf-8'
    re_obj = re.search('\((.*)\)', response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("响应无效，请检查网络连接状态")
    res = json.loads(re_obj.group(1))
    if res['result'] == '1':
        status["success"] = True
        status['msg'] = res['msg']
    else:
        if res['ret_code'] == '2':
            status['success'] = True
            status['msg'] = "已经上线，无需重复登录"
            status['username'] = ''
        else:
            if res['msg'] == '':
                status['success'] = False
                status['msg'] = "IP地址无效或网络繁忙"
            else:
                status['success'] = False
                res_msg = base64.b64decode(res['msg']).decode(encoding='utf-8')
                status['msg'] = f"用户名和密码错误，原错误信息：{res_msg}"
    return status

def logout(ip):
    status = {
        'success': False,
        'msg': '',
    }
    cur_status = get_status(str(ip))
    if not cur_status['is_online']:
        status['success'] = True
        status['msg'] = "未上线，无需注销"
        return status
    params = {
        'c': 'Portal',
        'a': 'unbind_mac',
        'user_account': str(cur_status['username']),
        'wlan_user_mac': str(cur_status['mac']),
        'wlan_user_ip': str(ip),
    }
    response = requests.get('http://192.168.199.21:801/eportal/', params=params, headers=HEADERS, verify=False)
    re_obj = re.search('\((.*)\)', response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("响应无效，请检查网络连接状态")
    unbind_mac_status = json.loads(re_obj.group(1))
    params = {
        'c': 'Portal',
        'a': 'logout',
        'ac_logout': '1',
        'wlan_user_ip': str(ip),
    }
    response = requests.get('http://192.168.199.21:801/eportal/', params=params, headers=HEADERS, verify=False)
    re_obj = re.search('\((.*)\)', response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("响应无效，请检查网络连接状态")
    logout_status = json.loads(re_obj.group(1))
    cur_status = get_status(str(ip))
    if not cur_status['is_online']:
        status['success'] = True
        status['msg'] = f"解绑mac时：{unbind_mac_status['msg']}，注销时：{logout_status['msg']}"
    else:
        status['success'] = False
        status['msg'] = f"解绑mac时：{unbind_mac_status['msg']}，注销时：{logout_status['msg']}"
    return status
