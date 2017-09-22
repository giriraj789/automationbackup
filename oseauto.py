#!/usr/bin/env python
import re 
import math
import os


etcdmasterdata = open("/etc/etcd/etcd.conf", "r")
for line in etcdmasterdata:
   if re.match('ETCD_INITIAL', line):
    line = line
#
def string_cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item,'', x)
    return x
#
unwanted_list= ['ETCD_INITIAL_CLUSTER=','https://',':2380','\n']
newline = string_cleanup(line, unwanted_list)
print("newline: ", newline)
    
data = newline
data_list = re.split('=|,', data)

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

a_dict = {}
b_dict = {}
a_dict = dict(zip(host, host_name))
b_dict = dict(zip(ip, host_ip))

#print a_dict
#print b_dict

#
for k,v in a_dict.items():
    print str(k+'='+v)
   
#
for k,v in b_dict.items():
    print str(k+'='+v)
