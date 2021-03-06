#!/usr/bin/python

import boto
import time
from boto.vpc import VPCConnection
outnetcidr="10.20.30.0/24"
cgw="cgw-a3dfeed7"
vgw="vgw-6a0b3a1e"

def newroutadd():
 addroute = c.create_vpn_connection_route(outnetcidr, vpnid)
 print(addroute)

def availwait():
 for i in vpns:
  state = i.state
  if state != "available":
   time.sleep(10)
   availwait()
  else:
   newroutadd()

def get():
 for i in vpns:
  vpnid = i.id
  state = i.state
  tunnels = i.tunnels
 if state != "deleted":
  print(vpnid, state, tunnels)
  print(routeflag)
  if routeflag == "1":
   availwait()
   exit()
  else:
   exit()
 else:
  print ("Deleted vpn: ", vpnid);

def createvpn():
 newvpn = c.create_vpn_connection("ipsec.1",cgw,vgw,1,0)
 print newvpn;
 routeflag="1"
 get()

c = boto.vpc.connect_to_region("eu-west-1")

routeflag="0"
vpns = c.get_all_vpn_connections()
if str(vpns) == "[]":
 print "No vpn tunnel configured..."
 createvpn()
else:
 get()
 createvpn()
