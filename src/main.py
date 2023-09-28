import cpu_network
import getpass

IP = ''
USERNAME = ''
PASSWORD = ''

def main():
    ip = IP
    username = USERNAME
    password = PASSWORD
    if ip == '':
        ip = input('Please enter an ip address (Leave blank for automatic detection): ')
        if ip == '':
            ip = cpu_network.get_ip_remote()
            print(f'\nIP={ip}')
    else:
        print(f'\nIP={ip}')
    if username == '':
        username = input('Please enter your username: ')
        if username == '':
            print('\nTerminating')
            return
    else:
        print(f'Username={username}')
    if password == '':
        password = getpass.getpass('Please enter your password: ')
        if password == '':
            print('\nTerminating')
            return
    else:
        print("Password is already given")
    a = input("\nPress Enter to confirm, or Ctrl+C to terminate: ")
    print(cpu_network.login(ip, username, password))
    
if __name__ == '__main__':
    main()
