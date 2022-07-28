import boto3
import time
import csv
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

data = []

for region in ["us-east-1", "us-west-1"]:
    file_system_ids = []
    
    instances = boto3.resource('ec2', region_name=region).instances.all()
    
    instance_subnets = {}
    for instance in instances:
        
        flag = 0
        name = ""
        for tag in instance.tags:
            if "OS" in tag["Key"] and "Windows" in tag["Value"]:
                flag = 1
                break
            if tag["Key"] == "Name":
                name = tag["Value"]
        if flag != 1:
            try:
                instance_subnets[instance.subnet_id].append([instance.id, name])
            except:
                instance_subnets[instance.subnet_id] = [[instance.id, name]]
    
    client = boto3.client('efs', region_name=region)
    ssm_client = boto3.client('ssm', region_name=region)
    response = client.describe_file_systems()
    for filesystem in response["FileSystems"]:
        file_system_ids.append(filesystem["FileSystemId"])
    
    for id in file_system_ids:
        print(id, end = " ")
        data.append({})
        data[-1]["File System Id"] = id
        response = client.describe_mount_targets(
            FileSystemId = id
        )
        print(len(response["MountTargets"]))
        if len(response["MountTargets"]) == 0:
            data[-1]["Attached"] = "No"
            
        else:
            data[-1]["Attached"] = "Yes"
            data[-1]["Subnet Ids"] = ""
            for mount in response["MountTargets"]:
                data[-1]["Subnet Ids"] += mount["SubnetId"] + ", "
            
            data[-1]["Possible Targets"] = ""
            data[-1]["Targets"] = ""
            for subnet in data[-1]["Subnet Ids"].split(", "):
                if subnet == "":
                    continue
                try:
                    for instance in instance_subnets[subnet]:
                        try:   
                            response = ssm_client.send_command(
                                        InstanceIds=[instance[0]],
                                        DocumentName="AWS-RunShellScript",
                                        Parameters={'commands': ["df -kh"]},
                                        )
                            
                            command_id = response['Command']['CommandId']
                            time.sleep(2)
                            output = ssm_client.get_command_invocation(
                                  CommandId=command_id,
                                  InstanceId=instance[0]
                                )
                            
                            if output['StandardOutputContent'] == "":
                                raise Exception()
                            if id in output['StandardOutputContent']:
                                print(instance)
                                data[-1]["Targets"] += instance[1] + ", "
                        except:
                            print("SSM not working on " + instance[1])
                            data[-1]["Possible Targets"] += instance[1] + ", "
                except:
                    print(subnet + " not found in environment!!!")
                    
print(data)
"""                                               
fields = ['File System Id', 'Attached', 'Subnet Ids', 'Targets', 'Possible Targets']
file_name = "EFS.csv"

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
"""