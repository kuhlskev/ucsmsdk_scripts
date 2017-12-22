# -*- coding: utf-8 -*-
from ucsmsdk.ucshandle import UcsHandle
import sys
from pandas import ExcelFile
from argparse import ArgumentParser
import getpass
from ucsmsdk.ucsexception import UcsOperationError

ucs_list = ['172.16.54.166']
ucs_username = 'ucspe'
ucs_password = 'ucspe'
xl_file = 'host_to_mac.xls'


if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-i', '--interactive', action='store_true', default=False,
                        help="Enter Password Interactively")
    args = parser.parse_args()

    host_list = []
    if args.interactive == True:        
        while True:
            host = raw_input("Enter UCSM to query (enter to continue): ")
            if host == "":
                break
            host_list.append(host) 
        username = raw_input("Enter Username: ")   
        password = getpass.getpass(prompt="Enter Password: ")
    else:
        # Use the Variables above main
        password = ucs_password
        username = ucs_username
        host_list = ucs_list

    if host_list != []:  #this will be the default path as interactive input creates a list
        handle = []
        #for host in args.host_list: # Doesnt work as argument seen as a string, not a list of strings
        for host in host_list:
            print host
            handle_instance = UcsHandle(host, username, password)
            handle_instance.login()
            handle.append(handle_instance)
    else:
        handle = UcsHandle(args.host, username, password)
        handle.login()

    service_profile = 'org-root/org-Kev/ls-kev-sp-8'
    service_profile = 'sys/chassis-5/blade-1'
    mo = handle[0].query_dn(service_profile)
    print mo.usr_lbl
    mo.usr_lbl = 'hostnameX'
    handle[0].add_mo(mo, True)
    handle[0].commit()