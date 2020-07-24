#!/usr/bin/python

#Author: Vijay Sachdeva
#Script For: Automating Cloudstack 4.13 Installation

import subprocess
import os
import pyfiglet
import termcolor

hostname="Enterhostname"
username = os.geteuid()
banner = pyfiglet.figlet_format("       Cloudstack Deployment")
print(termcolor.colored(banner, 'green', attrs=['bold']))
print(termcolor.colored('              Author: Vijay Sachdeva', 'red', attrs=['bold']))
print("\nUser ID: " + str(username))
machine = os.name
print("Machine Type: " + machine)


print(termcolor.colored('\n=================', 'red', attrs=['bold']))
print(termcolor.colored('Setting Hostname', 'green', attrs=['bold']))
print(termcolor.colored('=================', 'red', attrs=['bold']))
subprocess.call(["hostnamectl", "set-hostname", hostname])
print(termcolor.colored('\n=================', 'red', attrs=['bold']))
print(termcolor.colored('Hostname Changed: ' + hostname, 'green', attrs=['bold']))
print(termcolor.colored('=================', 'red', attrs=['bold']))
print(termcolor.colored('\n=================', 'red', attrs=['bold']))
print(termcolor.colored('Updating RPMs installed', 'red', attrs=['bold']))
print(termcolor.colored('\n=================', 'red', attrs=['bold']))
subprocess.call("yum update -y", shell=True)

def selinux():
    print(termcolor.colored('\n===============================', 'red', attrs=['bold']))
    print(termcolor.colored('Disabling Selinux and Firewalld', 'green', attrs=['bold']))
    print(termcolor.colored('===============================', 'red', attrs=['bold']))
    subprocess.call("setenforce permissive", shell=True)
    subprocess.call("sed -i ""/^SELINUX=/" "c\SELINUX=disabled"" /etc/sysconfig/selinux", shell=True)
    subprocess.call("systemctl disable firewalld", shell=True)


def packages():
    nameserver = open("/etc/resolv.conf","w")
    dnsdata = ["nameserver 8.8.8.8 \n", "nameserver 4.2.2.2 \n"]
    nameserver.writelines(dnsdata)
    nameserver.close()
    for i in ["epel-release", "wget", "net-tools", "python-setuptools", "ntp", "libselinux-python", "rng-tools"]
        subprocess.call("yum install " + i + " -y", shell=True)
        print(termcolor.colored('================================', 'red', attrs=['bold']))
        print(termcolor.colored(i + ' package has been installed', 'green', attrs=['bold']))
        print(termcolor.colored('================================', 'red', attrs=['bold']))
    subprocess.call("wget -O /usr/bin/cmk https://github.com/apache/cloudstack-cloudmonkey/releases/download/6.0.0/cmk.linux.x86-64", shell=True)
    subprocess.call("chmod 755 /usr/bin/cmk", shell=True)



def mysql_connect():
        print(termcolor.colored('\n=======================', 'blue', attrs=['bold']))
        print(termcolor.colored('My-SQL Python Connector', 'red', attrs=['bold']))
        print(termcolor.colored('=======================', 'blue', attrs=['bold']))
        pyfile = open("/etc/yum.repos.d/mysqlconnectors.repo","w")
        pydata = ["[mysql-community] \n", "name=MySQL Community connectors \n", "baseurl=http://repo.mysql.com/yum/mysql-connectors-community/el/$releasever/$basearch/ \n", "enabled=1 \n", "gpgcheck=1 \n"]
        pyfile.writelines(pydata)
        pyfile.close()
        subprocess.call("rpm --import http://repo.mysql.com/RPM-GPG-KEY-mysql", shell=True)
        subprocess.call("yum install mysql-connector-python", shell=True)
        subprocess.call("yum install http://mirror.centos.org/centos/7/os/x86_64/Packages/mysql-connector-java-5.1.25-3.el7.noarch.rpm", shell=True)

def cloudstack():
        print(termcolor.colored('\n=======================', 'red', attrs=['bold']))
        print(termcolor.colored('CloudStack Repository', 'green', attrs=['bold']))
        print(termcolor.colored('=======================', 'red', attrs=['bold']))
        file1 = open("/etc/yum.repos.d/cloudstack.repo","w")
        data = ["[cloudstack-4.13LTS] \n","name=cloudstack \n","baseurl=http://packages.shapeblue.com/cloudstack/upstream/centos7/4.13/ \n","enabled=1 \n","gpgcheck=1 \n","gpgkey=http://packages.shapeblue.com/release.asc \n"]

        file1.writelines(data)
        file1.close()

        subprocess.call("wget http://packages.shapeblue.com/release.asc", shell=True)
        subprocess.call("rpm --import release.asc", shell=True)

        for cld in ["cloudstack-management", "cloudstack-usage"]:
            subprocess.call("yum install " + cld + " -y", shell=True)
            print(termcolor.colored('\n=========================================', 'red', attrs=['bold']))
            print(termcolor.colored(cld + ' has bee installed',  'green', attrs=['bold']))
            print(termcolor.colored('=========================================', 'red', attrs=['bold']))


def mgmt1():
        print(termcolor.colored('\n===============================', 'red', attrs=['bold']))
        print(termcolor.colored('Setting Up Management Server-1', 'green', attrs=['bold']))
        print(termcolor.colored('===============================', 'red', attrs=['bold']))
        subprocess.call("cloudstack-setup-databases cloud:password@10.210.64.15 --deploy-as=root:password", shell=True)
        subprocess.call("cloudstack-setup-management", shell=True)
        print(termcolor.colored('\nStarting Cloudstack Management Service', 'green', attrs=['bold']))
        subprocess.call("systemctl restart cloudstack-management", shell=True)
        print(termcolor.colored('\nStarting Cloudstack Usage Service', 'green', attrs=['bold']))
        subprocess.call("systemctl restart cloudstack-management", shell=True)

def mgmt2():
        print(termcolor.colored('\n===============================', 'red', attrs=['bold']))
        print(termcolor.colored('Setting Up Management Server-2', 'green', attrs=['bold']))
        print(termcolor.colored('===============================', 'red', attrs=['bold']))
        subprocess.call("cloudstack-setup-databases cloud:password@10.210.64.15", shell=True)
        subprocess.call("cloudstack-setup-management", shell=True)
        print(termcolor.colored('\nStarting Cloudstack Management Service', 'green', attrs=['bold']))
        subprocess.call("systemctl restart cloudstack-management", shell=True)
        print(termcolor.colored('\nStarting Cloudstack Usage Service', 'green', attrs=['bold']))
        subprocess.call("systemctl restart cloudstack-management", shell=True)

def system_vm():
        print(termcolor.colored('\n===============================', 'red', attrs=['bold']))
        print(termcolor.colored('Setting Up System-VM', 'green', attrs=['bold']))
        print(termcolor.colored('===============================', 'red', attrs=['bold']))
        subprocess.call("mount -t nfs 10.210.64.23:/secondary /mnt", shell=True)
        subprocess.call("/usr/share/cloudstack-common/scripts/storage/secondary/cloud-install-sys-tmplt -m /mnt/ -u http://download.cloudstack.org/systemvm/4.11/systemvmtemplate-4.11.3-kvm.qcow2.bz2 -h kvm -F", shell=True)


selinux()
packages()
cloudstack()
mgmt1()
mgmt2()
system_vm()
