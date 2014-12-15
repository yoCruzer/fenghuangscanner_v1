#coding=utf-8
__author__ = 'wilson'
import ctypes,sys
import argparse
import socket
import time
import re
import platform
import threading
from threading import Thread
from lib.printers import printPink,printRed,printGreen
from Queue import Queue
try:
    from subprocess import Popen, PIPE
    lowversion=False
except:
    lowversion=True

from mysql import mysql_main
from mssql import mssql_main
from ftp import ftp_main
from smb import smb_main
from ssh import ssh_main
from telnet import telnet_main
import _mssql
import uuid

socket.setdefaulttimeout(5)  #设置了全局默认超时时间
#变量定义
posts=[21,22,23,25,53,80,81,110,135,139,389,443,445,873,1043,1433,1434,1521,3306,3307,3389,4848,5800,5900,8080,8090,22022,22222,27017,28017]
PROBES=[
    '\r\n\r\n',
    'GET / HTTP/1.0\r\n\r\n',
    'GET / \r\n\r\n',
    '\x01\x00\x00\x00\x01\x00\x00\x00\x08\x08',
    '\x80\0\0\x28\x72\xFE\x1D\x13\0\0\0\0\0\0\0\x02\0\x01\x86\xA0\0\x01\x97\x7C\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0',
    '\x03\0\0\x0b\x06\xe0\0\0\0\0\0',
    '\0\0\0\xa4\xff\x53\x4d\x42\x72\0\0\0\0\x08\x01\x40\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x40\x06\0\0\x01\0\0\x81\0\x02PC NETWORK PROGRAM 1.0\0\x02MICROSOFT NETWORKS 1.03\0\x02MICROSOFT NETWORKS 3.0\0\x02LANMAN1.0\0\x02LM1.2X002\0\x02Samba\0\x02NT LANMAN 1.0\0\x02NT LM 0.12\0',
    '\x80\x9e\x01\x03\x01\x00u\x00\x00\x00 \x00\x00f\x00\x00e\x00\x00d\x00\x00c\x00\x00b\x00\x00:\x00\x009\x00\x008\x00\x005\x00\x004\x00\x003\x00\x002\x00\x00/\x00\x00\x1b\x00\x00\x1a\x00\x00\x19\x00\x00\x18\x00\x00\x17\x00\x00\x16\x00\x00\x15\x00\x00\x14\x00\x00\x13\x00\x00\x12\x00\x00\x11\x00\x00\n\x00\x00\t\x00\x00\x08\x00\x00\x06\x00\x00\x05\x00\x00\x04\x00\x00\x03\x07\x00\xc0\x06\x00@\x04\x00\x80\x03\x00\x80\x02\x00\x80\x01\x00\x80\x00\x00\x02\x00\x00\x01\xe4i<+\xf6\xd6\x9b\xbb\xd3\x81\x9f\xbf\x15\xc1@\xa5o\x14,M \xc4\xc7\xe0\xb6\xb0\xb2\x1f\xf9)\xe8\x98',
    '\x16\x03\0\0S\x01\0\0O\x03\0?G\xd7\xf7\xba,\xee\xea\xb2`~\xf3\0\xfd\x82{\xb9\xd5\x96\xc8w\x9b\xe6\xc4\xdb<=\xdbo\xef\x10n\0\0(\0\x16\0\x13\0\x0a\0f\0\x05\0\x04\0e\0d\0c\0b\0a\0`\0\x15\0\x12\0\x09\0\x14\0\x11\0\x08\0\x06\0\x03\x01\0',
    '< NTP/1.2 >\n',
    '< NTP/1.1 >\n',
    '< NTP/1.0 >\n',
    '\0Z\0\0\x01\0\0\0\x016\x01,\0\0\x08\0\x7F\xFF\x7F\x08\0\0\0\x01\0 \0:\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\04\xE6\0\0\0\x01\0\0\0\0\0\0\0\0(CONNECT_DATA=(COMMAND=version))',
    '\x12\x01\x00\x34\x00\x00\x00\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x0c\x03\x00\x28\x00\x04\xff\x08\x00\x01\x55\x00\x00\x00\x4d\x53\x53\x51\x4c\x53\x65\x72\x76\x65\x72\x00\x48\x0f\x00\x00',
    '\0\0\0\0\x44\x42\x32\x44\x41\x53\x20\x20\x20\x20\x20\x20\x01\x04\0\0\0\x10\x39\x7a\0\x01\0\0\0\0\0\0\0\0\0\0\x01\x0c\0\0\0\0\0\0\x0c\0\0\0\x0c\0\0\0\x04',
    '\x01\xc2\0\0\0\x04\0\0\xb6\x01\0\0\x53\x51\x4c\x44\x42\x32\x52\x41\0\x01\0\0\x04\x01\x01\0\x05\0\x1d\0\x88\0\0\0\x01\0\0\x80\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x08\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x01\0\0\x40\0\0\0\x40\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x02\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x08\0\0\0\x01\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\x01\x04\0\0\x01\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x20\x20\x20\x20\x20\x20\x20\x20\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\xff\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\xe4\x04\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x7f',
    '\x41\0\0\0\x3a\x30\0\0\xff\xff\xff\xff\xd4\x07\0\0\0\0\0\0test.$cmd\0\0\0\0\0\xff\xff\xff\xff\x1b\0\0\0\x01serverStatus\0\0\0\0\0\0\0\xf0\x3f\0'
    ]

