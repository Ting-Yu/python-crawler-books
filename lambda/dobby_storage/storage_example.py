import storage
#
file_storage = storage.FileStorage()
#
# 1. Local storage
result = file_storage.save('test.txt', 'destination.txt')
print(f"Local storage File {result}.")

# 2. Using S3 storage with upload_file
file_storage.use_disk('s3')
result = file_storage.save('test.txt', 'destination.txt', bucket_name='fribooker')
print(f"S3 storage with upload_file File {result}.")

# 3. Using S3 storage with upload_fileobj
result = file_storage.save('test.txt', 'destination.txt', bucket_name='fribooker', use_fileobj=True)
print(f"S3 storage with upload_fileobj File {result}.")