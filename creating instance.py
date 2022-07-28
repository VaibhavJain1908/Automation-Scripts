import boto3
import time
import warnings
warnings.filterwarnings("ignore")
start_time = time.time()

num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
instance_names = [input() for i in range(num)]

    
ec2_client = boto3.client("ec2")
for name in instance_names:
    instances = ec2_client.run_instances(
        ImageId="ami-08895422b5f3aa64a",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key':'Name',
                    'Value':name
                },
            ]
        }],
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True|False,
                'DeleteOnTermination': True|False,
                'PrivateIpAddress': 'string',
                'SubnetId': 'string',  
            },
        ],  
        KeyName='string',
        SecurityGroupIds=[
            'string',
        ],
        IamInstanceProfile={
            'Arn': 'string',
            'Name': 'string'
        },   
    )

    print("Creating Instance " + name)
    
"""
BlockDeviceMappings=[
{
    'DeviceName': 'string',
    'VirtualName': 'string',
    'Ebs': {
        'DeleteOnTermination': True|False,
        'Iops': 123,
        'SnapshotId': 'string',
        'VolumeSize': 123,
        'VolumeType': 'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3',
        'KmsKeyId': 'string',
        'Throughput': 123,
        'OutpostArn': 'string',
        'Encrypted': True|False
    },
    'NoDevice': 'string'
},
],
ImageId='string',
InstanceType='a1.medium'|'a1.large'|'a1.xlarge'|'a1.2xlarge'|'a1.4xlarge'|'a1.metal'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'c5.large'|'c5.xlarge'|'c5.2xlarge'|'c5.4xlarge'|'c5.9xlarge'|'c5.12xlarge'|'c5.18xlarge'|'c5.24xlarge'|'c5.metal'|'c5a.large'|'c5a.xlarge'|'c5a.2xlarge'|'c5a.4xlarge'|'c5a.8xlarge'|'c5a.12xlarge'|'c5a.16xlarge'|'c5a.24xlarge'|'c5ad.large'|'c5ad.xlarge'|'c5ad.2xlarge'|'c5ad.4xlarge'|'c5ad.8xlarge'|'c5ad.12xlarge'|'c5ad.16xlarge'|'c5ad.24xlarge'|'c5d.large'|'c5d.xlarge'|'c5d.2xlarge'|'c5d.4xlarge'|'c5d.9xlarge'|'c5d.12xlarge'|'c5d.18xlarge'|'c5d.24xlarge'|'c5d.metal'|'c5n.large'|'c5n.xlarge'|'c5n.2xlarge'|'c5n.4xlarge'|'c5n.9xlarge'|'c5n.18xlarge'|'c5n.metal'|'c6g.medium'|'c6g.large'|'c6g.xlarge'|'c6g.2xlarge'|'c6g.4xlarge'|'c6g.8xlarge'|'c6g.12xlarge'|'c6g.16xlarge'|'c6g.metal'|'c6gd.medium'|'c6gd.large'|'c6gd.xlarge'|'c6gd.2xlarge'|'c6gd.4xlarge'|'c6gd.8xlarge'|'c6gd.12xlarge'|'c6gd.16xlarge'|'c6gd.metal'|'c6gn.medium'|'c6gn.large'|'c6gn.xlarge'|'c6gn.2xlarge'|'c6gn.4xlarge'|'c6gn.8xlarge'|'c6gn.12xlarge'|'c6gn.16xlarge'|'c6i.large'|'c6i.xlarge'|'c6i.2xlarge'|'c6i.4xlarge'|'c6i.8xlarge'|'c6i.12xlarge'|'c6i.16xlarge'|'c6i.24xlarge'|'c6i.32xlarge'|'c6i.metal'|'cc1.4xlarge'|'cc2.8xlarge'|'cg1.4xlarge'|'cr1.8xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge'|'d3.xlarge'|'d3.2xlarge'|'d3.4xlarge'|'d3.8xlarge'|'d3en.xlarge'|'d3en.2xlarge'|'d3en.4xlarge'|'d3en.6xlarge'|'d3en.8xlarge'|'d3en.12xlarge'|'dl1.24xlarge'|'f1.2xlarge'|'f1.4xlarge'|'f1.16xlarge'|'g2.2xlarge'|'g2.8xlarge'|'g3.4xlarge'|'g3.8xlarge'|'g3.16xlarge'|'g3s.xlarge'|'g4ad.xlarge'|'g4ad.2xlarge'|'g4ad.4xlarge'|'g4ad.8xlarge'|'g4ad.16xlarge'|'g4dn.xlarge'|'g4dn.2xlarge'|'g4dn.4xlarge'|'g4dn.8xlarge'|'g4dn.12xlarge'|'g4dn.16xlarge'|'g4dn.metal'|'g5.xlarge'|'g5.2xlarge'|'g5.4xlarge'|'g5.8xlarge'|'g5.12xlarge'|'g5.16xlarge'|'g5.24xlarge'|'g5.48xlarge'|'g5g.xlarge'|'g5g.2xlarge'|'g5g.4xlarge'|'g5g.8xlarge'|'g5g.16xlarge'|'g5g.metal'|'hi1.4xlarge'|'hpc6a.48xlarge'|'hs1.8xlarge'|'h1.2xlarge'|'h1.4xlarge'|'h1.8xlarge'|'h1.16xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'i3.large'|'i3.xlarge'|'i3.2xlarge'|'i3.4xlarge'|'i3.8xlarge'|'i3.16xlarge'|'i3.metal'|'i3en.large'|'i3en.xlarge'|'i3en.2xlarge'|'i3en.3xlarge'|'i3en.6xlarge'|'i3en.12xlarge'|'i3en.24xlarge'|'i3en.metal'|'im4gn.large'|'im4gn.xlarge'|'im4gn.2xlarge'|'im4gn.4xlarge'|'im4gn.8xlarge'|'im4gn.16xlarge'|'inf1.xlarge'|'inf1.2xlarge'|'inf1.6xlarge'|'inf1.24xlarge'|'is4gen.medium'|'is4gen.large'|'is4gen.xlarge'|'is4gen.2xlarge'|'is4gen.4xlarge'|'is4gen.8xlarge'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'m4.16xlarge'|'m5.large'|'m5.xlarge'|'m5.2xlarge'|'m5.4xlarge'|'m5.8xlarge'|'m5.12xlarge'|'m5.16xlarge'|'m5.24xlarge'|'m5.metal'|'m5a.large'|'m5a.xlarge'|'m5a.2xlarge'|'m5a.4xlarge'|'m5a.8xlarge'|'m5a.12xlarge'|'m5a.16xlarge'|'m5a.24xlarge'|'m5ad.large'|'m5ad.xlarge'|'m5ad.2xlarge'|'m5ad.4xlarge'|'m5ad.8xlarge'|'m5ad.12xlarge'|'m5ad.16xlarge'|'m5ad.24xlarge'|'m5d.large'|'m5d.xlarge'|'m5d.2xlarge'|'m5d.4xlarge'|'m5d.8xlarge'|'m5d.12xlarge'|'m5d.16xlarge'|'m5d.24xlarge'|'m5d.metal'|'m5dn.large'|'m5dn.xlarge'|'m5dn.2xlarge'|'m5dn.4xlarge'|'m5dn.8xlarge'|'m5dn.12xlarge'|'m5dn.16xlarge'|'m5dn.24xlarge'|'m5dn.metal'|'m5n.large'|'m5n.xlarge'|'m5n.2xlarge'|'m5n.4xlarge'|'m5n.8xlarge'|'m5n.12xlarge'|'m5n.16xlarge'|'m5n.24xlarge'|'m5n.metal'|'m5zn.large'|'m5zn.xlarge'|'m5zn.2xlarge'|'m5zn.3xlarge'|'m5zn.6xlarge'|'m5zn.12xlarge'|'m5zn.metal'|'m6a.large'|'m6a.xlarge'|'m6a.2xlarge'|'m6a.4xlarge'|'m6a.8xlarge'|'m6a.12xlarge'|'m6a.16xlarge'|'m6a.24xlarge'|'m6a.32xlarge'|'m6a.48xlarge'|'m6g.metal'|'m6g.medium'|'m6g.large'|'m6g.xlarge'|'m6g.2xlarge'|'m6g.4xlarge'|'m6g.8xlarge'|'m6g.12xlarge'|'m6g.16xlarge'|'m6gd.metal'|'m6gd.medium'|'m6gd.large'|'m6gd.xlarge'|'m6gd.2xlarge'|'m6gd.4xlarge'|'m6gd.8xlarge'|'m6gd.12xlarge'|'m6gd.16xlarge'|'m6i.large'|'m6i.xlarge'|'m6i.2xlarge'|'m6i.4xlarge'|'m6i.8xlarge'|'m6i.12xlarge'|'m6i.16xlarge'|'m6i.24xlarge'|'m6i.32xlarge'|'m6i.metal'|'mac1.metal'|'p2.xlarge'|'p2.8xlarge'|'p2.16xlarge'|'p3.2xlarge'|'p3.8xlarge'|'p3.16xlarge'|'p3dn.24xlarge'|'p4d.24xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'r4.large'|'r4.xlarge'|'r4.2xlarge'|'r4.4xlarge'|'r4.8xlarge'|'r4.16xlarge'|'r5.large'|'r5.xlarge'|'r5.2xlarge'|'r5.4xlarge'|'r5.8xlarge'|'r5.12xlarge'|'r5.16xlarge'|'r5.24xlarge'|'r5.metal'|'r5a.large'|'r5a.xlarge'|'r5a.2xlarge'|'r5a.4xlarge'|'r5a.8xlarge'|'r5a.12xlarge'|'r5a.16xlarge'|'r5a.24xlarge'|'r5ad.large'|'r5ad.xlarge'|'r5ad.2xlarge'|'r5ad.4xlarge'|'r5ad.8xlarge'|'r5ad.12xlarge'|'r5ad.16xlarge'|'r5ad.24xlarge'|'r5b.large'|'r5b.xlarge'|'r5b.2xlarge'|'r5b.4xlarge'|'r5b.8xlarge'|'r5b.12xlarge'|'r5b.16xlarge'|'r5b.24xlarge'|'r5b.metal'|'r5d.large'|'r5d.xlarge'|'r5d.2xlarge'|'r5d.4xlarge'|'r5d.8xlarge'|'r5d.12xlarge'|'r5d.16xlarge'|'r5d.24xlarge'|'r5d.metal'|'r5dn.large'|'r5dn.xlarge'|'r5dn.2xlarge'|'r5dn.4xlarge'|'r5dn.8xlarge'|'r5dn.12xlarge'|'r5dn.16xlarge'|'r5dn.24xlarge'|'r5dn.metal'|'r5n.large'|'r5n.xlarge'|'r5n.2xlarge'|'r5n.4xlarge'|'r5n.8xlarge'|'r5n.12xlarge'|'r5n.16xlarge'|'r5n.24xlarge'|'r5n.metal'|'r6g.medium'|'r6g.large'|'r6g.xlarge'|'r6g.2xlarge'|'r6g.4xlarge'|'r6g.8xlarge'|'r6g.12xlarge'|'r6g.16xlarge'|'r6g.metal'|'r6gd.medium'|'r6gd.large'|'r6gd.xlarge'|'r6gd.2xlarge'|'r6gd.4xlarge'|'r6gd.8xlarge'|'r6gd.12xlarge'|'r6gd.16xlarge'|'r6gd.metal'|'r6i.large'|'r6i.xlarge'|'r6i.2xlarge'|'r6i.4xlarge'|'r6i.8xlarge'|'r6i.12xlarge'|'r6i.16xlarge'|'r6i.24xlarge'|'r6i.32xlarge'|'r6i.metal'|'t1.micro'|'t2.nano'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'t2.xlarge'|'t2.2xlarge'|'t3.nano'|'t3.micro'|'t3.small'|'t3.medium'|'t3.large'|'t3.xlarge'|'t3.2xlarge'|'t3a.nano'|'t3a.micro'|'t3a.small'|'t3a.medium'|'t3a.large'|'t3a.xlarge'|'t3a.2xlarge'|'t4g.nano'|'t4g.micro'|'t4g.small'|'t4g.medium'|'t4g.large'|'t4g.xlarge'|'t4g.2xlarge'|'u-6tb1.56xlarge'|'u-6tb1.112xlarge'|'u-9tb1.112xlarge'|'u-12tb1.112xlarge'|'u-6tb1.metal'|'u-9tb1.metal'|'u-12tb1.metal'|'u-18tb1.metal'|'u-24tb1.metal'|'vt1.3xlarge'|'vt1.6xlarge'|'vt1.24xlarge'|'x1.16xlarge'|'x1.32xlarge'|'x1e.xlarge'|'x1e.2xlarge'|'x1e.4xlarge'|'x1e.8xlarge'|'x1e.16xlarge'|'x1e.32xlarge'|'x2iezn.2xlarge'|'x2iezn.4xlarge'|'x2iezn.6xlarge'|'x2iezn.8xlarge'|'x2iezn.12xlarge'|'x2iezn.metal'|'x2gd.medium'|'x2gd.large'|'x2gd.xlarge'|'x2gd.2xlarge'|'x2gd.4xlarge'|'x2gd.8xlarge'|'x2gd.12xlarge'|'x2gd.16xlarge'|'x2gd.metal'|'z1d.large'|'z1d.xlarge'|'z1d.2xlarge'|'z1d.3xlarge'|'z1d.6xlarge'|'z1d.12xlarge'|'z1d.metal'|'x2idn.16xlarge'|'x2idn.24xlarge'|'x2idn.32xlarge'|'x2iedn.xlarge'|'x2iedn.2xlarge'|'x2iedn.4xlarge'|'x2iedn.8xlarge'|'x2iedn.16xlarge'|'x2iedn.24xlarge'|'x2iedn.32xlarge'|'c6a.large'|'c6a.xlarge'|'c6a.2xlarge'|'c6a.4xlarge'|'c6a.8xlarge'|'c6a.12xlarge'|'c6a.16xlarge'|'c6a.24xlarge'|'c6a.32xlarge'|'c6a.48xlarge'|'c6a.metal'|'m6a.metal'|'i4i.large'|'i4i.xlarge'|'i4i.2xlarge'|'i4i.4xlarge'|'i4i.8xlarge'|'i4i.16xlarge'|'i4i.32xlarge',
Ipv6AddressCount=123,
Ipv6Addresses=[
    {
        'Ipv6Address': 'string'
    },
],
KernelId='string',
KeyName='string',
MaxCount=123,
MinCount=123,
Monitoring={
    'Enabled': True|False
},
Placement={
    'AvailabilityZone': 'string',
    'Affinity': 'string',
    'GroupName': 'string',
    'PartitionNumber': 123,
    'HostId': 'string',
    'Tenancy': 'default'|'dedicated'|'host',
    'SpreadDomain': 'string',
    'HostResourceGroupArn': 'string'
},
RamdiskId='string',
SecurityGroupIds=[
    'string',
],
SecurityGroups=[
    'string',
],
SubnetId='string',
UserData='string',
AdditionalInfo='string',
ClientToken='string',
DisableApiTermination=True|False,
DryRun=True|False,
EbsOptimized=True|False,
IamInstanceProfile={
    'Arn': 'string',
    'Name': 'string'
},
InstanceInitiatedShutdownBehavior='stop'|'terminate',
NetworkInterfaces=[
    {
        'AssociatePublicIpAddress': True|False,
        'DeleteOnTermination': True|False,
        'Description': 'string',
        'DeviceIndex': 123,
        'Groups': [
            'string',
        ],
        'Ipv6AddressCount': 123,
        'Ipv6Addresses': [
            {
                'Ipv6Address': 'string'
            },
        ],
        'NetworkInterfaceId': 'string',
        'PrivateIpAddress': 'string',
        'PrivateIpAddresses': [
            {
                'Primary': True|False,
                'PrivateIpAddress': 'string'
            },
        ],
        'SecondaryPrivateIpAddressCount': 123,
        'SubnetId': 'string',
        'AssociateCarrierIpAddress': True|False,
        'InterfaceType': 'string',
        'NetworkCardIndex': 123,
        'Ipv4Prefixes': [
            {
                'Ipv4Prefix': 'string'
            },
        ],
        'Ipv4PrefixCount': 123,
        'Ipv6Prefixes': [
            {
                'Ipv6Prefix': 'string'
            },
        ],
        'Ipv6PrefixCount': 123
    },
],
PrivateIpAddress='string',
ElasticGpuSpecification=[
    {
        'Type': 'string'
    },
],
ElasticInferenceAccelerators=[
    {
        'Type': 'string',
        'Count': 123
    },
],
TagSpecifications=[
    {
        'ResourceType': 'capacity-reservation'|'client-vpn-endpoint'|'customer-gateway'|'carrier-gateway'|'dedicated-host'|'dhcp-options'|'egress-only-internet-gateway'|'elastic-ip'|'elastic-gpu'|'export-image-task'|'export-instance-task'|'fleet'|'fpga-image'|'host-reservation'|'image'|'import-image-task'|'import-snapshot-task'|'instance'|'instance-event-window'|'internet-gateway'|'ipam'|'ipam-pool'|'ipam-scope'|'ipv4pool-ec2'|'ipv6pool-ec2'|'key-pair'|'launch-template'|'local-gateway'|'local-gateway-route-table'|'local-gateway-virtual-interface'|'local-gateway-virtual-interface-group'|'local-gateway-route-table-vpc-association'|'local-gateway-route-table-virtual-interface-group-association'|'natgateway'|'network-acl'|'network-interface'|'network-insights-analysis'|'network-insights-path'|'network-insights-access-scope'|'network-insights-access-scope-analysis'|'placement-group'|'prefix-list'|'replace-root-volume-task'|'reserved-instances'|'route-table'|'security-group'|'security-group-rule'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'subnet-cidr-reservation'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-connect-peer'|'transit-gateway-multicast-domain'|'transit-gateway-route-table'|'volume'|'vpc'|'vpc-endpoint'|'vpc-endpoint-service'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log',
        'Tags': [
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    },
],
LaunchTemplate={
    'LaunchTemplateId': 'string',
    'LaunchTemplateName': 'string',
    'Version': 'string'
},
InstanceMarketOptions={
    'MarketType': 'spot',
    'SpotOptions': {
        'MaxPrice': 'string',
        'SpotInstanceType': 'one-time'|'persistent',
        'BlockDurationMinutes': 123,
        'ValidUntil': datetime(2015, 1, 1),
        'InstanceInterruptionBehavior': 'hibernate'|'stop'|'terminate'
    }
},
CreditSpecification={
    'CpuCredits': 'string'
},
CpuOptions={
    'CoreCount': 123,
    'ThreadsPerCore': 123
},
CapacityReservationSpecification={
    'CapacityReservationPreference': 'open'|'none',
    'CapacityReservationTarget': {
        'CapacityReservationId': 'string',
        'CapacityReservationResourceGroupArn': 'string'
    }
},
HibernationOptions={
    'Configured': True|False
},
LicenseSpecifications=[
    {
        'LicenseConfigurationArn': 'string'
    },
],
MetadataOptions={
    'HttpTokens': 'optional'|'required',
    'HttpPutResponseHopLimit': 123,
    'HttpEndpoint': 'disabled'|'enabled',
    'HttpProtocolIpv6': 'disabled'|'enabled',
    'InstanceMetadataTags': 'disabled'|'enabled'
},
EnclaveOptions={
    'Enabled': True|False
},
PrivateDnsNameOptions={
    'HostnameType': 'ip-name'|'resource-name',
    'EnableResourceNameDnsARecord': True|False,
    'EnableResourceNameDnsAAAARecord': True|False
},
MaintenanceOptions={
    'AutoRecovery': 'disabled'|'default'
}
"""
    
print("--- %s seconds ---" % (time.time() - start_time))