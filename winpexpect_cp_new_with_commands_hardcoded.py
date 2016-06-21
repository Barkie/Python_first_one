import traceback
import xlrd
import xlwt
import sys
import os
import glob
import time
import shutil
import re
import winpexpect

WIDTH_CONST = 256
widths = 13, 24
headers = (
    'IP_Addr', 'Status')
wb = xlwt.Workbook()
ws = wb.add_sheet('IP LIST', cell_overwrite_ok=True)
# set width
for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width
# writing first row
for index, header in enumerate(headers):
    ws.write(0, index, header)

iprb = xlrd.open_workbook('c:/python/checkpoint/ip.xls')
sheet = iprb.sheet_by_name('IPs')
num_rows = sheet.nrows
num_cols = sheet.ncols
ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]
user_file = open('c:/python/checkpoint/auth_login.txt')
user = user_file.read()
passwd_file = open('c:/python/checkpoint/auth_passwd.txt')
passwd = passwd_file.read()
expert_passwd_file = open('c:/python/checkpoint/auth_expert_passwd.txt')
expert_passwd = expert_passwd_file.read()

prompt = '.*> '
expert_prompt = '.*# '
not_found = '.*Invalid command:.*'
no_expert_pass = '.*"set expert-password".*'
wrong_expert_pass = '.*Wrong password.*'
enter_expert_pass = '.*expert password:'
sk1 = '\n\n\n---------------------------------------------\n'

def main(i):
    # Use SSH client to login
    try:
        # Create a new SSH client object
        ssh = paramiko.SSHClient()

        # Set SSH key parameters to auto accept unknown hosts
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        # Connect to the host
        ssh.connect(hostname=host, username=user, password=passwd)

        # Create a client interaction class which will interact with the host
        interact = SSHClientInteraction(ssh, timeout=5, display=True)
        interact.expect(prompt)

        # Run the first command and capture the cleaned output, if you want
        # the output without cleaning, simply grab current_output instead.
        interact.send('netstat -rnv')
        interact.expect(prompt)
        route_list = 'netstat -rnv \n' + interact.current_output_clean

        # Now let's do the same for the ls command but also set a timeout for
        # this specific expect (overriding the default timeout)
        #interact.send('ls -l /')
        #interact.expect(prompt, timeout=5)
        #cmd_output_ls = interact.current_output_clean
        interact.send('expert')
        entering_expert_index = interact.expect([no_expert_pass, enter_expert_pass])
        if entering_expert_index == 0:
            print('no expert password, need to set it')
            no_expert_password = interact.current_output_clean
            set_expert_pass = no_expert_password
            file.write(set_expert_pass)
            file.close()
            ws.write(i, 1, 'No Expert Password. Need to set up.')
            i += 1
        elif entering_expert_index == 1:
            print('cp asked for expert password, entering it')
            interact.send(expert_passwd)
            expert_mode_index = interact.expect([wrong_expert_pass, expert_prompt])
            if expert_mode_index == 0:
                print('wrong expert pass')
                wrong_expert_pass_output = interact.current_output_clean                
                file.write(wrong_expert_pass_output)
                file.close()
                ws.write(i, 1, 'Wrong Expert Password')
                i += 1
            elif expert_mode_index == 1:
                print('password ok, continuing')
                interact.send('cat /etc/sysconfig/netconf.C')
                interact.expect(expert_prompt)
                netconf = 'cat /etc/sysconfig/netconf.C \n' + interact.current_output_clean
                
                interact.send('cat /etc/hosts.allow')
                interact.expect(expert_prompt)
                hosts = 'cat /etc/hosts.allow \n' + interact.current_output_clean

                interact.send('cat /etc/hosts')
                interact.expect(expert_prompt)
                hosts1 = 'cat /etc/hosts \n' + interact.current_output_clean

                interact.send('cat /etc/passwd')
                interact.expect(expert_prompt)
                passwords = 'cat /etc/passwd \n' + interact.current_output_clean\

                interact.send('cat /etc/resolv.conf')
                interact.expect(expert_prompt)
                resolv = 'cat /etc/resolv.conf \n' + interact.current_output_clean

                interact.send('cat /etc/sysconfig/ntp')
                interact.expect(expert_prompt)
                ntp = 'cat /etc/sysconfig/ntp \n' + interact.current_output_clean
                output = sk1+route_list+sk1+netconf+sk1+hosts+sk1+hosts1+sk1+passwords+sk1+resolv+sk1+ntp
                file.write(output)
                file.close()
                ws.write(i, 1, 'OK')
                i += 1

    except TimeoutError:
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        file.write('Connection Failed')
        file.close
        ws.write(i, 1, 'Connection Failed')
        i += 1
        
    except Exception:
        traceback.print_exc()
        errorstatus = 'connection failed'
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        file.write('Connection Failed(exception)')
        file.close()
        ws.write(i, 1, 'UnknownError')
        i += 1
    finally:
        try:
            ssh.close()
        except:
            pass              
    return i

row = 1
for host in ip_addr_list:
        ws.write(row, 0, host)
        row = main(row)
wb.save('C:/python/checkpoint/result.xls')        
        


#if __name__ == '__main__':
#    main()
