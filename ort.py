import boto3
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

services = ['ntpd', 'chronyd', 'auditd', 'amazon-ssm-agent', 'ds_agent']

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

ssm_client = boto3.client('ssm')
service_statuses = [{} for i in instance_names]

i = 0
for instance in instances:
    
    flag = 0
    for tag in instance.tags:
        if tag["Key"] == "OS" and tag["Value"] == "Windows":
            flag =1
        if tag["Key"] == "Name":
            service_statuses[i]["Instance Id"] = instance.id
            service_statuses[i]["Instance Name"] = tag["Value"]
            service_statuses[i]["IP Address"] = instance.private_ip_address
            service_statuses[i]["Instance Type"] = instance.instance_type
            
            for iface in instance.network_interfaces:
                service_statuses[i]["Region"] = iface.subnet.availability_zone
            
        elif tag["Key"] == "Environment":
            service_statuses[i]["Environment"] = tag["Value"]
    service_statuses[i]["Security Groups"] = ""
    for sg in instance.security_groups:
        service_statuses[i]["Security Groups"] += sg['GroupName'] + ","
        
    if instance.state["Name"] == "stopped":
        print("Error!! " + service_statuses[i]["Instance Name"] + "Server in stopped state")
        i += 1
        continue
    
    print("=================\n" + service_statuses[i]["Instance Name"] + "\n=================")
    
    try:
        if flag == 0:
            for service in services:
                response = ssm_client.send_command(
                            InstanceIds=[instance.id],
                            DocumentName="AWS-RunShellScript",
                            Parameters={'commands': ["systemctl status " + service]}, )
                
                command_id = response['Command']['CommandId']
                time.sleep(2)
                
                print("Currently checking status of " + service, end=" - ")
                output = ssm_client.get_command_invocation(
                      CommandId=command_id,
                      InstanceId=instance.id
                    )
                
                service_statuses[i][service + ' evidence'] = "".join(output['StandardOutputContent'].splitlines()[:5])
                if "active (running)" in output['StandardOutputContent']:
                    service_statuses[i][service] = "Yes"
                elif output['StandardOutputContent'] == "":
                    service_statuses[i][service] = ""
                else:
                    service_statuses[i][service] = "No"    
                print(service_statuses[i][service])
                
            response = ssm_client.send_command(
                        InstanceIds=[instance.id],
                        DocumentName="AWS-RunShellScript",
                        Parameters={'commands': ["/opt/splunkforwarder/bin/splunk status"]}, )
            
            command_id = response['Command']['CommandId']
            time.sleep(2)
            
            print("Currently checking status of splunk")
            output = ssm_client.get_command_invocation(
                  CommandId=command_id,
                  InstanceId=instance.id
                )
            
            service_statuses[i]['splunk evidence'] = output['StandardOutputContent']
            if "is running" in output['StandardOutputContent']:
                service_statuses[i]["splunk"] = "Yes"
            elif output['StandardOutputContent'] == "":
                raise Exception()
            else:
                service_statuses[i]["splunk"] = "No"
                
        else:
            print(service_statuses[i]["Instance Name"] + " is a windows server !!")
    except:
        print("Error checking for server " + service_statuses[i]["Instance Name"] + "!!!")
    
    i += 1

fields = ['Instance Name', 'Instance Id', 'IP Address', 'Region', 'Instance Type', 'Environment', 'splunk', 'splunk evidence', 'ntpd', 'ntpd evidence', 'chronyd', 'chronyd evidence', 'auditd', 'auditd evidence', 'amazon-ssm-agent', 'amazon-ssm-agent evidence', 'ds_agent', 'ds_agent evidence']
file_name = "ORT Sheet.csv"
fields.extend(["Security Groups"])

# writing to csv file
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows
    writer.writerows(service_statuses) 
print('\nDataFrame is written to Excel File successfully.\n')

print("--- %s seconds ---" % (time.time() - start_time))