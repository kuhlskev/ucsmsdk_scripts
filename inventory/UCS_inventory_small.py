# -*- coding: utf-8 -*-
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.inventory import get_inventory
handle = UcsHandle('172.16.54.166', 'ucspe', 'ucspe') # ucsm_ip, username, password
handle.login()
myinventory = get_inventory(handle=handle, file_format='csv', file_name='UCS_inventory.csv')

    