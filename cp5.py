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
import paramiko_expect
import traceback
from paramiko_expect import SSHClientInteraction
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
prompt = 'test-checkpoint-for-scripts>'
def ssh_connection():
        """ssh connection process"""
        try:
            # Connect to the host
            ssh.connect(hostname=host, username=user, password=passwd)
            interact = SSHClientInteraction(ssh, timeout=10, display=True)
            print('ok')
        except TimeoutError:
        	print('surprise motherfucker')          
                
        
def commands():
        """ssh write commands"""
        interact = SSHClientInteraction(ssh, timeout=10, display=True)
        interact.send('lock database override')
        interact.expect('\n.*> ')
        interact.send('fw tab -t connections -s')
        print('sended IF, expecting >')
        interact.expect('\n.*> ')
        print('ok!')
        cmd_output_uname = interact.current_output_clean
        print(cmd_output_uname)
#        time.sleep(25)
#        output = stdout.readlines()
#        print('current output', output)
#        
#        return output
ssh.connect(hostname=host, username=user, password=passwd)
prompt = 'trevor@test-deb-morgan:~$'
interact = SSHClientInteraction(ssh, timeout=10, display=True)
#interact.expect('>')
interact.send('show interface External')
#interact.send('>')
print('sended IF, expecting >')
interact.expect('\n.*> ')
interact.send('fw tab -t connections -s')
interact.expect('.*> ')
cmd_output_uname = interact.current_output
print(cmd_output_uname)
print('ok!')
#print(cmd_output_uname)

#ssh_connection()
#commands()

#for host in ip_addr_list:
#        print(host)
#        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
#        print('started connection')
#        ssh_connection()
#        commands()
        #print('connected')
        #for item in commands_list:
        #        print('current command', item)
        #        result = commands()
        #        print('current result', result)
        #        file.write(''.join(result))
#        file.close()

        
#for item in ip_addr_list:
#        host = ip_addr_list[0]
#        p=pexpect.fdpexpect.fdspawn('ssh admin@10.10.0.254')
#        print(host)
#    re.sub("^\s+|\n|\r|\s+$", '', str_all.decode())
#    file = open('{0}'.format(ip_addr_list[num_ips]),"wb")
#    file.write(str_all)
#    num_ips += 1
