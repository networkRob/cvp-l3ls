import sys, jsonrpclib
sys.path.append('/usr/lib64/python2.7/site-packages/')
import yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVariableNames as GVN


def sendCmd(commands):
    if ztp == True:
        user = cvpGV.getValue(GVN.ZTP_USERNAME)
        passwd = cvpGV.getValue(GVN.ZTP_PASSWORD)
    else:
        user = cvpGV.getValue(GVN.CVP_USERNAME)
        passwd = cvpGV.getValue(GVN.CVP_PASSWORD)
    url = "https://%s:%s@%s/command-api"%(user,passwd,hostip)
    switch = jsonrpclib.Server(url)
    response = switch.runCmds(1,commands)[0]
    return(response)


#Variable declarations
yFile = 'hostvars/l3ls.yml'

smac = cvpGV.getValue(GVN.CVP_MAC)
ztp = cvpGV.getValue(GVN.ZTP_STATE)
hostip = cvpGV.getValue(GVN.CVP_IP)
infoY = yaml.load(open(yFile))
shost = sendCmd(['show hostname'])['hostname']

#L3 interfaces
for r1 in infoY['L3'][shost]:
    lip = r1['ip']
    lstatus = r1['status']
    print('interface %s' %(r1['interface']))
    if lip == '0.0.0.0':
        print(' switchport mode access')
    else:
        print(' no switchport')
        print(' ip address %s/%s' %(lip,r1['cidr']))
    if lstatus == 'disable':
        print(' shutdown')
    print(' description %s' %(r1['description']))
    print('!')
print('ip routing')
print('!')
print('router bgp %s' %(infoY['BGP'][shost]['as']))
print(' maximum-paths 4 ecmp 4')
for r1 in infoY['BGP'][shost]['bgp_neighbors']:
    for r2 in infoY['topology'][shost]['connections']:
        if r1['device'] == r2['device']:
            reINT = r2['interface']
            for r3 in infoY['L3'][r1['device']]:
                if reINT == r3['interface']:
                    reIP = r3['ip']
    print(' neighbor %s remote-as %s' %(r1['device'],r1['remote-as']))
print(' redistribute connected')
print('!')