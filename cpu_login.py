import requests
import sys
import getpass
def get_ip():
    import socket
    ip = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
def login(username, password, ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }
    params = (
        ('c', 'Portal'),
        ('a', 'login'),
        ('login_method', '1'),
        ('user_account', username),
        ('user_password', password),
        ('wlan_user_ip', ip),
    )
    # print(IP)
    response = requests.get('http://192.168.199.21:801/eportal/', headers=headers, params=params, verify=False)
def main():
    args = len(sys.argv)
    O = 0
    if args <= O + 1:
        USERNAME = input('Please enter your username: ')
        PASSWORD = getpass.getpass('Please enter your password: ')
    elif args == O + 2:
        USERNAME = sys.argv[1]
        PASSWORD = getpass.getpass('Please enter your password: ')
    elif args >= O + 3:
        USERNAME = sys.argv[1]
        PASSWORD = sys.argv[2]
    IP = get_ip()
    print(IP)
    login(USERNAME, PASSWORD, IP)
if __name__ == '__main__':
    main()
