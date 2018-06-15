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
curINT = infoY['configurations'][shost]['interfaces']
lcurINT = []
lloopINT = {}
lsvis = []
VARP = False


#L3 ethernet interfaces
for r1 in curINT['ethernet']:
    cid = curINT['ethernet'][r1]
    lipn = '%s/%s' %(cid['ip'],cid['cidr'])
    lstatus = cid['status']
    lcurINT.append((r1,{'ipn':lipn,'status':lstatus,'mode':cid['mode'],'desc':cid['description']}))

lcurINT.sort()

#L3 SVIs
for r1 in curINT['svi']:
    cid = curINT['svi'][r1]
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
    lsvis.append((r1,{'ipn':lipn,'varp':lvarp,'mlag':lmlag}))

lsvis.sort()
    
#Output for L3 interfaces

#Ethernet Interfaces
for r1 in lcurINT:
    print('interface %s' %(r1[0]))
    if r1[1]['status'] == 'disable':
        print(' shutdown')
    print(' description %s'%r1[1]['desc'])
    if r1[1]['mode'] == 'L3':
        print(' no switchport')
        print(' ip address %s'%r1[1]['ipn'])
    else:
        print(' switchport mode %s'%(r1[1]['mode']))
    print('!')

#Loopback Interfaces
for r1 in curINT['loopback']:
    cidl = curINT['loopback']
    print('interface %s'%r1)
    llIP = '%s/%s'%(cidl[r1]['ip'],cidl[r1]['cidr'])
    print(' ip address %s'%llIP)
    lloopINT[r1] = llIP
    print('!')

#SVIs
for r1 in lsvis:
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