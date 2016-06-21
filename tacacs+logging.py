import re
import shutil
import os
from os import listdir
import xlrd
import xlsxwriter


#WIDTH_CONST = 256
#widths = 50, 27, 30, 50, 36, 20
#headers = (
#    'FileName', 'Hostname', 'logging', 'aaa-model', 'aaa auth', 'tacacs')

listFF = listdir('C:/python/configs/')
# create excel workbook with write permissions (xlwt module)
workbook = xlsxwriter.Workbook('C:/python/outputdir/tacacs.xlsx')
# create sheet IP LIST with cell overwrite rights
ws = workbook.add_worksheet()
# set width
#for index, width in enumerate(widths):
#    ws.col(index).width = WIDTH_CONST * width
# writing first row
#for index, header in enumerate(headers):
#    ws.write(0, index, headers
ws.set_column('A:A', 33)
ws.set_column('B:B', 22)
ws.set_column('C:C', 17)
ws.set_column('D:D', 54)
ws.set_column('F:F', 50)
# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})
#top row settings (bold font)
ws.write(0, 0, 'Name', bold)
ws.write(0, 1, 'Subtheme name', bold)
ws.write(0, 2, 'Requirement', bold)
ws.write(0, 3, 'Supplemental Guidance', bold)
ws.write(0, 4, 'Requirement Enhancements', bold)
ws.write(0, 5, 'Referencies', bold)

#create counter
i = 1

def search():
    #w/o this thing counter do not work inside function
    global i
    #trying to find hostname of the device
    hostname = re.findall(r"\nhostname.([\S\s].*)\n", some_str)
    # if some1 is found
    if hostname != []:
        #remove_duplicates
        hostname_no_duplic = list(set(hostname))
        hostname_str = ' '.join(hostname_no_duplic)
        #write to the excel
        ws.write(i, 1, hostname_str)
    # trying to find all logging strings
    logging = re.findall(r"\n(logging.*)", some_str)
    if logging != []:
    	logging_no_duplic = list(set(logging))
    	logging_str = ' \n'.join(logging_no_duplic)
    	# write to excel
    	ws.write(i, 2, logging_str)
    # trying to find aaa-model
    aaa = re.findall(r"(.*aaa new-model.*)\n", some_str)
    if aaa != []:
    	aaa_no_duplic = list(set(aaa))
    	aaa_str = ' '.join(aaa_no_duplic)
    	# write to excel
    	ws.write(i, 3, aaa_str)
    aaa_auth = re.findall(r"\n(.*aaa authentication.*|.*aaa authorization.*)", some_str)
    if aaa_auth != []:
    	aaa_no_duplic = list(set(aaa_auth))
    	aaa_auth_str = ' \n'.join(aaa_no_duplic)\
    	# write to excel
    	ws.write(i, 4, aaa_auth_str)
    tacacs = re.findall(r"\n(.*tacacs-server.*)", some_str)
    if tacacs != []:
    	tacacs_no_duplic = list(set(tacacs))
    	tacacs_str = ' \n'.join(tacacs_no_duplic)
    	# write to excel
    	ws.write(i, 5, tacacs_str)
    print('info saved')
    #counter+1 to next excel line
    i += 1

    
for file in listFF:
   f = open('C:/python/configs//{0}'.format(file), 'r+')
   some_str = f.read()
   print(i, file)
   #write filename in first column
   ws.write(i, 0, file)
   search()
   print('ready')
   
workbook.close()
print('wb saved')
