#!/usr/bin/python

import boto
import sys
import os
from xml.dom import minidom
from pprint import pprint
from paramiko import SSHClient
from scp import SCPClient
from netaddr import IPAddress
from boto.vpc import VPCConnection

ourvpngw = "10.20.30.40"
theirsubnet = "172.254.0.0/16"
oursubnet = "10.20.30.0/24"
secretfile = "ipsec.secrets"
configfile = "ipsec.conf"
template = "ipsec.conf.template"
scparray=[]
cnt = 0
open(secretfile, 'w').close()
file = open(configfile, 'w')
filetmpl = open(template, 'r')
for line in filetmpl.readlines():
 file.write(line)
filetmpl.close()

c = boto.vpc.connect_to_region("eu-west-1")

vpns = c.get_all_vpn_connections()
for i in vpns:
 vpnid = i.id
 state = i.state
 if state != "deleted":
     config = i.customer_gateway_configuration
     if config == "[]":
      print("No configured tunnels found.")
      exit()
     else:
      xmldoc = minidom.parseString(config)
      ipsec_tunnel = xmldoc.getElementsByTagName('ipsec_tunnel')

for tun in ipsec_tunnel:
 vpn_gateway = tun.getElementsByTagName('vpn_gateway')
 pre_shared_key = tun.getElementsByTagName('pre_shared_key')
 value = pre_shared_key[0]
 parse = value.firstChild
 psk = parse.data
 for gw in vpn_gateway:
  tunnel_outside_address = gw.getElementsByTagName('tunnel_outside_address')
  for outip in tunnel_outside_address:
    ip_address = outip.getElementsByTagName('ip_address')
    value = ip_address[0]
    parse = value.firstChild
    externalip = parse.data
  tunnel_inside_address = gw.getElementsByTagName('tunnel_inside_address')
  for inip in tunnel_inside_address:
    ip_address = inip.getElementsByTagName('ip_address')
    value = ip_address[0]
    parse = value.firstChild
    internalip = parse.data
    ourip = IPAddress(internalip) + 1
    ourinternalip = str(ourip)
 
 cnt = cnt+1
 aws = str(cnt);

 file = open(secretfile, 'a')
 file.write(externalip + " : PSK  " + "\"" + psk + "\"" + "\n")
 file.close()

 variables = [ourinternalip,oursubnet,theirsubnet,externalip,internalip]
 print("leftsubnet={0}/30,{1}\nright={3}\nrightsubnet={4}/30,{3}\nauto=start".format,variables)
 file = open(configfile, 'a')
 file.write("\nconn aws-" + aws + "\n\tleftsubnet=" + ourinternalip + "/30," + oursubnet + "\n\tright=" + externalip + "\n\trightsubnet=" + internalip + "/30," + theirsubnet + "\n\tauto=start\n")
 file.close()

scparray.append(secretfile)
scparray.append(configfile)
localpath = "."
for cnf in scparray:
 remotepath = "/etc"
 localpath = (cnf)
 s=""
 buildpath = (remotepath, "/", cnf)
 remotepath = s.join(buildpath)
 print("Config file to be transfered: ", localpath);
 print("Destination on ", ourvpngw, ": ", remotepath);
 
 ssh = SSHClient()
 ssh.load_system_host_keys()
 ssh.connect(ourvpngw, port=666, username="root")

 scp = SCPClient(ssh.get_transport())
 scp.put(localpath, remotepath)
