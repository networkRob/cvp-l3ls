import sys
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


#Variable declarations
yFile = 'hostvars/dc1.yml'

select_mac = cvpGV.getValue(GVN.CVP_MAC)

yaml_file = open(yFile)
info_yaml = yaml.load(yaml_file)
yaml_file.close()

shost = info_yaml['device'][select_mac]

#Grabbing sections of the YAML file
global_vlan = info_yaml['global']['leafs']['VLANS']
device_vlan = info_yaml['configurations'][shost]['VLANS']


if device_vlan['global']:
    for r1 in global_vlan:
        print('vlan %s'%r1['vlan'])
        if r1['name'] != None:
            print(' name %s'%r1['name'])
        if r1['trunkgroup'] != None:
            print(' trunk group %s'%r1['trunkgroup'])
        print('!')
for r1 in device_vlan['custom']:
    print('vlan %s'%r1['vlan'])
    if r1['name'] != None:
        print(' name %s'%r1['name'])
    if r1['trunkgroup'] != None:
        print(' trunk group %s'%r1['trunkgroup'])
    print('!')
