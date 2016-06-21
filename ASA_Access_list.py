import re
import shutil
import os
from os import listdir
import xlrd
import xlwt
import time

# Timer trigger to count time at the end of a script
start_time = time.time()

# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 30, 18, 10, 10, 30, 30, 20, 20

# Excel column names
headers = (
    'FileName', 'ACL name', 'Rule', 'Type',
    'Source', 'Destination', 'Service', 'Test(debug)')
    

def find_all_acl(some_str):
    """trying to find all ACL strings in the config"""
    acl = ''
    # Trying to find all ACL strings in the config
    search_result = re.findall(r"(access-list.*)", some_str)
    # If ACL strings are found, returning
    if search_result:
        acl = search_result
    
    # Removing duplicates
    return list(set(acl))


def find_acl_name(some_str):
    """trying to find ACL name"""
    name = ''
    acl_name = re.findall(r"access-list (\S*)", some_str)
    # If ACL name is found - returning 
    if acl_name:
        name = acl_name
    
    # Removing duplicates
    return list(set(name))


def find_acl_rule(some_str):
    """trying to find ACL rule (permit/deny)"""
    rule = ''
    search_rule = re.findall(r"(permit|deny)", some_str)
    # if rule is found, returning
    if search_rule:
        rule = search_rule

    # Removing duplicates    
    return list(set(rule))


def find_service_rule(some_str):
    """trying to find service type(icmp/tcp/IP)"""
    rule = ''
    search_rule = re.findall(r"(?:permit|deny) (\S*)", some_str)
    # if type is found, returning
    if search_rule:
        rule = search_rule

    # Removing duplicates    
    return list(set(rule))
    


def find_source(some_str):
    """trying to find source"""
    rule = ''
    search_rule = re.findall(r"(?:permit|deny) (?:\S*) (any|host \S*|[\d\S]* [\d\S]*)", some_str)
    # searching for the "host" info
    search_host = re.findall(r"host (\S*)", ''.join(search_rule))
    # if "host" is found, clearing, returning only one IP.
    if search_host:
        rule = search_host
    # if no "host" is found, returning raw search result (ANY/Network)
    else:
        rule = search_rule

    # Removing duplicates
    return list(set(rule))


def find_destin(some_str):
    """trying to find destination"""
    rule = ''
    search_rule = re.findall(r"(?:permit|deny) (?:\S*) (?:any|host \S*|[\d\S]* [\d\S]*) (host \S*|[\d\S]* [\d\S]*)", some_str)
    # searching for the "host" info
    search_host = re.findall(r"host (\S*)", ''.join(search_rule))
    # if "host" is found, clearing, returning only one IP.
    if search_host:
        rule = search_host
        # if no "host" is found, returning raw search result (ANY/Network)
    else:
        rule = search_rule

    # Removing duplicates
    return list(set(rule))



def find_ports(some_str):
    """trying to find port or ports range"""
    rule = ''
    # Searching for the eq port/service
    search_rule = re.findall(r"eq (\S*)", some_str)
    # Searching for the first range port
    search_range1 = re.findall(r"range (\S*) \S*", some_str)
    # Searching for the second range port
    search_range2 = re.findall(r"range (?:\S*) (\S*)", some_str)
    # if port range is found, joining port range items with "-"
    if search_range1:
        search_range = ''.join(search_range1) + '-' + ''.join(search_range2)
        return_rule = rule + ''.join(search_range)
    # if no range is found, returning only "eq" port/service info
    else:
        return_rule = rule + ''.join(search_rule)

    # Removing duplicates
    return list(return_rule)





# Selecting directory where Cisco ASA configuration files stored
listFF = listdir('C:/python/configs_ASA/')

# Creating excel workbook with write permissions (xlwt module)
wb = xlwt.Workbook()

# Creating sheet IP LIST with cell overwrite rights
ws = wb.add_sheet('IP LIST', cell_overwrite_ok=True)

# Setting width
for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width

# Writing first row
for index, header in enumerate(headers):
    ws.write(0, index, header)


def search(i):
    """main function"""

    # Searching all ACL strings
    acl = find_all_acl(some_str)
    # For every found ACL string running new search
    for item_str in map(''.join, acl):
        # Finding ACL name
        acl_name = find_acl_name(item_str)
        # If something is found then converting to string and writing to excel
        if acl_name:            
            ws.write(i, 1, ''.join(acl_name))

        # Trying to find ACL rule info
        acl_rule = find_acl_rule(item_str)
        # If something is found then converting to string and writing to excel
        if acl_rule:         
            ws.write(i, 2, ''.join(acl_rule))

        # Trying to find ACL service
        find_service = find_service_rule(item_str)
        # If something is found then converting to string and writing to excel
        if find_service:            
            ws.write(i, 3, ''.join(find_service))

        # Trying to find source
        source = find_source(item_str)
        # If something is found then converting to string and writing to excel
        if source:            
            ws.write(i, 4, ''.join(source))

        # Trying to find destination
        destin = find_destin(item_str)
        # If something is found then converting to string and writing to excel
        if destin:            
            ws.write(i, 5, ''.join(destin))

        # Trying to find port/ports range
        ports = find_ports(item_str)
        if ports:
            ws.write(i, 6, ''.join(ports))
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
    f = open('C:/python/configs_ASA//{0}'.format(file), 'r+')
    # Reading file content
    some_str = f.read()
    # Printing row, file (debug purpose)
    print(row, file)
    # Write filename in first column
    ws.write(row, 0, file)
    row = search(row)
    # Saving excel workbook
    wb.save('C:/python/outputdir/ASA_list.xls')

    # Debug purposes

   
# Checking script time and printing
print("--- %s seconds ---" % (time.time() - start_time))
