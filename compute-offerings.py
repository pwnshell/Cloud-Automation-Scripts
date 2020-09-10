#!/usr/bin/python

#Author: Vijay Sachdeva
#Script for creating n number of compute offerings

import pyfiglet
import subprocess
import termcolor

cname = open("/opt/name", "r")
cpu = open("/opt/cpu", "r")
ram = open("/opt/mem", "r")

try:
        banner = pyfiglet.figlet_format("            Compute Offerings")
        print(termcolor.colored(banner, 'green', attrs=['bold']))
        for i, j, k in zip(cname, cpu, ram):
                l=i.strip()
                m=j.strip()
                n=k.strip()
                subprocess.call(["cmk", "create", "serviceoffering", "name=" + str(l), "displaytext=" + str(l), "cpunumber=" + str(m), "cpuspeed=2000", "memory=" + str(n), "offerha=true", "tags=SSD", "hosttags=CIMI"])

except KeyboardInterrupt:
        print("\n")
        print(termcolor.colored('\n[+] Ctrl+C..Bye..!!', 'red'))

cname.close()
cpu.close()
ram.close()
