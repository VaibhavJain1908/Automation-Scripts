import boto3
import csv
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

volume_data = []

for region in ["us-east-1", "us-west-1"]:
    ec2 = boto3.resource('ec2', region_name = region)
    volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]) # if you want to list out only attached volumes
    
    for volume in volumes:
        id = volume.id
        size = volume.size
        project = "-"
        name = "-"
        mount = "-"
        server_type = "-"
        environment = "-"
        os = "-"
        application = "-"
        core_application_group = "-"
        try:
            for tag in volume.tags:
                if "server" in tag["Key"].lower():
                    server_type = tag["Value"]
                elif "environment" in tag["Key"].lower():
                    environment = tag["Value"]
                elif "name" in tag["Key"].lower():
                    name = tag["Value"]
                elif "mount" in tag["Key"].lower():
                    mount = tag["Value"]
                elif "project" in tag["Key"].lower():
                    project = tag["Value"]
                elif "application" in tag["Key"].lower():
                    application = tag["Value"]
                elif "core" in tag["Key"].lower():
                    core_application_group = tag["Value"]
                elif "os" in tag["Key"].lower():
                    os = tag["Value"]
                else:
                    print(tag)
            
        except:
            print(id, "No Tags")
        
        volume_data.append({'Name':name, 'Volume Id':id, 'Size (in GB)':size, 'Server Type':server_type, 'Environment':environment, 'OS':os, 'Project':project, 'Application':application, 'Core Application Group':core_application_group, 'Mount':mount})
        
file_name = 'Available Volume Data.csv'
fields = ['Name', 'Volume Id', 'Size (in GB)', 'Server Type', 'Environment', 'OS', 'Project', 'Application', 'Core Application Group', 'Mount']
# writing to csv file 
with open(file_name, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names)
    writer.writeheader()
        
    # writing data rows 
    writer.writerows(volume_data) 
print('\nDataFrame is written to Excel File successfully.\n')

print("--- %s seconds ---" % (time.time() - start_time))