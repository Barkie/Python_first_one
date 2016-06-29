import re
from os import listdir
import xlwt
import time
import sqlite3
from urllib.request import Request, urlopen


# Timer trigger to count time at the end of a script
start_time = time.time()


listFF = listdir('C:/python/cpinfo/')


# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 50, 27, 30, 50, 36, 20, 20, 20

# Excel column names
headers = (
    'FileName', 'Policy Name', 'Hostname', 'Interface', 'IP address',
    'Mask', 'IP_ADD', 'MAC', 'INTERFACE')
    
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



sqlite_file = 'c:/python/db_test/checkpoint.db'    # Name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('c:/python/db_test/checkpoint.db')
# Creating cursor to work with DB
c = conn.cursor()

# Value = column name
c_ID = 'Row_Number'
c_filename = 'File_name'
c_hostname = 'Policy_Name'
c_dev_id = 'Hostname'
c_local_iface = 'Interface'
c_holdtime = 'IP_address'
c_capability = 'Mask'
c_remote_platform = 'IP_ADD'
c_remote_iface = 'MAC'
c_mac_vl = 'INTERFACE'


# Creating tables with columns
cur.execute("DROP TABLE IF EXISTS CDP")
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2}, {nf7} {tf2}, {nf8} {tf2}, {nf9} {tf2})'\
          .format(tn='CDP', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname,\
            nf4=c_dev_id, nf5=c_local_iface, nf6=c_holdtime, nf7=c_capability, nf8=c_remote_platform, nf9=c_remote_iface))

cur.execute("DROP TABLE IF EXISTS MAC")
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2}, {nf7} {tf2})'\
          .format(tn='MAC', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_mac_vl,\
            nf5=c_mac_id, nf6=c_mac_iface, nf7=c_ven_info))

cur.execute("DROP TABLE IF EXISTS IP_IF")
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2})'\
          .format(tn='IP_IF', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_if_num,\
            nf5=c_if_name, nf6=c_if_ip))

cur.execute("DROP TABLE IF EXISTS VL_IF")
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf2}, {nf4} {tf2}, {nf5} {tf2}, {nf6} {tf2}, {nf7} {tf2}, {nf8} {tf2})'\
          .format(tn='VL_IF', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, nf4=c_if_num,\
            nf5=c_if_name, nf6=c_vl_ac, nf7=c_vl_na, nf8=c_vl_tr))

# Committing changes, closing DB
conn.commit()
conn.close()







def hostname(some_str):
  """trying to find hostname of the Check Point"""
  hostname_final = ''
  hostname = re.findall(b"/opt/CPinfo-10/bin/(.*).mod.cpi\n", some_str)
  if hostname:
    hostname_final = ''.join([x.decode("utf-8") for x in list(set(hostname))])

  return hostname_final


def policy(some_str):
  """trying to find policy name"""
  policy_final = ''
  policy = re.findall(b"Policy name:\s*(.*)\n", some_str)
  if policy:
    # decode bytes to unicode
    policy_final = ''.join([x.decode("utf-8") for x in list(set(policy))])

  return policy_final


def get_all_interfaces(some_str):
  """trying to find all interfaces and addresses"""
  getifs_final = ''
  getifs = re.findall(b"localhost (.* (?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3})\n", some_str)
  if getifs:
    # decode bytes to unicode
    getifs_final = ''.join([x.decode("utf-8") for x in getifs])
    eth_ip = re.findall(r"(.{1,15} (?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3})", getifs_final)
    getifs_final = eth_ip
  
  return sorted(list(set(getifs_final)))


def get_if_name(some_str):
  """trying to get if name"""
  eth_final = ''
  eth_name = re.findall(r"(\S*).(?:[0-9]{1,3}\.){3}[0-9]{1,3} (?:[0-9]{1,3}\.){3}[0-9]{1,3}", some_str)
  if eth_name:
    eth_final = eth_name

  return eth_final


def get_if_ip_add(some_str):
  """trying to get if ip add"""
  ipadd_final = ''
  ipadd = re.findall(r"((?:[0-9]{1,3}\.){3}[0-9]{1,3})\s255", some_str)
  if ipadd:
    ipadd_final = ipadd

  return ipadd_final

def get_if_ip_mask(some_str):
  """trying to get if ip mask"""
  mask_final = ''
  mask = re.findall(r"((?:[255]{1,3}\.){2}[0-9]{1,3}\.[0-9]{1,3})", some_str)
  if mask:
    mask_final = mask

  return mask_final

def search_arp_list(some_str):
  """trying to find arp list"""
  arp_final = ''
  arp = re.findall(b"\/proc\/net\/arp\n.*\n.*Device\n([\S\s]*)\n.*\n.*\n\/proc\/net\/dev\n", some_str)
  if arp:
    arp_string = ''.join([x.decode("utf-8") for x in arp])
    arp_final = re.findall(r"([\S]*)(?:\s*[\S]*){2}\s*([\S]*)\s*[\S]*\s*([\S]*)\n", arp_string)

  return arp_final


# Main function
def search(i):
    print(i)
    # search Policy name
    policy_final = policy(some_str)
    # write policy to excel
    ws.write(i, 1, policy_final)
    # search hostname of checkpoint
    hostname_final = hostname(some_str)
    # write to the excel
    ws.write(i, 2, hostname_final)
    eth_ip = get_all_interfaces(some_str)
    print(eth_ip)
    # if something is found, do
    if eth_ip:
      # for every item in the list (iface+ip+mask) split items and write to different excel columns
      for item in eth_ip:
        # searching IF name
        if_name = get_if_name(item)
        ws.write(i, 3, if_name)
        # searching IF IP add
        if_ip_add = get_if_ip_add(item)
        # write ipaddress to excel
        ws.write(i, 4, if_ip_add)
        # searching IF IP mask
        mask = get_if_ip_mask(item)
        # write netmask to excel
        ws.write(i, 5, mask)
        # counter +1 for next excel row (new interface)
        i += 1
    arp_list = search_arp_list(some_str)
    if arp_list:
      for item in arp_list:
        ip_second_if_address = item[0]
        # write to excel
        ws.write(i, 6, ip_second_if_address)

        mac_second_address = item[1]
        # write to texcel
        ws.write(i, 7, mac_second_address)

        if_second_name = item[2]
        # write to excel
        ws.write(i, 8, if_second_name)
        i += 1
    # counter +1 for next next excel row (new file)
    i += 1
    return i


row = 1
# main script    
for file in listFF:
  # open file from listdir cpinfo in read_binary mode
  f = open('C:/python/cpinfo//{0}'.format(file), 'rb')
  print(row)
  print(file)
  some_str = f.read()
  # print number row, name of a file
  print(row, file)
  # write filename in first column
  ws.write(row, 0, file)
  # starting main func
  row = search(row)
  # saving workbook
  wb.save('C:/python/outputdir/cpinfo_interface_list.xls')

   
# Checking script time and printing
print("--- %s seconds ---" % (time.time() - start_time))
