import boto3
import csv
import time
import warnings
from termcolor import colored
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

# Reading Account IDS and IAM Roles from the user
num = int(input("Enter number of account: "))
print("Enter {num} account ids below:".format(num=num))
account_ids = [input() for i in range(num)]

print("\nEnter {num} iam roles below:".format(num=num))
iam_roles = [input() for i in range(num)]

print("\nStarting the process . . .\n")
# Calculating Time to execute the whole program
start_time = time.time()

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
        
        if region == "us-west-1" and not ("prod" in iam_roles[i].lower() or "security" in iam_roles[i].lower() or "sharedservices" in iam_roles[i].lower()):
            continue
        
        ec2 = session.resource('ec2', region_name=region)

        instances = ec2.instances.all()
        for inst in instances:
            data.append({})
            data[-1]["Resource ID"] = inst.id
            data[-1]["Tags"] = ""
            for tag in inst.tags:
                data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                if "name" in tag["Key"].lower():
                    data[-1]["Resource Name"] = tag["Value"]

            if "environment" in data[-1]["Tags"] and "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                data[-1]["Tags present"] = "Yes"
            else:
                data[-1]["Tags present"] = "No"

        volumes = ec2.volumes.all()
        for vol in volumes:
            data.append({})
            data[-1]["Resource ID"] = vol.id
            data[-1]["Tags"] = ""
            try:
                for tag in vol.tags:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + vol.id)
                
        ec2 = session.client('ec2', region_name=region)
        
        subnets = ec2.describe_subnets()['Subnets']
        for sub in subnets:
            data.append({})
            data[-1]["Resource ID"] = sub['SubnetId']
            data[-1]["Tags"] = ""
            try:
                for tag in sub['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + sub['SubnetId'])
                
        vpcs = ec2.describe_vpcs()['Vpcs']
        for vpc in vpcs:
            data.append({})
            data[-1]["Resource ID"] = vpc['VpcId']
            data[-1]["Tags"] = ""
            try:
                for tag in vpc['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + vpc['VpcId'])
                    
        security_groups = ec2.describe_security_groups()['SecurityGroups']
        for sg in security_groups:
            data.append({})
            data[-1]["Resource ID"] = sg['GroupId']
            data[-1]["Tags"] = ""
            try:
                for tag in sg['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + sg['GroupId'])
        
        network_interfaces = ec2.describe_network_interfaces()['NetworkInterfaces']
        for ni in network_interfaces:
            data.append({})
            data[-1]["Resource ID"] = ni['NetworkInterfaceId']
            data[-1]["Tags"] = ""
            try:
                for tag in ni['TagSet']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + ni['NetworkInterfaceId'])
                
        route_tables = ec2.describe_route_tables()['RouteTables']
        for rb in route_tables:
            data.append({})
            data[-1]["Resource ID"] = rb['RouteTableId']
            data[-1]["Tags"] = ""
            try:
                for tag in rb['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + rb['RouteTableId'])
                
        internet_gateways = ec2.describe_internet_gateways()['InternetGateways']
        for ig in internet_gateways:
            data.append({})
            data[-1]["Resource ID"] = ig['InternetGatewayId']
            data[-1]["Tags"] = ""
            try:
                for tag in ig['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + ig['InternetGatewayId'])
                
        customer_gateways = ec2.describe_customer_gateways()['CustomerGateways']
        for cg in customer_gateways:
            data.append({})
            data[-1]["Resource ID"] = cg['CustomerGatewayId']
            data[-1]["Tags"] = ""
            try:
                for tag in cg['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + cg['CustomerGatewayId'])
                
        network_acls = ec2.describe_network_acls()['NetworkAcls']
        for na in network_acls:
            data.append({})
            data[-1]["Resource ID"] = na['NetworkAclId']
            data[-1]["Tags"] = ""
            try:
                for tag in na['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + na['NetworkAclId'])
                
        vpn_connections = ec2.describe_vpn_connections()['VpnConnections']
        for vpn in vpn_connections:
            data.append({})
            data[-1]["Resource ID"] = vpn['VpnConnectionId']
            data[-1]["Tags"] = ""
            try:
                for tag in vpn['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + vpn['VpnConnectionId'])
                
        vpn_gateways = ec2.describe_vpn_gateways()['VpnGateways']
        for vpg in vpn_gateways:
            data.append({})
            data[-1]["Resource ID"] = vpg['VpnGatewayId']
            data[-1]["Tags"] = ""
            try:
                for tag in vpg['Tags']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + vpg['VpnGatewayId'])
                
        rds = session.client('rds', region_name=region)
        
        db_instances = rds.describe_db_instances()['DBInstances']
        for dbi in db_instances:
            data.append({})
            data[-1]["Resource ID"] = dbi['DBInstanceArn']
            data[-1]["Tags"] = ""
            try:
                for tag in dbi['TagList']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if dbi["DBInstanceIdentifier"]:
                        data[-1]["Resource Name"] = dbi["DBInstanceIdentifier"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + dbi['DBInstanceArn'])
                
        db_snapshots = rds.describe_db_snapshots()['DBSnapshots']
        for dbs in db_snapshots:
            data.append({})
            data[-1]["Resource ID"] = dbs['DBSnapshotArn']
            data[-1]["Tags"] = ""
            try:
                for tag in dbs['TagList']:
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + dbs['DBSnapshotArn'])
                
        db_subnet_groups = rds.describe_db_subnet_groups()['DBSubnetGroups']
        for dbsg in db_subnet_groups:
            data.append({})
            data[-1]["Resource ID"] = dbsg['DBSubnetGroupArn']
            data[-1]["Tags"] = ""
            try:
                for tag in rds.list_tags_for_resource(ResourceName=data[-1]["Resource ID"]):
                    data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "name" in tag["Key"].lower():
                        data[-1]["Resource Name"] = tag["Value"]

                if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                    data[-1]["Tags present"] = "Yes"
                else:
                    data[-1]["Tags present"] = "No"
            except:
                print("No Tags in " + dbsg['DBSubnetGroupArn'])

        def all_lb(lb_type,*args):

            # Describing all NLBs in a region of an environment
            try:
                if lb_type == 'alb':
                    elb = session.client('elbv2', region_name=region)
                    name = 'LoadBalancers'
                    bals = elb.describe_load_balancers()
                elif lb_type == 'elb':
                    elb = session.client('elb', region_name=region)
                    name = 'LoadBalancerDescriptions'
                    bals = elb.describe_load_balancers()
            except Exception as exc:
                print(exc)

            if name == 'LoadBalancers':
                for elb2 in bals[name]:
                    data.append({})
                    data[-1]["Resource ID"] = elb2['LoadBalancerArn']
                    data[-1]["Resource Name"] = elb2['LoadBalancerName']
                    data[-1]["Tags"] = ""

                    tags = elb.describe_tags(
                        ResourceArns=[elb2['LoadBalancerArn']]
                        )

                    for tag in tags['TagDescriptions'][0]['Tags']:
                        data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                    if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                        data[-1]["Tags present"] = "Yes"
                    else:
                        data[-1]["Tags present"] = "No"

            else:
                for elb2 in bals[name]:
                    for elb2 in bals[name]:
                        data.append({})
                        data[-1]["Resource Name"] = elb2['LoadBalancerName']
                        data[-1]["Tags"] = ""

                        tags = elb.describe_tags(
                            LoadBalancerNames=[elb2['LoadBalancerName']]
                            )

                        for tag in tags['TagDescriptions'][0]['Tags']:
                            data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

                        if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                            data[-1]["Tags present"] = "Yes"
                        else:
                            data[-1]["Tags present"] = "No"

        all_lb(lb_type='elb')
        all_lb(lb_type='alb')
        
    s3 = session.client('s3')
    
    buckets = s3.list_buckets()['Buckets']
    for bkt in buckets:
        data.append({})
        data[-1]["Resource Name"] = bkt['Name']
        data[-1]["Tags"] = ""
        try:
            for tag in s3.get_bucket_tagging(Bucket=bkt['Name'])['TagSet']:
                data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"

            if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
                data[-1]["Tags present"] = "Yes"
            else:
                data[-1]["Tags present"] = "No"
        except:
            print("No Tags in " + bkt['Name'])

# Csv file for tagged resources
file_name = '/home/AVJ1007/Resource Tags.csv'
fields = ['Resource Name', 'Resource ID', 'Tags', 'Tags present']

# writing to csv file
with open(file_name, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames = fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(data)
    print('\nResource IDs are written to Excel File successfully.\n')

print("--- %s seconds ---" % (time.time() - start_time))