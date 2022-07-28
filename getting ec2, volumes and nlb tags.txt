import boto3
import time
import csv
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

data = []

# EC2 Instances
ec2 = boto3.resource('ec2')
instances = ec2.instances.all()
for instance in instances:
    data.append({})
    data[-1]['Resource ID'] = instance.id
    
    data[-1]['Tags'] = ""
    for tag in instance.tags:
        
        if tag["Key"] == "Name":
            data[-1]['Resource Name'] = tag["Value"]
        
        data[-1]['Tags'] += tag["Key"] + ' = ' + tag["Value"] + '; '

# Volumes
volumeIds = []
ec2 = boto3.resource('ec2')
volumes = ec2.volumes.all()
for volume in volumes:
    data.append({})
    data[-1]['Resource ID'] = volume.id
    
    data[-1]['Tags'] = ""
    for tag in volume.tags:
        
        if tag["Key"] == "Name":
            data[-1]['Resource Name'] = tag["Value"]
        
        data[-1]['Tags'] += tag["Key"] + ' = ' + tag["Value"] + '; '
 
# NLBs
def all_lb(lb_type,*args):
    lbs = []
    try:
        if lb_type == 'alb':
            elb = boto3.client('elbv2')
            name = 'LoadBalancers'
        elif lb_type == 'elb':
            elb = boto3.client('elb')
            name = 'LoadBalancerDescriptions'
    except Exception as exc:
        print(exc)
        exit(1)

    bals = elb.describe_load_balancers()

    for elb2 in bals[name]:
        lbs.append(elb2['LoadBalancerName'])
    
    if len(lbs) != 0:
        elb_tags = elb.describe_tags(
            LoadBalancerNames=lbs,
        )
        
        for elb in elb_tags['TagDescriptions']:
            data[-1]['Resource Name'] = elb['LoadBalancerName']
            
            data[-1]['Tags'] = ""
            for tag in elb['Tags']:
                data[-1]['Tags'] += tag["Key"] + ' = ' + tag["Value"] + '; '

all_lb(lb_type='elb')
all_lb(lb_type='alb')


fields = ['Resource Name', 'Resource ID', 'Tags']
file_name = "Tags.csv"

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