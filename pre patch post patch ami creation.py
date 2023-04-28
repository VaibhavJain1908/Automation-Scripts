import boto3
import time
import datetime
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

today = datetime.date.today()

# Account, IAM Role and Region for which we want to take AMIs
account_id = input("Enter Account ID: ")
iam_role = input("Enter IAM Role name for the assuming: ")
region = input("Enter the region (east/west): ")

client = boto3.client('sts')
role_object = client.assume_role(
    RoleArn = 'arn:aws:iam::{account_id}:role/{iam_role}'.format(account_id=account_id, iam_role=iam_role),
    RoleSessionName = '{iam_role}-session'.format(iam_role=iam_role))

temp_credentials = role_object['Credentials']

session = boto3.session.Session(
    aws_access_key_id = temp_credentials['AccessKeyId'],
    aws_secret_access_key = temp_credentials['SecretAccessKey'],
    aws_session_token = temp_credentials['SessionToken'], )

# Taking Server names from user
num = int(input("\nEnter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

# Filtering out the Instances
client = session.client('ec2', region_name="us-"+region+"-1")
ec2 = session.resource('ec2', region_name="us-"+region+"-1")
instances = ec2.instances.filter(
    Filters = [{  
    'Name': 'tag:Name',
    'Values': instance_names
    }]
)

print("\n--------------------\n       Menu       \n--------------------")
print("1. Offline 'Post Shutdown'")
print("2. Online 'Without Shutting Down'")
choice = int(input("\nEnter your choice (1/2): "))

if choice == 1:
    
    choice = input("\nAre you sure you want to stop the instances ? (y/n): ")
    if choice.lower() == "n":
        print("\nPlease Run the script again !!")
    
    elif choice.lower() == "y":
    
        print("\n--------------------\n       Menu       \n--------------------")
        print("1. Pre Patch")
        print("2. Post Patch")
        choice = int(input("\nEnter your choice (1/2): "))
        
        if choice == 1 or choice == 2:
        
            print("\n=========Stopping Instances=========\n")
            instances.stop() 
            
            for instance in instances:
                instanceName = ""
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        instanceName = tag['Value']
                        break
                
                instance.wait_until_stopped()
                
                # Creating Offline Pre and Post Patch AMI
                if choice == 1:
                    print("Creating Pre Patch AMI for " + instanceName)
                    client.create_image(InstanceId=instance.id, Name=instanceName + '_PrePatchWithReboot_' + str(today.day).rjust(2, '0') + str(today.month).rjust(2, '0') + str(today.year))
                    time.sleep(2)
                else:
                    print("Creating Post Patch AMI for " + instanceName)
                    client.create_image(InstanceId=instance.id, Name=instanceName + '_PostPatchWithReboot_' + str(today.day).rjust(2, '0') + str(today.month).rjust(2, '0') + str(today.year))
                    time.sleep(2)
            
            print("\n=========Starting Instances=========")        
            instances.start()
            
            # Waiting until all instance's pass 2/2 status checks
            k = 0
            while (k < 7):
                
                servers_status = {}
                flag = 0
                
                for instance in  instances:
                    response = client.describe_instance_status(
                        InstanceIds=[
                            instance.id
                        ]
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
                        
                    if count != 2:
                        flag = 1
                        break
                    
                if flag == 1:
                    k += 1
                    time.sleep(120)
                    continue
                else:
                    print("\nAll Servers are up and running fine\n")
                    break
                
            # If Even after waiting for almost 15 minutes, all instances doesn't pass 2/2 status checks
            if k == 7:
                print("\nAlert !! Please check as some of the servers have not passed 2/2 status check yet !!\n")
                
                for instance in  instances:
                    response = client.describe_instance_status(
                        InstanceIds=[
                            instance.id
                        ]
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
                        
                    if count != 2:
                        instanceName = ""
                        for tag in instance.tags:
                            if tag['Key'] == 'Name':
                                print(tag["Value"] + " : " + str(count) + "/2 passed")
        
    else:
        print("\nWrong Choice, try again !!")

elif choice == 2:
    
    print("\n--------------------\n       Menu       \n--------------------")
    print("1. Pre Patch")
    print("2. Post Patch")
    choice = int(input("\nEnter your choice (1/2): "))

    print("\n==============================\n")
    
    for instance in instances:
        instanceName = ""
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                instanceName = tag['Value']
                break
        
        # Creating Online Pre and Post Patch AMI
        if choice == 1:
            print("Creating Pre Patch AMI for " + instanceName)
            client.create_image(InstanceId=instance.id, Name=instanceName + '_PrePatchWithoutReboot_' + str(today.day).rjust(2, '0') + str(today.month).rjust(2, '0') + str(today.year))
            time.sleep(2)
        elif choice == 2:
            print("Creating Post Patch AMI for " + instanceName)
            client.create_image(InstanceId=instance.id, Name=instanceName + '_PostPatchWithoutReboot_' + str(today.day).rjust(2, '0') + str(today.month).rjust(2, '0') + str(today.year))
            time.sleep(2)
 

print("\n--- %s seconds ---" % (time.time() - start_time))