#!/usr/bin/python

import boto
from boto.vpc import VPCConnection
import sys, getopt

givenid = sys.argv[1]

c = boto.vpc.connect_to_region("eu-west-1")

c.delete_vpn_connection(givenid)

vpns = c.get_all_vpn_connections()
print vpns;
