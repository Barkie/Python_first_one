import re
import shutil
import os
from os import listdir
import xlrd
import xlwt
import time
# time check - start time
start_time = time.time()

WIDTH_CONST = 256
widths = 50, 27, 30, 50, 36, 20, 20, 20
headers = (
    'FileName', 'Hostname', 'Interface Number', 'Description/Nameif', 'IP address',
    'cdp', 'static route', 'summary(testing purpose)')
    

def find_device_hostname(some_str):
    """trying to find hostname of the device"""
    hostname = ''
    # trying to find hostname of the device
    search_result = re.findall(r"\nhostname.([\S\s].*)\n", some_str)
    # if some1 is found	
    if search_result:
        #remove_duplicates
        hostname = search_result
        
    return hostname


def find_all_interfaces_with_ip(some_str):
    """find all interfaces with IP addresses"""
    vlanif = re.findall(
	        r"\ninterface ((?:Loopback.*|Tunnel.*|GigabitEthernet.*|Vlan.*|Fast.*\n|Serial.*)[^\!]*ip address "
	        "(?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3}\s)?", some_str)
        
    # removing duplicates and sorting
    return sorted(list(set(vlanif)))
    
    
def find_interface_type_and_name(some_str):
    """find interface type and name"""
    # trying to find interface type and name 
    interface = re.findall(r"(Loopback\S*|Tunnel\S*|GigabitEthernet\S*|Vlan\S*|Fast\S*|Serial\S*)\s", some_str)
    
    # remove duplicates
    return list(set(interface))
    

def find_ASA_nameif(some_str):
	"""find Cisco ASA nameif"""
	# trying to find ASA interface name
	interface_asa = re.findall(r"nameif ([\S\s]*?)\n", some_str)

	# remove duplicates
	return list(set(interface_asa))


def find_description(some_str):
    """find Cisco switch/router interface description"""
    # trying to find description 
    description = re.findall(r"description ([\S\s]*?)\n", some_str)
    
    # remove duplicates
    return list(set(description))
    

def find_ip_address(some_str):
	"""find IP address of the interface"""
	# trying to find IP address
	ip_address = re.findall(r"ip address ((?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3})\s?$", some_str)

	#remove duplicates
	return list(set(ip_address))


def find_secondary_ip_address(some_str):
	"""find secondary IP addres of the interface"""
	# trying to find secondary IP address
	ip_sec_address = re.findall(r"ip address ((?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3}) secondary", some_str)

	#remove_duplicates
	return list(set(ip_sec_address))





listFF = listdir('C:/python/configs/')
# create excel workbook with write permissions (xlwt module)
wb = xlwt.Workbook()
# create sheet IP LIST with cell overwrite rights
ws = wb.add_sheet('IP LIST', cell_overwrite_ok=True)
# set width
for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width
# writing first row
for index, header in enumerate(headers):
    ws.write(0, index, header)


def search(i):
    # w/o this thing counter do not work inside function
    # BADPRACTICE/fix later!
    global i
    # find hostname
    hostname = find_device_hostname(some_str)
    if hostname:
        ws.write(i, 1, ''.join(hostname))
    # trying to find all interfaces with IP addresses
    vlanif = find_all_interfaces_with_ip(some_str)
    # for every interface run new searches
    for item_str in map(''.join, vlanif):

        interface = find_interface_type_and_name(item_str)
        # if something is found then convert to string and write to excel
        if interface:            
            ws.write(i, 2, ''.join(interface))

        # trying to find Cisco switch/router/industrial switch interface description
        descr = find_description(item_str)
        # if something is found then convert to string and write to excel
        if descr:         
            ws.write(i, 3, ''.join(descr))

        # trying to find Cisco ASA interface name
        nameif = find_ASA_nameif(item_str)
        # if something is found then convert to string and write to excel
        if nameif:            
            ws.write(i, 3, ''.join(nameif))

        # trying to find IP address terminated on the interface
        ip = find_ip_address(item_str)
        # if something is found then convert to string and write to excel
        if ip:            
            ws.write(i, 4, ''.join(ip))

        # trying to find secondary IP address terminated on the interface
        ip_sec = find_secondary_ip_address(item_str)
        if ip_sec:       
            #counter +1
            i += 1
            ws.write(i, 4, ''.join(ip_sec) + ' secondary')

        # debug thing, write raw interface string found in another excel column, for debug purposes
        ws.write(i, 7, item_str)
        # counter +1 for the next line (secondary IP address)
        i += 1

    print('info saved')
    # counter+1 to next excel line
    i += 1
    
    return i


row = 1
for file in listFF:
   f = open('C:/python/configs//{0}'.format(file), 'r+')
   some_str = f.read()
   print(row, file)
   #write filename in first column
   ws.write(row, 0, file)
   row = search(row)
   print('ready')
   
wb.save('C:/python/outputdir/interface_vlan_list_test.xls')
print('wb saved')
# script time check
print("--- %s seconds ---" % (time.time() - start_time))
