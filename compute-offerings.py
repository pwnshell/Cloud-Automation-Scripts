#!/usr/bin/python

#Author: Vijay Sachdeva
#Script for creating n number of compute offerings

import pyfiglet
import subprocess
import termcolor

x = open("/opt/name", "r")
y = open("/opt/cpu", "r")
z = open("/opt/mem", "r")


banner = pyfiglet.figlet_format("            Compute Offerings")
print(termcolor.colored(banner, 'green', attrs=['bold']))
for i, j, k in zip(x, y, z):
   subprocess.call(["cmk", "create", "serviceoffering", "name=" + str(i), "displaytext=" + str(i), "cpunumber=" + str(j), "cpuspeed=2000", "memory=" + str(k), "offerha=true", "tags=SSD", "hosttags=CIMI"])
