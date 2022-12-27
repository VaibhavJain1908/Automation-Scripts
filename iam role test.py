import boto3
import warnings
warnings.filterwarnings("ignore")

# Reading Account IDS, IAM Roles and tags to be added from the user
num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("\nEnter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

# Assuming IAM Roles of different accounts through STS
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
        for instance in ec2.instances.all():
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    print(tag["Value"])