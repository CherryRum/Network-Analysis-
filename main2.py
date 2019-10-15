# coding=utf-8

import os
import time
import subprocess
import json


class Reconnect:  # 初始化重启
    def __init__(self):
        self.every = 5  # 检测间隔时间，单位5秒

    def get_CurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def login(self):
        print(self.get_CurrentTime(), u"拼命连网中...")
        filename = "user_account.json"
        user_account = {}
        try:
            with open(filename) as f_obj:
                user_account = json.load(f_obj)
        except FileNotFoundError:
            username = input("input your account ")
            password = input("input your password ")
            user_account["username"] = username
            user_account["password"] = password
            with open(filename, 'w') as f_obj:
                json.dump(user_account, f_obj)
                print("We'll remember you when you come back, " + username + "!")
        else:
            username = user_account["username"]
            password = user_account["password"]
        os.system("rasdial 宽带连接 {} {}".format(username,password))
        print(u'连上了...现在开始看连接是否正常')


    def can_Connect(self):
        fnull = open(os.devnull, 'w')
        result = subprocess.call('ping www.baidu.com', shell=True, stdout=fnull, stderr=fnull)
        fnull.close()
        if result:
            return False
        else:
            return True

    def main(self):
        print(self.get_CurrentTime(), u"Hi，欢迎使用自动登陆系统")
        while True:
            self.login()
            while True:
                can_connect = self.can_Connect()

                if not can_connect:
                    print(self.get_CurrentTime(), u"断网了...")
                    os.system("rasphone -h 宽带连接")
                    self.login()
                    time.sleep(2)
                else:
                    print(self.get_CurrentTime(), u"一切正常...")
                time.sleep(self.every)
            time.sleep(self.every)


reconnect = Reconnect()
reconnect.main()
