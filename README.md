# S3-utils-monitoring
This repository contains scripts for managing and extracting metadata from videos.

video_metadata.py
The video_metadata.py script allows you to upload videos to an S3 bucket along with their metadata. It performs the following tasks:

Uploads a video file to an S3 bucket.
Extracts metadata from the video, including frame rate, total frames, and duration.
Stores the metadata in a separate JSON file in the S3 bucket.
extract_metadata.py
The extract_metadata.py script retrieves metadata from JSON files stored in an S3 bucket. It performs the following tasks:

Retrieves object keys by extension and prefix from the S3 bucket.
Extracts the desired part of the object key.
Retrieves the JSON file contents from the S3 bucket.
Parses the JSON data and stores it in a dictionary with the extracted filename as the key.
Prerequisites
Before running these scripts, make sure you have the following:

Python 3.x installed.
Boto3 library installed. You can install it using pip install boto3.
Usage
Clone the repository: git clone https://github.com/SohailWarraich/S3-utils-monitoring.git

Install the required dependencies:

pip install boto3

Modify the necessary configurations in the scripts, such as the S3 bucket name,prefix and folder paths.

Run the scripts using the Python interpreter:
