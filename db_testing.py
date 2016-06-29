 try:
                c.execute(("INSERT INTO {tn} ({idc}, {host}, {devid}, {locif}, {hold}, {cap}, {plat}, {remif}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)").\
                    format(tn='CDP', idc=c_ID, host=c_hostname, devid=c_dev_id, locif=c_local_iface,\
                        hold=c_holdtime, cap=c_capability, plat=c_remote_platform, remif=c_remote_iface), cdp_id)