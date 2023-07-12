import boto3
from dateutil.parser import parse
import datetime
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

# Account IDS
account_ids = ["891108200673", "782515806757", "706212970319", "234638522024", "680442571075", "864273633830"]

# IAM Roles
iam_roles = ["Dev_IAM_Role_AMICreation", "PreProd_IAM_Role_AMICreation", "Test_IAM_Role_AMICreation", "Training_IAM_Role_AMICreation", "Prod_IAM_Role_AMICreation", "SharedServices_IAM_Role_AMICreation"]

# Assuming IAM Roles of different accounts through STS
client = boto3.client('sts')

data = []
for i in range(len(iam_roles)):
    
    print("=================\n" + "    " + iam_roles[i].split("_")[0] + "\n=================")
    
    role_object = client.assume_role(
        RoleArn = 'arn:aws:iam::{account_id}:role/{iam_role}'.format(account_id=account_ids[i], iam_role=iam_roles[i]),
        RoleSessionName = '{iam_role}-session'.format(iam_role=iam_roles[i]))

    temp_credentials = role_object['Credentials']

    session = boto3.session.Session(
        aws_access_key_id = temp_credentials['AccessKeyId'],
        aws_secret_access_key = temp_credentials['SecretAccessKey'],
        aws_session_token = temp_credentials['SessionToken'], )

    ec2 = session.client('ec2', region_name="us-east-1")
    ims = ec2.describe_images(Owners=['self'])
    
    ami_data = []
    pending = []
    for im in ims['Images']:
        create_date = im['CreationDate']
        day_old = days_old(create_date)
        ami_id = im['ImageId']
        ami_name = im['Name']
        name = ""
        try:
            for tag in im['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
        except:
            name = ""
        
        if "awsbackup" in ami_name.lower() and day_old == 0:
            ami_data.append(im)
        if im['State'] != 'available':
            pending.append(ami_name)
            
    print("Count = " + str(len(ami_data)))
    print("Pending : " + "\n          ".join(pending))
    data.extend(ami_data)
        
print("\nTotal Backups = " + str(len(data)))
