import re
import shutil
import os
from os import listdir
import xlrd
import xlwt

listFF = listdir('C:/python/configs/')
#create excel workbook with write permissions (xlwt module)
wb = xlwt.Workbook()
#create sheet IP LIST with cell overwrite rights
ws = wb.add_sheet('IP LIST', cell_overwrite_ok=True)
#writing first row
ws.col(0).width = 256 * 50
ws.col(1).width = 256 * 27
ws.col(2).width = 256 * 30

ws.write(0, 0, 'FileName')
ws.write(0, 1, 'Hostname')
ws.write(0, 2, 'Failover')

#create counter
i = 1

def search():
    global i
    hostname = re.findall(r"\nhostname.([\S\s].*)\n", str)
    if hostname != []:
        #remove_duplicates
        hostname_no_duplic = list(set(hostname))
        hostname_str = ' '.join(hostname_no_duplic)
        ws.write(i, 1, hostname_str)

    #search fileover info
    failover = re.findall(r"(Failover[\S\s].*)\n", str)
    if failover != []:
        #remove_duplicates
        failover_no_dupl = list(set(failover))
        failover_str = ' '.join(failover_no_dupl)
        ws.write(i, 2, failover_str)
    print('info saved')
    #counter+1 to next excel line
    i += 1

    
for file in listFF:
   f = open('C:/python/configs//{0}'.format(file), 'r+')
   str = f.read()
   print(i, file)
   #write filename in first column
   ws.write(i, 0, file)
   search()
   print('ready')
   
wb.save('C:/python/outputdir/failover_info.xls')
