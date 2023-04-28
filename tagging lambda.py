import boto3
import csv
import time
import datetime
import warnings
warnings.filterwarnings("ignore")

data = []
csv_data = []

print("\nStarting the process . . .\n")

# Calculating Time to execute the whole program
today = datetime.date.today()
start_time = time.time()

# For EC2 Instances
def add_tags_to_ec2(session, tags, region):
    instanceIds = []
    data = []
    ec2 = session.resource('ec2', region_name=region)

    # Describing all EC2s in a region of an environment
    """
    For the testing we will instead use below

    instances = ec2.instances.filter(
        Filters = [{
        'Name': 'tag:Name',
        'Values': ['sapdsusevul']
        }])
    """
    instances = ec2.instances.all()
    for instance in instances:
        instanceIds.append(instance.id)

    print("=================\nEC2 Instances\n=================")

    # Adding tags to all EC2 instances in a region of an environment using instance ids
    try:
        ec2.create_tags(
            Resources=instanceIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in instanceIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the ec2 instances, it will print the error.
    except Exception as exc:
        print(exc)

        if len(instanceIds) == 0:
            print(region + " not present in environment !!")
        for id in instanceIds:
            print("Could not add tags to " + id)


    return data


# For Volumes
def add_tags_to_volumes(session, tags, region):
    volumeIds = []
    data = []
    ec2 = session.resource('ec2', region_name=region)

    # Describing all Volumes in a region of an environment
    """
    For the testing we will instead use below

    volumes = ec2.volumes.filter(
        VolumeIds = ['vol-00de1e9aaafd412c8', 'vol-0a9d99c06450c2013', 'vol-0ad2f6c32e6a11b9a', 'vol-0b9ef73f0d1a72396'])
    """
    volumes = ec2.volumes.all()
    for volume in volumes:
        volumeIds.append(volume.id)

    print("=================\nVolumes\n=================")

    # Since the number of volumes in a region of an environment is pretty large, we are adding the tags in batches of 100 volumes
    batch = 0
    while batch < len(volumeIds):
        previous = batch
        batch += 100

        # Adding tags to 100 volumes in a region of an environment at a time using volume ids
        try:
            ec2.create_tags(
                Resources=volumeIds[previous : batch],
                Tags=tags
            )

            # Adding resource ids on which the tags are added successfully to the csv file data
            for id in volumeIds[previous : batch]:
                data.append({})
                data[-1]["Resource ID"] = id
                print("Adding tags to " + id)

        # If there is any error while adding tags to the volumes, it will print the error with the conflicted volume ids
        except Exception as exc:
            print(exc)
            print("Problem in batch: " + str(batch))
            for id in volumeIds[previous : batch]:
                print("Could not add tags to " + id)

    return data


# For NLBs
def add_tags_to_nlb(session, tags, region):
    print("=================\nNLB\n=================")

    data = []
    def all_lb(lb_type,*args):
        lbs = []

        # Describing all NLBs in a region of an environment
        try:
            if lb_type == 'alb':
                elb = session.client('elbv2', region_name=region)
                name = 'LoadBalancers'

                """
                For the testing we will instead use below
                bals = elb.describe_load_balancers(
                    Names=<load_balancer_names_list>)
                """
                bals = elb.describe_load_balancers()
            elif lb_type == 'elb':
                elb = session.client('elb', region_name=region)
                name = 'LoadBalancerDescriptions'

                """
                For the testing we will instead use below
                bals = elb.describe_load_balancers(
                    LoadBalancerNames=<load_balancer_names_list>)
                """
                bals = elb.describe_load_balancers()
        except Exception as exc:
            print(exc)

        if name == 'LoadBalancers':
            for elb2 in bals[name]:
                lbs.append(elb2['LoadBalancerArn'])

            # Adding tags to all NLBs in a region of an environment using Load Balancer Names
            if len(lbs) != 0:
                for lb_name in lbs:
                    try:
                        elb.add_tags(
                            ResourceArns=[lb_name],
                            Tags=tags
                        )

                        # Adding resource ids on which the tags are added successfully to the csv file data
                        data.append({})
                        data[-1]["Resource ID"] = lb_name
                        print("Adding tags to " + lb_name)

                    except Exception as exc:
                        print(exc)
                        print("Could not add tags to " + lb_name)

        else:
            for elb2 in bals[name]:
                lbs.append(elb2['LoadBalancerName'])

            # Adding tags to all NLBs in a region of an environment using Load Balancer Names
            if len(lbs) != 0:
                for lb_name in lbs:
                    try:
                        elb.add_tags(
                            LoadBalancerNames=[lb_name],
                            Tags=tags
                        )

                        # Adding resource ids on which the tags are added successfully to the csv file data
                        data.append({})
                        data[-1]["Resource ID"] = lb_name
                        print("Adding tags to " + lb_name)

                    except Exception as exc:
                        print(exc)
                        print("Could not add tags to " + lb_name)

    all_lb(lb_type='elb')
    all_lb(lb_type='alb')

    return data

# For Customer Gateways
def add_tags_to_customer_gateways(session, tags, region):
    cgIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Customer Gateways in a region of an environment
    customer_gateways = ec2.describe_customer_gateways()['CustomerGateways']
    for cg in customer_gateways:
        cgIds.append(cg['CustomerGatewayId'])

    print("=================\nCustomer Gateways\n=================")

    # Adding tags to all Customer Gateways in a region of an environment using customer gateway ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=cgIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in cgIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the customer gateways, it will print the error.
    except Exception as exc:
        print(exc)

        if len(cgIds) == 0:
            print(region + " not present in environment !!")
        for id in cgIds:
            print("Could not add tags to " + id)

    return data

# For Subnets
def add_tags_to_subnets(session, tags, region):
    subIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Subnets in a region of an environment
    subnets = ec2.describe_subnets()['Subnets']
    for sub in subnets:
        subIds.append(sub['SubnetId'])

    print("=================\nsubnets\n=================")

    # Adding tags to all Subnets in a region of an environment using subnet ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=subIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in subIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the subnets, it will print the error.
    except Exception as exc:
        print(exc)

        if len(subIds) == 0:
            print(region + " not present in environment !!")
        for id in subIds:
            print("Could not add tags to " + id)

    return data

# For Internet Gateways
def add_tags_to_internet_gateways(session, tags, region):
    igIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Internet Gateways in a region of an environment
    internet_gateways = ec2.describe_internet_gateways()['InternetGateways']
    for ig in internet_gateways:
        igIds.append(ig['InternetGatewayId'])

    print("=================\nInternet Gateways\n=================")

    # Adding tags to all Internet Gateways in a region of an environment using internet gateway ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=igIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in igIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the internet gateways, it will print the error.
    except Exception as exc:
        print(exc)

        if len(igIds) == 0:
            print(region + " not present in environment !!")
        for id in igIds:
            print("Could not add tags to " + id)

    return data

# For Network ACLs
def add_tags_to_network_acls(session, tags, region):
    naIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Network ACLs in a region of an environment
    network_acls = ec2.describe_network_acls()['NetworkAcls']
    for na in network_acls:
        naIds.append(na['NetworkAclId'])

    print("=================\nNetwork ACLs\n=================")

    # Adding tags to all Network ACLs in a region of an environment using network acl ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=naIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in naIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the network acls, it will print the error.
    except Exception as exc:
        print(exc)

        if len(naIds) == 0:
            print(region + " not present in environment !!")
        for id in naIds:
            print("Could not add tags to " + id)

    return data

# For Network Interfaces
def add_tags_to_network_interfaces(session, tags, region):
    niIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Network Interfaces in a region of an environment
    network_interfaces = ec2.describe_network_interfaces()['NetworkInterfaces']
    for ni in network_interfaces:
        niIds.append(ni['NetworkInterfaceId'])

    print("=================\nNetwork Interfaces\n=================")

    # Adding tags to all Network Interfaces in a region of an environment using network interface ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=niIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in niIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the network interfaces, it will print the error.
    except Exception as exc:
        print(exc)

        if len(niIds) == 0:
            print(region + " not present in environment !!")
        for id in niIds:
            print("Could not add tags to " + id)

    return data

# For Route Tables
def add_tags_to_route_tables(session, tags, region):
    rbIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Route Tables in a region of an environment
    route_tables = ec2.describe_route_tables()['RouteTables']
    for rb in route_tables:
        rbIds.append(rb['RouteTableId'])

    print("=================\nRoute Tables\n=================")

    # Adding tags to all Route Tables in a region of an environment using route table ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=rbIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in rbIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the route tables, it will print the error.
    except Exception as exc:
        print(exc)

        if len(rbIds) == 0:
            print(region + " not present in environment !!")
        for id in rbIds:
            print("Could not add tags to " + id)

    return data

# For Security Groups
def add_tags_to_security_groups(session, tags, region):
    sgIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Security Groups in a region of an environment
    security_groups = ec2.describe_security_groups()['SecurityGroups']
    for sg in security_groups:
        sgIds.append(sg['GroupId'])

    print("=================\nSecurity Groups\n=================")

    # Adding tags to all Security Groups in a region of an environment using security group ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=sgIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in sgIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the security groups, it will print the error.
    except Exception as exc:
        print(exc)

        if len(sgIds) == 0:
            print(region + " not present in environment !!")
        for id in sgIds:
            print("Could not add tags to " + id)

    return data

# For Vpcs
def add_tags_to_vpcs(session, tags, region):
    vpcIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Vpcs in a region of an environment
    vpcs = ec2.describe_vpcs()['Vpcs']
    for vpc in vpcs:
        vpcIds.append(vpc['VpcId'])

    print("=================\nVpcs\n=================")

    # Adding tags to all Vpcs in a region of an environment using vpc ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=vpcIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in vpcIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the vpcs, it will print the error.
    except Exception as exc:
        print(exc)

        if len(vpcIds) == 0:
            print(region + " not present in environment !!")
        for id in vpcIds:
            print("Could not add tags to " + id)

    return data

# For Vpn Connections
def add_tags_to_vpn_connections(session, tags, region):
    vpn_connectionIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Vpn Connections in a region of an environment
    vpn_connections = ec2.describe_vpn_connections()['VpnConnections']
    for vpn in vpn_connections:
        vpn_connectionIds.append(vpn['VpnConnectionId'])

    print("=================\nVpnConnections\n=================")

    # Adding tags to all Vpn Connections in a region of an environment using vpn connection ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=vpn_connectionIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in vpn_connectionIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the vpn connections, it will print the error.
    except Exception as exc:
        print(exc)

        if len(vpn_connectionIds) == 0:
            print(region + " not present in environment !!")
        for id in vpn_connectionIds:
            print("Could not add tags to " + id)

    return data

# For Vpn Gateways
def add_tags_to_vpn_gateways(session, tags, region):
    vpn_gatewayIds = []
    data = []
    ec2 = session.client('ec2', region_name=region)

    # Describing all Vpn Gateways in a region of an environment
    vpn_gateways = ec2.describe_vpn_gateways()['VpnGateways']
    for vpn in vpn_gateways:
        vpn_gatewayIds.append(vpn['VpnGatewayId'])

    print("=================\nVpngateways\n=================")

    # Adding tags to all Vpn Gateways in a region of an environment using vpn gateway ids
    try:
        ec2 = session.resource('ec2', region_name=region)
        ec2.create_tags(
            Resources=vpn_gatewayIds,
            Tags=tags
        )

        # Adding resource ids on which the tags are added successfully to the csv file data
        for id in vpn_gatewayIds:
            data.append({})
            data[-1]["Resource ID"] = id
            print("Adding tags to " + id)

    # If there is any error while adding tags to the vpn gateways, it will print the error.
    except Exception as exc:
        print(exc)

        if len(vpn_gatewayIds) == 0:
            print(region + " not present in environment !!")
        for id in vpn_gatewayIds:
            print("Could not add tags to " + id)

    return data

# For DB Instances
def add_tags_to_db_instances(session, tags, region):
    db_instanceArns = []
    data = []
    rds = session.client('rds', region_name=region)

    # Describing all DB Instances in a region of an environment
    db_instances = rds.describe_db_instances()['DBInstances']
    for dbi in db_instances:
        db_instanceArns.append(dbi['DBInstanceArn'])

    print("=================\nDBInstances\n=================")

    # Adding tags to all DB Instances in a region of an environment using db instance arns
    try:
        
        for arn in db_instanceArns:
            
            rds.add_tags_to_resource(
                ResourceName=arn,
                Tags=tags
            )
            
            # Adding resource Arns on which the tags are added successfully to the csv file data
            data.append({})
            data[-1]["Resource ID"] = arn
            print("Adding tags to " + arn)

    # If there is any error while adding tags to the db instances, it will print the error.
    except Exception as exc:
        print(exc)

        if len(db_instanceArns) == 0:
            print(region + " not present in environment !!")
        for arn in db_instanceArns:
            print("Could not add tags to " + arn)

    return data

# For DB Snapshots
def add_tags_to_db_snapshots(session, tags, region):
    db_snapshotArns = []
    data = []
    rds = session.client('rds', region_name=region)

    # Describing all DB Snapshots in a region of an environment
    db_snapshots = rds.describe_db_snapshots()['DBSnapshots']
    for dbs in db_snapshots:
        db_snapshotArns.append(dbs['DBSnapshotArn'])

    print("=================\nDBSnapshots\n=================")

    # Adding tags to all DB Snapshots in a region of an environment using db snapshot arns
    try:
        
        for arn in db_snapshotArns:
            
            rds.add_tags_to_resource(
                ResourceName=arn,
                Tags=tags
            )
            
            # Adding resource Arns on which the tags are added successfully to the csv file data
            data.append({})
            data[-1]["Resource ID"] = arn
            print("Adding tags to " + arn)

    # If there is any error while adding tags to the db snapshots, it will print the error.
    except Exception as exc:
        print(exc)

        if len(db_snapshotArns) == 0:
            print(region + " not present in environment !!")
        for arn in db_snapshotArns:
            print("Could not add tags to " + arn)

    return data

# For DB Subnet Groups
def add_tags_to_db_subnet_groups(session, tags, region):
    db_subnet_groupArns = []
    data = []
    rds = session.client('rds', region_name=region)

    # Describing all DB Subnet Groups in a region of an environment
    db_subnet_groups = rds.describe_db_subnet_groups()['DBSubnetGroups']
    for dbsg in db_subnet_groups:
        db_subnet_groupArns.append(dbsg['DBSubnetGroupArn'])

    print("=================\nDBSubnetGroups\n=================")

    # Adding tags to all DB Subnet Groups in a region of an environment using db subnet group arns
    try:
        
        for arn in db_subnet_groupArns:
            
            rds.add_tags_to_resource(
                ResourceName=arn,
                Tags=tags
            )
            
            # Adding resource Arns on which the tags are added successfully to the csv file data
            data.append({})
            data[-1]["Resource ID"] = arn
            print("Adding tags to " + arn)

    # If there is any error while adding tags to the db subnet groups, it will print the error.
    except Exception as exc:
        print(exc)

        if len(db_subnet_groupArns) == 0:
            print(region + " not present in environment !!")
        for arn in db_subnet_groupArns:
            print("Could not add tags to " + arn)

    return data

# For Buckets
def add_tags_to_buckets(session, tags):
    bucketNames = []
    data = []
    s3 = session.client('s3')

    # Describing all Buckets in a region of an environment
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        bucketNames.append(bucket['Name'])

    print("=================\nBuckets\n=================")

    # Adding tags to all Buckets in a region of an environment using bucket names
    try:
        
        for bucket in bucketNames:
            
            s3.put_bucket_tagging(
                Bucket=bucket,
                Tagging={
                    'TagSet': tags
                    }
            )
            
            # Adding resource Arns on which the tags are added successfully to the csv file data
            data.append({})
            data[-1]["Resource ID"] = bucket
            print("Adding tags to " + bucket)

    # If there is any error while adding tags to the buckets, it will print the error.
    except Exception as exc:
        print(exc)

        for bucket in bucketNames:
            print("Could not add tags to " + bucket)

    return data

# For Stacks
"""
def add_tags_to_stacks(session, tags, region):
    stackNames = []
    data = []
    cf = session.client('cloudformation', region_name=region)

    # Describing all Stacks in a region of an environment
    stacks = cf.describe_stacks()['Stacks']
    for stack in stacks:
        stackNames.append(stack['StackName'])

    print("=================\nStacks\n=================")

    # Adding tags to all Stacks in a region of an environment using stack names
    try:
        
        for stack in stackNames:
            
            cf.update_stack(
                StackName=stack,
                UsePreviousTemplate=True,
                Tags=tags
            )
            
            # Adding resource Arns on which the tags are added successfully to the csv file data
            data.append({})
            data[-1]["Resource ID"] = stack
            print("Adding tags to " + stack)

    # If there is any error while adding tags to the stacks, it will print the error.
    except Exception as exc:
        print(exc)

        if len(stackNames) == 0:
            print(region + " not present in environment !!")
        for stack in stackNames:
            print("Could not add tags to " + stack)

    return data
"""

# For the Environment tag
def add_environment_tag_to_ec2_resources(session, region):
    data = []
    ec2 = session.resource('ec2', region_name=region)

    # Describing all EC2s in a region of an environment
    """
    For the testing we will instead use below

    instances = ec2.instances.filter(
        Filters = [{
        'Name': 'tag:Name',
        'Values': ['sapdsusevul']
        }])
    """
    instances = ec2.instances.all()
    for instance in instances:

        # Getting the EC2 Instance's Environment
        env = ""
        for tag in instance.tags:
            if tag["Key"] == "Environment":
                env = tag["Value"]
                break

        # Setting the value of environment tag
        if env == "Development" or env == "Development-Internal Test Server":
            env = "dev"
        elif env == "Development2" or env == "Dev2":
            env = "dev2"
        elif env == "Test" :
            env = "test"
        elif env == "Test2":
            env = "test2"
        elif env == "Training":
            env = "training"
        elif env == "Sandbox":
            env = "sbx"
        elif env == "PreProd":
            env = "preprod"
        elif env == "Production":
            env = "prod"
        elif env == "Security":
            env = "security"
        elif env == "Shared Services" or env == "SharedServices":
            env = "sharedservices"
        elif env == "Shared Services DR":
            env = "sharedservicesdr"
        elif env == "Production DR":
            env = "proddr"
        elif env == "SIT1":
            env = "sit1"
        elif env == "SIT2":
            env = "sit2"
        elif env == "Legacy":
            env = "legacy"
        elif env == "Training2":
            env = "training2"
        elif env == "Legacy":
            env = "legacy"
        elif env == "":
            continue

        resource_ids = [instance.id]

        # Describing the volumes of a particular instance
        for volume in instance.volumes.all():
            resource_ids.append(volume.id)
            
        # Describing the subnet, network interfaces, security groups and vpc of the instance
        resource_ids.append(instance.subnet_id)
        
        resource_ids.append(instance.vpc_id)
        
        for ni in instance.network_interfaces:
            resource_ids.append(ni.id)
            
        for sg in instance.security_groups:
            resource_ids.append(sg['GroupId'])

        # Adding the environment tag to the EC2 Instance and its Volumes, subnet, network interfaces, security groups and vpc
        try:
            ec2.create_tags(
                Resources=resource_ids,
                Tags=[
                    {"Key": "environment",
                      "Value": env}])

            # Adding resource ids on which the environment tag is added successfully to the csv file data
            for id in resource_ids:
                data.append({})
                data[-1]["Resource ID"] = id

        # If there is any error while adding environment tag to the ec2 instance and its volumes, subnet, network interfaces, security groups and vpc. It will print the error along with instance id.
        except Exception as exc:
            print(exc)
            print("Problem in adding Environment tag to " + instance.id + " and its volumes, subnet, network interfaces, security groups and vpc.")

def lambda_handler(event, context):
    
    # Account IDS
    account_ids = ["891108200673", "782515806757", "706212970319", "234638522024", "680442571075", "120750199101", "864273633830"]
    
    # IAM Roles
    iam_roles = ["Dev_IAM_Role_Tagging", "PreProd_IAM_Role_Tagging", "Test_IAM_Role_Tagging", "Training_IAM_Role_Tagging", "Prod_IAM_Role_Tagging", "Security_IAM_Role_Tagging", "SharedServices_IAM_Role_Tagging"]

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
        
        # Printing the current account name
        print("----------------------------------------\nFetching Tags from resources in " + iam_roles[i].split("_")[0] + "\n----------------------------------------")
    
        for region in ["us-east-1", "us-west-1"]:
            
            if region == "us-west-1" and not ("prod" in iam_roles[i].lower() or "security" in iam_roles[i].lower() or "sharedservices" in iam_roles[i].lower()) or ("preprod" in iam_roles[i].lower() and region == "us-west-1"):
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
                elif "aviatrix" in data[-1]["Resource Name"].lower() and "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
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
                    for tag in rds.list_tags_for_resource(ResourceName=data[-1]["Resource ID"])["TagList"]:
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
                
        tags = [{"Key":"company", "Value":"lw"}, {"Key":"supervisory-organization", "Value":"Application Management"}, {"Key":"cost-center", "Value":"804"}]
        
        for region in ["us-east-1", "us-west-1"]:
            
            if region == "us-west-1" and not ("prod" in iam_roles[i].lower() or "security" in iam_roles[i].lower() or "sharedservices" in iam_roles[i].lower()) or ("preprod" in iam_roles[i].lower() and region == "us-west-1"):
                continue
            
            add_tags_to_ec2(session, tags, region)
            add_tags_to_volumes(session, tags, region)
            add_tags_to_nlb(session, tags, region)
            add_tags_to_vpcs(session, tags, region)
            add_tags_to_subnets(session, tags, region)
            add_tags_to_security_groups(session, tags, region)
            add_tags_to_network_interfaces(session, tags, region)
            add_tags_to_customer_gateways(session, tags, region)
            add_tags_to_internet_gateways(session, tags, region)
            add_tags_to_network_acls(session, tags, region)
            add_tags_to_route_tables(session, tags, region)
            add_tags_to_vpn_connections(session, tags, region)
            add_tags_to_vpn_gateways(session, tags, region)
            add_tags_to_db_instances(session, tags, region)
            add_tags_to_db_snapshots(session, tags, region)
            add_tags_to_db_subnet_groups(session, tags, region)
        
            if region == "us-east-1":
                add_tags_to_buckets(session, tags)
                
            add_environment_tag_to_ec2_resources(session, region)
            
    for j in range(len(data)):
        if "Tags present" not in data[j].keys() or data[j]["Tags present"] == "No":
            if "Resource Name" in data[j].keys() or "Resource ID" in data[j].keys():
                csv_data.append({})
            
            if "Resource Name" in data[j].keys():
                csv_data[-1]["Resource Name"] = data[j]["Resource Name"]
                
            if "Resource ID" in data[j].keys():
                csv_data[-1]["Resource ID"] = data[j]["Resource ID"]
    
    # Csv file for tagged resources
    file_name = 'Resource Tags.csv'
    fields = ['Resource Name', 'Resource ID']
    
    # writing to csv file
    with open('/tmp/' + file_name, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
    
        # writing headers (field names)
        writer.writeheader()
    
        # writing data rows
        writer.writerows(csv_data)
        print('\nResource IDs are written to Excel File successfully.\n')
        
    # Uploading the CSV file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file('/tmp/' + file_name, 'lw-tagging-lambda-central', str(today.year) + '/' + str(today.month).rjust(2, '0') + '/' + str(today.day).rjust(2, '0') + '/' + file_name, ExtraArgs={'ACL': 'bucket-owner-full-control'})
        print('Upload done !!') 
    
    except Exception as e:
        # Sending SNS notification
        sns_client = boto3.client('sns')
    
        message = "\n\nData could not be uploaded to S3 !!\n\n"
        print("Error : Could not upload file to S3.\n" + str(e))
        
        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:891108200673:Tagging',
            Message=message,
            Subject="Tagging !!",
        )['MessageId']
        
        return response
    
    print("--- %s seconds ---" % (time.time() - start_time))
