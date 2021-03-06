# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module provides apis to query server inventory
"""

import json
from ucsmsdk.ucsexception import UcsOperationError

inventory_spec = {
    "cpu": {
        "class_id": "ProcessorUnit",
        "props": [
            {"prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "arch"},
            {"prop": "cores"},
            {"prop": "cores_enabled"},
            {"prop": "oper_state"},
            {"prop": "socket_designation"},
            {"prop": "speed"},
            {"prop": "stepping"},
            {"prop": "threads"}
        ]
    },
    "fabric_interconnect": {
        "class_id": "NetworkElement",
        "props": [
            {"prop": "dn"},
            {"prop": "version"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "oob_if_gw"},
            {"prop": "oob_if_ip"},
            {"prop": "oob_if_mask"},
            {"prop": "total_memory"}
        ]
    },
    "memory": {
        "class_id": "MemoryUnit",
        "ignore": [
            {"prop": "presence", "value": "missing"}
        ],
        "props": [
            {"prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "capacity"},
            {"prop": "clock"},
            {"prop": "presence"}]
    },
    "psu": {
        "class_id": "EquipmentPsu",
        "ignore": [
            {"prop": "presence", "value": "missing"}
        ],
        "props": [
            {"prop": "id"},
            {"prop": "dn"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "type"},
            {"prop": "oper_state"}
        ]
    },
    "pci": {
        "class_id": "PciEquipSlot",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "mac_left"},
            {"prop": "mac_right"},
            {"prop": "smbios_id"},
            {"prop": "discovery_state"},
            {"prop": "controller_reported"}]
    },
    "vic": {
        "class_id": "AdaptorUnit",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "blade_id"},
            {"prop": "chassis_id"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "presence"},
            {"prop": "part_number"},
            {"prop": "admin_power_state"},
            {"prop": "base_mac"},
            {"prop": "conn_path"},
            {"prop": "conn_status"},
            {"prop": "perf"},
            {"prop": "voltage"},
            {"prop": "thermal"},
            {"prop": "pci_addr"},
            {"prop": "version"},
            {"prop": "pci_slot"}]
    },
    "storage": {
        "class_id": "StorageController",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "type"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "oprom_boot_status"},
            {"prop": "raid_support"},
            {"prop": "version"}
        ],
    },
    "disks": {
        "class_id": "StorageLocalDisk",
        "props": [
            {"label": "Server", "prop": "dn"},                
            {"prop": "id"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "device_type"},
            {"prop": "connection_protocol"},
            {"prop": "disk_state"},
            {"prop": "block_size"},
            {"prop": "bootable"},
            {"prop": "link_speed"},
            {"prop": "number_of_blocks"},
            {"prop": "operability"},
            {"prop": "presence"},
            {"prop": "size"},
            {"prop": "version"},
            {"prop": "power_state"}
        ]
    },
    "vNICs": {
        "class_id": "AdaptorHostEthIf",
        "props": [
            {"label": "Server", "prop": "dn"},
            {"prop": "id"},
            {"prop": "name"},
            {"prop": "cdn_name"},
            {"prop": "mac"},
            {"prop": "mtu"},
            {"prop": "admin_state"},
            {"prop": "boot_dev"},
            {"prop": "chassis_id"},
            {"prop": "side"},
            {"prop": "slot_id"},
            {"prop": "switch_id"},
            {"prop": "presence"},
            {"prop": "discovery"},
            {"prop": "link_state"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "ep_dn"},
            {"prop": "host_port"},
            {"prop": "if_type"},
            {"prop": "if_role"},
            {"prop": "order"},
            {"prop": "original_mac"}
        ]
    },
    "vHBAs": {
        "class_id": "AdaptorHostFcIf",
        "props": [
            {"prop": "id"},
            {"prop": "dn"},
            {"prop": "model"},
            {"prop": "vendor"},
            {"prop": "serial"},
            {"prop": "wwn"},
            {"prop": "node_wwn"},
            {"prop": "admin_state"},
            {"prop": "order"},
            {"prop": "boot_dev"},
            {"prop": "cdn_name"},
            {"prop": "discovery"},
            {"prop": "chassis_id"},
            {"prop": "ep_dn"},
            {"prop": "host_port"},
            {"prop": "name"},
            {"prop": "if_role"},
            {"prop": "if_type"},
            {"prop": "link_state"},
            {"prop": "max_data_field_size"},
            {"prop": "presence"},
            {"prop": "oper_state"},
            {"prop": "operability"},
            {"prop": "original_node_wwn"},
            {"prop": "original_wwn"}
        ]
    },
    "Blades": {
        "class_id": "ComputeBlade",
        "props": [
            {"prop": "admin_power"}, 
            {"prop": "admin_state"}, 
            {"prop": "asset_tag"}, 
            {"prop": "assigned_to_dn"},
            {"prop": "association"},
            {"prop": "availability"},
            {"prop": "available_memory"},
            {"prop": "chassis_id"},
            {"prop": "dn"},
            {"prop": "memory_speed"},
            {"prop": "model"},
            {"prop": "num_of_adaptors"},
            {"prop": "num_of_cores"},
            {"prop": "num_of_cores_enabled"},
            {"prop": "num_of_cpus"},
            {"prop": "num_of_eth_host_ifs"},
            {"prop": "num_of_fc_host_ifs"},
            {"prop": "oper_power"},
            {"prop": "oper_state"},
            {"prop": "original_uuid"},
            {"prop": "part_number"},
            {"prop": "serial"},
            {"prop": "server_id"},
            {"prop": "slot_id"},
            {"prop": "status"},
            {"prop": "total_memory"},
            {"prop": "uuid"},
            {"prop": "vendor"},
            {"prop": "version"}
        ]
    },
    "firmware": {
        "class_id": "FirmwareRunning",
        "props": [
            {"prop": "type"},
            {"prop": "dn"},
            {"prop": "version"}
        ]

    }

}


def _sanitize_and_store(mo_dict, prop, mo):
    value = getattr(mo, prop, None)
    if value:
        value = value.strip()
    mo_dict[prop] = value


def _should_ignore(comp, obj):
    if "ignore" not in comp:
        return False

    for ig in comp["ignore"]:
        name, value = ig["prop"], ig["value"]
        if getattr(obj, name, None) == value:
            return True
    return False


def _check_and_create_key(ds, key, value={}):
    if key in ds:
        return
    ds[key] = value


def _get_inventory(handle, comp, spec, inventory):
    component = spec[comp]
    class_id = component["class_id"]
    mos = handle.query_classid(class_id)

    ip = handle.ip
    _check_and_create_key(ds=inventory, key=ip, value={})
    _check_and_create_key(ds=inventory[ip], key=comp, value=[])
    inv_comp = inventory[ip][comp]
    for mo in mos:
        mo_dict = {}
        for each in component["props"]:
            prop = each["prop"]
            class_id = each["class"] if "class" in each else None
            method = each["method"] if "method" in each else None

            if class_id:
                if method == "query_children":
                    sub_mos = handle.query_children(in_dn=mo.dn,
                                                    class_id=class_id)
                    sub_mo = sub_mos[0]

                if sub_mo:
                    if _should_ignore(component, sub_mo):
                        continue
                    _sanitize_and_store(mo_dict, prop, sub_mo)
            else:
                if _should_ignore(component, mo):
                    continue
                _sanitize_and_store(mo_dict, prop, mo)
        if len(mo_dict) > 0:
            inv_comp.append(mo_dict)


def _get_inventory_csv(inventory, file_name, spec=inventory_spec):
    import csv
    if file_name is None:
        raise UcsOperationError("Inventory collection",
                                "file_name is a required parameter")
    f = csv.writer(open(file_name, "w"))

    x = inventory
    for comp in spec:
        f.writerow([comp.upper()])
        props = spec[comp]["props"]
        keys = [y['prop'] for y in props]
        keys.insert(0, "Host")
        f.writerow(keys)

        for ip in x:
            if comp not in x[ip]:
                continue
            host_component = x[ip][comp]
            if len(host_component) == 0:
                continue
            for entry in host_component:
                row_val = []
                for key in keys:
                    if key not in entry:
                        continue
                    row_val.append(entry[key])
                row_val.insert(0, ip)
                f.writerow(row_val)

        f.writerow([])
        f.writerow([])


def _get_search_script():
    script = """
