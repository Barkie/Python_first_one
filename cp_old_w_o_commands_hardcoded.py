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
prompt = '.*> '
expert_prompt = '.*# '
not_found = '.*Invalid command:.*'
no_expert_pass = '.*"set expert-password".*'
wrong_expert_pass = '.*Wrong password.*'
enter_expert_pass = '.*expert password:'
def ssh_connection():
        """ssh connection process"""
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        print(host + ' connecting')
        try:
            # Connect to the host
            ssh.connect(hostname=host, username=user, password=passwd)
        except:
                file.write('host ' + host + ' is DOWN. SSH is not possible')
                print('surprise motherfucker')
        interact = SSHClientInteraction(ssh, timeout=20, display=True)
        for item in commands_list:
                answer = commands(item)
        print('ok')
        file.close()

                
        
def commands(i):
        """ssh write commands"""
        print('sending command')
        answer = ''
        interact.send(i)
        print('command sended, expecting results')
        found_index = interact.expect([not_found, prompt])
        if found_index == 0:
            print('command not found, trying expert mode')
            interact.send('expert')
            entering_expert_index = interact.expect([no_expert_pass, enter_expert_pass])
            if entering_expert_index == 0:
                print('no expert password, need to set it')
#                no_expert_output = interact.current_output_clean
#                if no_expert_output:
#                    answer = answer + no_expert_output
                # something here to write to file
            elif entering_expert_index == 1:
                print('cp asked for expert password, entering it')
                interact.send(expert_passwd)
                expert_mode_index = ([wrong_expert_pass, expert_prompt])
                if expert_mode_index == 0:
                    print('wrong expert pass')
#                    wrong_expert_pass_output = interact.current_output_clean
#                    if wrong_expert_pass_output:
#                        answer = answer + wrong_expert_pass_output
                    #something here to write to file
                elif expert_mode_index == 1:
                    print('password ok, continuing')
                    interact.send(i)
                    interact.expect(expert_prompt)
                    interact.send('\n')
                    interact.expect(expert_prompt)
                    exp_cmd_output = interact.current_output_clean
            if exp_cmd_output:
                answer = '\n' + '\n---------------------------------' + '\n' + i + '\n' + answer + '\n' + exp_cmd_output
                interact.send('exit')
                interact.expect(prompt)
        elif found_index == 1:
            cmd_output = interact.current_output_clean
            if cmd_output:
                answer = '\n' + '\n---------------------------------' + '\n' + i + '\n' +answer + '\n' + cmd_output
        print('ANSWER_START' + answer + 'ANSWER_END')
                     
            
        return answer




for host in ip_addr_list:
        ssh_connection()

        
#for item in ip_addr_list:
#        host = ip_addr_list[0]
#        p=pexpect.fdpexpect.fdspawn('ssh admin@10.10.0.254')
#        print(host)
#    re.sub("^\s+|\n|\r|\s+$", '', str_all.decode())
#    file = open('{0}'.format(ip_addr_list[num_ips]),"wb")
#    file.write(str_all)
#    num_ips += 1
