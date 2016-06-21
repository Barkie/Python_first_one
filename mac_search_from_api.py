import re
import os
from os import listdir
import xlrd
import xlwt
import time
from urllib.request import Request, urlopen

# Timer trigger to count time at the end of a script
start_time = time.time()

# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 30, 18, 10, 10, 30, 30, 20, 20

# Excel column names
headers = (
    'Number', 'Mac-address', 'Vendor')

def find_vendor(some_str):
   """trying to find mac-address vendor"""
   empty_return = 'No vendor info'
   mac_web_url = 'http://macvendors.co/api/' + some_str + '/xml'
   try:
      req = Request(mac_web_url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read().decode(encoding='UTF-8')
      vendor =  re.findall(r"<company>(.*)</company", webpage)
      if vendor:
         empty_return = vendor
   except:
       print('something is wrong. error.')
   return empty_return

def find_mac(some_str):
	"""trying to find mac-addresses in the file"""
	mac_add = re.findall(r"((?:[a-fA-F0-9]{4}.){2}(?:[a-fA-F0-9]{4}))", some_str)
	empty_return = 'No mac-add info(Check mac-add file and format'
	if mac_add:
		empty_return = mac_add

	return empty_return

# Selecting directory where Cisco configuration files stored
listFF = listdir('C:/python/MAC_LIST/')

# Creating excel workbook with write permissions (xlwt module)
wb = xlwt.Workbook()

# Creating sheet IP LIST with cell overwrite rights
ws = wb.add_sheet('MAC_LIST', cell_overwrite_ok=True)

# Setting width
for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width

# Writing first row
for index, header in enumerate(headers):
    ws.write(0, index, header)



def search(i):
    """main function"""

    # Searching all ACL strings
    mac_list = find_mac(some_str)
    # For every found ACL string running new search
    for item_str in map(''.join, mac_list):
        #writing number row
        #ws.write(i, 0, ''.join(i))
        #writing mac
        ws.write(i, 1, ''.join(item_str))
        #searching vendor
        vendor_info = find_vendor(item_str)
        if vendor_info:
        	ws.write(i, 2, ''.join(vendor_info))
        # Counter +1 for the next line (next ACL string)
        i += 1
    # For each file searched print at the end of searching
    print('info saved')


    return i
        


# Start row
row = 1
# Starting script for every file in the config directory
for file in listFF:
    # Cpening file from folder file list
    f = open('C:/python/MAC_LIST//{0}'.format(file), 'r+')
    # Reading file content
    some_str = f.read()
    # Printing row, file (debug purpose)
    print(row, file)
    # Write filename in first column
    ws.write(row, 0, file)
    row = search(row)
    # Saving excel workbook
    wb.save('C:/python/outputdir/MAC_list.xls')

    # Debug purposes

   
# Checking script time and printing
print("--- %s seconds ---" % (time.time() - start_time))
