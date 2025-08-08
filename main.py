import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Get all snapshots owned by the account
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    # Get all volume and instance details
    volumes = ec2.describe_volumes()['Volumes']
    instances = ec2.describe_instances()['Reservations']

    # Collect all attached volume IDs
    attached_volumes = set()
    for reservation in instances:
        for instance in reservation['Instances']:
            for mapping in instance.get('BlockDeviceMappings', []):
                attached_volumes.add(mapping['Ebs']['VolumeId'])

    # Collect all active volume IDs
    active_volumes = set(vol['VolumeId'] for vol in volumes)

    #Identify stale snapshots
    for snap in snapshots:
        vol_id = snap.get('VolumeId')
        if vol_id not in attached_volumes and vol_id not in active_volumes:
            print(f"Deleting stale snapshot: {snap['SnapshotId']}")
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
