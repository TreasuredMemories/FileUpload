import argparse
import configparser
import os

import requests
from urllib3 import encode_multipart_formdata


class miniTools:
    def __init__(self):
        self.url = ""
        self.local_path= ""
        self.file_path=""
        self.data = {}
        self.headers = {}
        self.check_config()

    # 校验配置文件是否存在
    def check_config(self):
        if (os.path.exists("config.ini")):
            self.read_config()
        else:
            self.write_config()

    # 读取配置文件
    def read_config(self):
        con = configparser.ConfigParser()
        con.read("config.ini", encoding="utf-8")

        self.url = con["url"]["remote"]
        self.local_path = con["local"]["path"]

        header_options = con.options("headers")
        for item in header_options:
            key = item
            value = con.get("headers",item)
            self.headers[key]= value

        data_options = con.options("data")
        for item in data_options:
            key = item
            value = con.get("data",item)
            self.data[key]= value
    # 写配置文件提示信息
    def write_config(self):
        con = configparser.ConfigParser()
        con.read("config.ini")
        con.add_section("url")
        con.set("url", "remote", "远程上传接口")
        con.add_section("data")
        con.set("data", "key1", "value1")
        con.set("data", "key2", "value2")
        con.add_section("headers")
        con.set("headers", "key", "value")
        con.set("headers", "key2", "value2")
        con.add_section("local")
        con.set("local","path","C://file")

        with open("config.ini", "w+", encoding="utf8") as f:
            con.write(f)

    # 获取cmd的图片路径
    def get_cmd_input(self):
        # 获取输入参数
        parser = argparse.ArgumentParser(description='微信公众号：小豪技术栈')
        parser.add_argument('-l', type=str, help='文件所在位置')
        args = parser.parse_args()
        self.file_path = args.l
        return args.l

    # 文件在本地指定文件夹做一次备份
    def backup_into_local(self,url):
        # if(not os.path.exists(self.local_path)):
        #     os.mkdir(self.local_path)
        # with open(self.file_path ,'wb+') as f:
        #     f.write("")
        pass
    # 上传文件
    def upload(self):
        fileurl = self.get_cmd_input()
        self.data['file'] = ("2.jpg", open(fileurl, 'rb').read())
        encode_data = encode_multipart_formdata(self.data)
        self.data = encode_data[0]
        self.headers['Content-Type'] = encode_data[1]
        result = requests.post(self.url, headers=self.headers, data=self.data).json()

        print(result["result"])


if __name__ == '__main__':
    tool = miniTools()
    tool.upload()
