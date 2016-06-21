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
from pexpect import pxssh
import paramiko
# time check - start time
start_time = time.time()

rb = xlrd.open_workbook('c:/python/checkpoint/ip.xls')
sheet = rb.sheet_by_name('IPs')
num_rows = sheet.nrows
num_cols = sheet.ncols
ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]
num_ips = 0
host = '10.10.0.254'
user = 'admin'
passwd = '1q2w3e'
#p=pexpect.popen_spawn.PopenSpawn(ssh + host)
#p = pxssh.pxssh()
