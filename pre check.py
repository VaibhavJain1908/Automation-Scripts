import boto3
import time
import csv
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

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
data = [{} for i in instance_names]

i = 0
for instance in instances:
    for tag in instance.tags:
        if tag["Key"] == "Name":
            data[i]["Instance Id"] = instance.id
            data[i]["Instance Name"] = tag["Value"]
    try:        
        response = ssm_client.send_command(
                    InstanceIds=[instance.id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ["uname -a"]},
                    )
        
        command_id = response['Command']['CommandId']
        time.sleep(2)
        output = ssm_client.get_command_invocation(
              CommandId=command_id,
              InstanceId=instance.id
            )
        data[i]["Kernel"] = output['StandardOutputContent']
        
        response = ssm_client.send_command(
                    InstanceIds=[instance.id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ["uptime"]},
                    )
        
        command_id = response['Command']['CommandId']
        time.sleep(2)
        output = ssm_client.get_command_invocation(
              CommandId=command_id,
              InstanceId=instance.id
            )
        data[i]["Uptime"] = output['StandardOutputContent']
        
        response = ssm_client.send_command(
                    InstanceIds=[instance.id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ["date"]},
                    )
        
        command_id = response['Command']['CommandId']
        time.sleep(2)
        output = ssm_client.get_command_invocation(
              CommandId=command_id,
              InstanceId=instance.id
            )
        data[i]["Date"] = output['StandardOutputContent']
    except:
        print("Error checking for " + data[i]["Instance Name"] + " (" + instance.id + ")")
        
    i+=1
                
fields = ['Instance Name', 'Instance Id', 'Kernel', 'Uptime', 'Date']
file_name = "Pre Checks.csv"

# writing to csv file
with open(file_name, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows
    writer.writerows(data) 
print('\nDataFrame is written to Excel File successfully.\n')
    
print("--- %s seconds ---" % (time.time() - start_time))
