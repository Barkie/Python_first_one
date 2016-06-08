import traceback
import paramiko
from paramiko_expect import SSHClientInteraction
import xlrd




iprb = xlrd.open_workbook('c:/python/checkpoint/ip.xls')
sheet = iprb.sheet_by_name('IPs')
num_rows = sheet.nrows
num_cols = sheet.ncols
ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]

user = 'admin'
passwd = '1q2w3e'
expert_passwd = '1q2w3e'
prompt = '.*> '
expert_prompt = '.*# '
not_found = '.*Invalid command:.*'
no_expert_pass = '.*"set expert-password".*'
wrong_expert_pass = '.*Wrong password.*'
enter_expert_pass = '.*expert pass.*'


def expert_mode():
    interact.send('expert')
    entering_expert_index = interact.expect([no_expert_pass, enter_expert_pass])
    if entering_expert_index == 0:
        print('no expert password, need to set it')
    elif entering_expert_index == 1:
        print('cp asked for expert password, entering it')
        interact.send(expert_passwd)
        expert_mode_index = interact.expect([wrong_expert_pass, expert_prompt])
        if expert_mode_index == 0:
            print('wrong expert pass')
        elif expert_mode_index == 1:   
           print('password ok, continuing') 
           commands()

def commands():
    interact.send('cat /etc/sysconfig/netconf.C')
    interact.expect(expert_prompt)
    interact.send('cat /etc/hosts.allow')
    interact.expect(expert_prompt)
    interact.send('cat /etc/hosts')
    interact.expect(expert_prompt)
    interact.send('cat /etc/passwd')
    interact.expect(expert_prompt)
    interact.send('cat /etc/resolv.conf')
    interact.expect(expert_prompt)
    interact.send('cat /etc/sysconfig/ntp')
    interact.expect(expert_prompt)      

def main():
    # Use SSH client to login
    try:
        # Create a new SSH client object
        ssh = paramiko.SSHClient()

        # Set SSH key parameters to auto accept unknown hosts
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        ssh.connect(hostname=host, username=user, password=passwd)

        # Create a client interaction class which will interact with the host
        interact = SSHClientInteraction(ssh, timeout=5, display=True)
        interact.expect(prompt)

        # Run the first command and capture the cleaned output, if you want
        # the output without cleaning, simply grab current_output instead.
        interact.send('netstat -rnv')
        interact.expect(prompt)
        route_list = interact.current_output_clean
        expert_mode()
        exp_cmd_output = interact.current_output_clean
        # To expect multiple expressions, just use a list.  You can also
        # selectively take action based on what was matched.

        # Method 1: You may use the last_match property to find out what was
        # matched
        #interact.send('~/paramiko_expect-demo-helper.py')
        #interact.expect([prompt, 'Please enter your name: '])
        #if interact.last_match == 'Please enter your name: ':
        #    interact.send('Fotis Gimian')
        #    interact.expect(prompt)

        # Method 2: You may use the matched index to determine the last match
        # (like pexpect)
        #interact.send('~/paramiko_expect-demo-helper.py')
        #found_index = interact.expect([prompt, 'Please enter your name: '])
        #if found_index == 1:
        #    interact.send('Fotis Gimian')
        #    interact.expect(prompt)

        # Send the exit command and expect EOF (a closed session)
        #interact.send('exit')
        #interact.expect()

        ## Print the output of each command
        #print '-'*79
        #print 'Cleaned Command Output'
        #print '-'*79
        #print 'uname -a output:'
        #print cmd_output_uname
        #print 'ls -l / output:'
        #print cmd_output_ls

    except Exception:
        traceback.print_exc()
    finally:
        try:
            client.close()
        except:
            pass
#    return exp_cmd_output


for host in ip_addr_list:
        file = open('c:/python/checkpoint/{0}.txt'.format(host),"a")
        answers = main()
#        file.write(answers)
#        file.close()
#if __name__ == '__main__':
#    main()
