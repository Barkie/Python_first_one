import re
import shutil
import os
from os import listdir
import xlrd
import xlwt
import time
import sqlite3

sqlite_file = 'c:/python/db_test/sw.db'    # Name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('c:/python/db_test/sw.db')
# Creating cursor to work with DB
c = conn.cursor()

# Value = column name
c_ID = 'Row_Number'
c_filename = 'File_name'
c_hostname = 'Hostname'
c_dev_id = 'Device_ID'
c_local_iface = 'Local_Interface'
c_holdtime = 'Holdtime'
c_capability = 'Capability'
c_remote_platform = 'Remote_Platform'
c_remote_iface = 'Remote_Interface'
c_mac_vl = 'Vlan'
c_mac_id = 'Mac_Address'
c_mac_iface = 'Interface'
c_if_num = 'Interface_Name'
c_if_name = 'Interface_Description'
c_if_ip = 'Interface_IP'
c_vl_ac = 'Access_Vlan'
c_vl_na = 'Native_Vlan'
c_vl_tr = 'Trunk_Vlan'

# Creating tables with columns
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2}, {nf7} {tf2}, {nf8} {tf2}, {nf9} {tf2})'\
          .format(tn='CDP', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname,\
            nf4=c_dev_id, nf5=c_local_iface, nf6=c_holdtime, nf7=c_capability, nf8=c_remote_platform, nf9=c_remote_iface))

c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2})'\
          .format(tn='MAC', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_mac_vl,\
            nf5=c_mac_id, nf6=c_mac_iface))

c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2})'\
          .format(tn='IP_IF', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_if_num,\
            nf5=c_if_name, nf6=c_if_ip))

c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2}, {nf7} {tf2}, {nf8} {tf2})'\
          .format(tn='VL_IF', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_if_num,\
            nf5=c_if_name, nf6=c_vl_ac, nf7=c_vl_na, nf8=c_vl_tr))

# Committing changes, closing DB
conn.commit()
conn.close()

# Timer trigger to count time at the end of a script
start_time = time.time()

# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 50, 27, 30, 50, 36, 20, 20, 20

# Excel column names
headers = (
    'FileName', 'Hostname', 'Interface Number', 'Description/Nameif', 'IP address',
    'cdp', 'static route', 'summary(testing purpose)')
    

def find_device_hostname(some_str):
    """trying to find hostname of the device"""
    hostname = ''
    # Trying to find hostname of the device
    search_result = re.findall(r"\nhostname.([\S\s].*)\n", some_str)
    # If hostname is found, returning
    if search_result:
        hostname = search_result
    
    # Removing duplicates
    return list(set(hostname))


def find_all_interfaces_with_ip(some_str):
        """find all interfaces with IP addresses"""
        vlanif = re.findall(
                    r"\ninterface ((?:Loopback.*|Tunnel.*|GigabitEthernet.*|Vlan.*|Fast.*\n|Serial.*)[^\!]*ip address "
                    "(?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3}\s)?", some_str)
        
        # Removing duplicates and sorting
        return sorted(list(set(vlanif)))
    

def find_all_interfaces_with_vlans(some_str):
    """trying to find all interfaces with descriptions and vlans"""
    all_ifs_returned = ''
    if_intfname = re.findall(r"\ninterface (?:(TenGigabitEthernet.*?)\n)|(?:(GigabitEthernet.*?)\n)|(?:(Fast.*?)\n)|(?:(Serial.*?)\n)", ''.join(some_str))
 
    if_descrip = re.findall(r"\n.*description (.*)\n", ''.join(some_str))
    vlan_list_access = re.findall(r"\n.*(?:switchport access vlan (.*))\n", ''.join(some_str))
    vlan_list_native = re.findall(r"\n.*(?:switchport trunk native vlan (.*))\n", ''.join(some_str))
    vlan_list_trunk = re.findall(r"\n.*(?:switchport trunk allowed vlan (.*))\n", ''.join(some_str))
    if (if_descrip or vlan_list_trunk or vlan_list_access or vlan_list_native):
        all_ifs_returned = if_intfname


    return list(set(all_ifs_returned)), list(set(if_descrip)), list(set(vlan_list_access)), list(set(vlan_list_native)), list(set(vlan_list_trunk))



