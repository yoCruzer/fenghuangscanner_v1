#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
import telnetlib


usernames=[
 'administrator',
 'root',
 'wilson',
 'test',
 'web',
 'www',
 'nobody',
]

passwords=[
    '',
    '1',
    '12',
    '123',
    '1234',
    '12345',
    '123456',
    '1234567',
    '12345678',
    '123456789',
    '1234567890',
    '654321',
    '54321',
    '00000000',
    '88888888',
    'pass',
    'password',
    'passwd',
    '!@#$%^',
    '1q2w3e',
    'qawsed',
    'pwd',
    '1qaz2ws3e4',
    'qazwsxedc',
    '!@#$%^&*',

]

def telnet_test_login(ip,password,username,port):
    crack=0
    tn = telnetlib.Telnet(ip,port=port,timeout=5)
    tn.read_until("login: ")
    tn.write(username+ '\r')
    #等一会再 输入密码
    time.sleep(3)
    #需要接受一下输出 - -|||
    tn.read_very_eager()
    tn.write(password + "\r")
    #等一会再 接受数据
    time.sleep(4)
    msg=tn.read_some()
    tn.close()
    #判断msg是不是login fail 或者error
    if msg.strip()=='':
        lock.acquire()
        print "%s telnet's %s:%s login fail " %(ip,username,password)
        lock.release()
    if re.search("(.*?)fail",msg,re.I):
        lock.acquire()
        print "%s telnet's %s:%s login fail " %(ip,username,password)
        lock.release()
    else:
        if re.search("(.*?)incorrect",msg,re.I):
            lock.acquire()
            print "%s telnet's %s:%s login fail " %(ip,username,password)
            lock.release()
        else:
            lock.acquire()
            printGreen("%s telnet has weaken password!!-------%s:%s\r\n" %(ip,username,password))
            result.append("%s telnet has weaken password!!-------%s:%s\r\n" %(ip,username,password))
            lock.release()
            crack=1
        return crack

def telnet():
    while True:
        ip,port=sp.get()
        flag=0
        try:
            #弱口令爆破
            for username in usernames:
                if telnet_test_login(ip,username,username,port)==1:
                    break
                if telnet_test_login(ip,username+'123',username,port)==1:
                    break
                if telnet_test_login(ip,username+'123456',username,port)==1:
                    break
                for password in passwords:
                    tn = telnetlib.Telnet(ip,port=port,timeout=5)
                    tn.read_until("login: ")
                    tn.write(username+ '\r')
                    #等一会再 输入密码
                    time.sleep(3)
                    #需要接受一下输出 - -|||
                    tn.read_very_eager()
                    tn.write(password + "\r")
                    #等一会再 接受数据
                    time.sleep(4)
                    msg=tn.read_some()
                    tn.close()

                    if msg.strip()=='':
                        lock.acquire()
                        print "%s telnet's %s:%s login fail " %(ip,username,password)
                        lock.release()						
                    #判断msg是不是login fail 或者error
                    if re.search("(.*?)fail",msg,re.I):
                        lock.acquire()
                        print "%s telnet's %s:%s login fail " %(ip,username,password)
                        lock.release()
                    else:
                        if re.search("(.*?)incorrect",msg,re.I):
                            lock.acquire()
                            print "%s telnet's %s:%s login fail " %(ip,username,password)
                            lock.release()
                        else:
                            lock.acquire()
                            printGreen("%s telnet has weaken password!!-------%s:%s\r\n" %(ip,username,password))
                            result.append("%s telnet has weaken password!!-------%s:%s\r\n" %(ip,username,password))
                            lock.release()
                            flag=1
                            break
                if flag == 1:
                    flag=0
                    break

        except Exception,e:
            printPink(e)

        sp.task_done()
def telnet_main(ipdict,threads):
    if len(ipdict['telnet'])!=0:
        printPink("crack telnet  now...")
        print "[*] start crack telnet %s" % time.ctime()
        starttime=time.time()
        global sp
        sp=Queue()
        global lock
        crack=0
        lock = threading.Lock()
        global result
        result=[]
        for i in xrange(threads):
            t = Thread(target=telnet)
            t.setDaemon(True)
            t.start()

        for ip in ipdict['telnet']:
            sp.put((str(ip).split(':')[0],str(ip).split(':')[1]))

        sp.join()
        print "[*] stop crack telnet %s" % time.ctime()
        print "[*] crack telnet done,it has Elapsed time:%s " % (time.time()-starttime)
        return result