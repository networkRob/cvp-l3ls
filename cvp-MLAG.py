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
curINT = infoY['configurations'][shost]['interfaces']
curBGP = infoY['configurations'][shost]['BGP']
lcurINT = []
lloopINT = {}


#MLAG Configurations
# Add code for MLAG