import sys, jsonrpclib
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


#Variable declarations
yFile = 'hostvars/l3ls.yml'
virtual_MAC = '00:1c:73:00:00:99'

smac = cvpGV.getValue(GVN.CVP_MAC)
sIP = cvpGV.getValue(GVN.CVP_IP)
infoY = yaml.load(open(yFile))
shost = infoY['device'][smac]

#Grabbing sections of the YAML file
gloVLAN = infoY['global']['leafs']['VLANS']
curVLAN = infoY['configurations'][shost]['VLANS']


if curVLAN['global']:
    for r1 in gloVLAN:
        print('vlan %s'%r1['vlan'])
        if r1['name'] != None:
            print(' name %s'%r1['name'])
        if r1['trunkgroup'] != None:
            print(' trunk group %s'%r1['trunkgroup'])
        print('!')
for r1 in curVLAN['custom']:
    print('vlan %s'%r1['vlan'])
    if r1['name'] != None:
        print(' name %s'%r1['name'])
    if r1['trunkgroup'] != None:
        print(' trunk group %s'%r1['trunkgroup'])
    print('!')