<script>
    function myFunction() {
    // Declare variables
    var input, filter, table, tr, td, i, j, tds, ths, matched;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    tr = document.getElementsByTagName("tr");

    // Loop through all table rows, and hide
    // those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td");
        ths = tr[i].getElementsByTagName("th");
        matched = false;
        if (ths.length > 0) {
            matched = true;
        }
        else {
            for (j = 0; j < tds.length; j++) {
                td = tds[j];
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    matched = true;
                    break;
                }

            }
        }
        if (matched == true) {
            tr[i].style.display = "";
        }
        else {
            tr[i].style.display = "none";
        }
        }
    }
</script>
"""
    return script


def _get_inventory_html(inventory, file_name, spec=inventory_spec):
    if file_name is None:
        raise UcsOperationError("Inventory collection",
                                "file_name is a required parameter")
    f = open(file_name, "w")

    html = ""
    html += "<html>\n"

    html += "<head>\n"
    html += _get_search_script()
    html += "</head>\n"
    html += "<body>\n"
    html += """
    <br>
    <input type="text" id="searchInput" onkeyup="myFunction()" placeholder="Search..">
    </br>
    """

    x = inventory
    for comp in spec:
        html += '<table border="1">'
        html += "<br><br>" + comp.upper()

        props = spec[comp]["props"]
        keys = [y['prop'] for y in props]
        keys.insert(0, "Host")
        html += '<tr style="background-color: gainsboro;">'
        for key in keys:
            html += "<th>" + key + "</th>"
        html += '</tr>'

        for ip in x:
            if comp not in x[ip]:
                continue
            host_component = x[ip][comp]
            if len(host_component) == 0:
                continue
            for entry in host_component:
                row_val = []
                for key in keys:
                    if key not in entry:
                        continue
                    row_val.append(entry[key])
                row_val.insert(0, ip)
                html += "<tr>"
                for each in row_val:
                    if each is None:
                        each = ""
                    html += "<td>" + each + "</td>"
                html += "</tr>"

    html += "</table>\n"
    html += "</body>"
    html += "</html>"
    f.write(html)
    f.close()


def get_inventory(handle,
                  component="all",
                  file_format="json",
                  file_name=None,
                  spec=inventory_spec):
    """
    This method fetches the inventory of the server for various
    items like cpus, memory, psu or the entire server.

    Args:
        handle (UcsHandle or list of UcsHandle):
            Can consume a single handle or a list of handles
        component (string): comma separated values for the components
            "all" - will get inventory for all components
            For individual components use -
                "cpu, disk, memory, psu, pci, vic, vnic, vhba,
                storage, fabric_interconnect"
        file_format (string): "json", "csv", "html"
        file_name (string): file name to save the data to.
        spec (dictionary): only for advanced usage

    Returns:
        json formatted inventory data. additionally data is also written to
        a file, if one is specified.
    """

    inventory = {}

    if isinstance(handle, list):
        servers = handle
    else:
        servers = [handle]

    for server in servers:
        components = component
        if not isinstance(component, list):
            components = [component]
        if "all" in components:
            for comp in spec.keys():
                _get_inventory(server, comp, spec, inventory)
        else:
            for comp in components:
                if comp not in spec:
                    raise UcsOperationError("Inventory Collection",
                                            ("Unsupported component type:" +
                                             str(component)))

                _get_inventory(server, comp, spec, inventory)
    #split out the firmware, then add into the relevant spot in the dict
    for ip in inventory: #iterate through UCSM
        firmware = inventory[ip].pop('firmware') #remove the firmware section and set aside
        #print firmware
        for item in ['vic', 'storage','Blades', 'fabric_interconnect']: #iterate through things that have firmware
            for element, value in enumerate(inventory[ip][item]): # find the list of object in dict with firmware
                for index, firmware_item in enumerate(firmware): # iterate the list of items in the firmware list
                    #print firmware_item
                    if inventory[ip][item][element]['dn'] in firmware_item['dn'] and 'mgmt/fw-system' in firmware_item['dn'] and firmware_item['version'] != "":
                        #print firmware_item['version']
                        #print inventory[ip][item][element]
                        inventory[ip][item][element]['version'] = firmware_item['version']
                        firmware.pop(index) #remove element from firmware list 
        # storage controller version WIP
        #for element, value in enumerate(inventory[ip]['storage']): # find the list of object in dict with firmware
            #for index, firmware_item in enumerate(firmware): # iterate the list of items in the firmware list
                #print firmware_item
                #if inventory[ip][item][element]['dn'] in firmware_item['dn'] and 'fw-boot-loader' in firmware_item['dn'] and firmware_item['version'] != "":
                    #print firmware_item['version']
                    #print inventory[ip][item][element]
                #    inventory[ip][item][element]['version'] = firmware_item['version']
                #    firmware.pop(index) #remove element from firmware list 


    #iterate through inventory to add firmware to components
    if file_format == "csv":
        _get_inventory_csv(inventory=inventory, file_name=file_name, spec=spec)
    elif file_format == "html":
        _get_inventory_html(inventory=inventory, file_name=file_name, spec=spec)
    elif file_format == "json" and file_name:
        f = open(file_name, 'w')
        f.write(json.dumps(inventory))
        f.close()

    return inventory


from ucsmsdk.ucshandle import UcsHandle
#from ucsmsdk.utils.inventory import get_inventory # Missing dn in disk section, recreating locally
from yaml import dump
import sys
from argparse import ArgumentParser
import getpass

ucs_IP = '172.16.54.166'
ucs_list = ['172.16.54.166','172.16.54.169']
ucs_username = 'ucspe'
ucs_password = 'ucspe'

if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    # Input parameters, made it easier - all interactive or all via vars in script
    #parser.add_argument('--host', type=str, required=False, #default='172.16.54.166',
    #                    help="The device IP or DN")
    # Need to decide strategy on list of UCSM, interactive seems best for now
    #parser.add_argument('--host_list', type=list, required=False,
    #                    help="The list of device IP or DN")
    #parser.add_argument('-u', '--username', type=str, default='ucspe',
    #                    help="UCSM Login")
    #parser.add_argument('-p', '--password', type=str, default='ucspe',
    #                    help="UCSM Password")
    parser.add_argument('-i', '--interactive', type=bool, default=True,
                        help="Enter Password Interactively True/False, if False vars in script used")
    args = parser.parse_args()

    host_list = []
    #if args.host != None and args.host_list != None:
    #    print 'Host and Host_list are mutually exclusive'
    #    sys.exit()
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

    myinventory = get_inventory(handle=handle, file_format='csv', file_name='UCS_inventory.csv')
    with open ('UCS_inventory.yaml', 'w')  as outfile:
        dump(myinventory, outfile, default_flow_style=False)
