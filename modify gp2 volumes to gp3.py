import boto3
from termcolor import colored

print(colored("\n\n*****************************************************\n***************************************************","blue",attrs=["bold"]))
print(colored("******","blue",attrs=["bold"]) + "##" + colored("********","blue",attrs=["bold"]) + "##" + colored("**********","blue",attrs=["bold"]) + "##" + colored("*******************","blue",attrs=["bold"]))
print(colored("*******","blue",attrs=["bold"]) + "##" + colored("******","blue",attrs=["bold"]) + "##" + colored("***********","blue",attrs=["bold"]) + "##" + colored("*****************","blue",attrs=["bold"]))
print(colored("********","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##"  + colored("***************","blue",attrs=["bold"]))
print(colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("*******","blue",attrs=["bold"]) + "##" + colored("****","blue",attrs=["bold"]) + "##" + colored("*************","blue",attrs=["bold"]))
print(colored("**********","blue",attrs=["bold"]) + "####" + colored("*********","blue",attrs=["bold"]) + "##" + colored("**","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("***********","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]) + "##" + colored("************","blue",attrs=["bold"]))
print(colored("*************************************\n***********************************\n\n","blue",attrs=["bold"]))

ec2 = boto3.client('ec2')

print("\nEnter Volumes to change Type from Gp2 to Gp3 below:")
volumes = []
while True:
    volume = input()
    if volume == "":
        break
    volumes.append(volume)

i = 0    
for vol in volumes:
    i += 1
    result = ec2.modify_volume(VolumeId=vol, VolumeType="gp3", Iops=3000, Throughput=125)
    print(str(i) + ". " + vol)
    print('  Original Size: ' + result['VolumeModification']['OriginalSize'] + ' Target Size: ' + result['VolumeModification']['TargetSize'])
    print('  Original Type: ' + result['VolumeModification']['OriginalVolumeType'] + ' Target Type: ' + result['VolumeModification']['TargetVolumeType'])
    print('  Original Iops: ' + result['VolumeModification']['OriginalIops'] + ' Target Iops: ' + result['VolumeModification']['TargetIops'])