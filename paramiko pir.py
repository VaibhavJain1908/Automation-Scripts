import csv
import paramiko
import getpass
import datetime
import time
from colorama import Fore
from colorama import Style
import warnings
warnings.filterwarnings("ignore")

print(Fore.BLUE + Style.BRIGHT + "\n\n*****************************************************\n***************************************************")
print("******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******************")
print("*******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "******" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*****************")
print("********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "***************")
print("*********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*******" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "****" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "*************")
print("**********" + Style.RESET_ALL + "####" + Fore.BLUE + Style.BRIGHT + "*********" + Style.RESET_ALL + "##" +  Fore.BLUE + Style.BRIGHT + "**" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("***********" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************" + Style.RESET_ALL + "##" + Fore.BLUE + Style.BRIGHT + "************")
print("*************************************\n***********************************\n\n" + Style.RESET_ALL)

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

data = []
def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def pre_checks(ssh, server, username, password):
    print("=========")
    
    data.append({'server':server})
    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")

    commands = ["uname -a", "uptime", "date", "free -gh"]
    if hostname == "":        
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + server + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1:
                    continue
                if cmd == "uname -a":
                    data[-1]["kernel (before)"] = line + "\n"
                elif cmd == "free -gh":
                    data[-1]["swap (before)"] = line + "\n"
                else:
                    data[-1][cmd + " (before)"] = line + "\n"
                print(line),
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            for line in stdout.readlines():
                if cmd == "uname -a":
                    data[-1]["kernel (before)"] = line + "\n"
                elif cmd == "free -gh":
                    data[-1]["swap (before)"] = line + "\n"
                else:
                    data[-1][cmd + " (before)"] = line + "\n"
                print(line),

    print("=========")
    
def post_checks(ssh, server, username, password):
    print("=========")
    
    j = 0
    while True:
        if data[j]['server'] == server:
            break
        j+=1
        
    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")
    
    commands = ["registercloudguest --clean", "/opt/splunkforwarder/bin/splunk restart", "systemctl restart amazon-ssm-agent"]
    if hostname == "":        
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + server + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1:
                    continue
                print(line),
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            for line in stdout.readlines():
                print(line),
    
    commands = ["uname -a", "uptime", "date", "free -gh"]
    if hostname == "":        
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + server + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1:
                    continue
                if cmd == "uname -a":
                    data[j]["kernel (after)"] = line + "\n"
                elif cmd == "free -gh":
                    data[j]["swap (after)"] = line + "\n"
                else:
                    data[j][cmd + " (after)"] = line + "\n"
                print(line),
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            for line in stdout.readlines():
                if cmd == "uname -a":
                    data[j]["kernel (after)"] = line + "\n"
                elif cmd == "free -gh":
                    data[j]["swap (after)"] = line + "\n"
                else:
                    data[j][cmd + " (after)"] = line + "\n"
                print(line),
                
    commands = ["zypper lu", "cat /etc/resolv.conf", "/opt/splunkforwarder/bin/splunk status", "rm /usr/bin/scp", "systemctl status amazon-ssm-agent | head"]
    if hostname == "":        
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + server + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            lines = stdout.readlines()
            
            if cmd == "zypper lu":
                if "No updates found." in "".join(lines):
                    data[j]["patching status"] = "No updates found."
                else:
                    data[j]["patching status"] = "".join(lines[2:])
                    
            elif cmd == "cat /etc/resolv.conf":
                if len(lines) == 0 or "".join(lines) == "":
                    data[j]["resolv.conf status"] = "empty"
                else:
                    data[j]["resolv.conf status"] = "".join(lines[2:])
            
            elif cmd == "/opt/splunkforwarder/bin/splunk status":
                if "splunkd is running" in "".join(lines):
                    data[j]["splunk status"] = "running"
                else:
                    data[j]["splunk status"] = "stopped"   
                data[j]["splunk evidence"] = "".join(lines[2:]).encode('utf-8')
                    
            elif cmd == "systemctl status amazon-ssm-agent | head":
                if "active (running)" in "".join(lines):
                    data[j]["amazon-ssm-agent status"] = "running"
                else:
                    data[j]["amazon-ssm-agent status"] = "stopped"
                data[j]["ssm evidence"] = "".join(lines[2:]).encode('utf-8')
                    
            i = -1
            for line in lines:
                i += 1
                if i==0 or i==1:
                    continue
                print(line),
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            lines = stdout.readlines()
            
            if cmd == "zypper lu":
                if "No updates found." in "".join(lines):
                    data[j]["patching status"] = "No updates found."
                else:
                    data[j]["patching status"] = "".join(lines)
                    
            elif cmd == "cat /etc/resolv.conf":
                if len(lines) == 0 or "".join(lines) == "":
                    data[j]["resolv.conf status"] = "empty"
                else:
                    data[j]["resolv.conf status"] = "".join(lines)
            
            elif cmd == "/opt/splunkforwarder/bin/splunk status":
                if "splunkd is running" in "".join(lines):
                    data[j]["splunk status"] = "running"
                else:
                    data[j]["splunk status"] = "stopped"
                data[j]["splunk evidence"] = "".join(lines).encode('utf-8')
                    
            elif cmd == "systemctl status amazon-ssm-agent | head":
                if "active (running)" in "".join(lines):
                    data[j]["amazon-ssm-agent status"] = "running"
                else:
                    data[j]["amazon-ssm-agent status"] = "stopped"
                data[j]["ssm evidence"] = "".join(lines).encode('utf-8')
                    
            for line in lines:
                print(line),

    print("=========")

chnge_num = raw_input("\nEnter Change Number: ")    

print("--------------------\n       Menu       \n--------------------")
print("1. Pre Checks")
print("2. Post Checks")
choice = int(raw_input("Enter your choice: "))

if choice == 2:
    with open(chnge_num + '_PIR.csv') as pscfile:
        reader = csv.DictReader(pscfile)
        for row in reader:
            data.append(row)

num = int(raw_input("\nEnter number of servers: "))
print("\nEnter server names: ")
servers = []
for i in range(num):
    servers.append(raw_input())

username = raw_input("\nUsername: ")
password = getpass.getpass()

start_time = time.time()

print("\n=========")
for server in servers:
    print(server)
    try:
        ssh = get_ssh(server, username, password)
        
        if choice == 1:
            pre_checks(ssh, server, username, password)
            
        if choice == 2:
            post_checks(ssh, server, username, password)
            
        ssh.close()
        del ssh
    except Exception as exc:
        print(exc)
        print("Issue logging into " + server)
    
file_name = chnge_num + '_PIR.csv'
fields = ['server', 'kernel (before)', 'kernel (after)', 'uptime (before)', 'uptime (after)', 'date (before)', 'date (after)', 'swap (before)', 'swap (after)', 'patching status', 'resolv.conf status', 'splunk status', 'splunk evidence', 'amazon-ssm-agent status', 'ssm evidence']

# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields)
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows 
    writer.writerows(data)
print('\nPIR is written to Excel File successfully.\n')

print("--- %s seconds ---" % (time.time() - start_time))
