import boto3
import os
import json
import cv2
import botocore.exceptions

s3_client = boto3.client('s3')


def upload_video_with_metadata(file_path, bucket_name, object_key, frame_rate, total_frames, duration_sec, folder_prefix):
    # Check if the video and metadata already exist in S3
    if check_existing_object(bucket_name, object_key) or check_existing_object(bucket_name, object_key + '.metadata.json'):
        print(f"Video and metadata already exist in S3: {object_key}")
        return

    # Define the object key with the desired folder structure
    object_key = folder_prefix + object_key

    # Upload the video to S3
    s3_client.upload_file(file_path, bucket_name, object_key)

    # Get the size of the uploaded file
    file_size = os.path.getsize(file_path)
    content_size_mb = file_size / (1024 * 1024)  # Convert to MB

    # Define the metadata
    metadata = {
        'x-amz-meta-frame-rate': str(frame_rate),
        'x-amz-meta-total-frames': str(total_frames),
        'x-amz-meta-duration-sec': str(duration_sec),
        'Content-Size': str(content_size_mb),
        'ObjectKey': object_key
    }

    # Store the metadata as a separate JSON file
    metadata_key = object_key + '.metadata.json'
    metadata_json = json.dumps(metadata)
    s3_client.put_object(Body=metadata_json, Bucket=bucket_name, Key=metadata_key)

    print("Video uploaded successfully with metadata.")


def check_existing_object(bucket_name, object_key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e


def create_prefix_if_not_exist(bucket_name, folder_prefix):
    # Check if the prefix already exists in the bucket
    try:
        s3_client.head_object(Bucket=bucket_name, Key=folder_prefix)
        print(f"Prefix already exists in S3: {folder_prefix}")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Create the prefix in the bucket
            s3_client.put_object(Body='', Bucket=bucket_name, Key=folder_prefix)
            print(f"Prefix created in S3: {folder_prefix}")
        else:
            raise e


def extract_video_metadata(file_path):
    # Open the video file
    video = cv2.VideoCapture(file_path)

    # Check if the video file is successfully opened
    if not video.isOpened():
        error_message = f"Failed to open video file: {file_path}"
        video.release()
        return None, None, None, error_message

    # Get video metadata
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Check if the metadata values are valid
    if fps == 0 or total_frames == 0:
        error_message = f"Invalid video metadata: {file_path}"
        video.release()
        return None, None, None, error_message

    duration_sec = total_frames / fps

    # Release the video file
    video.release()

    return fps, total_frames, duration_sec, None


def process_videos_in_folder(folder_path, bucket_name, folder_prefix):
    create_prefix_if_not_exist(bucket_name, folder_prefix)

    problematic_videos = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            object_key = file_name
            fps, total_frames, duration_sec, error_message = extract_video_metadata(file_path)

            if error_message is not None:
                problematic_videos.append((file_name, error_message))
                continue

            upload_video_with_metadata(file_path, bucket_name, object_key, fps, total_frames, duration_sec, folder_prefix)

    # Print problematic videos and their error messages
    if problematic_videos:
        print("Problematic videos:")
        for video, error in problematic_videos:
            print(f"- {video}: {error}")


def main():
    folder_path = 'folder path'
    bucket_name = 'bucket name'
    folder_prefix = 'folder/subfolder/'  # Update with your desired folder structure within the bucket

    process_videos_in_folder(folder_path, bucket_name, folder_prefix)


if __name__ == '__main__':
    main()
