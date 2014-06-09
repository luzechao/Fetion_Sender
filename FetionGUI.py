# -*- coding:utf-8 -*-
# file: FetionGUI
# by Lu Zechao 2014-6-7
"""-----------------------------------------------------------------------------
    使用HTTPS调用飞信接口:
    https://quanapi.sinaapp.com/fetion.php?u=飞信登录手机号&p=飞信登录密码&to=接收飞信的手机号&m=飞信内容
    返回结果为Json格式，result=0时表示发送成功
    {“result”:0,”message”:”\u53d1\u9001\u6210\u529f”}
-----------------------------------------------------------------------------"""

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
import sys
import httplib
import urllib
import re
import time
import json
import base64

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
                 fromTel, 
                 pwd):
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

class FetionGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("简易飞信客户端")
        self.m = Menu(self.root)
        self.root.config(menu = self.m)
        self.filemenu = Menu(self.m)
        self.m.add_cascade(label = "文件",menu=self.filemenu)
        self.filemenu.add_command(label = "新建",command = newApp)
        self.filemenu.add_command(label = "保存密码",command = self.savePWD)
        self.filemenu.add_command(label = "读取密码",command = self.readPWD)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "退出",command = self.exit)
        self.editmenu = Menu(self.m)
        self.m.add_cascade(label = "编辑",menu=self.editmenu)
        self.editmenu.add_command(label = "清空内容",command=self.clearAll)
        self.editmenu.add_command(label = "上一个收件人",command=self.cancel)
        self.editmenu.add_command(label = "保存草稿",command=self.saveTemp)
        self.editmenu.add_command(label = "读取草稿",command=self.readTemp)
        self.editmenu.add_command(label = "添加表情",command=self.emoji)
        self.helpmenu = Menu(self.m)
        self.m.add_cascade(label = "帮助",menu=self.helpmenu)
        self.helpmenu.add_command(label ="关于",command=self.about)
        Label(self.root,text="用户名:").grid(sticky=E)
        Label(self.root,text="密码:").grid(sticky=E)
        
        Label(self.root,text="接收者:").grid(sticky=E)
        Label(self.root,text="内容:").grid(sticky=E)
        self.eUser = StringVar()
        Entry(self.root,textvariable = self.eUser).grid(row=0,column=1)
        self.ePWD = StringVar()
        Entry(self.root,textvariable = self.ePWD).grid(row=1,column=1)
        self.emsg = StringVar()
        Entry(self.root,textvariable = self.emsg).grid(row=3,
            column=1,rowspan=3)
        self.erec = StringVar()
        Entry(self.root,textvariable = self.erec).grid(row=2,column=1)
        Button(self.root,text="发送",command=self.sent).grid(row=6,
            column=0)
        Button(self.root,text="保存日志",command=self.savelog).grid(row=6,column=1)
        self.status= StringVar()
        self.status.set("发送状态：未发送")
        Label(self.root,textvariable=self.status).grid(row=7,column=0,columnspan=2)

        
        self.root.mainloop()
        
        


    def cancel(self):
        try:
            self.erec.set(self.lastrec)
        except AttributeError:
            showerror(title="出错了！",message="未发送无法指定上一个联系人~")
        
    def about(self):
        showinfo(title = "关于",message ="作者：陆泽超")
    def emoji(self):
        self.top = Toplevel()
        self.top.title('表情')
        
        v1=StringVar()
        Entry(self.top,width=40,textvariable=v1).pack()
        v1.set(" (´･ω･｀) (≖ ‿ ≖)✧ （´∀｀*) ,,Ծ‸Ծ,, π__π")
        v2=StringVar()
        Entry(self.top,width=40,textvariable=v2).pack()
        v2.set(" (/= _ =)/~┴┴  (╬▔皿▔)  ∑(っ °Д °;)っ ╮(╯▽╰)╭")
        Label(self.top,text="请复制粘贴使用").pack()
        
    def savePWD(self):
        self.name=base64.encodestring(self.eUser.get())
        self.password=base64.encodestring(self.ePWD.get())
        self.user = open('UserInfo.txt','w')
        self.user.write(self.name+self.password)
        self.user.close()

    def exit(self):
        question=askyesno(title = "草稿",message="是否保存草稿")
        if question:
            self.saveTemp()
        self.root.quit()
        self.root.destroy()

    def clearAll(self):
        self.emsg.set("")

    def saveTemp(self):
        try:
            self.save = asksaveasfile(defaultextension=".txt",title="保存草稿")
            
            self.save.write(self.emsg.get())
            self.save.close()

        except AttributeError:
            showwarning(title="出错了！",message="未指定路径")


    def readTemp(self):
        try:
            self.Read = askopenfile(defaultextension=".txt",title="读取草稿")
            self.emsg.set(self.Read.read())
            self.Read.close()
        except AttributeError:
            showwarning(title="出错了！",message="未指定路径")
    def readPWD(self):
        try:
            self.f = open("UserInfo.txt",'r')
            self.dename=self.f.readline()
            self.depwd=self.f.readline()
            self.eUser.set(base64.decodestring(self.dename))
            self.ePWD.set(base64.decodestring(self.depwd))
            self.f.close()
        except IOError:
            showwarning(title="出错了！",message="未保存密码")
            

    def sent(self):
        
        self.ff = Fetion(self.erec.get(),self.emsg.get(),self.eUser.get(),self.ePWD.get())
        self.answer = self.ff.SendMsg()
        self.data = self.answer.read()
        self.jdata=json.loads(self.data)
        if self.jdata['result']==0:
            self.status.set("发送状态：成功发送")
            self.lastrec=self.erec.get()
            self.emsg.set("")
            self.erec.set("")
        else:
            self.status.set("发送状态：发送失败")
    def savelog(self):

        msg2log(self.emsg.get())
def newApp():
        FetionGUI()
app = FetionGUI()
