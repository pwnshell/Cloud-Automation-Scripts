#!/usr/bin/python
import pyfiglet
import subprocess
import termcolor
x = ["1C_1R", "2C_2R"]
y = [1, 2]
z = [1024, 2048]
banner = pyfiglet.figlet_format("            Compute Offerings")
print(termcolor.colored(banner, 'green', attrs=['bold']))
for i, j, k in zip(x, y, z):
   subprocess.call(["cmk", "create", "serviceoffering", "name=" + str(i), "displaytext=" + str(i), "cpunumber=" + str(j), "cpuspeed=2000", "memory=" + str(k), "offerha=true", "tags=SSD", "hosttags=CIMI"])