SIGNS=[
    'http|^HTTP.*',
    'ssh|SSH-2.0-OpenSSH.*',
    'ssh|SSH-1.0-OpenSSH.*',
    'netbios|^\x79\x08.*BROWSE',
    'netbios|^\x79\x08.\x00\x00\x00\x00',
    'netbios|^\x05\x00\x0d\x03',
    'netbios|^\x83\x00',
    'netbios|^\x82\x00\x00\x00',
    'netbios|\x83\x00\x00\x01\x8f',
    'backdoor-fxsvc|^500 Not Loged in',
    'backdoor-shell|GET: command',
    'backdoor-shell|sh: GET:',
    'bachdoor-shell|[a-z]*sh: .* command not found',
    'backdoor-shell|^bash[$#]',
    'backdoor-shell|^sh[$#]',
    'backdoor-cmdshell|^Microsoft Windows .* Copyright .*>',
    'dell-openmanage|^\x4e\x00\x0d',
    'finger|^\r\n	Line	  User',
    'finger|Line	 User',
    'finger|Login name: ',
    'finger|Login.*Name.*TTY.*Idle',
    'finger|^No one logged on',
    'finger|^\r\nWelcome',
    'finger|^finger:',
    'finger|^must provide username',
    'finger|finger: GET: ',
    'ftp|^220.*\n331',
    'ftp|^220.*\n530',
    'ftp|^220.*FTP',
    'ftp|^220 .* Microsoft .* FTP',
    'ftp|^220 Inactivity timer',
    'ftp|^220 .* UserGate',
    'ftp|^220(.*?)',
    'http|^HTTP/0.',
    'http|^HTTP/1.',
    'http|<HEAD>.*<BODY>',
    'http|<HTML>.*',
    'http|<html>.*',
    'http|<!DOCTYPE.*',
    'http|^Invalid requested URL ',
    'http|.*<?xml',
    'http|^HTTP/.*\nServer: Apache/1',
    'http|^HTTP/.*\nServer: Apache/2',
    'http-iis|.*Microsoft-IIS',
    'http-iis|^HTTP/.*\nServer: Microsoft-IIS',
    'http-iis|^HTTP/.*Cookie.*ASPSESSIONID',
    'http-iis|^<h1>Bad Request .Invalid URL.</h1>',
    'http-jserv|^HTTP/.*Cookie.*JServSessionId',
    'http-tomcat|^HTTP/.*Cookie.*JSESSIONID',
    'http-weblogic|^HTTP/.*Cookie.*WebLogicSession',
    'http-vnc|^HTTP/.*VNC desktop',
    'http-vnc|^HTTP/.*RealVNC/',
    'ldap|^\x30\x0c\x02\x01\x01\x61',
    'ldap|^\x30\x32\x02\x01',
    'ldap|^\x30\x33\x02\x01',
    'ldap|^\x30\x38\x02\x01',
    'ldap|^\x30\x84',
    'ldap|^\x30\x45',
    'smb|^\0\0\0.\xffSMBr\0\0\0\0.*',
    'msrdp|^\x03\x00\x00\x0b',
    'msrdp|^\x03\x00\x00\x11',
    'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x12.\0$',
    'msrdp|^\x03\0\0\x17\x08\x02\0\0Z~\0\x0b\x05\x05@\x06\0\x08\x91J\0\x02X$',
    'msrdp|^\x03\0\0\x11\x08\x02..}\x08\x03\0\0\xdf\x14\x01\x01$',
    'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x03.\0$',
    'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\0\0\0',
    'msrdp|^\x03\0\0\x0e\t\xd0\0\0\0[\x02\xa1]\0\xc0\x01\n$',
    'msrdp|^\x03\0\0\x0b\x06\xd0\0\x004\x12\0',
    'msrdp-proxy|^nmproxy: Procotol byte is not 8\n$',
    'msrpc|^\x05\x00\x0d\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
    'msrpc|\x05\0\r\x03\x10\0\0\0\x18\0\0\0....\x04\0\x01\x05\0\0\0\0$',
    'mssql|^\x04\x01\0C..\0\0\xaa\0\0\0/\x0f\xa2\x01\x0e.*',
    'mssql|^\x05\x6e\x00',
    'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
    'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
    'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
    'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
    'mssql|^\x04\x01\0\x25\0\0\x01\0\0\0\x15\0\x06\x01.*',
    'mssql|^\x04\x01\x00\x25\x00\x00\x01.*',
    'mysql|^\x19\x00\x00\x00\x0a',
    'mysql|^\x2c\x00\x00\x00\x0a',
    'mysql|hhost \'',
    'mysql|khost \'',
    'mysql|mysqladmin',
    'mysql|whost \'',
    'mysql|^\(\x00\x00',
    'mysql|this MySQL',
    'mysql|^N\x00',
    'mssql|;MSSQLSERVER;',
    'mongodb|^.*version.....([\.\d]+)',
    'nagiosd|Sorry, you \(.*are not among the allowed hosts...',
    'nessus|< NTP 1.2 >\x0aUser:',
    'oracle-tns-listener|\(ERROR_STACK=\(ERROR=\(CODE=',
    'oracle-tns-listener|\(ADDRESS=\(PROTOCOL=',
    'oracle-dbsnmp|^\x00\x0c\x00\x00\x04\x00\x00\x00\x00',
    'oracle-https|^220- ora',
    'oracle-rmi|\x00\x00\x00\x76\x49\x6e\x76\x61',
    'oracle-rmi|^\x4e\x00\x09',
    'postgres|Invalid packet length',
    'postgres|^EFATAL',
    'rlogin|login: ',
    'rlogin|rlogind: ',
    'rlogin|^\x01\x50\x65\x72\x6d\x69\x73\x73\x69\x6f\x6e\x20\x64\x65\x6e\x69\x65\x64\x2e\x0a',
    'rpc-nfs|^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
    'rpc|\x01\x86\xa0',
    'rpc|\x03\x9b\x65\x42\x00\x00\x00\x01',
    'rpc|^\x80\x00\x00',
    'rsync|^@RSYNCD:.*',
    'smux|^\x41\x01\x02\x00',
    'snmp-public|\x70\x75\x62\x6c\x69\x63\xa2',
    'snmp|\x41\x01\x02',
    'socks|^\x05[\x00-\x08]\x00',
    'ssh|^SSH-',
    'ssh|^SSH-.*openssh',
    'ssl|^..\x04\0.\0\x02',
    'ssl|^\x16\x03\x01..\x02...\x03\x01',
    'ssl|^\x16\x03\0..\x02...\x03\0',
    'ssl|SSL.*GET_CLIENT_HELLO',
    'ssl|-ERR .*tls_start_servertls',
    'ssl|^\x16\x03\0\0J\x02\0\0F\x03\0',
    'ssl|^\x16\x03\0..\x02\0\0F\x03\0',
    'ssl|^\x15\x03\0\0\x02\x02\.*',
    'ssl|^\x16\x03\x01..\x02...\x03\x01',
    'ssl|^\x16\x03\0..\x02...\x03\0',
    'sybase|^\x04\x01\x00',
    'telnet|^\xff\xfd',
    'telnet-disabled|Telnet is disabled now',
    'telnet|^\xff\xfe',
    'telnet|^xff\xfb\x01\xff\xfb\x03\xff\xfb\0\xff\xfd.*',

    'tftp|^\x00[\x03\x05]\x00',
    'http-tomcat|.*Servlet-Engine',
    'uucp|^login: password: ',
    'vnc|^RFB.*',
    'webmin|.*MiniServ',
    'webmin|^0\.0\.0\.0:.*:[0-9]',
    'websphere-javaw|^\x15\x00\x00\x00\x02\x02\x0a',
    'db2|.*SQLDB2RA']


