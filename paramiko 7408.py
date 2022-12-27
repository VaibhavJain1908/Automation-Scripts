import paramiko
import getpass
import datetime
import time
from colorama import Fore
from colorama import Style
import warnings
warnings.filterwarnings("ignore")

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def ssh_func(ssh, server, username, password, files):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    print("=========")

    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")
        
    if hostname == "":  
        stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"', get_pty=True)
        stdin.write(password + '\n')
        stdin.flush()
        i = -1
        for line in stdout.readlines():
            i += 1
            if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                continue
            hostname += line.strip()
            
        for file in files:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + "chmod 775 " + file)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "chmod 775 ' + file + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1 or "bash: /home/" + username + "/.bashrc: Not a directory" in line or "[sudo] password for " + username + ":" in line:
                    continue
                print(line),

    else:
        for file in files:
            print(Fore.RED + Style.BRIGHT + hostname + ":~ # " + Style.RESET_ALL + "chmod 775 " + file)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "chmod 775 ' + file + '"')
            stdin.flush()
            for line in stdout.readlines():
                print(line),

    print("=========")
    del stdin, stdout, stderr

num = raw_input("Number of servers: ")
print("Enter ip of " + num + " servers below:")
servers = [raw_input() for i in range(int(num))]

username = raw_input("Username: ")
password = getpass.getpass()

start_time = time.time()
for server in servers:
    print(server)
    print("Enter files: ")
    files = []
    while True:
        file = raw_input()
        if file == "":
            break
        files.append(file)
    try:
        ssh = get_ssh(server, username, password)
        ssh_func(ssh, server, username, password, files)

        ssh.close()
        del ssh
    except Exception as e:
        print(e)
        print("Issue logging into " + server)

print("--- %s seconds ---" % (time.time() - start_time))