def find_all_interfaces(some_str):
    """trying to find all interfaces in the text file"""
    all_ifs = re.findall(r"\ninterface ((?:TenGigabitEthernet.*?!)|(?:GigabitEthernet.*?!)|(?:Fast.*?!)|(?:Serial.*?!)\n)", some_str, re.S)
    if all_ifs:
        for item in all_ifs:
            print('----NEW INT----')
            print(item)

        return list(set(all_ifs))



def remove_empty_values_from_tuple(some_str):
    for item in some_str:
        clearing_to_list = [t for t in item if t]
        conv_to_string = ''.join(clearing_to_list)

        return conv_to_string

def cdp_nei(some_str):
        """find all cdp neighbors"""
        # Trying to find cdp neighbor output info
        cdp_nei = re.findall(
                r"\n.*#.*cdp nei.*\n([\S\s]*?)?.*#.*\n", some_str)
        # Cleaning cdp output info from headers
        cdp_nei_cleaned = re.findall(r"Port ID\n([\S\s]*)\n", ''.join(cdp_nei))

        # Splitting cleaned cdp output info to strings, returning
        cdp_nei_splited_list = re.findall(
            r'(\S*)[\s\n]{1,}(\S*.\S*)\s{1,}(\S*)\s{1,}'
            '(\w(?:\s\w){0,4}) \s{1,}(.{10})(\S* \S*)', ''.join(cdp_nei_cleaned))

        # Removing duplicates
        return list(set(cdp_nei_splited_list))
    

def mac_list(some_str):
        """find all mac_addresses"""
        # Trying to find Mac Address Table output info
        mac_lst = re.findall(
                r"\n.*Mac Address Table.*\n([\S\s]*?)?.*#.*\n", some_str)
        # Cleaning MAC table from static CPU MACs
        mac_lst_cleaned = re.findall(r"CPU\n( \d[\S\s]*)", ''.join(mac_lst))
        # Splitting cleaned MAC table output to strings, returning
        mac_lst_splited = re.findall(
            r'(\d{1,4})\s*(\S*)\s*DYNAMIC\s*(\S*)\n', ''.join(mac_lst_cleaned))

        # Removing duplicates
        return list(set(mac_lst_splited))


def find_interface_type_and_name(some_str):
        """find interface type and name"""
        # Trying to find interface type and name 
        interface = re.findall(r"(Loopback\S*|Tunnel\S*|GigabitEthernet\S*|Vlan\S*|Fast\S*|Serial\S*)\s", some_str)
    
        # Removing duplicates
        return list(set(interface))
    

def find_ASA_nameif(some_str):
        """find Cisco ASA nameif"""
        # Trying to find ASA interface name
        interface_asa = re.findall(r"nameif ([\S\s]*?)\n", some_str)

        # Removing duplicates
        return list(set(interface_asa))


def find_description(some_str):
        """find Cisco switch/router interface description"""
        # Trying to find description 
        description = re.findall(r"description ([\S\s]*?)\n", some_str)
    
        # Removing duplicates
        return list(set(description))
    

def find_ip_address(some_str):
        """find IP address of the interface"""
        # Trying to find IP address
        ip_address = re.findall(r"ip address ((?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3})\s?$", some_str)

        # Removing duplicates
        return list(set(ip_address))


def find_secondary_ip_address(some_str):
        """find secondary IP addres of the interface"""
        # Trying to find secondary IP address
        ip_sec_address = re.findall(r"ip address ((?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3}) secondary", some_str)

        # Removing duplicates
        return list(set(ip_sec_address))


