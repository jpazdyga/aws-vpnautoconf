#!/usr/bin/python

import boto
from boto.vpc import VPCConnection
outnetcidr="10.20.30.0/24"

def addroute():
 for i in vpns:
  print(i)
  vpnid = i.id
  state = i.state
  tunnels = i.tunnels
  if state != "deleted":
   print (vpnid, state, tunnels);
   addroute = c.create_vpn_connection_route(outnetcidr, vpnid)
   print addroute;
  else:
   print ("Deleted vpns: ", vpnid);


c = boto.vpc.connect_to_region("eu-west-1")

vpns = c.get_all_vpn_connections()
if str(vpns) == "[]":
 print "No vpn tunnel configured..."
 exit()
else:
 addroute()
