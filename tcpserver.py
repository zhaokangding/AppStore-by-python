from socket import * # 引入套接字模块

install = "ZRW get install"
uninstall = "ZRW uninstall"
find = "find"
change_source = "change source"
close = "close"



def handle_command(connectionSocket, command):
    '''
    处理命令
    :param connectionSocket: 套接字接口
    :param command: 需要处理的命令
    :return: 处理成功返回1 否则返回 -1
    '''
    command_type = command[0:len(command) - command[::-1].find(" ") - 1]
    # 按照不同的指令类型进行不同测处理
    if command_type == install:
        apkname = command[len(command) - command[::-1].find(" ") : -1]
        handle_install(connectionSocket, apkname)
        return 1
    elif command_type == change_source:
        new_source = command[len(command) - command[::-1].find(" ") : -1]
        handle_change_source(connectionSocket, new_source)
        return 1
    elif command_type == find:
        info = command[len(command) - command[::-1].find(" ") : -1]
        handle_find(connectionSocket, info)
        return 1
    else:
        return -1



def handle_install(connectionSocket, apkname):
    '''
    下载命令，从软件源获得软件包并发送给客户端
    :param connectionSocket: 套接字接口
    :param apkname: 安装包名字
    :return: 成功返回 1 否则返回 -1
    '''
        
    '''
        TODO:  基于软件源或者基于开源工具
    '''
    if apkname in dic:                                                          #判断是否在字典中
        path = dic[apkname]['local']
        filesize = os.path.getsize(path)
        file_send(connectionSocket, path, filesize)
        return 1        
    else:
        return -1



def handle_change_source(connectionSocket, new_source):
    '''
    修改软件源
    :param connectionSocket: 套接字接口
    :param new_source: 新的软件源
    :return: 成功返回 1  否则返回-1
    '''
    '''
        TODO: 完成修改软件源
    '''
    pass


def handle_find(connectonSocket, info):
    '''
    搜索软件信息
    :param connectonSocket: 套接字
    :param info: 搜索信息
    :return: 成功返回 1 否则返回 -1
    '''

    '''
        TODO: 完成软件信息的搜索，通过套接字返回给客户端
              有两类搜索，一直是基于分类，一种是基于名字
    '''
    pass



def create_dic(source):
    '''
    获取软件源里面软件的信息
    :param source: 软件源
    :return: 一个字典，包含软件源的软件的所有信息
    '''
    pass




def file_send(connectionSocket, filename, filesize):
    '''
    发送安装包
    :param connectionSocket: 套接字接口
    :param filename: 文件名
    :param filesize: 文件大小
    :return: 发送成功返回 1 否则返回 -1
    '''
    # pass
    try:
        size = 0
        with open(filename, "rb") as file:
            while size < filesize:
                filedata = file.read(1024)
                connectionSocket.send(filedata)
                size = size + 1024
        return 1
    except:
        return -1


command_list = [install, uninstall, find, change_source, close] # 可以处理的指令集合

serverPort = 12002 # 设置服务器端口号为12002

serverSocket = socket(AF_INET, SOCK_STREAM) # 创建欢迎套接字，第一个参数指示底层网络使用IPv4地址，第二个参数指示该套接字是SOCK_STREAM类型，这表明它是一个TCP套接字
serverSocket.bind(('', serverPort)) # 将端口号与欢迎套接字关联起来
# serverSocket.listen(1) # 等待某个客户的访问
print('The server is ready to receive\n') 
while True:
    serverSocket.listen(1)  # 等待某个客户的访问
    connectionSocket, addr = serverSocket.accept() # 当客户访问时，调用accept()方法，为这个特定客户创建一个新套接字，由客户专用
    command = connectionSocket.recv(1024).decode() # 接收来自客户端的字符

    print('From client: ', command) # 打印用于可视化
    # 处理客户端的命令
    command_type = command[0:len(command) - command[::-1].find(" ") - 1]
    if (command_type not in command_list):
        messig_back = "未定义的命令，请重新输入"
        connectionSocket.send(messig_back.encode())  # 返回错误信息
        connectionSocket.close()  # 关闭这个套接字
    elif command == "close" :
        messig_back = "88"
        connectionSocket.send(messig_back.encode())
        connectionSocket.close()  # 关闭这个套接字
        continue
    else:
        messig_back = "command valid"
        connectionSocket.send(messig_back.encode())
        handle_command(connectionSocket, command) #命令处理函数




