#!/usr/bin/python

#Author: Vijay Sachdeva
#Script For: Automating Cloudstack Installation

import subprocess
import os
import pyfiglet
import termcolor

hostname="yottacldmummgmt01"
username = os.geteuid()
banner = pyfiglet.figlet_format("       Cloudstack Deployment")
print(termcolor.colored(banner, 'red', attrs=['bold']))
print("User ID: " + str(username))
machine = os.name
print("Machine Type: " + machine)


print(termcolor.colored('=========================', 'blue', attrs=['bold']))
print(termcolor.colored('Setting Hostname', 'red', attrs=['bold']))
print(termcolor.colored('=========================', 'blue', attrs=['bold']))
subprocess.call(["hostnamectl", "set-hostname", hostname])

def selinux():
    print(termcolor.colored('=======================', 'blue', attrs=['bold']))
    print(termcolor.colored('Disabling Selinux and Firewalld', 'red', attrs=['bold']))
    print(termcolor.colored('=======================', 'blue', attrs=['bold']))
    subprocess.call("setenforce permissive", shell=True)
    subprocess.call("sed -i ""/^SELINUX=/ c\SELINUX=permissive" "/etc/selinux/config", shell=True)
    subprocess.call("systemctl disable firewalld", shell=True)


def packages():
    nameserver = open("/etc/resolv.conf","w")
    dnsdata = ["nameserver 8.8.8.8 \n", "nameserver 4.2.2.2 \n"]
    nameserver.writelines(dnsdata)
    nameserver.close()
    for i in ["epel-release", "wget", "net-tools", "python-setuptools", "ntp", "libselinux-python", "rng-tools"]:
        subprocess.call("yum install " + i + " -y", shell=True)
        print(termcolor.colored('================================', 'blue', attrs=['bold']))
        print(termcolor.colored(i + ' package has been installed', 'red', attrs=['bold']))
        print(termcolor.colored('================================', 'blue', attrs=['bold']))
    subprocess.call("wget -O /usr/bin/cmk https://github.com/apache/cloudstack-cloudmonkey/releases/download/6.0.0/cmk.linux.x86-64", shell=True)
    subprocess.call("chmod 755 /usr/bin/cmk", shell=True)


def mysql_connect():
        print(termcolor.colored('=======================', 'blue', attrs=['bold']))
        print(termcolor.colored('My-SQL Python Connector', 'red', attrs=['bold']))
        print(termcolor.colored('=======================', 'blue', attrs=['bold']))
        pyfile = open("/etc/yum.repos.d/mysqlconnectors.repo","w")
        pydata = ["[mysql-community] \n", "name=MySQL Community connectors \n", "baseurl=http://repo.mysql.com/yum/mysql-connectors-community/el/$releasever/$basearch/ \n", "enabled=1 \n", "gpgcheck=1 \n"]
        pyfile.writelines(pydata)
        pyfile.close()
        subprocess.call("rpm --import http://repo.mysql.com/RPM-GPG-KEY-mysql", shell=True)
        subprocess.call("yum install mysql-connector-python", shell=True)

def cloudstack():
        print(termcolor.colored('=======================', 'blue', attrs=['bold']))
        print(termcolor.colored('CloudStack Repository', 'red', attrs=['bold']))
        print(termcolor.colored('=======================', 'blue', attrs=['bold']))
        file1 = open("/etc/yum.repos.d/cloudstack.repo","w")
        data = ["[cloudstack-4.13LTS] \n","name=cloudstack \n","baseurl=http://packages.shapeblue.com/cloudstack/upstream/centos7/4.13/ \n","enabled=1 \n","gpgcheck=1 \n","gpgkey=http://packages.shapeblue.com/release.asc \n"]

        file1.writelines(data)
        file1.close()

        subprocess.call("wget http://packages.shapeblue.com/release.asc", shell=True)
        subprocess.call("rpm --import release.asc", shell=True)

        for cld in ["cloudstack-management", "cloudstack-usage"]:
            subprocess.call("yum install " + cld + " -y", shell=True)
            print("========================================")
            print(cld + " has bee installed")
            print("========================================")


def mgmt1():
        print("===============================")
        print("Setting Up Management Server-1")
        print("===============================")
        subprocess.call("cloudstack-setup-databases cloud:password@mysql-master-ip --deploy-as=root:password -i mgmt-vip-ip", shell=True)
        subprocess.call("cloudstack-setup-management", shell=True)

def mgmt2():
        print("===============================")
        print("Setting Up Management Server-2")
        print("===============================")
        subprocess.call("cloudstack-setup-databases cloud:password@mysql-master-ip -i mgmt-vip-ip", shell=True)
        subprocess.call("cloudstack-setup-management", shell=True)

def system_vm():
        
        print("===============================")
        print("Setting Up System-VM")
        print("===============================")
        subprocess.call("mount -t nfs nfs-ip:/nsfshare /mnt", shell=True)
        subprocess.call("/usr/share/cloudstack-common/scripts/storage/secondary/cloud-install-sys-tmplt -m /mnt/ -u http://download.cloudstack.org/systemvm/4.14/systemvmtemplate-4.14.0-kvm.qcow2.bz2 -h kvm -F", shell=True)


selinux()
packages()
mysql_connect()
cloudstack()
mgmt1()
mgmt2()
system_vm()