# Selecting directory where Cisco configuration files stored
listFF = listdir('C:/python/configs/')

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
    # Creating counter for CDP
    b = i

    # Creating counter for MAC
    z = i

    counter = i
    # Searching hostname
    hostname = find_device_hostname(some_str)
    # If hostname is found, writing to excel
    if hostname:
        ws.write(i, 1, ''.join(hostname))
    
    # Finding cdp neighbors
    cdp_nei_splited_list = cdp_nei(some_str)
    # If splitted cdp list exist
    if cdp_nei_splited_list:
        # Searching every splitted string and setting multiple values (Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID)
        for cdp_info in cdp_nei_splited_list:
            dev_id = cdp_info[0]
            local_iface = cdp_info[1]
            holdtime = cdp_info[2]
            capability = cdp_info[3]
            platform = cdp_info[4]
            remote_iface = cdp_info[5]
            print(b)    #debug purposes
            print(hostname) #debug purposes
            print(dev_id)   #debug purposes
            print(local_iface)  #debug purposes
            # Setting list of splitted values (for SQlite DB writing)
            cdp_id = (b, ''.join(hostname), ''.join(dev_id), ''.join(local_iface), ''.join(holdtime), ''.join(capability), ''.join(platform), ''.join(remote_iface))
            # Writing splitted values to excel
            ws.write(b, 10, ''.join(dev_id))
            ws.write(b, 11, ''.join(local_iface))
            ws.write(b, 12, ''.join(holdtime))
            ws.write(b, 13, ''.join(capability))
            ws.write(b, 14, ''.join(platform))
            ws.write(b, 15, ''.join(remote_iface))
            # Trying to write splitted values into SQlite DB
            try:
                c.execute(("INSERT INTO {tn} ({idc}, {host}, {devid}, {locif}, {hold}, {cap}, {plat}, {remif}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)").\
                    format(tn='CDP', idc=c_ID, host=c_hostname, devid=c_dev_id, locif=c_local_iface,\
                        hold=c_holdtime, cap=c_capability, plat=c_remote_platform, remif=c_remote_iface), cdp_id)
            # Exception (not used ATM, for PRIMARY KEY future usage)
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(t_file))
            # Counter +1 for next CDP string search
            b += 1
    # If no CDP info is found, writing to excel
    else:
        ws.write(b, 10, 'No cdp info found')

    # Finding MAC table    
    mac_lst_splited = mac_list(some_str)
    # If splitted MAC table exist, continuing
    if mac_lst_splited:
        # Searching every splitted string and setting multiple values (Vlan    Mac Address       Ports)
        for mac in mac_lst_splited:
            mac_vlan_id = mac[0]
            mac_id = mac[1]
            mac_interface = mac[2]
            # Setting list of splitted values (for SQlite DB writing)
            mac_params = (z, ''.join(hostname), ''.join(mac_vlan_id), ''.join(mac_id), ''.join(mac_interface))
            # Writing splitted values to excel
            ws.write(z, 17, ''.join(mac_vlan_id))
            ws.write(z, 18, ''.join(mac_id))
            ws.write(z, 19, ''.join(mac_interface))
            # Trying to write splitted values into SQlite DB
            try:
                c.execute(("INSERT INTO {tn} ({idc}, {host}, {vl}, {mac}, {macif}) VALUES (?, ?, ?, ?, ?)").\
                    format(tn='MAC', idc=c_ID, host=c_hostname, vl=c_mac_vl, mac=c_mac_id,\
                        macif=c_mac_iface), mac_params)
            # Exception (not used ATM, for PRIMARY KEY future usage)
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(t_file))    
            # Counter +1 for next MAC string search
            z += 1
    # If no MAC table is found, writing to excel
    else:
        ws.write(z, 17, 'no mac-address info found')

    all_ifs_list = find_all_interfaces(some_str)
    if all_ifs_list:
        for item in all_ifs_list:
            val1name, val2descr, val3vlac, val4vlnat, val5vltr = find_all_interfaces_with_vlans(item)
            if val1name:
                val1name = remove_empty_values_from_tuple(val1name)
                vl_params = (counter, ''.join(hostname), ''.join(val1name), ''.join(val2descr), ''.join(val3vlac), ''.join(val4vlnat), ''.join(val5vltr))
                print(vl_params)
                try:
                    c.execute(("INSERT INTO {tn} ({idc}, {host}, {ifname}, {ifdes}, {vlac}, {vlna}, {vltr}) VALUES (?, ?, ?, ?, ?, ?, ?)").\
                        format(tn='VL_IF', idc=c_ID, host=c_hostname, ifname=c_if_num, ifdes=c_if_name,\
                            vlac=c_vl_ac, vlna=c_vl_na, vltr=c_vl_tr), vl_params)
                # Exception (not used ATM, for PRIMARY KEY future usage)
                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(t_file))    
                counter += 1

    # Trying to find all interfaces with IP addresses
    vlanif = find_all_interfaces_with_ip(some_str)
    # For every found interface running new search
    for item_str in map(''.join, vlanif):
        # Finding interface ID
        interface = find_interface_type_and_name(item_str)
        # If something is found then converting to string and writing to excel
        if interface:            
            ws.write(i, 2, ''.join(interface))

        # Trying to find Cisco switch/router/industrial switch interface description
        descr = find_description(item_str)
        # If something is found then converting to string and writing to excel
        if descr:         
            ws.write(i, 3, ''.join(descr))

        # Trying to find Cisco ASA interface name
        nameif = find_ASA_nameif(item_str)
        # If something is found then converting to string and writing to excel
        if nameif:            
            ws.write(i, 3, ''.join(nameif))

        # Trying to find IP address terminated on the interface
        ip = find_ip_address(item_str)
        # If something is found then converting to string and writing to excel
        if ip:            
            ws.write(i, 4, ''.join(ip))

        # Trying to find secondary IP address terminated on the interface
        ip_sec = find_secondary_ip_address(item_str)
        if ip_sec:       
            # Counter +1 for the next line (secondary IP address)
            i += 1
            ws.write(i, 4, ''.join(ip_sec) + ' secondary')
        # Setting list of values (for SQlite DB writing)
        if_id = (i, ''.join(hostname), ''.join(interface), ''.join(descr), ''.join(nameif), ''.join(ip))
        # Trying to write values into SQlite DB
        try:
            c.execute(("INSERT INTO {tn} ({idc}, {host}, {ifn}, {descr}, {nameif}, {ip}) VALUES (?, ?, ?, ?, ?, ?)").\
                format(tn='IP_IF', idc=c_ID, host=c_hostname, ifn=c_if_num, descr=c_if_name, nameif=c_if_name, ip=c_if_ip,), if_id)
        # Exception (not used ATM, for PRIMARY KEY future usage)
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(t_file))          
        # Debug thing, write raw interface string found in another excel column. Debug purposes.
        ws.write(i, 7, item_str)
        # Counter +1 for the next line (next interface-ip)
        i += 1
    # For each file searched print at the end of searching
    print('info saved')
    # Counter+1 to next excel line (next device in the listFF file list)
    i += 1

    # Searching max value of strings from CDP, MAC, Interface. Selecting max one and returning for next file search
    if i >= b:
        b = i
    if z >= b:
        i = z

    return i
        
    

# Start row
row = 1
# Starting script for every file in the config directory
for file in listFF:
    # Cpening file from folder file list
    f = open('C:/python/configs//{0}'.format(file), 'r+')
    # Reading file content
    some_str = f.read()
    # Printing row, file (debug purpose)
    print(row, file)
    # Write filename in first column
    ws.write(row, 0, file)
    # Row number = result of search function
    try:
       # Connecting to DB
       conn = sqlite3.connect('c:/python/db_test/sw.db')
       # Creating cursor to work with DB
       c = conn.cursor()
       # Starting main search function
       row = search(row)
       # Saving excel workbook
       wb.save('C:/python/outputdir/interface_vlan_list_test.xls')
       # Commiting changes to DB and closing DB.
       conn.commit()
       conn.close()
    # Debug purposes
    except Exception:
       raise Exception
       print('Exception throwed', file)
       print('ready')
       # closing file
       f.close()
   
# Checking script time and printing
print("--- %s seconds ---" % (time.time() - start_time))
