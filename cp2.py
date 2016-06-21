import re
import shutil
import os
from os import listdir
import glob
import xlrd
import xlwt
import time
import sys
import winpexpect
import paramiko

# time check - start time
start_time = time.time()

iprb = xlrd.open_workbook('c:/python/checkpoint/ip.xls')
sheet = iprb.sheet_by_name('IPs')
num_rows = sheet.nrows
num_cols = sheet.ncols
cmrb = xlrd.open_workbook('c:/python/checkpoint/commands.xls')
sheet1 = cmrb.sheet_by_name('commands')
num_rows1 = sheet1.nrows
num_cols1 = sheet1.ncols

ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]
commands_list = [sheet1.row_values(rawnum)[0] for rawnum in range(sheet1.nrows)]
num_ips = 0
host = '10.10.0.254'
user = 'admin'
passwd = '1q2w3e'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


px = winpexpect.winspawn('c:/python/openssh/bin/ssh.exe ' + user + '@' + host)
fout = open('c:/python/checkpoint/{0}++.txt'.format(host),"w")
px.logfile_read = fout
px.timeout = 35
px.expect('authorized use only.')
px.sendline(passwd)
#create log file with in IP.txt format (10.1.1.1.txt, for example)
fout = open('c:/python/checkpoint/{0}++.txt'.format(host),"wb")
#push pexpect logfile_read output to log file
px.sendline('\n')
px.sendline('\n')
px.sendline('show interfaces all\n')
px.sendline('\n')

        
#for item in ip_addr_list:
#        host = ip_addr_list[0]
#        p=pexpect.fdpexpect.fdspawn('ssh admin@10.10.0.254')
#        print(host)
#    re.sub("^\s+|\n|\r|\s+$", '', str_all.decode())
#    file = open('{0}'.format(ip_addr_list[num_ips]),"wb")
#    file.write(str_all)
#    num_ips += 1
