import sys
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


#Variable declarations
yFile = 'hostvars/dc1.yml'
virtual_MAC = '00:1c:73:00:00:99'

select_mac = cvpGV.getValue(GVN.CVP_MAC)
sIP = cvpGV.getValue(GVN.CVP_IP)

yaml_file = open(yFile)
info_yaml = yaml.load(yaml_file)
yaml_file.close()

shost = info_yaml['device'][select_mac]

#Grabbing sections of the YAML file
device_interfaces = info_yaml['configurations'][shost]['interfaces']
list_device_interfaces = []
#dict_loopback_interfaces = {}
list_svi_interfaces = []
VARP = False


#L3 ethernet interfaces
for r1 in device_interfaces['ethernet']:
    cid = device_interfaces['ethernet'][r1]
    lipn = '%s/%s' %(cid['ip'],cid['cidr'])
    lstatus = cid['status']
    list_device_interfaces.append((r1,{'ipn':lipn,'status':lstatus,'mode':cid['mode'],'desc':cid['description'],'portChannel':cid['portchannel']}))

list_device_interfaces.sort()

#L3 SVIs
for r1 in device_interfaces['svi']:
    cid = device_interfaces['svi'][r1]
    lipn = '%s/%s' %(cid['ip'],cid['cidr'])
    lvarp = None
    lmlag = False
    try:
        if cid['varp'] != None:
            VARP = True
            lvarp = cid['varp']
    except:
        pass
    try:
        if cid['mlag']:
            lmlag = True
        else:
            lmlag = False
    except:
        pass
    list_svi_interfaces.append((r1,{'ipn':lipn,'varp':lvarp,'mlag':lmlag}))

list_svi_interfaces.sort()
    
#Output for L3 interfaces

#Ethernet Interfaces
for r1 in list_device_interfaces:
    print('interface %s' %(r1[0]))
    if r1[1]['status'] == 'disable':
        print(' shutdown')
    print(' description %s'%r1[1]['desc'])
    if r1[1]['mode'] == 'L3':
        print(' no switchport')
        print(' ip address %s'%r1[1]['ipn'])
    else:
        print(' switchport mode %s'%(r1[1]['mode']))
        if r1[1]['portChannel'] != None:
            print(' channel-group %s mode active' %r1[1]['portChannel'])
    print('!')

#Loopback Interfaces
for r1 in device_interfaces['loopback']:
    cidl = device_interfaces['loopback']
    print('interface %s'%r1)
    llIP = '%s/%s'%(cidl[r1]['ip'],cidl[r1]['cidr'])
    print(' ip address %s'%llIP)
    #lloopINT[r1] = llIP
    print('!')

#SVIs
for r1 in list_svi_interfaces:
    print('interface %s'%r1[0])
    print(' ip address %s'%r1[1]['ipn'])
    if r1[1]['varp'] != None:
        print(' ip virtual-router address %s'%r1[1]['varp'])
    if r1[1]['mlag']:
        print(' no autostate')
    print('!')
if VARP:
    print('ip virtual-router mac-address %s'%virtual_MAC)
    print('!')