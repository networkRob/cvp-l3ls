import sys, jsonrpclib, yaml
from cvplibrary import CVPGlobalVariables as cvpGV
from cvplibrary import GlobalVriableNames as GVN


def sendCmd(commands):
    if ztp == True:
        user = cvpGV.getValue(GVN.ZTP_USERNAME)
        passwd = cvpGV.getValue(GVN.ZTP_PASSWORD)
    else:
        user = cvpGV.getValue(GVN.CVP_USERNAME)
        passwd = cvpGV.getValue(GVN.CVP_PASSWORD)
    url = "https://{0}:{1}@{2}/command-api".format(user,passwd,hostip)
    switch = jsonrpclib.Server(url)
    response = switch.runCmds(1,commands)[0]
    return(response)


#Variable declarations
yFile = 'hostvars/l3ls.yml'

smac = cvpGV.getValue(GVN.CVP_MAC)
ztp = cvpGV.getValue(GVN.ZTP_STATE)
hostip = cvpGV.getValue(GVN.CVP_IP)
infoY = yaml.load(yFile)
shost = sendCmd(['show hostname'])['hostname']

#L3 interfaces
for r1 in infoY['L3'][shost]:
    print('interface {0}'.format(r1['interface']))
    print(' no switchport')
    print(' ip address {0}/{1}'.format(r1['ip'],r1['cidr']))
    print(' description {0}'.format(r1['description']))
    print('!')

print('router bgp {0}'.format(infoY['BGP'][shost]['as']))
for r1 in i['BGP'][shost]['bgp_neighbors']:
    for r2 in i['topology'][shost]['connections']:
        if r1['device'] == r2['device']:
            reINT = r2['interface']
            for r3 in i['L3'][r1['device']]:
                if reINT == r3['interface']:
                    reIP = r3['ip']
    print(' neighbor {0} remote-as {1}'.format(r1['device'],r1['remote-as']))
print(' redistribute connected')
print('!')