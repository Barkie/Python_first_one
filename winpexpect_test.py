import sys
import winpexpect
import xlwt
import xlrd
import pywintypes

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

def skip():
    px.send('\n')
    px.expect(']# ')
    px.send('\n')
    px.expect(']# ')
    px.send('\n')
    px.expect(']# ')
    
for host in ip_addr_list:
    EXPECTSTUB = 'expectStub.exe'
    #plink px = winpexpect.winspawn('c:/python/openssh/bin/plink.exe -t ' + user + '@' + host)
    px = winpexpect.winspawn('c:/python/openssh/bin/plink.exe -ssh ' + user + '@' + host, timeout=6, stub=EXPECTSTUB)
    fout = open('c:/python/checkpoint/test_debug/{0}.txt'.format(host),"w")
    #px.logfile = sys.stdout
    px.logfile_read = fout
    px.expect('password:')
    px.send('1q2w3e\n')
    px.expect('>')
    px.send('expert\n')
    px.expect('password:', timeout=5)
    px.send('1q2w3e\n')
    px.expect('now.', timeout=10)
    px.send('\n')
    px.expect('.*Expert.*')
    skip()
    px.send('cat /etc/hosts\n')
    skip()
    px.send('cat /etc/passwd\n')
    skip()
    px.send('cat /etc/sysconfig/ntp\n')
    skip()
    px.send('cat /etc/passwd\n')
    skip()
#    px.expect('scripts:0]')
#    px.sendline('cat /etc/sysconfig/ntp')
#    px.send('\n')
#    px.expect('scripts:0]')
	


