#!/usr/bin/env python
### PREREQUISTE
### 1. Should be executed from Ansible controller server/system or jump box.
### 2. Python =<2.7.
### 3. Ansible inventry server/system configured with password less ssh to all OSE master servers. 
### USE OF SCRIPT :::: <python> <scriptname> <osemaster1server_fqdn> <output_ansible_inventry_file>
### FOR EXAMPLE::: python osebackup_host_inventry.py osemaster1.example.com > backuphosts

import re 
import os
import sys
import subprocess

## Importing ETCD file from OSE master server, first server is always a preference and extracting OSE all master servers details

ose = sys.argv[1]
os.system("scp " + ose + ":/etc/etcd/etcd.conf etcd.conf")

etcdmasterdata = open("etcd.conf", "r")
linedata = ""
for line in etcdmasterdata:
    if line.startswith('ETCD_INITIAL_CLUSTER='):
     linedata = line

print linedata

## Filter function for eliminating unwanted strings and characters from data

def string_cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item,'', x)
    return x

## Applying Filter function

unwanted_list= ['ETCD_INITIAL_CLUSTER=','https://',':2380']
newline = string_cleanup(linedata, unwanted_list)
print newline     
data = newline
data_list = re.split('=|,', data)

## Iteration based two separate lists for OSE hostnames and IP addressees

host_name = data_list[::2]
host_ip = data_list[1::2]

y = int(len(host_name))

## Iteration begins

ip = []
count = 0
while count < y:
 ip.append("masterip_" + str(count+1))
 count = count + 1

host = []
count = 0
while count < y:
 host.append("master" + str(count+1))
 count = count + 1

## Dictionary for merging OSE hostnames and IP addresses lists

host_dict = {}
ip_dict = {}
host_dict = dict(zip(host, host_name))
ip_dict = dict(zip(ip, host_ip))

## Creating Backup host inventory file 

print "[OSEV3:children]\nmasters\ncontroller\nmaster1\nmaster2\nmaster3"
print ""
print "[OSEV3:vars]\nansible_ssh_user=root"
for k, v in host_dict.items():
   print str(k+'='+v)
for k, v in ip_dict.items():
   print str(k+'='+v)
print ""
print"[masters]"
for k,v in host_dict.items():
    print str(v)
print ""
print"[controller]"
controllerhostname = os.uname()[1]
ci = subprocess.check_output(("hostname", "-i"))
controllerip = ci.strip('\n')
print str(controllerhostname+'='+controllerip)

#END
