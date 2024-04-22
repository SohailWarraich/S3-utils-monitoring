import boto3
import json

def get_object_keys_by_extension(bucket_name, prefix, extension):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Retrieve all object keys from the bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    object_keys = []

    # Extract the object keys that match the specified extension from the response
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith(extension):
                object_keys.append(obj['Key'])

    return object_keys

def extract_filename_from_key(object_key, delimiter):
    # Split the object key based on the delimiter and extract the desired part
    filename = object_key.split(delimiter)[0]
    return filename

def get_data_from_json_files(bucket_name, object_keys, delimiter):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Initialize an empty dictionary to store the JSON data
    json_data = {}

    # Iterate over the object keys
    for key in object_keys:
        # Retrieve the JSON file contents
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')

        # Parse the JSON data
        data = json.loads(content)

        # Extract the desired part of the object key
        filename = extract_filename_from_key(key, delimiter)

        # Store the JSON data in the dictionary with the extracted filename as the key
        json_data[filename] = data

    return json_data

def main():
    # Specify the bucket name, prefix, extension, and delimiter
    bucket_name = 'bucket-name'
    prefix = 'folder/subfolder/'  # Update with the desired folder path
    extension = '.json'
    delimiter = '.'

    # Get object keys by extension and prefix
    json_object_keys = get_object_keys_by_extension(bucket_name, prefix, extension)

    # Get data from JSON files
    json_data = get_data_from_json_files(bucket_name, json_object_keys, delimiter)

    # Check if any metadata is found
    if not json_data:
        print("No metadata found.")
    else:
        # Print the separated JSON data
        for key, data in json_data.items():
            print(f"Meta Data for: {key}")
            # print("JSON Data:")
            print(data)
            print()

if __name__ == "__main__":
    main()
