# !/usr/bin/python3
# -*-coding:utf-8-*-
# Description: ssh utils
import paramiko, time


class SSHConnection(object):
    def __init__(self, host=None, port=None, username=None, pwd=None):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__pwd = pwd
        self.__transport = None
        self.__k = None
        self.__ssh=None

    def connect(self):
        # 创建连接对象
        transport = paramiko.Transport((self.__host, self.__port))
        transport.connect(username=self.__username, password=self.__pwd)
        self.__transport = transport
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh._transport = self.__transport
        print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), 'connected')

    # 关闭连接
    def close(self):
        self.__transport.close()
        # print('关闭Transport连接\n')
        # print('disconnected\n')
        print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())),'disconnected\n\n')

    def upload(self, local_path, target_path):
        """
        本地上传文件到服务器
        :param local_path: 本地文件地址
        :param target_path: 目标文件路径
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        """
        服务器下载文件到本地
        :param remote_path: 服务器文件路径
        :param local_path: 本地目标路径
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command,errlist=[],timeout_tf=100):
        """
        执行指定命令
        :param command: 命令
        :return:输入，输出，错误
        """
        # print(command)
        commandex='bash -lc \''+command+'\''
        # 执行命令，标准输入，输出，错误
        stdin, stdout, stderr = self.__ssh.exec_command(commandex,timeout=timeout_tf)
        # 获取命令结果
        outputs = stdout.read().decode('utf-8','ignore')
        #outputs = str(outputs, encoding="utf-8")
        return outputs

class CContainerCheck(object):
    def __init__(self):
        self.sshConnectionHost=None
        self.sshConnectionLxc=None
        self.rootip = '172.21.9.248'
        self.containerPort= 35620
        self.username = 'root'
        self.password = 'Admin@huawei'

    # 交采模块测试
    def portAlter(self):
        try:
            self.sshConnectionLxc = SSHConnection(self.rootip, self.containerPort, self.username, self.password)
            self.sshConnectionLxc.connect()
            # var = 1
            # while var == 1:
            #     alter = self.sshConnectionLxc.cmd('./portApp_ar alter')
            #     print(alter)
            print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), './portApp_ar alter')
            for i in range(3):
                alter = self.sshConnectionLxc.cmd('./portApp_ar alter')
                print(alter)
                # if (alter.find('失败') >= 0):
                #     print('交采模块测试失败\n')
                # else:
                #     print('交采模块测试成功\n')
            self.sshConnectionLxc.close()
            return True

        except paramiko.SSHException:
            # print(paramiko.SSHException)
            print('连接主机服务器异常,检测失败! \n')
            return False

    # 载波模块测试
    def portAma1(self):
        try:
            self.sshConnectionLxc = SSHConnection(self.rootip, self.containerPort, self.username, self.password)
            self.sshConnectionLxc.connect()
            # self.sshConnectionLxc.upload('shell/portApp_ar', 'portApp_ar')
            # self.sshConnectionLxc.upload('shell/config.json', 'config.json')
            print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), './portApp_ar carrier')
            for i in range(3):
                ama1 = self.sshConnectionLxc.cmd('./portApp_ar carrier')
                print(ama1)
            # if (ama1.find('失败') >= 0):
            #     print('载波模块测试失败')
            # else:
            #     print('载波模块测试成功')
            self.sshConnectionLxc.close()
            return True

        except paramiko.SSHException:
            print('连接主机服务器异常,检测失败! \n')
            return False

    # 串口485模式测试
    def port485(self):
        try:
            self.sshConnectionLxc = SSHConnection(self.rootip, self.containerPort, self.username, self.password)
            self.sshConnectionLxc.connect()
            # self.sshConnectionLxc.upload('shell/portApp_ar', 'portApp_ar')
            # self.sshConnectionLxc.upload('shell/config.json', 'config.json')
            # out = self.sshConnectionLxc.cmd('chmod 555 portApp_ar; ./portApp_ar 485')
            # resList.append(out)
            # var = 1
            # while var == 1:
            #     rs485 = self.sshConnectionLxc.cmd('cd /mnt/internal_storage; ./portCheck')
            # # out = self.sshConnectionLxc.cmd('./portApp_ar 485 2>&1 ')
            # # out = self.sshConnectionLxc.cmd('./portCheck')
            #     print(rs485)
            #     time.sleep(5)
            # self.sshConnectionLxc.cmd('^C')
            # var = 1
            # while var == 1:
            # print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), 'cd /mnt/internal_storage')
            print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), './portCheck')
            for i in range(2):
                rs485 = self.sshConnectionLxc.cmd('cd /mnt/internal_storage\n ./portCheck')
                print(rs485)
            # print('./portApp_ar 485')
            # rs485 = self.sshConnectionLxc.cmd('./portApp_ar 485')
            # print(rs485)
            # if (rs485.find('数据长度') >= 0):
            #     print('串口485模式测试成功')
            # else:
            #     print('串口485模式测试失败')
            self.sshConnectionLxc.close()
            return True

        except paramiko.SSHException:
            print('连接主机服务器异常,检测失败! \n')
            return False

    # 传感器测试
    def portsensor(self):
        try:
            self.sshConnectionLxc = SSHConnection(self.rootip, self.containerPort, self.username, self.password)
            self.sshConnectionLxc.connect()
            print(time.strftime('[%Y.%m.%d %H:%M:%S]', time.localtime(time.time())), './bin/ctapp  -c  /mnt/internal_storage/conf/config.json')
            sensor = self.sshConnectionLxc.cmd('cd /mnt/internal_storage\n ./bin/ctapp  -c  /mnt/internal_storage/conf/config.json')
            print(sensor)
            self.sshConnectionLxc.close()
            return True

        except paramiko.SSHException:
            print('连接主机服务器异常,检测失败! \n')
            return False