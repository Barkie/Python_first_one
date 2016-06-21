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
#host = '10.10.0.254'
user = 'admin'
passwd = '1q2w3e'
expert_passwd = '1q2w3e'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
prompt = '\n.*> '
expert_prompt = '\n.*# '
not_found = '\n.*Invalid command:.*'
no_expert_pass = '\n.*"set expert-password".*'
wrong_expert_pass = '\n.*Wrong password.*'
enter_expert_pass = '\n.*expert password:'
#def ssh_connection():
#        """ssh connection process"""
#        try:
#            # Connect to the host
#            ssh.connect(hostname=host, username=user, password=passwd)
#            interact = SSHClientInteraction(ssh, timeout=10, display=True)
#            print('ok')
#        except TimeoutError:
#        	print('surprise motherfucker')          
#
#
#        return interact
                
        
def commands():
        """ssh write commands"""
        try:
            ssh.connect(hostname=host, username=user, password=passwd)
        except TimeoutError:
            print('surprise motherfucker, host is down')
        interact = SSHClientInteraction(ssh, timeout=10, display=True)\
        print('connected')
        interact.send(item)
        found_index = interact.expect([not_found, prompt])
        if found_index == 0:
            print('command not found, trying expert mode')
            interact.send('expert')
            entering_expert_index = interact.expect([no_expert_pass, enter_expert_pass])
            if entering_expert_index == 0:
                print('no expert password, need to set it')
                no_expert_output = interact.current_output_clean
                # something here to write to file
            elif entering_expert_index == 1:
                print('cp asked for expert password, entering it')
                interact.send(expert_passwd)
                expert_mode_index([wrong_expert_pass, expert_prompt])
                if expert_mode_index == 0:
                    print('wrong expert pass')
                    #something here to write to file
                elif expert_mode_index == 1:
                    print('password ok, continuing')
            interact.send(i)
            interact.expect(expert_prompt)
            interact.send('exit')
            interact.expect(prompt)




for host in ip_addr_list:
        print(host)
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
#        ssh_connection()
        commands()
        file.close()

        
#for item in ip_addr_list:
#        host = ip_addr_list[0]
#        p=pexpect.fdpexpect.fdspawn('ssh admin@10.10.0.254')
#        print(host)
#    re.sub("^\s+|\n|\r|\s+$", '', str_all.decode())
#    file = open('{0}'.format(ip_addr_list[num_ips]),"wb")
#    file.write(str_all)
#    num_ips += 1
