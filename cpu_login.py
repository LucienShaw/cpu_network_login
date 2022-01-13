import requests
def get_ip():
    import socket
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
    # USERNAME = input('Please enter your username: ')
    # PASSWORD = input('Please enter your password: ')
    USERNAME = ''
    PASSWORD = ''
    IP = get_ip()
    login(USERNAME, PASSWORD, IP)
if __name__ == '__main__':
    main()

