import re
import shutil
import os
from os import listdir
import glob
import xlrd
import xlwt
import time
import sys
import pexpect
from pexpect import popen_spawn
import paramiko
# time check - start time
start_time = time.time()

rb = xlrd.open_workbook('c:/python/checkpoint/ip.xls')
sheet = rb.sheet_by_name('IPs')
num_rows = sheet.nrows
num_cols = sheet.ncols
ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]
num_ips = 0
user = 'admin'
passwd = '1q2w3e'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def ssh_connection():
        """ssh connection process"""
        try:
            ssh.connect(host, username=user, password=passwd, timeout = '3')
        except TimeoutError:
        	print('surprise motherfucker')          
                
        
def if_all():
        """ssh write commands"""
        stdin, stdout, stderr = ssh.exec_command("show interfaces all")
        interfaces = stdout.readlines()
        
        return interfaces


def if_LAN1():
        stdin, stdout, stderr = ssh.exec_command("show interface Lan1")
        LAN1 = stdout.readlines()

        return LAN1


def if_LAN2():
        stdin, stdout, stderr = ssh.exec_command("show interface Lan2")
        LAN2 = stdout.readlines()

        return LAN2



for host in ip_addr_list:
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        ssh_connection()
        all_if = if_all()
        if_LAN1 = if_LAN1()
        if_LAN2 = if_LAN2()
        file.write(''.join(all_if))
        file.write('\n')
        file.write('\n')
        file.write(''.join(if_LAN1))
        file.write('\n')
        file.write('\n')
        file.write(''.join(if_LAN2))
        file.close()

        
#for item in ip_addr_list:
#        host = ip_addr_list[0]
#        p=pexpect.fdpexpect.fdspawn('ssh admin@10.10.0.254')
#        print(host)
#    re.sub("^\s+|\n|\r|\s+$", '', str_all.decode())
#    file = open('{0}'.format(ip_addr_list[num_ips]),"wb")
#    file.write(str_all)
#    num_ips += 1