#获取ip列表函数
def getips(ip):
    if ip:
        if re.findall('^\d+\.\d+\.\d+\.(.*)$', ip):
                ips = []
                ip_pre = ""
                try:
                    for pre in ip.split('.')[0:3]:
                        ip_pre = ip_pre + pre + '.'
                    start=int(ip.split('.')[3].split('-')[0])
                    end=int(ip.split('.')[3].split('-')[1])
                    for i in range(start, end):
                        ips.append(ip_pre + str(i))
                    return ips
                except:
                    printRed("[!] not a valid ip given. you should put ip like 192.168.1.1-253")
                    exit()
        else:
            printRed("[!] not a valid ip given. you should put ip like 192.168.1.1-253")
            exit()

#ping扫描函数
def pinger():
    global lock

    while True:
        global pinglist
        ip=q.get()
        if platform.system()=='Linux':
            p=Popen(['ping','-c 2',ip],stdout=PIPE)
            m = re.search('(\d)\sreceived', p.stdout.read())
            try:
                if m.group(1)!='0':
                    pinglist.append(ip)
                    lock.acquire()
                    printRed("%s is live!!\r\n" % ip)
                    lock.release()
            except:pass

        if platform.system()=='Windows':
            p=Popen('ping -n 2 ' + ip, stdout=PIPE)
            m = re.findall('TTL', p.stdout.read())
            if m:
                pinglist.append(ip)
                lock.acquire()
                printRed("%s is live!!\r\n" % ip)
                lock.release()
        q.task_done()


