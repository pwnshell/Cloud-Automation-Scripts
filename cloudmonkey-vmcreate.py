#!usr/bin/python

#Author: Vijay Sachdeva

import subprocess
import os
import pyfiglet
import termcolor


def vm_create():
    try:
        banner = pyfiglet.figlet_format("      CLOUDMONKEY VM-CREATOR")
        print(termcolor.colored(banner, 'green', attrs=['bold']))
        print(termcolor.colored('              Author: Vijay Sachdeva', 'red', attrs=['bold']))
        userid = os.geteuid()
        machine = os.name
        print(termcolor.colored("\nYour ID is: " + str(userid), 'red', attrs=['bold']))
        print(termcolor.colored("Your Machine Type: " + machine.upper(), 'red', attrs=['bold']))

        zone = input(termcolor.colored('Enter Zone ID: ', 'red', attrs=['bold']))
        template = input(termcolor.colored('Enter Template ID: ', 'red', attrs=['bold']))
        offering = input(termcolor.colored('Enter Service Offering ID: ', 'red', attrs=['bold']))
        network = input(termcolor.colored('Enter Guest Network ID: ', 'red', attrs=['bold']))
        vm_count = input(termcolor.colored('How many VMs you want to create: ', 'red', attrs=['bold']))
        vm_name = input(termcolor.colored('VM Name: ', 'red', attrs=['bold']))

        if userid == 0:
            print(termcolor.colored('\nCreating VMs..please relax and wait for it to complete', 'green', attrs=['blink']))
            for i in range(int(vm_count)):
                subprocess.call(["cmk", "deploy", "virtualmachine", "zoneid=" + str(zone), "templateid=" + str(template), "serviceofferingid=" + str(offering), "networkids=" + str(network), "name=" + str(vm_name) + "-" + str(i)])
        
        else:
            print(termcolor.colored('\nYou need to be root to execute this program', 'red', attrs=['bold']))

    except KeyboardInterrupt:
        print("\n")
        print(termcolor.colored('\n[+] Ctrl+C..Bye..!!', 'red'))



vm_create()
