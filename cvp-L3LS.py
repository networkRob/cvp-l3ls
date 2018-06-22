"""
This script is used to create BGP configurations within the L3 leaf and spine topology.
"""

import sys
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


#Variable declarations
yFile = 'hostvars/dc1.yml'

smac = cvpGV.getValue(GVN.CVP_MAC)

yaml_file = open(yFile)
infoY = yaml.load(yaml_file)
yaml_file.close()

shost = infoY['device'][smac]

#Grabbing sections of the YAML file
curINT = infoY['configurations'][shost]['interfaces']
curBGP = infoY['configurations'][shost]['BGP']
lloopINT = None

try:
    lloopINT = curINT['loopback']['Loopback0']['ip']
    lloopINTN = '%s/%s'%(lloopINT,curINT['loopback']['Loopback0']['cidr'])
except:
    pass

#Start BGP Section
print('router bgp %s' %(curBGP['as']))
if lloopINT != None:    
    print(' router-id %s'%(lloopINT))
print(' maximum-paths 4 ecmp 4')
for r1 in curBGP['bgp_neighbors']:
    rede = r1[0]
    reint = r1[1]
    reas = infoY['configurations'][rede]['BGP']['as']
    reip = infoY['configurations'][rede]['interfaces']['ethernet'][reint]['ip']
    print(' neighbor %s remote-as %s' %(reip,reas))
    print(' neighbor %s maximum-routes 12000'%(reip))
if lloopINT != None:
    print(' network %s'%lloopINTN)
print('!')