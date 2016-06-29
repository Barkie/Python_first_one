import re
from os import listdir
import time
import xlwt
from io import StringIO
# Timer trigger to count time at the end of a script
start_time = time.time()


listFF = listdir('C:/python/cpinfo/')

# Excel NO_IDEA_what value (xlwt settings, something to deal with column size)
WIDTH_CONST = 256

# Excel column width
widths = 13, 43, 25, 35, 35, 25, 8, 8, 8, 8, 25

# Excel column names
headers = (
    'Rule Number', 'chkpf_uid', 'Rule Name', 'Src name', 'Dst name', 'Service', 'Action', 'Track', 'Install On', 'Time', 'Comment', 'Disable')

# Creating excel workbook with write permissions (xlwt module)    
wb = xlwt.Workbook()


def objects(some_str):
  """trying to find all objects in the cpinfo"""
  objects_list_final = ''
  obj_list_binary = re.findall(b':Name \((.*)\)\r{0,1}\n.*:Table \((.*)\)\r{0,1}\n.*:Uid \("(.*)\"\)\r{0,1}\n', some_str)
  print(type(obj_list_binary))
  print(len(obj_list_binary))
  if obj_list_binary:
    objects_list_final = obj_list_binary
    #objects_list_final = ([x.decode("cp1251") for x in obj_list_binary])
  return list(set(objects_list_final))


# Main function
def search(i):
  # Search all rules unfiltered
  objects_list = objects(some_str)
  # Searching every rule for details
  for item in objects_list:
    final_list = ([x.decode("cp1251") for x in item])
    ws.write(i, 1, final_list[0])
    ws.write(i, 2, final_list[1])
    ws.write(i, 3, final_list[2])
    i += 1
        # counter +1 for next next excel row (new file)
  return i


row = 1
# main script    
for file in listFF: 
  # Creating sheet IP LIST with cell overwrite rights
  print(file)
  table_name = file[:30]
  print(table_name)
  ws = wb.add_sheet('{0}'.format(table_name), cell_overwrite_ok=True)
  # Setting width
  for index, width in enumerate(widths):
    ws.col(index).width = WIDTH_CONST * width
  # Writing first row
  for index, header in enumerate(headers):
    ws.write(0, index, header)
  print('Working on file ' + file)
  # Cpening file from folder file list
  f = open('C:/python/cpinfo//{0}'.format(file), 'rb')
  # Reading file content
  # Printing row, file (debug purpose)
  print(row, file)
  # Row number = result of search function
  # open file from listdir cpinfo in read_binary mode
  print('Working on file ' + file)
  some_str = f.read()
  # starting main func
  row = search(row)
  row = 1
  # saving workbook
  f.close()
  wb.save('C:/python/outputdir/checkpoint_objects.xls')
  print(file + ' analyzing finished\n\n----------------------------------------------------')

   
# Checking script time and printing
print("--- Script time = %s seconds ---" % (time.time() - start_time))
