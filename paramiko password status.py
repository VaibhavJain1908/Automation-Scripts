import paramiko
import getpass
import datetime
import time
import warnings
warnings.filterwarnings("ignore")

paramiko.util.log_to_file("filename.log")
today = datetime.date.today()

def get_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username=username, password=password)

    return ssh

def ssh_func(ssh, server, username, password, users):
    output.append("=========\n")
    print("=========")
    
    stdin, stdout, stderr = ssh.exec_command('sudo su - -c "hostname"')
    stdin.flush()
    hostname = ""
    for line in stdout.readlines():
        hostname += line.replace("\n", "")

    if hostname == "":        
        for user in users:
            output.append(server + ":~ # passwd --status " + user + "\n")
            print(server + ":~ # passwd --status " + user)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "passwd --status ' + user + '"', get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            i = -1
            for line in stdout.readlines():
                i += 1
                if i==0 or i==1:
                    continue
                output.append(line)
                print(line),
            
    else:
        for user in users:
            output.append(hostname + ":~ # passwd --status " + user + "\n")
            print(hostname + ":~ # passwd --status " + user)
            stdin, stdout, stderr = ssh.exec_command('sudo su - -c "passwd --status ' + user + '"', get_pty=True)
            stdin.flush()
            for line in stdout.readlines():
                output.append(line)
                print(line),

    output.append("=========\n")
    print("=========")

output = []

num = raw_input("Number of servers: ")
print("Enter names of " + num + " servers below:")
servers = [raw_input() for i in range(int(num))]

username = raw_input("Username: ")
password = getpass.getpass()

start_time = time.time()

output.append("=========\n")
print("=========")
for server in servers:
    output.append(server + "\n")
    print(server)
    print("Enter users: ")
    users = []
    while True:
        user = raw_input()
        if user == "":
            break
        users.append(user.replace(":", ""))
    try:
        ssh = get_ssh(server, username, password)
        ssh_func(ssh, server, username, password, users)

        ssh.close()
        del ssh
    except Exception as exc:
        output.append(str(exc) + "\n")
        print(exc)
        output.append("Issue logging into " + server + "\n")
        print("Issue logging into " + server)
        
with open("output.txt", "w") as f:
    f.writelines(output)

print("--- %s seconds ---" % (time.time() - start_time))
