import boto3
import os


def ec2_create_key(keyname):
    my_path = os.path.expanduser("~/" + keyname + "_ssh.pem")

    try:
        if os.path.exists(my_path) and os.path.getsize(my_path) > 0:
            print("Warning!!! Key wasn't created because " + my_path + " already exists")
            return 0
        else:
            keypair = ec2_client.create_key_pair(KeyName=keyname)

            print("Key is being exported to "  + my_path)
            with open(my_path, "w+") as line:
                print(keypair['KeyMaterial'], file=line)
                print(keypair['KeyMaterial'])
            line .close()
            return 1
    except:
        return 0


def ec2_create_sg(type, sgname):

    try:
        if type == 'ssh':
            response = ec2_client.create_security_group(GroupName=sgname, Description='SG for ssh')
            ec2_client.authorize_security_group_ingress(
                GroupId=response['GroupId'],
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ]
            )
            print("Security GroupID {} was crated".format(response['GroupdId']))
            return 1
        elif type == 'web':
            response = ec2_client.create_security_group(GroupName=sgname, Description='SG for web')
            ec2_client.authorize_security_group_ingress(
                GroupId=response['GroupId'],
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 443,
                     'ToPort': 443,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ]
            )
            print("Security GroupID {} was crated".format(response['GroupdId']))
            return 1
        else:
            print("Security Group creation process had failed, unknown type!")
            return 0
    except:
        print("Security Group creation process had failed, very likely due to duplicate SG Naming!")
        return 0


ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')


# Create EC2 SG
ec2_create_sg("ssh", "ssh_sg2")

# Create EC2 Key
ec2_create_key("ssh_key2")

ec2_resource.create_instances(ImageId='ami-f2d3638a', MinCount=1, MaxCount=1, SecurityGroups=['ssh_sg2'], KeyName='ssh_key2', InstanceType='t2.micro')
