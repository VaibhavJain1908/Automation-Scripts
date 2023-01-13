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
    
    data.append({'Server':server})
    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")

    commands = ["rpm -qa | grep -i odbc", "date"]
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
                if cmd == "rpm -qa | grep -i odbc":
                    data[-1]["ODBC Installation Evidence"] = line + "\n"
                else:
                    data[-1]["Date"] = line + "\n"
                print(line),
            
    else:
        for cmd in commands:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + cmd)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "' + cmd + '"', get_pty=True)
            stdin.flush()
            lines = stdout.readlines()
            if cmd == "rpm -qa | grep -i odbc":
                data[-1]["ODBC Installation Evidence"] = "".join(lines)
            else:
                data[-1]["Date"] = "".join(lines)
            print(lines),

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

username = raw_input("Username: ")
password = getpass.getpass()

start_time = time.time()

print("\n=========")
for server in servers:
    print(server)
    try:
        ssh = get_ssh(server, username, password)
        
        if choice == 1:
            pre_checks(ssh, server, username, password)
            
        ssh.close()
        del ssh
    except Exception as exc:
        print(exc)
        print("Issue logging into " + server)
    
file_name = chnge_num + '_PIR_DR.csv'
fields = ['Server', 'Date', 'ODBC Installation Evidence']

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
