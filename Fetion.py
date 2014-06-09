# -*- coding:utf-8 -*-
# file: SendFetion.py
# by Lee 2013-9-18
"""-----------------------------------------------------------------------------
    使用HTTPS调用飞信接口:
    https://quanapi.sinaapp.com/fetion.php?u=飞信登录手机号&p=飞信登录密码&to=接收飞信的手机号&m=飞信内容
    返回结果为Json格式，result=0时表示发送成功
    {“result”:0,”message”:”\u53d1\u9001\u6210\u529f”}
-----------------------------------------------------------------------------"""
import sys
import httplib
import urllib
import re
import time
import json

class Fetion:
    """
       model to call fetionapi.
       attribute:url, fromTel, pwd, toTel, msg
       function:Trans, format_url, SendMsg
    """
    url = "https://quanapi.sinaapp.com/fetion.php?u="
    def __init__(self,
                 toTel,
                 msg,
                 fromTel = '150xxxxxxxx',  # default my phone
                 pwd = 'password***'):
        self.fromTel = fromTel
        self.pwd = pwd
        self.toTel = toTel
        self.msg = self.Trans(msg)
    def Trans(self, msg):
        # change space to '%20', otherwise error raised
        return re.sub(" ", "%20", str(msg))
    def format_url(self):
        url_address = self.url + self.fromTel \
            + "&p=" + self.pwd \
            + "&to=" + self.toTel \
            + "&m=" + self.msg
        return url_address
    def SendMsg(self):
        # call the api by http get method
        return urllib.urlopen(self.format_url())
def msg2log(msg):
    logfile = open('MyFetion.log', 'a')
    now = time.strftime('%Y%m%d %H:%M:%S')
    logfile.write('\n'+ now + '\n' + msg + '\n')
    logfile.close()
 
def main():
    # format mutual message
    print "\n" + " "*10 + "*"*60
    print " "*10 + " Personal Fetion"
    print " "*10 + " Enter the number and message what you want to send to."
    print " "*10 + " blank number means yourself,"
    print " "*10 + " and a blank message line to exit."
    print " "*10 + "*"*60
    # get the destination phone number
    toTel = raw_input("Input the target telphone number:")
    if toTel == "":
        toTel = "15026686350"  # none input for a target most used
    # get the message and send by Fetion class
    while True:
        msg = raw_input("Message:")
        if msg == "":
            break  # none input to quit
        else:
            print "Sending...."
            msg2log(msg)
            ff = Fetion(toTel, msg)
            answer = ff.SendMsg()
            data = answer.read()
            jdata=json.loads(data)
            if jdata['result']==0:
                print 'Done.^_^\n'
            else:
                print 'Fail.-_=\n'            
if __name__ == '__main__':
    main()
