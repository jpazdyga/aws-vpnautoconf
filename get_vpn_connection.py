#!/usr/bin/python

from pprint import pprint
import boto
from boto.vpc import VPCConnection

c = boto.vpc.connect_to_region("eu-west-1")

vpns = c.get_all_vpn_connections()
for i in vpns:
 vpnid = i.id
 state = i.state
 print (vpnid, ": ", state);
# if state != "deleted":
#     config = i.customer_gateway_configuration
#     print config;
#  pprint(i.__dict__)

