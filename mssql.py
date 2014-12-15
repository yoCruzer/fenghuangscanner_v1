#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
import pymssql

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



def mssql_connect(ip,username,password,port):
    crack =0
    try:
        db=pymssql.connect(server=ip,port=port,user=username,password=password)
        if db:
            crack=1
    except Exception, e:
        lock.acquire()
        print "%s sql service 's %s:%s login fail " %(ip,username,password)
        lock.release()
        return crack
        pass
    return crack

def mssql():
    while True:
        ip,port=sp.get()
        flag=0
        usernames=file2list('mssql_user.txt')
        passwords=file2list('mssql_pass.txt')

        for username in usernames:
            if mssql_connect(ip,username,username,port)==1:
                    lock.acquire()
                    printGreen("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                    result.append("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                    lock.release()
                    break

            if mssql_connect(ip,username,username+'123',port)==1:
                    lock.acquire()
                    printGreen("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    result.append("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                    lock.release()
                    break

            if mssql_connect(ip,username,username+'123456',port)==1:
                    lock.acquire()
                    printGreen("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    result.append("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                    lock.release()
                    break
            if mssql_connect(ip,username,'',port)==1:
                    lock.acquire()
                    printGreen("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                    result.append("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                    lock.release()
                    break

            for password in passwords:
                    if mssql_connect(ip,username,password,port)==1:
                        lock.acquire()
                        printGreen("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        result.append("%s sql service at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        lock.release()
                        flag=1
                        break
            if flag==1:
                flag=0
                break

        sp.task_done()

def mssql_main(ipdict,threads):
    printPink("crack sql serice  now...")
    print "[*] start crack sql serice  %s" % time.ctime()
    starttime=time.time()
    global sp
    sp=Queue()
    global lock
    lock = threading.Lock()
    global result
    result=[]

    for i in xrange(threads):
        t = Thread(target=mssql)
        t.setDaemon(True)
        t.start()

    for ip in ipdict['mssql']:
        sp.put((str(ip).split(':')[0],int(str(ip).split(':')[1])))

    sp.join()

    print "[*] stop crack sql serice  %s" % time.ctime()
    print "[*] crack sql serice  done,it has Elapsed time:%s " % (time.time()-starttime)
    return result
