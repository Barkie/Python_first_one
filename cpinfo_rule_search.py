import re
from os import listdir
import xlwt
import time


# Timer trigger to count time at the end of a script
start_time = time.time()


listFF = listdir('C:/python/cpinfo_rules/')


# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 50, 27, 30, 50, 36, 20, 20, 20

# Excel column names
headers = (
    'chkpf_uid', 'ClassName', 'Name', 'Src name', 'Src table', 'Dst name', 'Dst table', 'Rule disabled?')
    
# Creating excel workbook with write permissions (xlwt module)
wb = xlwt.Workbook()

# Creating sheet IP LIST with cell overwrite rights
ws = wb.add_sheet('Rules List', cell_overwrite_ok=True)

# Setting width
for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width

# Writing first row
for index, header in enumerate(headers):
    ws.write(0, index, header)



def main_rule(some_str):
  """trying to find hostname of the Check Point"""
  rule_final = ''
  rule = re.findall(b"(:rule \(\n[\S\s]*?\s{4}\)\n\s{3}\)\n\s{2}\))", some_str)
  if rule:
    rule_final = ([x.decode("cp1251") for x in rule])

  return rule_final


def class_name(some_str):
  """trying to find policy name"""
  class_final = ''
  class_name = re.findall(r":ClassName \((.*rule)\)\n", some_str)
  if class_name:
    # decode bytes to unicode
    class_final = class_name

  return class_final


def rule_name(some_str):
  """trying to find all interfaces and addresses"""
  rule_name_final = ''
  rule = re.findall(r'\s{4}:name \("?(.*[^"])"*?\)', some_str)
  if rule:
    # decode bytes to unicode
    rule_name_final = rule
    
  
  return rule_name_final

def header_name(some_str):
  """trying to find all interfaces and addresses"""
  header_final = ''
  header = re.findall(r'.*:header_text \("?(.*[^"])"*?\)', some_str)
  if header:
    # decode bytes to unicode
    header_final = header
    
  
  return header_final


def src(some_str):
  """trying to get if name"""
  src_final = ''
  src = re.findall(r".*:src([\S\s]*):through", some_str)
  if src:
    src_objects = re.findall(r":Name \((.*)\)\n.*:Table \((.*)\)", ''.join(src))
    src_final = src_objects

  return src_final


def dst(some_str):
  """trying to get if ip add"""
  dst_final = ''
  dst = re.findall(r".*:dst([\S\s]*):install", some_str)
  if dst: 
    dst_objects = re.findall(r":Name \((.*)\)\n.*:Table \((.*)\)", ''.join(dst))
    if dst_objects:
      dst_final = dst_objects
  return dst_final


def disabled(some_str):
  """trying to find disabled rule or not"""
  disabled_final_info = ''
  disabled = re.findall(r'\s{4}:disabled \((.*)\)', some_str)
  if disabled:
    # decode bytes to unicode
    disabled_final_info = disabled
    
  
  return disabled_final_info
  

def oid_num(some_str):
  """trying to find rule OID"""
  oid_num_final = ''
  oid_num = re.findall(r'\s{4}:chkpf_uid \("{0,}(.*)"+?\)\n.*:ClassName (?:\(security.*\))', some_str)
  if oid_num:
    # decode bytes to unicode
    oid_num_final = oid_num
    
  
  return oid_num_final
# def get_if_ip_mask(some_str):
#   """trying to get if ip mask"""
#   mask_final = ''
#   mask = re.findall(r"((?:[255]{1,3}\.){2}[0-9]{1,3}\.[0-9]{1,3})", some_str)
#   if mask:
#     mask_final = mask

#   return mask_final

# def search_arp_list(some_str):
#   """trying to find arp list"""
#   arp_final = ''
#   arp = re.findall(b"\/proc\/net\/arp\n.*\n.*Device\n([\S\s]*)\n.*\n.*\n\/proc\/net\/dev\n", some_str)
#   if arp:
#     arp_string = ''.join([x.decode("utf-8") for x in arp])
#     arp_final = re.findall(r"([\S]*)(?:\s*[\S]*){2}\s*([\S]*)\s*[\S]*\s*([\S]*)\n", arp_string)

#   return arp_final


# Main function
def search(i):

  print(i)
  # search Policy name
  main_scan = main_rule(some_str)
  # write policy to excel
  for item in map (''.join, main_scan):
    b = i
    # Rule OID finder
    oid_num_id = oid_num(item)
    if oid_num_id:
      ws.write(i, 0, oid_num_id)
    # Class name finder
    class_scaned = class_name(item)
    # Rule header name finder
    header_scaned = header_name(item)
    if header_scaned:
      ws.write(i, 2, header_scaned)
    # Rule status finder
    disabled_info = disabled(item)
    if disabled_info:
      ws.write(i, 7, disabled_info)
    # Rule name finder
    rule_scaned = rule_name(item)
    if rule_scaned:
      ws.write(i, 2, rule_scaned)    
    if class_scaned:
      ws.write(i, 1, class_scaned)
      print(class_scaned)
      if class_scaned != ['security_header_rule']:
        print('Ura, ne header')
        src_list = src(item)
        for s_item in src_list:
          s_name = s_item[0]
          buf = StringIO()
          buf.write(s_name + '\n')
          s_table = s_item[1]
          ws.write(i, 3, buf.getvalue())
          ws.write(i, 4, s_table)
          
        # Rule destination info finder
        dst_list = dst(item)
        for d_item in dst_list:
          d_name = d_item[0]
          d_table = d_item[1]
          ws.write(b, 5, d_name)
          ws.write(b, 6, d_table)
          b += 1    
    if b >= i:
      i = b
    #counter +1 for next next excel row (new file)
    i += 1
  return i


row = 1
# main script    
for file in listFF:
  # open file from listdir cpinfo in read_binary mode
  f = open('C:/python/cpinfo_rules//{0}'.format(file), 'rb')
  print(row)
  print(file)
  some_str = f.read()
  # print number row, name of a file
  print(row, file)
  # write filename in first column
  #ws.write(row, 0, file)
  # starting main func
  row = search(row)
  # saving workbook
  wb.save('C:/python/outputdir/cpinfo_rules.xls')

   
# Checking script time and printing
print("--- %s seconds ---" % (time.time() - start_time))
