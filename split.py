import re

f = open('c:/python/db_test/cdp1.txt', 'r+')
some_str = f.read()
some_re = re.findall(r"Port ID\n([\S\s]*)\n", some_str)
some_re_splt = re.findall(r'(\S*)[\s\n]{1,}(\S*.\S*)\s{1,}(\S*)\s{1,}(\w(?:\s\w){0,4})\s{1,}(\S*(?: Ser)?)\s{1,}(\S* \S*)', ''.join(some_re))
item_ids = 0, 1, 2, 3, 4, 5
dev_id = local_iface = holdtime = capability = platform = remote_iface = 0
cdp_fields = dev_id, local_iface, holdtime, capability, platform, remote_iface

def split_motherfucker():
        """Split every string in the cdp neighbor info"""    
        dev_id = item[0]
        local_iface = item[1]
        holdtime = item[2]
        capability = item[3]
        platform = item[4]
        remote_iface = item[5]
        
        return dev_id, local_iface, holdtime, capability, platform, remote_iface


for item in some_re_splt:
        dev_id, local_iface, holdtime, capability, platform, remote_iface = split_mutherfucker()
#        split_mutherfucker()
        print('\n-----\n')
        print('Device ID = ', dev_id)
        print('Local Interface = ', local_iface)
        print('Holdtime = ', holdtime)
        print('Capability = ', capability)
        print('Remote Device Platform = ', platform)
        print('Remote Device LOL Interface = ', remote_iface)
        
	
