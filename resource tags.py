import boto3
import csv
import time
import warnings
warnings.filterwarnings("ignore")

# Calculating Time to execute the whole program
start_time = time.time()

data = []
ec2 = boto3.resource('ec2')

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
        data[-1]["Tags added"] = "Yes"
    else:
        data[-1]["Tags added"] = "No"
        
volumes = ec2.volumes.all()
for vol in volumes:
    data.append({})
    data[-1]["Resource ID"] = vol.id
    data[-1]["Tags"] = ""
    for tag in vol.tags:
        data[-1]["Tags"] += tag["Key"] + " = " + tag["Value"] + "\n"
        
        if "name" in tag["Key"].lower():
            data[-1]["Resource Name"] = tag["Value"]
    
    if "company" in data[-1]["Tags"] and "cost-center" in data[-1]["Tags"] and "supervisory-organization" in data[-1]["Tags"]:
        data[-1]["Tags added"] = "Yes"
    else:
        data[-1]["Tags added"] = "No"
        
def all_lb(lb_type,*args):
    
    # Describing all NLBs in a region of an environment
    try:
        if lb_type == 'alb':
            elb = boto3.client('elbv2')
            name = 'LoadBalancers'
            bals = elb.describe_load_balancers()
        elif lb_type == 'elb':
            elb = boto3.client('elb')
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
                data[-1]["Tags added"] = "Yes"
            else:
                data[-1]["Tags added"] = "No"
                    
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
                    data[-1]["Tags added"] = "Yes"
                else:
                    data[-1]["Tags added"] = "No"
            
all_lb(lb_type='elb')
all_lb(lb_type='alb')

# Csv file for tagged resources
file_name = 'Resource Tags.csv'
fields = ['Resource Name', 'Resource ID', 'Tags', 'Tags added']

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