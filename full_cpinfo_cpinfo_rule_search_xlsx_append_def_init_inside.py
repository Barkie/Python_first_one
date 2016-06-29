import re
from os import listdir
import time
import xlwt
from io import StringIO
# timer trigger to count time at the end of a script
start_time = time.time()

# folder with rulebases files
listFF = listdir('C:/python/rulebases_5_0/')

# excel module (xlwt) variable, something to deal with column size)
WIDTH_CONST = 256

# excel column width
widths = 13, 43, 25, 35, 35, 25, 8, 8, 8, 8, 25

# excel column names
headers = (
    'Rule Number', 'chkpf_uid', 'Rule Name', 'Src name', 'Dst name', 'Service', 'Action', 'Track', 'Install On', 'Time', 'Comment', 'Disable')

# creating excel workbook with write permissions (xlwt module)    
wb = xlwt.Workbook()


def main_rule(some_str):
  """trying to find hostname of the Check Point"""
  rule_final = ''
  rule = re.findall(b"(:rule \(\r{0,1}\n[\S\s]*?\s{4}\)\r{0,1}\n\s{3}\)\r{0,1}\n\s{2}\))", some_str)
  if rule:
    rule_final = ([x.decode("cp1251") for x in rule])
  #print('rule final len ') #debug purpose
  #print(len(rule_final)) #debug purpose
  return rule_final

def class_name(some_str):
  """trying to find policy name"""
  class_final = ''
  class_name = re.findall(r":ClassName \((.*rule)\)\r{0,1}\n", some_str)
  if class_name:
    # decode bytes to unicode
    class_final = class_name
  #print(len(class_final))
  return class_final

