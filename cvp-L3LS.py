import sys, jsonrpclib
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


#Variable declarations
yFile = 'hostvars/l3ls.yml'

smac = cvpGV.getValue(GVN.CVP_MAC)
infoY = yaml.load(open(yFile))
shost = infoY['device'][smac]

#Grabbing sections of the YAML file
curINT = infoY['topology'][shost]['interfaces']
curBGP = infoY['topology'][shost]['BGP']
lcurINT = []
lloopINT = {}


#L3 interfaces
for r1 in curINT['ethernet']:
    cid = curINT['ethernet'][r1]
    lipn = '%s/%s' %(cid['ip'],cid['cidr'])
    lstatus = cid['status']
    lcurINT.append((r1,{'ipn':lipn,'status':lstatus,'mode':cid['mode'],'desc':cid['description']}))

lcurINT.sort()

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
for r1 in curINT['loopback']:
    cidl = curINT['loopback']
    print('interface %s'%r1)
    llIP = '%s/%s'%(cidl[r1]['ip'],cidl[r1]['cidr'])
    print(' ip address %s'%llIP)
    lloopINT[r1] = llIP
    print('!')

#Start BGP Section
print('router bgp %s' %(curBGP['as']))
print(' router-id %s'%(curINT['loopback']['Loopback0']['ip']))
print(' maximum-paths 4 ecmp 4')
for r1 in curBGP['bgp_neighbors']:
    rede = r1[0]
    reint = r1[1]
    reas = infoY['topology'][rede]['BGP']['as']
    reip = infoY['topology'][rede]['interfaces']['ethernet'][reint]['ip']
    print(' neighbor %s remote-as %s' %(reip,reas))
    print(' neighbor %s maximum-routes 12000'%(reip))
for r1 in lloopINT:
    print(' network %s'%lloopINT[r1])
print('!')