#扫端口及其对应服务类型函数
def scanports():
    global signs,lock
    while True:
        ip,port=sp.get()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #定义超时时间 5秒
        s.settimeout(5)
        #判断端口的服务类型
        service='Unknown'
        try:
            s.connect((ip,port))
        except:
            sp.task_done()
            continue

        try:
            result = s.recv(256)
            service=matchbanner(result,signs)
        except:
            for probe in PROBES:
                try:
                    s.close()
                    sd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sd.settimeout(5)
                    sd.connect((ip,port))
                    sd.send(probe)
                except:
                    continue
                try:
                    result=sd.recv(256)
                    service=matchbanner(result,signs)
                    if service!='Unknown':
                        break
                except:
                    continue
        if service not in ipdict:
            ipdict[service]=[]
            ipdict[service].append(ip+':'+str(port))
            lock.acquire()
            printRed("%s opening %s\r\n" %(ip,port))
            lock.release()
        else:
            ipdict[service].append(ip+':'+str(port))
            lock.acquire()
            printRed("%s opening %s\r\n" %(ip,port))
            lock.release()

        sp.task_done()


def prepsigns():
    signlist=[]
    for item in SIGNS:
        (label,pattern)=item.split('|',2)
        sign=(label,pattern)
        signlist.append(sign)
    return signlist

def matchbanner(banner,slist):
    for item in slist:
        p=re.compile(item[1])
        if p.search(banner)!=None:
            return item[0]
    return 'Unknown'

