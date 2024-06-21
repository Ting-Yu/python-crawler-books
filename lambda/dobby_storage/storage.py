import os
import json
import shutil
import boto3


class StorageConfig:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.default = self.config['default']
        self.disks = self.config['disks']

    def get_default_disk(self):
        return self.disks[self.default]

    def get_disk(self, disk_name):
        return self.disks.get(disk_name)


class LocalStorage:
    def __init__(self, root):
        self.root = root

    def save(self, file_path, destination):
        full_path = os.path.join(self.root, destination)
        shutil.copy(file_path, full_path)
        return full_path


class S3Storage:
    def __init__(self, key, secret, region, bucket=None):
        self.s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)
        self.bucket = bucket

    def save(self, file_path, object_name, bucket_name=None, use_fileobj=False):
        bucket = bucket_name or self.bucket
        if not bucket:
            raise ValueError("Bucket name must be specified either during initialization or when calling save method.")

        if use_fileobj:
            with open(file_path, 'rb') as file_obj:
                self.s3.upload_fileobj(file_obj, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        else:
            self.s3.upload_file(file_path, bucket, object_name, ExtraArgs={'ACL': 'public-read'})

        return f"https://{bucket}.s3.amazonaws.com/{object_name}"

class FileStorage:
    def __init__(self, config_path='storage.json'):
        self.config = StorageConfig(config_path)
        self._storage = self._initialize_storage(self.config.get_default_disk())

    def _initialize_storage(self, disk_config):
        driver = disk_config['driver']
        if driver == 'local':
            return LocalStorage(disk_config['root'])
        elif driver == 's3':
            key = os.environ.get('CUSTOM_AWS_ACCESS_KEY_ID', disk_config['key'])
            secret = os.environ.get('CUSTOM_AWS_SECRET_ACCESS_KEY', disk_config['secret'])
            region = os.environ.get('CUSTOM_AWS_DEFAULT_REGION', disk_config['region'])
            bucket = os.environ.get('CUSTOM_AWS_BUCKET', disk_config.get('bucket'))
            return S3Storage(key, secret, region, bucket)
        else:
            return None

    def save(self, file_path, destination=None, **kwargs):
        if isinstance(self._storage, LocalStorage):
            return self._storage.save(file_path, destination or os.path.basename(file_path))
        elif isinstance(self._storage, S3Storage):
            bucket_name = kwargs.get('bucket_name')
            use_fileobj = kwargs.get('use_fileobj', False)
            return self._storage.save(file_path, destination or os.path.basename(file_path), bucket_name, use_fileobj)
        else:
            return self._dynamic_save(file_path, destination, **kwargs)

    def _dynamic_save(self, file_path, destination, **kwargs):
        driver = kwargs.get('driver')
        if driver == 's3':
            key = kwargs.get('key', os.environ.get('CUSTOM_AWS_ACCESS_KEY_ID'))
            secret = kwargs.get('secret', os.environ.get('CUSTOM_AWS_SECRET_ACCESS_KEY'))
            region = kwargs.get('region', os.environ.get('CUSTOM_AWS_DEFAULT_REGION'))
            bucket = kwargs.get('bucket', os.environ.get('CUSTOM_AWS_BUCKET'))
            use_fileobj = kwargs.get('use_fileobj', False)
            s3_storage = S3Storage(key, secret, region, bucket)
            return s3_storage.save(file_path, destination, bucket, use_fileobj)
        else:
            raise ValueError(f"Unsupported storage driver: {driver}")

    def use_disk(self, disk_name):
        disk_config = self.config.get_disk(disk_name)
        self._storage = self._initialize_storage(disk_config)