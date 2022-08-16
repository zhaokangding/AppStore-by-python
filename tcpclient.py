from socket import * # 引入套接字模块
serverName = gethostname() # 得到这台主机名，也就是服务器方的IP地址
serverPort = 12002 # 服务器程序的端口号, 通常这是公认的，这里我写的服务器程序中为12002

def file_recv(clientSocket, filename, filesize):
    '''
    接收安装包
    :param clientSocket: 套接字接口
    :param filename: 文件名
    :filesize: 文件大小
    :return: 接收成功返回 1 否则返回 -1
    '''
    # pass
    try:
        size = 0
        with open(filename, "wb") as file:
            while size < filesize:
                value = filesize -size
                if value > 1024:
                    getdata = clientSocket.recv(1024)
                else:
                    getdata = clientSocket.recv(value)
                file.write(getdata)
                size = size + 1024
        return 1
    except:
        return -1

def dict_recv(clientSocket):
    '''
    接收字典
    :param clientSocket: 套接字接口
    :param dict_name: 字典名
    :dict_size: 字典大小
    '''
    size = 0
    len_dict = int(clientSocket.recv(1024).decode())
    dict_new = ''
    while len_dict > 0:
        if len_dict >= 1024:
            dict_temp = clientSocket.recv(1024).decode()
            dict_new += dict_temp
            len_dict -= 1024
        else:
            dict_temp = clientSocket.recv(len_dict).decode()
            dict_new += dict_temp
            len_dict = 0
    return json.loads(dict_new)
        

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM) # 创建一个套接字，第一个参数指示底层网络使用IPv4地址，第二个参数指示该套接字是SOCK_STREAM类型，这表明它是一个TCP套接字
    clientSocket.connect((serverName, serverPort)) # 发起客户与服务器之间的TCP连接，第一个参数为服务器地址，第二个参数为服务器端口号

    command = input("Please input msg: ") # 输入从客户端发给服务器的信息

    # command 是用户输入的命令

    # 退出模块
    if(command == "close"):
        clientSocket.send(command.encode())  # 发给服务器
        messig_recv = clientSocket.recv(1024).decode()  # 接收来自服务器的字符
        if(messig_recv == "88" ):
            print("成功退出")
            clientSocket.close()  # 完成一次TCP连接，关闭客户的套接字
            break
        else:
            print("退出异常，请等待或强制退出！")
            continue

    clientSocket.send(command.encode()) # 发给服务器



    messig_recv = clientSocket.recv(1024).decode() # 接收来自服务器的字符
    if(messig_recv == "未定义的命令，请重新输入"):
        print('From Server: ', messig_recv) # 打印用于可视化

    '''
        TODO:
            对不同的命令处理来自服务器端的不同信息
            ZRW get install: 将安装包以二进制写的方式转到本地并调用其他命令进行软件的下载
            ZRW uninstall: 卸载安装包
            find : 处理来自服务器的软件信息
            change source: 改变软件源
    '''





    clientSocket.close() # 完成一次TCP连接，关闭客户的套接字
