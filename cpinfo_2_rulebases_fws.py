import re
from os import listdir
import time
import xlwt

# timer trigger to count time at the end of a script
start_time = time.time()

# folder with cpinfo files
listFF = listdir('C:/python/cpinfo/')


def rulebases(some_str):
  """trying to find rulebases info in CPinfo"""
  # creating final variable to return back from this function
  rulebases_final = ''
  # regex for rulebases searching
  rulebases = re.findall(
    b"----\n.*\/rulebases_5_0.fws\n[-]*\n([\S\s]*?\n\)\n)", some_str)
  # if rulebases found, decoding and changing to final variable
  if rulebases:
    rulebases_final = ([x.decode("cp1251") for x in rulebases])


  return rulebases_final

# open file from listdir cpinfo in read_binary mode
for file in listFF:
  # printing info to the IDLE
  print('Trying to open file ' + file)
  # opening file
  f = open('C:/python/cpinfo//{0}'.format(file), 'rb')
  # printing info to the IDLE
  print('File opened. Working on file ' + file)
  # reading file into variable 
  some_str = f.read()
  # opening/creating file in the format CPinfo_Name_Rulebases_5_0.fws
  rb_file = open('C:/python/rulebases_5_0//{0}'.format
    (file + '_rulebases_5_0.fws'), 'w')
  # filling variable with rulebases() function return variable
  rulebases_final = rulebases(some_str)
  # changing to the string and writing final result variable into file
  rb_file.write(''.join(rulebases_final))
  # closing rulebasesfile
  rb_file.close()
  # closing cpinfo file
  f.close()
  # printing info to the IDLE
  print(file + ' analyzing finished\n\n'
    '---------------------------------------------------')

   
# checking script time and printing to the IDLE
print("--- Script time = %s seconds ---" % (time.time() - start_time))
