  import pexpect
    import pxssh
    import sys          #hz module
    import re           #Parser module
    import os           #hz module
    import getopt
    import glob                     #hz module
    import xlrd                     #Excel read module
    import xlwt                     #Excel write module
    import telnetlib                #telnet module
    import shutil

    #open excel book
    rb = xlrd.open_workbook('/samba/allaccess/Energomera_Eltek_list.xlsx')
    #select work sheet
    sheet = rb.sheet_by_name('IPs')
    #rows number in sheet
    num_rows = sheet.nrows
    #cols number in sheet
    num_cols = sheet.ncols
    #creating massive with IP addresses inside
    ip_addr_list = [sheet.row_values(rawnum)[0] for rawnum in range(sheet.nrows)]
    #create excel workbook with write permissions (xlwt module)
    wb = xlwt.Workbook()
    #create sheet IP LIST with cell overwrite rights
    ws = wb.add_sheet('IP LIST', cell_overwrite_ok=True)
    #create counter
    i = 0
    #authorization details
    port = "23"                             #telnet port
    user = "admin"                         #telnet username
    password = "12345"                  #telnet password

    #firmware ask function
    def fw_info():
        print('asking for firmware')
        px.sendline('firmware info')
        px.expect('bt6000#')

    #firmware update function
    def fw_send():
        print('sending firmware')
        px.sendline('tftp server 172.27.2.21')
        px.expect('bt6000')
        px.sendline('firmware download tftp firmware.ext2')
        px.expect('Updating')
        px.sendline('y')
        px.send(chr(13))
        ws.write(i, 0, host)
        ws.write(i, 1, 'Energomera')

    #if eltek found - skip, write result in book
    def eltek_found():
        print(host, "is Eltek. Skipping")
        ws.write(i, 0, host)
        ws.write(i, 1, 'Eltek')

    #if 23 port telnet conn. refused - skip, write result in book
    def conn_refuse():
        print(host, "connection refused")
        ws.write(i, 0, host)
        ws.write(i, 1, 'Connection refused')

    #auth function
    def auth():
        print(host, "is up! Energomera found. Starting auth process")
        px.sendline(user)
        px.expect('assword')
        px.sendline(password)

    #start working with ip addresses in ip_addr_list massive
    for host in ip_addr_list:
    #spawn pexpect connection 
        px = pexpect.spawn('telnet ' + host)
        px.timeout = 35
        #create log file with in IP.txt format (10.1.1.1.txt, for example)
        fout = open('/samba/allaccess/Energomera_Eltek/{0}.txt'.format(host),"wb")
        #push pexpect logfile_read output to log file
        px.logfile_read = fout
        try:
            index = px.expect (['bt6000', 'sername', 'refused'])
            #if device tell us bt6000 - authorize        
            if index == 0:
                auth()  
                index1 = px.expect(['#', 'lease'])
                #if "#" - ask fw version immediatly
                if index1 == 0:
                    print('seems to controller ID already set')
                    fw_info()
                #if "Please" - press 2 times Ctrl+C, then ask fw version
                elif index1 == 1:
                    print('trying control C controller ID')
                    px.send(chr(3))
                    px.send(chr(3))
                    px.expect('bt6000')
                    fw_info()
    #firmware update start (temporarily off)
    #            fw_send()

    #Eltek found - func start
            elif index == 1:
                eltek_found()
    #Conn refused - func start
            elif index == 2:
                conn_refuse()
                #print output to console (test purposes)
                print(px.before)
            px.send(chr(13))
    #Copy from current log file to temp.txt for editing
            shutil.copy2('/samba/allaccess/Energomera_Eltek/{0}.txt'.format(host), '/home/bark/expect/temp.txt')
    #EOF result - skip host, write result to excel
        except pexpect.EOF:
            print(host, "EOF")
            ws.write(i, 0, host)
            ws.write(i, 1, 'EOF')
            #print output to console (test purposes)
            print(px.before)
    #Timeout result - skip host, write result to excel
        except pexpect.TIMEOUT:
            print(host, "TIMEOUT")
            ws.write(i, 0, host)
            ws.write(i, 1, 'TIMEOUT')
            #print output to console (test purposes)
            print(px.before)
            #Copy from current log file to temp.txt for editing
            shutil.copy2('/samba/allaccess/Energomera_Eltek/{0}.txt'.format(host), '/home/bark/expect/temp.txt') 
            #count +1 to correct output for Excel
        i += 1 
    #workbook save
    wb.save('/samba/allaccess/Energomera_Eltek_result.xls') 