#coding=utf-8
import time
import re
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
import MySQLdb


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


def mysql_connect(ip,username,password,port):
    crack =0
    try:
        db=MySQLdb.connect(ip,username,password,port=port)
        if db:
            crack=1
        db.close()
    except Exception, e:
        if e[0]==1129:
            lock.acquire()
            printRed("%s has too many connect \r\n" %(ip))
            lock.release()
        if e[0]==1045:
            lock.acquire()
            print "%s mysql's %s:%s login fail " %(ip,username,password)
            lock.release()
        return crack
        pass
    return crack

def mysql():
    while True:
        ip,port=sp.get()
        flag=0
        usernames=file2list('mysql_user.txt')
        passwords=file2list('mysql_pass.txt')
        for username in usernames:
            #test mysql is allow connect
            try:
                db=MySQLdb.connect(ip,username,password,port=port)
            except Exception, e:
                #print e
                if e[0]==1130:
                    lock.acquire()
                    printRed("%s not allow to connect\r\n" %(ip))
                    lock.release()
                    break

            if mysql_connect(ip,username,username,port)==1:
                lock.acquire()
                printGreen("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                result.append("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username))
                lock.release()
                break

            if mysql_connect(ip,username,username+'123',port)==1:
                lock.acquire()
                printGreen("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                result.append("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123'))
                lock.release()
                break

            if mysql_connect(ip,username,username+'123456',port)==1:
                lock.acquire()
                printGreen("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                result.append("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,username+'123456'))
                lock.release()
                break
            if mysql_connect(ip,username,'',port)==1:
                lock.acquire()
                printGreen("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                result.append("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,''))
                lock.release()
                break

            for password in passwords:
                if mysql_connect(ip,username,password,port)==1:
                    lock.acquire()
                    printGreen("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                    result.append("%s mysql at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                    lock.release()
                    flag=1
                    break

            if flag==1:
                flag=0
                break

        sp.task_done()
def mysql_main(ipdict,threads):

    printPink("crack mysql now...")
    print "[*] start crack mysql %s" % time.ctime()
    starttime=time.time()
    global sp
    sp=Queue()
    global lock
    lock = threading.Lock()
    global result
    result=[]

    for i in xrange(threads):
        t = Thread(target=mysql)
        t.setDaemon(True)
        t.start()

    for ip in ipdict['mysql']:
        sp.put((str(ip).split(':')[0],int(str(ip).split(':')[1])))

    sp.join()

    print "[*] stop crack mysql %s" % time.ctime()
    print "[*] crack mysql done,it has Elapsed time:%s " % (time.time()-starttime)
    return result