import sqlite3


sqlite_file = 'c:/python/db_test/sw.db'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('c:/python/db_test/sw.db')
c = conn.cursor()

c_ID = 'Row_Number'
c_filename = 'File_Name'
c_hostname = 'Hostname'

i = 1
file_name = 'UPSVUG_59022-NS-CR-01E 192.168.15.252 tech-support.txt'
hostname = 'KNPS-7206-1-.!DOT-10.1.23.2'

#        try:
#            c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
#                format(tn='ASO', idf=id_column, cn=column_name))
#        except sqlite3.IntegrityError:
#            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))
c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {tf}, {nf2} {tf2}, {nf3} {tf3})'\
          .format(tn='ASO', nf=c_ID, tf='INTEGER', nf2=c_filename, tf2='VARCHAR(255)', nf3=c_hostname, tf3='VARCHAR(255)'))        


#c.execute('CREATE TABLE ' + SW'(id INTEGER PRIMARY KEY, hostname VARCHAR(100), test_field VARCHAR(100))')


#        try:
#            c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
#                format(tn='ASO', idf=id_column, cn=column_name))
#        except sqlite3.IntegrityError:
#            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))
host_id = (i, file_name, hostname)

try:
    c.execute(("INSERT INTO {tn} ({idc}, {file}, {host}) VALUES (?, ?, ?)").\
              format(tn='ASO', idc=c_ID, file=c_filename, host=c_hostname), host_id)
except sqlite3.IntegrityError:
    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(t_file))
conn.commit()
conn.close()