def rule_name(some_str):
  """trying to find all interfaces and addresses"""
  rule_name_final = ''
  rule = re.findall(r'\s{4}:name \("?(.*[^"])"*?\)', some_str)
  if rule:
    # decode bytes to unicode
    rule_name_final = rule
  #print(len(rule_name_final))  
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
    src_objects = re.findall(r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", ''.join(src))
    if src_objects:
      src_buf = StringIO()
      for s_item in src_objects:
        s_name = s_item[0]
        src_buf.write(s_name + '\n')
      src_final = re.findall(r'([\S\s]*)\r{0,1}\n', src_buf.getvalue())
  return src_final

def dst(some_str):
  """trying to get destination info"""
  dst_final = ''
  dst = re.findall(r".*:dst([\S\s]*):install", some_str)
  if dst: 
    dst_objects = re.findall(r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", ''.join(dst))
    if dst_objects:
      dst_buf = StringIO()
      for d_item in dst_objects:
        d_name = d_item[0]
        dst_buf.write(d_name + '\n')  
      dst_final = re.findall(r'([\S\s]*)\r{0,1}\n', dst_buf.getvalue())
  return dst_final

def disabled(some_str):
  """trying to find disabled rule or not"""
  disabled_final = ''
  disabled = re.findall(r'\s{4}:disabled \((.*)\)', some_str)
  if disabled:
    if disabled != ['true']:
      disabled_final = 'Enabled'
    else:
      disabled_final = 'Disabled'
  return disabled_final
  

def oid_num(some_str):
  """trying to find rule OID"""
  oid_num_final = ''
  oid_num = re.findall(
    r'\s{4}:chkpf_uid \("{0,}(.*)"+?\)\r{0,1}\n.*:ClassName (?:\(security.*\))',
     some_str)
  if oid_num:
    # decode bytes to unicode
    oid_num_final = oid_num
  return oid_num_final

def services(some_str):
  """trying to find rule services"""
  services_final = ''
  srv = re.findall(r".*:services([\S\s]*):src", some_str)
  if srv:
    srv_objects = re.findall(
      r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", ''.join(srv))
    if srv_objects:
      srv_buf = StringIO()
      for srv_item in srv_objects:
        srv_name = srv_item[0]
        srv_buf.write(srv_name + '\n')
      services_final = re.findall(
        r'([\S\s]*)\r{0,1}\n', srv_buf.getvalue())
  return services_final

def action(some_str):
  """trying to find action status"""
  action_final = ''
  act = re.findall(r".*:action([\S\s]*):action", some_str)
  if act:
    act_objects = re.findall(
      r":ClassName \((.*)\)\r{0,1}\n.*:table \((.*)\)", 
      ''.join(act))
    if act_objects:
      act_buf = StringIO()
      for act_item in act_objects:
        act_name = act_item[0]
        act_buf.write(act_name + '\n')
      action_final = re.findall(
        r'([\S\s]*)_.*\r{0,1}\n', act_buf.getvalue())
  return action_final

def track(some_str):
  """trying to find Track status"""
  track_final = ''
  trc = re.findall(r".*:track([\S\s]*):dst", some_str)
  if trc:
    trc_objects = re.findall(
      r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", ''.join(trc))
    if trc_objects:
      trc_buf = StringIO()
      for trc_item in trc_objects:
        trc_name = trc_item[0]
        trc_buf.write(trc_name + '\n')     
      track_final = re.findall(
        r'([\S\s]*)\r{0,1}\n', trc_buf.getvalue())  
  return track_final

def install_on(some_str):
  """trying to find action status"""
  install_final = ''
  inst = re.findall(r".*:install([\S\s]*):name", some_str)
  if inst:
    inst_objects = re.findall(
      r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", 
      ''.join(inst))
    if inst_objects:
      inst_buf = StringIO()
      for inst_item in inst_objects:
        inst_name = inst_item[0]
        inst_buf.write(inst_name + '\n')      
      install_final = re.findall(
        r'([\S\s]*)\r{0,1}\n', inst_buf.getvalue())
  return install_final

def time_install(some_str):
  """trying to find Time installed info"""
  time_final = ''
  time = re.findall(r".*:time([\S\s]*):track", some_str)
  if time:
    time_objects = re.findall(
      r":Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)", ''.join(time))
    if time_objects:
      time_buf = StringIO()
      for time_item in time_objects:
        time_name = time_item[0]
        time_buf.write(time_name + '\n')
      time_final = re.findall(
        r'([\S\s]*)\r{0,1}\n', time_buf.getvalue())
  return time_final

def comment(some_str):
  """trying to find rule comments"""
  comment_final = ''
  comment = re.findall(
    r".*:comments.\(([\S\s]*?)\)\r{0,1}\n", some_str)
  if comment:
    comment_final = comment
  return comment_final

# main function
def search(i):
  # search all rules unfiltered
  main_scan = main_rule(some_str)
  # searching every rule for details
  for item in map (''.join, main_scan):
    # class name finder
    class_scaned = class_name(item)
    if class_scaned != ['security_header_rule']:
      # ws.write(i, 2, class_scaned)
      # rule OID finder
      oid_num_id = oid_num(item)
      if oid_num_id:
        ws.write(i, 1, oid_num_id)
      # rule name finder
      rule_scaned = rule_name(item)
      if rule_scaned:
        ws.write(i, 2, rule_scaned)    
      # rule disable status finder
      disabled_info = disabled(item)
      if disabled_info:
        ws.write(i, 11, disabled_info)
      # rule source info finder
      source_rules = src(item)
      if source_rules:
        ws.write(i, 3, ''.join(source_rules))
      # rule destination info finder
      destination_rules = dst(item)
      if destination_rules:
        ws.write(i, 4, destination_rules)
      # rule service info finder
      services_rules = services(item)
      if services_rules:
        ws.write(i, 5, services_rules)
      # rule action info finder
      action_rules = action(item)
      if action_rules:
        ws.write(i, 6, action_rules)
      # rule track info finder
      track_rules = track(item)
      if track_rules:
        ws.write(i, 7, track_rules)
      # rule install on info finder
      install_rules = install_on(item)
      if install_rules:
        ws.write(i, 8, install_rules)
      # rule Time info finder
      time_rules = time_install(item)
      if time_rules:
        ws.write(i, 9, time_rules)  
      # rule comment info finder
      comments_rules = comment(item)
      if comments_rules:
        ws.write(i, 10, comments_rules)

      # counter +1 for next next excel row (new file)
      i += 1
  return i


row = 1
# main script    
for file in listFF:
  # creating sheet IP LIST with cell overwrite rights
  table_name = file[:30]
  print(table_name)
  ws = wb.add_sheet('{0}'.format(table_name), cell_overwrite_ok=True)
  
  # setting width
  for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width

  # writing first row
  for index, header in enumerate(headers):
    ws.write(0, index, header)
  # open file from listdir cpinfo in read_binary mode
  f = open('C:/python/rulebases_5_0//{0}'.format(file), 'rb')
  print('Working on file ' + file)
  some_str = f.read()
  print(len(some_str))
  print(type(some_str))
  # write filename in first column
  #ws.write(row, 0, file)
  # starting main func
  row = search(row)
  row = 1
  # saving workbook
  try:
    wb.save('C:/python/outputdir/cpinfo_rules.xls')
  except PermissionError:
    # nice info output if PermissionError in SaveExcelWorkbook
    print('\n--------------------------------------------------'
          '\n--------------------ERROR-------------------------'
          '\nFile is opened! Close a file before continuing!!!!'
          '\n--------------------------------------------------'
          '\n-------------------------------------------------)')
    # stopping script if file is opened after expection accured
    raise Exception
  print(file + 
    ' analyzing finished\n\n----' \
    '------------------------------------------------')

   
# checking script time and printing
print("--- Script time = %s seconds ---" % (time.time() - start_time))
