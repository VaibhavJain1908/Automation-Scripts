import boto3
import csv
import time
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")

print(colored("\n\n*****************************************************\n***************************************************","blue",attrs=["bold"]))
print(colored("******","blue",attrs=["bold"]) + "##" + colored("********","blue",attrs=["bold"]) + "##" + colored("**********","blue",attrs=["bold"]) + "##" + colored("*******************","blue",attrs=["bold"]))
print(colored("*******","blue",attrs=["bold"]) + "##" + colored("******","blue",attrs=["bold"]) + "##" + colored("***********","blue",attrs=["bold"]) + "##" + colored("*****************","blue",attrs=["bold"]))
print(colored("********","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##"  + colored("***************","blue",attrs=["bold"]))
print(colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("*******","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("*************","blue",attrs=["bold"]))
print(colored("**********","blue",attrs=["bold"]) + "####" + colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("***********","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("*************************************\n***********************************\n\n","blue",attrs=["bold"]))

data = []
i = 0

# Reading Account IDS, IAM Roles and tags to be added from the user
num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("\nEnter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

start_time = time.time()
print("\n=========================\nFetching the List\n=========================\n")
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
        
        if region == "us-west-1" and not ("prod" in iam_roles[i].lower() or "security" in iam_roles[i].lower() or "sharedservices" in iam_roles[i].lower()):
            continue
        
        ec2 = session.resource('ec2', region_name=region)
        instances = ec2.instances.all()

        for ins in instances:
            my_dict = {"GP2 Volume Ids":""}
            for vol in ins.volumes.all():
                
                j = 0
                if vol.volume_type == "gp2":
                    
                    if j == 0:
                        my_dict["Instance ID"] = ins.id
                        my_dict["Private IP address"] = ins.private_ip_address
                        for tag in ins.tags:
                            if tag["Key"] == "Name":
                                my_dict["Server"] = tag["Value"]
                    
                    j += 1
                    my_dict["GP2 Volume Ids"] += vol.id + "\n"
                    
            if my_dict["GP2 Volume Ids"] != "":
                data.append(my_dict)
                
fields = ['Server', 'Instance ID', 'Private IP address', 'GP2 Volume Ids']
file_name = "GP2 Volume Instances List.csv"

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