# CPU 校园网登录认证
自动执行CPU校园网登录认证操作。  
## 功能
- 为任何指定的校园网IP地址登录认证；  
- 登录认证需要提供用户名及密码，所有信息仅保存在本地，且只会上传到CPU校园网服务器上用于登录认证事宜，不会泄露；  
- 为运行此程序的设备登录认证时可自动获取本设备IP地址；  
- 自动获取的IP地址为*直接连接校园网*的IP地址。因此，若运行此程序的设备通过路由器连接校园网，程序将正确取得路由器的出口IP地址用于登录；  
- 可以在CLI交互运行，也可后台自动运行。  
## 下载地址
请前往本仓库[Release](https://github.com/lucienshawls/CPU_Network_Auth/releases)界面下载对应系统的可执行文件。  
## 使用方法
### Windows
1. 直接运行  
  - 双击`cpu_network_auth.exe`, 根据指引输入IP地址、用户名和密码，使用回车键确认，结果中出现`Success`即为成功，若未成功可检查输入并重试一次  
2. 命令行运行  
  - 单击`cpu_network_auth.exe`所在文件夹的地址栏，输入`powershell`以打开命令窗口  
  - 使用方法举例：  
    ```powershell
    # 查看详细参数说明
    .\cpu_network_auth.exe -h

    # 使用当前文件夹下config.txt文件作为输入信息，并跳过确认提示
    # 使用-y或--yes-to-all跳过确认提示时，IP地址将自动获取，缺失的用户名和密码仍需在交互界面手动输入
    .\cpu_network_auth.exe -c .\config.txt -y

    # 手动指定全部或一部分信息，缺失的值需要在交互界面手动输入
    # 这里指定了IP地址和用户名，则密码需要在交互界面手动输入
    .\cpu_network_auth.exe --ip 10.x.x.x --username 2020xxxxxx
    ```  
### Linux
在Linux系统中应使用命令行运行。  
- 使用`cd`命令进入`cpu_network_auth`所在目录  
- 使用方法举例：  
    ```bash
    # 查看详细参数说明
    ./cpu_network_auth -h

    # 使用当前文件夹下config.txt文件作为输入信息，并跳过确认提示
    # 使用-y或--yes-to-all跳过确认提示时，IP地址将自动获取，缺失的用户名和密码仍需在交互界面手动输入
    ./cpu_network_auth -c ./config.txt -y

    # 手动指定全部或一部分信息，缺失的值需要在交互界面手动输入
    # 这里指定了IP地址和用户名，则密码需要在交互界面手动输入
    ./cpu_network_auth --ip 10.x.x.x --username 2020xxxxxx
    ```  
### 配置文件
- 配置文件样例如下，将对应值填写在等于号之后，即可配合`-c`或`-config`参数自动读取；  
    ```conf
    ip=10.x.x.x
    username=2020xxxxxx
    password=
    ```  
- 留空的值视为未提供，可能需要在交互界面手动输入；

### 友情链接
[Metaphorme/CPU-web-login](https://github.com/Metaphorme/CPU-web-login)
