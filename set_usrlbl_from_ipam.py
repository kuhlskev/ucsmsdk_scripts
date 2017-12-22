# -*- coding: utf-8 -*-
from ucsmsdk.ucshandle import UcsHandle
from pandas import ExcelFile
from argparse import ArgumentParser
import getpass
from ucsmsdk.ucsexception import UcsOperationError

ucs_list = ['172.16.54.166']
ucs_list = ['172.16.54.166','172.16.54.169']
ucs_username = 'ucspe'
ucs_password = 'ucspe'
xl_file = 'host_to_mac.xls'

def xls_to_dict(filepath):
    try:
        xls = ExcelFile(filepath)
    except IOError:
        print '%s File Not found'%filepath
        return {}
    df = xls.parse(xls.sheet_names[0])
    d = df.to_dict(orient='records')
    return d

def find_blade(handle, mac):
    '''Searches UCS for the adaptor with MAC and returns blade dn'''
    vn = handle.query_classid("AdaptorHostEthIf")
    for item in vn:
        if item.mac == mac:
            return item.dn.split('/adaptor')[0]
    return 'none'

def write_label(handle, dn, label):
    '''adds label to specified dn'''
    mo = handle.query_dn(dn)
    print 'old_label ' + mo.usr_lbl
    mo.usr_lbl = label
    handle.add_mo(mo, True)
    handle.commit()

def get_handle_list(args):
    host_list = []
    if args.interactive:        
        while True:
            host = raw_input("Enter UCSM to query (enter to continue): ")
            if host == "": break
            host_list.append(host) 
        username = raw_input("Enter Username: ")   
        password = getpass.getpass(prompt="Enter Password: ")
    else: # Use the Global Variables
        password = ucs_password
        username = ucs_username
        host_list = ucs_list
    handle_list = []
    #for host in args.host_list: # Doesnt work as argument seen as a string, not a list of strings
    for host in host_list:
        try:
            handle_instance = UcsHandle(host, username, password)
            handle_instance.login()
            handle_list.append(handle_instance)
        except:
            print "unable to connect to %s"%host
    return handle_list

if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-i', '--interactive', action='store_true', default=False,
                        help="Enter UCS Details Interactively")
    args = parser.parse_args()
    handle_list = get_handle_list(args)
    if args.interactive: xl_file = raw_input("Enter XLS filepath: ") 
    ipam_list = xls_to_dict(xl_file)
    for item in ipam_list:
        for handle in handle_list:
            blade_dn = find_blade(handle, item['mac'])
            if blade_dn != 'none':
                print '%s %s mac found on %s'%(item['hostname'], item['mac'], blade_dn)
                write_label(handle, blade_dn, item['hostname'])
                break                
        if blade_dn == 'none':
            print '%s %s mac not found'%(item['hostname'], item['mac'])