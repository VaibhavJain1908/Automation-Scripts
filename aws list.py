import boto3
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

data = []
i = 0

# Reading Account IDS, IAM Roles and tags to be added from the user
num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("\nEnter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

client = boto3.client('sts')
for i in range(len(iam_roles)):
    role_object = client.assume_role(
        RoleArn = 'arn:aws:iam::{account_id}:role/{iam_role}'.format(account_id=account_ids[i], iam_role=iam_roles[i]),
        RoleSessionName = '{iam_role}-session'.format(iam_role=iam_roles[i]))
    
    temp_credentials = role_object['Credentials']
    
    session = boto3.session.Session(
        aws_access_key_id = temp_credentials['AccessKeyId'],
        aws_secret_access_key = temp_credentials['SecretAccessKey'],
        aws_session_token = temp_credentials['SessionToken'], )
    
    for region in ["us-east-1", "us-west-1"]:
        ec2 = session.resource('ec2', region_name=region)
        instances = ec2.instances.all()
        for instance in instances:
            data.append({})
            data[i]["Instance ID"] = instance.id
            for tag in instance.tags:
                if tag["Key"] in ['Name', 'Backup', 'Environment', 'Server Type', 'CoreApplicationGroup', 'OS', 'Application', 'PROJECT', 'ServerType', 'environment', 'cost-center', 'company', 'supervisory-organization']:
                    data[i][tag["Key"]] = tag["Value"]
                    
            if instance.state['Name'] == 'running':      
                data[i]["Instance state"] = "Running"
            else:
                data[i]["Instance state"] = "Stopped"            
    
            data[i]["Instance type"] = instance.instance_type
            data[i]["Private IP address"] = instance.private_ip_address
            data[i]["Image ID"] = instance.image_id
            data[i]["Launch time"] = instance.launch_time
            try:
                data[i]["IAM instance profile ARN"] = instance.iam_instance_profile["Arn"]
            except:
                data[i]["IAM instance profile ARN"] = "-"
            data[i]["Monitoring"] = instance.monitoring["State"]
            
            if None == instance.key_pair:
                data[i]["Key name"] = "-"
            else:
                data[i]["Key name"] = instance.key_pair.name
            
            for iface in instance.network_interfaces:
                data[i]["Availability Zone"] = iface.subnet.availability_zone
            data[i]["Security group name"] = ""
            for sg in instance.security_groups:
                data[i]["Security group name"] += sg['GroupName'] + ","
                
            client = session.client('ec2', region_name=region)
            response = client.describe_instance_status(
                InstanceIds=[
                    instance.id
                ],
            )
            count = 0
            for status in response["InstanceStatuses"]:
                try:
                    if status["InstanceStatus"]["Status"] == "ok":
                        count += 1
                    if status["SystemStatus"]["Status"] == "ok":
                        count += 1
                        break          
                except:
                    continue
            if count == 0:
                data[i]["Status check"] = "-"
            else:
                data[i]["Status check"] = str(count) + "/2 checks passed"
                
            i+=1

fields = ['Name', 'Backup', 'Environment', 'Server Type', 'CoreApplicationGroup', 'OS', 'Application', 'PROJECT', 'environment', 'cost-center', 'company', 'supervisory-organization', 'ServerType', 'Instance ID', 'Instance state', 'Instance type', 'Status check', 'Availability Zone', 'Private IP address', 'Monitoring', 'Security group name', 'Key name', 'Image ID', 'Launch time', 'IAM instance profile ARN']
file_name = "AWS Server List.csv"

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

