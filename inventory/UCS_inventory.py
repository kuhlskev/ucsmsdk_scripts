# -*- coding: utf-8 -*-
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.inventory import get_inventory
from yaml import dump

ucs_IP = '172.16.54.166'
ucs_username = 'ucspe'
ucs_password = 'ucspe'

handle = UcsHandle(ucs_IP, ucs_username, ucs_password)
handle.login()

myinventory = get_inventory(handle=handle, file_format='csv', file_name='UCS_inventory.csv')

with open ('UCS_Inventory.yaml', 'w')  as outfile:
    dump(myinventory, outfile, default_flow_style=False)
    