#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
from impacket import smb
from impacket.smbconnection import *
from impacket.smb3structs import *

def file2list(filename):
    try:
        list=[]
        d=open(filename,'r')
        data=d.readline().strip('\r\n')
        while(data):
            list.append(data)
            data=d.readline().strip('\r\n')
    except Exception,e:
        if e[0]==2:
            lock.acquire()
            printRed("not such file:%s\r\n" %filename)
            lock.release()
    return list

def smb_connect(ip,username,password):
    crack =0
    try:
        smb = SMBConnection('*SMBSERVER', ip)
        smb.login(username,password)
        smb.logoff()
        crack =1
    except Exception, e:
        lock.acquire()
        print "%s smb 's %s:%s login fail " %(ip,username,password)
        lock.release()
        return crack
        pass

    return crack

def smb():
    while True:
        ip,port=sp.get()
        flag=0
        usernames=file2list('smb_user.txt')
        passwords=file2list('smb_pass.txt')

        for username in usernames:
            if smb_connect(ip,username,username)==1:
                    lock.acquire()
                    printGreen("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                    result.append("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                    lock.release()
                    break

            if smb_connect(ip,username,username+'123')==1:
                    lock.acquire()
                    printGreen("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    result.append("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    lock.release()
                    break

            if smb_connect(ip,username,username+'123456')==1:
                    lock.acquire()
                    printGreen("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    result.append("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    lock.release()
                    break
            if smb_connect(ip,username,'')==1:
                    lock.acquire()
                    printGreen("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,username,''))
                    result.append("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                    lock.release()
                    break

            for password in passwords:
                    if smb_connect(ip,username,password)==1:
                        lock.acquire()
                        printGreen("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        result.append("%s smb at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        lock.release()
                        flag=1
                        break
            if flag==1:
                flag=0
                break

        sp.task_done()

def smb_main(ipdict,threads):

    printPink("crack smb  now...")
    print "[*] start crack smb serice  %s" % time.ctime()
    starttime=time.time()
    global sp
    sp=Queue()
    global lock
    lock = threading.Lock()
    global result
    result=[]

    for i in xrange(threads):
        t = Thread(target=smb)
        t.setDaemon(True)
        t.start()

    for ip in ipdict['smb']:
        sp.put((str(ip).split(':')[0],int(str(ip).split(':')[1])))

    sp.join()

    print "[*] stop smb serice  %s" % time.ctime()
    print "[*] crack smb  done,it has Elapsed time:%s " % (time.time()-starttime)
    return result