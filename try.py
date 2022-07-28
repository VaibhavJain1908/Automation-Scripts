import boto3

client = boto3.client('sts')

num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("Enter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

for i in range(len(iam_roles)):
    role_object = client.assume_role(
        RoleArn=f'arn:aws:iam::{account_ids[i]}:role/{iam_roles[i]}',
        RoleSessionName=f'{iam_roles[i]}-session')
    
    credentials = role_object['Credentials']
    
    session = boto3.session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'], )
    
    