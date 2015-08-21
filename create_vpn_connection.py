#!/usr/bin/python

import boto
from boto.vpc import VPCConnection

def get():
 vpnid = vpns[0].id
 state = vpns[0].state
 tunnels = vpns[0].tunnels
 if state != "deleted":
  print (vpnid, state, tunnels);
  if routeflag == "1":
   addroute = c.create_vpn_connection_route("10.10.10.0/24", vpnid)
   print addroute;
   exit()
  else:
   exit()
 else:
  print ("Deleted vpns: ", vpnid);

def createvpn():
 newvpn = c.create_vpn_connection("ipsec.1","cgw-a3dfeed7","vgw-6a0b3a1e",1,0)
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
