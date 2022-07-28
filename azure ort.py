import time
import csv
from azure.mgmt.compute import compute_management_client
from azure.identity import AzureCliCredential

credentials = AzureCliCredential()
client = compute_management_client(credentials, subscription_id)

services = ['ntpd', 'chronyd', 'auditd', 'ds_agent']

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
vm_names = [input() for i in range(num)]

data =[]
start_time = time.time()
for i in range(len(vm_names)):
    
    data.append({})
    data["Virtual Machines"] = vm_names[i]
    run_command_parameters = {
        'command_id': 'RunShellScript', # For linux, don't change it
        'script': [
            'systemctl status ' + services[i]
        ]
    }
    poller = client.virtual_machines.run_command(
          resource_group_name,
          vm_names[i],
          run_command_parameters
    )
    result = poller.result()  # Blocking till executed
    print(result.value[0].message)  # stdout/stderr
    
    if "active (running)" in result.value[0].message:
        data[service] = "Yes"