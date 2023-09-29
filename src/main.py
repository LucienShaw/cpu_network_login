import cpu_network
import getpass
import os
import re
import argparse
import time

CONFIG = {
    'ip': '',
    'username': '',
    'password': ''
}

def parse_args():
    parser = argparse.ArgumentParser(description='CPU校园网登录认证')
    parser.add_argument('-c', '--config', type=str, help=f'指定配置文件路径', dest='config_file_path')
    parser.add_argument('--ip', type=str, help='指定IP地址（提供配置文件时无效）', dest='ip')
    parser.add_argument('--username', type=str, help='指定用户名（提供配置文件时无效）', dest='username')
    parser.add_argument('--password', type=str, help='指定密码（提供配置文件时无效）', dest='password')
    parser.add_argument('-y', '--yes-to-all', action='store_true', help='跳过所有确认提示', dest='skip_confirmation')
    args = parser.parse_args()
    return args

def read_config():
    config = {}

    for config_key in CONFIG.keys():
        config[config_key] = CONFIG[config_key]

    args = parse_args()
    if args.config_file_path is None:
        for config_key in CONFIG.keys():
            config_value = getattr(args, config_key)
            if config_value is not None:
                config[config_key] = config_value
    else:
        path = args.config_file_path
        if not os.path.exists(path):
            raise FileNotFoundError(f'配置文件 "{path}" 不存在。')
        with open(path, 'r', encoding='utf-8') as f:
            config_text = f.read()
        for config_key in CONFIG.keys():
            re_obj = re.search(f'{config_key}=(.*)', config_text)
            if re_obj is None:
                continue
            config[config_key] = re_obj.group(1)
    config['skip_confirmation'] = args.skip_confirmation

    return config

def main():
    config = read_config()
    ip = config['ip']
    username = config['username']
    password = config['password']
    skip_confirmation = config['skip_confirmation']
    if ip == '':
        if not skip_confirmation:
            ip = input('请输入校园网IP地址，留空以自动探测: ')
        if ip == '':
            ip = cpu_network.get_ip_remote()
            print(f'\nIP地址={ip}（自动探测）')
    else:
        print(f'\nIP地址={ip}')

    if username == '':
        username = input('请输入用户名: ')
        if username == '':
            print('\n未提供用户名，正在退出')
            return
    else:
        print(f'用户名={username}')

    if password == '':
        password = getpass.getpass('请输入密码，输入时不会显示: ')
        if password == '':
            print('\n未提供密码，正在退出')
            return
    else:
        print("密码已提供")
    if not skip_confirmation:
        confirm = input("\n请按回车键确认，或按Ctrl+C退出")
    print()
    print(cpu_network.login(ip, username, password))
    print('\n10秒后自动退出...')
    time.sleep(10)

if __name__ == '__main__':
    main()
