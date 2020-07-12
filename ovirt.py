#!/usr/bin/python

import subprocess
import os
import pyfiglet
import termcolor



def banner():
    ban = pyfiglet.figlet_format("    Ovirt Deployment")
    print(termcolor.colored(ban, 'green', attrs=['bold']))
    machine = os.name
    userid = os.geteuid()
    print(termcolor.colored('==============================================================================================', 'red', attrs=['bold']))
    print(termcolor.colored('[+] DISCLAIMER: Ovirt-Shell commands will only work when you setup the API authentication', 'blue', attrs=['bold']))
    print(termcolor.colored('\nReference Links below:', 'blue', attrs=['bold']))
    print(termcolor.colored('[+] 1. https://www.ovirt.org/develop/release-management/features/infra/cli.html', 'blue', attrs=['bold']))
    print(termcolor.colored('[+] 2. https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.1/pdf/rhevm_shell_guide/Red_Hat_Virtualization-4.1-RHEVM_Shell_Guide-en-US.pdf', 'blue', attrs=['bold']))
    print(termcolor.colored('==============================================================================================', 'red', attrs=['bold']))
    print(termcolor.colored('\nUser ID: ' + str(userid), 'green', attrs=['bold']))
    print(termcolor.colored('Machine Type: ' + str(machine), 'green', attrs=['bold']))

def ovirt_install():
    print(termcolor.colored('\n===================', 'red', attrs=['bold']))
    print(termcolor.colored('Updating Packages', 'green', attrs=['bold']))
    print(termcolor.colored('===================', 'red', attrs=['bold']))
    subprocess.call(["yum", "update", "-y"])
    print("")
    subprocess.call(["yum", "install", "https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm"])
    subprocess.call(["yum", "install", "ovirt-engine", "-y"])
    subprocess.call(["engine-setup"])

def ovirt_setup():
    print(termcolor.colored('============', 'red', attrs=['bold']))
    print(termcolor.colored('CREATING DC', 'green', attrs=['bold']))
    print(termcolor.colored('============', 'red', attrs=['bold']))
    dc_name = input(termcolor.colored('\nEnter DC Name: ', 'red', attrs=['bold']))
    subprocess.call(["ovirt-shell", "-E", "add datacenter --name " + dc_name + " --storage_type Shared --description " + dc_name])

    print(termcolor.colored('=================', 'red', attrs=['bold']))
    print(termcolor.colored('CREATING CLUSTER', 'green', attrs=['bold']))
    print(termcolor.colored('=================', 'red', attrs=['bold']))
    cluster = input(termcolor.colored('\nEnter Cluster Name: ', 'red', attrs=['bold']))
    subprocess.call(["ovirt-shell", "-E", "add cluster --name " + cluster + " --data_center-name " + dc_name])


    print(termcolor.colored('=======================', 'red', attrs=['bold']))
    print(termcolor.colored('ADDING HOST TO CLUSTER', 'green', attrs=['bold']))
    print(termcolor.colored('=======================', 'red', attrs=['bold']))
    hostname = input(termcolor.colored('\nEnter HostName: ', 'red', attrs=['bold']))
    ip = input(termcolor.colored('\nEnter IP Address: ', 'red', attrs=['bold']))
    password = input(termcolor.colored('\nEnter Password of host: ', 'red', attrs=['bold']))
    subprocess.call(["ovirt-shell", "-E", "add host --cluster-name " + cluster + " --name " + hostname + " --root_password " + password + " --address " + ip])

def vm_create():
    print(termcolor.colored('============', 'red', attrs=['bold']))
    print(termcolor.colored('ADDING VMs', 'green', attrs=['bold']))
    print(termcolor.colored('============', 'red', attrs=['bold']))
    vm_name = input(termcolor.colored('Enter VM Name: ', 'red', attrs=['bold']))
    temp_name = input(termcolor.colored('Enter Template Name: ', 'red', attrs=['bold']))
    vm_count = input(termcolor.colored('How many VMs you want to create: ', 'red', attrs=['bold']))

    print(termcolor.colored('\nCreating VMs..please relax and wait for it to complete', 'green', attrs=['blink']))
    for i in range(int(vm_count)):
            subprocess.call(["ovirt-shell", "-E", "add vm --name " + name + "-" + str(i) + " --cluster-name " + cluster + " --template-name " + temp_name])


banner()
ovirt_install()
ovirt_setup()
vm_create()
