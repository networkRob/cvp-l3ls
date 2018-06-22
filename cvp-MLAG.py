"""
This script is used to create MLAG configurations within the topology.
"""

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

device_mlag = info_yaml['configurations'][shost]['MLAG']
global_mlag = info_yaml['global']['leafs']['MLAG']

if device_mlag['enabled']:
    #Create PeerLink port-channel
    if device_mlag['global']:
        peer_link = global_mlag['peerLink']
        mlag_trunkgroup = ''
        port_channel_mode = ''
        for r1 in info_yaml['global']['leafs']['portchannel']:
            if r1['intf'] == peer_link:
                mlag_trunkgroup = r1['trunkgroup']
                port_channel_mode = r1['mode']
        print('interface %s' %peer_link)
        if mlag_trunkgroup != '':
            print(' switchport trunk group %s'%mlag_trunkgroup)
        if port_channel_mode != '':
            print(' switchport mode %s' %port_channel_mode)
    print('!')

    #MLAG Configurations
    peer_device = device_mlag['custom']['peer']
    peer_device_4094 = info_yaml['configurations'][peer_device]['interfaces']['svi']['Vlan4094']['ip']
    #Need code to get peer's Ma1 interface IP address for heartbeat
    print('mlag configuration')
    if device_mlag['global']:
        print(' local-interface %s' %global_mlag['local'])
        print(' peer-link %s' %global_mlag['peerLink'])
        print(' reload-delay mlag %s' %global_mlag['relDelay'])
        #print(' dual-primary detection delay %s action errdisable all-interfaces' %global_mlag['dualDelay'])
    print(' domain-id %s' %device_mlag['custom']['domainid'])
    print(' peer-address %s' %peer_device_4094)


