#!/usr/bin/env python
import re 
import math
import os
import sys
import subprocess

#importing etcd file from any masterserver and extracting master servers details

os.system("scp root@$1:/etc/etcd/etcd.conf etcd.conf")
etcdmasterdata = open("etcd.conf", "r")
for line in etcdmasterdata:
   if re.match('ETCD_INITIAL', line):
    line = line

#function to filter unwanted strings and characters from extracted data

def string_cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item,'', x)
    return x

#applying string_cleanup function

unwanted_list= ['ETCD_INITIAL_CLUSTER=','https://',':2380','\n']
newline = string_cleanup(line, unwanted_list)
    
data = newline
data_list = re.split('=|,', data)

# 2 seprate lists for hostname and ip address iteration based on data_list length

host_name = data_list[::2]
host_ip = data_list[1::2]

y = int(len(host_name))


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

#Dictonary for merging hostname and ipaddress lists

a_dict = {}
b_dict = {}
a_dict = dict(zip(host, host_name))
b_dict = dict(zip(ip, host_ip))

# Hostfile creation process starts
print "[OSEV3:children]\nmasters\ncontroller\nmaster1\nmaster2\nmaster3"
print ""
print "[OSEV3:vars]\nansible_ssh_user=root"
for k,v in a_dict.items():
    print str(k+'='+v)
#
for k,v in b_dict.items():
    print str(k+'='+v)
print ""
print"[masters]"
for k,v in a_dict.items():
    print str(v)
print ""
print"[controller]"
controllerhostname = os.uname()[1]
ci = subprocess.check_output(("hostname", "-i"))
controllerip = ci.strip('\n')
print str(controllerhostname+'='+controllerip)

#END
#HOW TO USE
#python backuphost_inventory.py master1.example.com

