import re
import json
import utils
import requests
from enum import Enum, unique


@unique
class AuthHost(Enum):
    General = "192.168.199.21"
    Dormitory = "172.17.253.3"


@unique
class TerminalType(Enum):
    Other = "0"
    PC = "1"
    Mobile = "2"
    Tablet_Landscape = "3"
    Tablet_Portrait = "4"


def get_ip(host: AuthHost = AuthHost.General) -> str:
    url = f"http://{host.value}/drcom/chkstatus"
    params = {"callback": ""}
    response = requests.get(url=url, params=params)
    response.encoding = "utf-8"
    re_obj = re.search(r"\((.*)\)", response.text)
    if response.status_code != 200 or re_obj is None:
        raise RuntimeError("获取IP地址失败，请检查网络连接状态")
    else:
        ip = json.loads(re_obj.group(1))["ss5"]
    return ip


def get_status(ip: str = "", host: AuthHost = AuthHost.General) -> dict:
    ip = str(ip) if isinstance(ip, str) and ip != "" else get_ip(host=host)

    status = {
        "success": False,
        "msg": "",
        "is_online": False,
        "ip": ip,
        "mac": "",
        "username": "",
    }

    url = f"http://{host.value}:801/eportal/portal/mac/find"
    params = {"wlan_user_ip": ip}
    response = requests.get(url=url, params=params)
    response.encoding = "utf-8"
    re_obj = re.search(r"jsonpReturn\((.*)\)", response.text)

    if response.status_code != 200 or re_obj is None:
        status["msg"] = "获取IP地址关联信息状态失败，请检查网络连接状态"
        return status
    res = json.loads(re_obj.group(1))

    status["msg"] = res["msg"]

    if res["result"] == 1:
        if res["list"][0]["online_ip"] != ip:
            status["msg"] = f"IP地址数据冲突，可能是提供的IP地址存在格式错误"
            return status
        status["is_online"] = True
        status["mac"] = res["list"][0]["online_mac"]
        status["username"] = res["list"][0]["user_account"]

    status["success"] = True
    return status


def login(
    username: str,
    password: str,
    ip: str = "",
    terminal_type: TerminalType = TerminalType.PC,
    host: AuthHost = AuthHost.General,
) -> dict:
    username = str(username)
    password = str(password)
    assert username != "", f"用户名不能为空"
    assert password != "", f"密码不能为空"
    ip = str(ip) if isinstance(ip, str) and ip != "" else get_ip(host=host)

    cur_status = get_status(ip=ip, host=host)
    if not cur_status["success"]:
        return {
            "success": False,
            "msg": cur_status["msg"],
            "ip": ip,
            "username": username,
        }

    if cur_status["is_online"]:
        return {
            "success": True,
            "msg": "已经上线，无需重复登录",
            "ip": ip,
            "username": cur_status["username"][:],
        }

    status = {
        "success": False,
        "msg": "",
        "ip": ip,
        "username": username,
    }

    url = f"http://{host.value}:801/eportal/portal/login"
    params = {
        "user_account": str(username),
        "user_password": str(password),
        "wlan_user_ip": str(ip),
        "terminal_type": terminal_type.value,
        # 访问设备
        # 0-其他
        # 1-PC
        # 2-手机
        # 3-平板(横屏)
        # 4-平板(竖屏)
    }
    response = requests.get(url=url, params=params)
    response.encoding = "utf-8"
    re_obj = re.search(r"jsonpReturn\((.*)\);", response.text)

    if response.status_code != 200 or re_obj is None:
        status["msg"] = "响应无效，请检查网络连接状态"
        return status
    res = json.loads(re_obj.group(1))

    if res["result"] == 1:
        status["success"] = True
        status["msg"] = res["msg"]
    else:
        if res["ret_code"] == 2:
            status["success"] = True
            status["msg"] = "已经上线，无需重复登录"
            status["username"] = ""
        else:
            if res["msg"] == "":
                status["success"] = False
                status["msg"] = "IP地址无效或网络繁忙"
            else:
                status["success"] = False
                status["msg"] = (
                    f'用户名或密码错误，或IP地址未接入网络，详细错误信息：{res["msg"]}'
                )
    return status


def logout(ip: str = "", host: AuthHost = AuthHost.General) -> dict:
    ip = str(ip) if isinstance(ip, str) and ip != "" else get_ip(host=host)

    cur_status = get_status(ip=ip, host=host)
    if not cur_status["is_online"]:
        return {
            "success": True,
            "msg": "未登录，无需登出",
            "ip": ip,
        }
    username = cur_status["username"]
    mac = cur_status["mac"]

    status = {
        "success": False,
        "msg": "",
        "ip": ip,
    }

    url_unbind = f"http://{host.value}:801/eportal/portal/mac/unbind"
    params_unbind = {
        "user_account": username,
        "wlan_user_mac": mac,
        "wlan_user_ip": utils.ip_to_int(ip=ip),
    }
    response_unbind = requests.get(url=url_unbind, params=params_unbind)
    res_unbind_re = re.search(r"jsonpReturn\((.*)\);", response_unbind.text)
    if response_unbind.status_code != 200 or res_unbind_re is None:
        res_unbind = {
            "result": 0,
            "msg": "响应无效，请检查网络连接状态",
        }
    else:
        res_unbind = json.loads(res_unbind_re.group(1))

    status["msg"] += f'尝试解绑MAC时："{res_unbind["msg"]}"；'
    if bool(res_unbind["result"]):
        status["success"] = True
        return status

    url_logout = f"http://{host.value}:801/eportal/portal/logout"
    params_logout = {
        "user_account": "drcom",
        "user_password": "123",
        "wlan_user_ip": ip,
    }
    response_logout = requests.get(url=url_logout, params=params_logout)
    res_logout_re = re.search(r"jsonpReturn\((.*)\);", response_logout.text)
    if response_logout.status_code != 200 or res_logout_re is None:
        res_unbind = {
            "result": 0,
            "msg": "响应无效，请检查网络连接状态",
        }
    else:
        res_logout = json.loads(res_logout_re.group(1))

    status["msg"] += f'尝试登出时："{res_logout["msg"]}"。'
    if bool(res_unbind["result"]) or bool(res_logout["result"]):
        status["success"] = True
    return status
