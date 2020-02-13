#!/user/bin/env python3 
"""
taxDeed.py: This program is used for tax deed purposes.
Requirements: python2.7 or later.

Error Codes:
------------
1) Endpoint is none. 
2) Endpoint authentication failed. 
"""

__author__ = "Michael Shobitan"
__copyright__ = "Copyright 2020, UIF Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "UIF"
__version__ = "0.1.1"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@yahoo.com"
__status__ = "Development"

import os
import re
import sys
import csv
import json
import time
import atexit
import shutil
import locale
import urllib3
import inspect
import argparse
import requests
import subprocess
import pandas as pd
from columnar import columnar
from collections import defaultdict
locale.setlocale(locale.LC_ALL, 'en_US')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fileDate = (time.strftime('%Y%m%d'))
fileTime = (time.strftime('%H%M%S'))

headers = {'Content-type':'application/json'}
endpoints = ['UIF-DRM1P', 'UIF-SOM1D']

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
            usage='use "python %(prog)s -h" for help',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)                                         

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='''Show this help message and exit.

arguments for cluster creation
    -e|--endpoint ENDPOINT, Rancher Endpoint
''')                                  

    requiredNamed = parser.add_argument_group('required arguments')
                                    
    requiredNamed.add_argument('-e',
                        '--endpoint',
                        choices=endpoints,
                        type=str,
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

taxDeedListFileCSV = 'Feb 2020.csv'
totalYearsDelinquentCSV = 'totalYearsDelinquent.csv'
filesToDelete = [taxDeedListFileCSV, totalYearsDelinquentCSV]

def error_handling():
    unexpected_error = ("Unexpected error:", sys.exc_info()[0])
    error = (sys.exc_info()[1])
    if("UPDATE_IN_PROGRESS" in str(error)):
        print("ERROR: The current cluster is in UPDATE_IN_PROGRESS state and can not be updated.")
    elif("No updates are to be performed" in str(error)):
        print("INFO: No updates are to be performed.")
    elif("No cluster found for name" in str(error)):
        print("EEROR: Cluster not found!")
    elif("list index out of range" in str(error)):
        print("ERROR: Please check your tag options!")
    elif("is in UPDATE_ROLLBACK_FAILED state" in str(error)):
        print("INFO: " + cluster + " is in update rollback failed state, cannot be updated.")
    elif("ResourceInUseException" in str(error)):
        print("INFO: " + cluster + " currently has update in progress!")
    elif("Cluster is already at the desired configuration" in str(error)):
        print("INFO: " + cluster + " is already at the desired configuration!")
    elif("No changes needed for the logging config provided" in str(error)):
        print("INFO: " + cluster + " is already at the desired configuration!")
    else:
        print("Unexpected error:", sys.exc_info()[1])
        raise
        print("ERROR: Unknown error, exiting...")
        removeAnsibleJSON_File()
        sys.exit(13)

def get_env_creds(argument):
    switch = {
        "UIF-DRM1P" : {"env_url" : "http://uif-drm1p.yahoo.com/v3",
                 "key" : "token-c8s9d",
                 "secret" : "sd7r7wwd4g7wzg86h7xjzxfgkqttqw6n9vxnxxk6k6vpx8t7rmg9dg",
                    },
        "UIF-SOM1D" : {"env_url" : "http://uif-som1d.yahoo.com/v3",
                 "key" : "toekn-xgswk",
                 "secret" : "hf2f52jmdtszlw9wx64d68dz2rrfdb9ls8vh87mmkp48gv98kl6w6n",
                    },
    }
    data = switch.get(argument, "ERROR: Invalid Environment!")

    env_url = data['env_url']
    key = data['key']
    secret = data['secret']

    return env_url, key, secret

endpointList = ['UIF-DRM1P', 'UIF-SOM1D']

taxDeedListFileExcel = 'Feb 2020.xlsx'

cd = os.chdir('/Users/mike/Documents/Life/Business/United Investments/Tax Deed List (Auction)')

data_xls = pd.read_excel(taxDeedListFileExcel, 'Sheet1', index_col=None)
data_xls.to_csv(taxDeedListFileCSV, index=False, header=1, encoding='utf-8')
with open(taxDeedListFileCSV, 'r') as f:
    d_reader = csv.DictReader(f)

    headers = d_reader.fieldnames

    data = []
    for line in d_reader:
        row = []
        for header in headers:
            row.append(line[header])
        
        data.append(row)

table = columnar(data, headers, no_borders=True)
print(table)

addressYearsDelinquentHighest = ''
totalYearsDelinquentHighest = 0
totalYearsDelinquentHighestOO = ''

addressBalanceHighest = ''
balanceHighest = 0
balanceHighestOO = ''

addressPropertyValueHighest = ''
propertyValueHighest = 0
propertyValueHighestOO = ''

highestValueDict = {}
for row in data:
    address = (row[0])
    ownerOccupied = (row[1])
    totalYearsDelinquent = (row[2])
    balance = (row[4])
    propertyValue = (row[5])
    if(totalYearsDelinquent != ''):
        totalYearsDelinquent = float(totalYearsDelinquent)
        if(totalYearsDelinquent > totalYearsDelinquentHighest):
            addressYearsDelinquentHighest = address
            totalYearsDelinquentHighestOO = ownerOccupied
            totalYearsDelinquentHighest = totalYearsDelinquent

    if(balance != ''):
        balance = float(balance)
        if(balance > balanceHighest):
            addressBalanceHighest = address
            balanceHighestOO = ownerOccupied
            balanceHighest = balance

    if(propertyValue != ''):
        propertyValue = float(propertyValue)
        if(propertyValue > propertyValueHighest):
            addressPropertyValueHighest = address
            propertyValueHighestOO = ownerOccupied
            propertyValueHighest = propertyValue
    else:
        # print('INFO: No value')
        pass

print('INFO: Most Years Delinquent \'' + addressYearsDelinquentHighest + '\'')
print('INFO: Owner Occupied ' + totalYearsDelinquentHighestOO)
print('INFO: Years ' + str(int(totalYearsDelinquentHighest)))

print('\nINFO: Highest Tax Balance \'' + addressBalanceHighest + '\'')
print('INFO: Owner Occupied ' + balanceHighestOO)
balanceHighest = locale.format_string("%.2f", balanceHighest, grouping=True)
print('INFO: Balance $' + str(balanceHighest))

print('\nINFO: Highest Property Value \'' + addressPropertyValueHighest + '\'')
print('INFO: Owner Occupied ' + propertyValueHighestOO)
propertyValueHighest = locale.format_string("%.2f", propertyValueHighest, grouping=True)
print('INFO: Balance $' + str(propertyValueHighest))

df = pd.read_csv(taxDeedListFileCSV)
df = df.sort_values('Total Years Deliquent', ascending=False)
df.to_csv(totalYearsDelinquentCSV, index=False)

with open(totalYearsDelinquentCSV, 'r') as f:
    d_reader = csv.DictReader(f)

    headers = d_reader.fieldnames

    data = []
    printLineCounter = 0
    printLineCount = 5
    print('\nINFO: Top ' + str(printLineCount) + ' Total Years Deliquent Properties\n--------------------------------------------')
    for line in d_reader:
        row = []
        for header in headers:
            if(header == 'Total Years Deliquent'):
                row.append(line[header])
                if(line['Total Years Deliquent'] != ''):
                    if(printLineCounter < 5):
                        printLineCounter += 1
                        print(str(printLineCounter) + ') ' + line['Address'] + ', ' + line[header] + ' years deliquent')
                    else:
                        break
        
        data.append(row)

table = columnar(data, headers, no_borders=True)
# print(table)

for thisFile in filesToDelete:
    if(os.path.isfile(thisFile)):
        os.remove(thisFile)

# fileOne = 'UIF_Main_' + fileDate + '_' + fileTime + '.csv'
# fileTwo = 'UIF_Relationship_' + fileDate + '_' + fileTime + '.csv'

# def writeToFile(rowValuesList):
#     headers = ['ci_name', 'type', 'subtype', 'first_asset_tag', 'second_asset_tag', 'sn_chassis', 'sn_hw_support', 'license_key', 'brief_description', 'division_managed_by', 'managing_region', 'managing_area', 'ci_management_group', 'status', 'current_usage', 'environment_type', 'support_level', 'sla_support_id', 'service_technology', 'vendor_contract_id', 'change_freeze', 'global', 'regional_affecting', 'under_change_management', 'qualified_ci', 'validated_ci', 'embedded_system', 'business_critical', 'dmz', 'maint_window', 'pso_type', 'month_within_quarter', 'week_within_month', 'day_with_week', 'time_within_day', 'reboot_after_maintenance', 'region', 'country', 'location', 'building', 'floor', 'room', 'grid', 'cabinet_ci_id', 'asset_owner', 'it_service', 'service_owner', 'service_category', 'network_service_type', 'logical_group_code', 'data_center_located', 'cost_center_fm_service', 'demarcation_point_a', 'demarcation_point_b', 'supervisor_model', 'no_of_supervisors', 'no_of_power_supplies', 'capacity_demand_plan', 'fm_tier_level', 'assetcenter_id', 'po_number', 'received_date', 'charge_start_date', 'charge_end_date', 'device_addition_reason', 'device_addition_source', 'device_reduction_reason', 'device_consolidation_target', 'warranty_expiration_date', 'shared_infrastructure_status', 'uc4_status', 'utilization_exception', 'manufacturer_product_vendor', 'model_product_name', 'version', 'bt_roadmap_id', 'allocated_cpu_core_count', 'total_cpu_core_count', 'cpu_type', 'cpu_speed', 'memory', 'vm_memory_cap', 'operating_system', 'service_pack_patch_set', 'build_number', 'patch_level', 'internal_disk_space_gb', 'server_limit', 'cluster_type', 'service_component', 'installation_date', 'host_id', 'remote_console', 'middleware_type', 'middleware_version', 'modules', 'domain_type', 'admin_url', 'domain_path', 'instance_type', 'instance_port_port_no', 'jvm_type', 'jvm_version', 'i_am_pxed_version', 'i_am_install_path', 'reverse_proxy', 'grouping_type', 'cluster_name', 'multicast_address', 'multicast_port', 'installation_path', 'power_up_plan', 'power_up_seq', 'power_down_plan', 'drp_outage_notes', 'tdrp_service_level', 'tdrp_summary', 'duration_of_last_tdrp_test', 'last_tdrp_test', 'backup_master_server', 'backup_notes', 'firmware_revision', 'total_raw_storage', 'added_at_time', 'added_by', 'last_updated_at_time', 'last_updated_by', 'last_scan_at_time', 'last_scanned_by', 'prod_move_at_time', 'prod_move_by', 'decom_move_at_time', 'decom_move_by', 'retire_move_at_time', 'retire_move_by', 'comments', 'number_of_users', 'document_home', 'external_ref_id', 'external_ref_reference', 'source_id', 'source_reference', 'database_name', 'database_instance_name', 'database_host', 'database_type', 'database_domain', 'development_type', 'sox_value', 'dr_rto_tier', 'confidentiality', 'integrity', 'risk_category', 'gxp', 'gcp', 'gdp', 'glp', 'gmp', 'pci', 'pi', 'spi', 'safe_harbor', 'ma201', 'dms_branding', 'printer_type', 'monitor_type', 'monitor_size', 'schema_name', 'approval_details', 'config_item_owner_full_name', 'contact_sc_id', 'user_id_nt_id', 'escalation_contacts', 'use_ci_owners_primary_location', 'monitoring_requirement', 'reason_for_no_monitoring', 'monitoring_dns_name', 'alert_assignment_group', 'incident_assignment_group', 'aliases_1', 'aliases_2', 'aliases_3', 'rfc_business_approvers', 'rfc_business_approvers_2', 'rfc_business_approvers_3', 'rfc_business_approvers_4', 'rfc_technical_approvers', 'rfc_technical_approvers_2', 'rfc_technical_approvers_3', 'rfc_technical_approvers_4', 'org_level_1', 'org_level_2', 'org_level_3', 'cost_center', 'usage_percent', 'org_level_1_2', 'org_level_2_2', 'org_level_3_2', 'cost_center_2', 'usage_percent_2', 'org_level_1_3', 'org_level_2_3', 'org_level_3_3', 'cost_center_3', 'usage_percent_3', 'org_level_1_4', 'org_level_2_4', 'org_level_3_4', 'cost_center_4', 'usage_percent_4', 'domain_group', 'dns_name', 'default_gateway', 'tcpip_address', 'mac_address', 'bandwidth', 'network_port', 'teamed', 'connection_type', 'domain_group_2', 'dns_name_2', 'default_gateway_2', 'tcpip_address_2', 'mac_address_2', 'bandwidth_2', 'network_port_2', 'teamed_2', 'connection_type_2', 'domain_group_3', 'dns_name_3', 'default_gateway_3', 'tcpip_address_3', 'mac_address_3', 'bandwidth_3', 'network_port_3', 'teamed_3', 'connection_type_3', 'total_floor_space_sq_ft', 'power_capacity_kw', 'cooling_capacity_btu', 'additional_attribute', 'attribute_size', 'attribute_value', 'additional_attribute_2', 'attribute_size_2', 'attribute_value_2', 'additional_attribute_3', 'attribute_size_3', 'attribute_value_3', 'impact_threshold', 'ci_id_logical_name', 'pfz_authentication', 'child_downstream', 'action_type', 'update_description', 'sc_ticket_num']
#     with open(fileOne,'w') as csvFile:
#         writer = csv.DictWriter(csvFile,fieldnames=headers)
#         writer.writeheader()
#         writer.writerows(rowValuesList)

# writeToFile(rowValuesList)

# def writeToFileTwo(rowValuesListTwo):
#     fileTwoheaders = ['downstream_ci_id', 'downstream_ci_name', 'downstream_type_subtype', 'upstream_ci_id', 'upstream_ci_name', 'upstream_relationship_type', 'relationship_subtype', 'type_subtype', 'unique_id', 'ci_relationship_status']
#     with open(fileTwo,'w') as csvFile:
#         writer = csv.DictWriter(csvFile,fieldnames=fileTwoheaders)
#         writer.writeheader()
#         writer.writerows(rowValuesListTwo)

# writeToFileTwo(rowValuesListTwo)