def write_file(file,contents):
    f2 = open(file,'a')
    f2.write(contents)
    f2.close()



if __name__ == '__main__':
    #接受cmd参数
    parser = argparse.ArgumentParser(description='ports&*weak password scanner. teams:t00ls&&xdsec.  author: wilson ')
    parser.add_argument('--ip',action="store",required=True,dest="ip",type=str,help='ip like 192.168.1.1-254')
    parser.add_argument('--f',action="store",required=True,dest="path",type=str,help='get you results in this file')
    parser.add_argument("--threads",action="store",required=False,dest="threads",type=int,default=50,help='Maximum threads, default 50')
    parser.add_argument("--P",action="store",required=False,dest="isping",type=str,default='yes',help='--P not mean no ping frist,default yes')

    args = parser.parse_args()
    ip = args.ip
    file=args.path
    threads=args.threads
    isping=args.isping



    #获取ip列表
    ips=getips(ip)


    print "Scanning for live machines..."
    starttime=time.time()
    friststarttime=time.time()
    print "[*] start Scanning at %s" % time.ctime()
    #isping=='no' 就禁ping扫描
    #默认ping 扫描
    if isping=='yes':
        if lowversion==True:
            print "your python may not support ping ,please update python to 2.7"
            exit()
        pinglist=[]
        q=Queue()
        lock = threading.Lock()

        for i in xrange(threads):
            t = Thread(target=pinger)
            t.setDaemon(True)
            t.start()

        for ip in ips:
            q.put(ip)
        q.join()

    else:
        pinglist=ips

    if len(pinglist)==0:
        print "not find any live machine - -|||"
        exit()

    print "[*] Scanning for live machines done,it has Elapsed time:%s " % (time.time()-starttime)


#=========================我是分割线=============================================#

#多线程扫描端口，并且识别出端口是什么类型服务
    print "Scanning ports now..."
    print "[*] start Scanning live machines' ports at %s" % time.ctime()
    starttime=time.time()
    sp=Queue()
    lock = threading.Lock()
    #signs 匹配端口对应的服务
    global signs
    signs=prepsigns()

    #端口对应服务  放到一个ipdict[service]字典中
    global ipdict
    ipdict={}

    for i in xrange(threads):
        st=Thread(target=scanports)
        st.setDaemon(True)
        st.start()

    for scanip in pinglist:
        for port in posts:
            sp.put((scanip,port))
    sp.join()

    print "[*] Scanning ports done,it has Elapsed time:%s " % (time.time()-starttime)

    #将服务端口 信息 记录文件
    for name in ipdict.keys():
        contents=str(name)+' service has:\n'+'       '+str(ipdict[name])+'\n'
        write_file(contents=contents,file=file)

#=========================我是分割线=============================================#

    result={}
    write_file(contents='\r\nweaken password:\n',file=file)

    for name in ipdict.keys():
#多线程爆破mysql弱口令
        if name=='mysql':
            result['mysql']=mysql_main(ipdict,threads)
#多线程爆破mssql弱口令
        if name=='mssql':
            result['mssql']=mssql_main(ipdict,threads)
#多线程爆破ftp弱口令
        if name=='ftp':
            result['ftp']=ftp_main(ipdict,threads)
#多线程爆破smb弱口令
        if name=='smb':
            result['smb']=smb_main(ipdict,threads)
#多线程爆破ssh弱口令
        if name=='ssh':
            result['ssh']=ssh_main(ipdict,threads)

#多线程爆破telnet弱口令 telnet 没有处理好 速度慢 出错率高
        #if name=='telnet':
            #result['telnet']=ssh_main(ipdict,threads)


    printRed("[*] all has done at %s" % time.ctime())
    printRed("[*] all has done,it has Elapsed time:%s \r\n" % (time.time()-friststarttime))

    #将弱口令 信息 记录文件

    if len(result)!=0:
        for name in result.keys():
                for i in xrange(len(result[name])):
                    write_file(contents=result[name][i],file=file)
    else:
        write_file(contents='no weaken password = =|||',file=file)

    printRed("I have put all you want into %s" % file)