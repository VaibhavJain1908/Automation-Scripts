import boto3
import csv
import time
start_time = time.time()

data = []

for region in ["us-east-1", "us-west-1"]:
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.all()
    for instance in instances:
        tags = []
        flag = 0
        for volume in instance.volumes.all():
            try:
                for tag in volume.tags:
                    if tag["Key"].lower() == "mount":
                        if tag["Value"] not in tags:
                            tags.append(tag["Value"])
                        else:
                            flag = 1
                        break
                
                    if flag == 1:
                        if volume.volume_type != "gp3":
                            flag = 0
                        break
    
                if flag == 1:
                    data.append({})
                    for t in instance.tags:
                        if t["Key"] == "Name":
                            data[-1]["Server"] = t["Value"]
                            break
                    break
                        
            except:
                print("No tags in volume " + volume.id)
            
fields = ['Server']
file_name = "SLES 15.csv"

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