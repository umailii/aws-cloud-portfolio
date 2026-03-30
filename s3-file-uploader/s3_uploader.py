import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

# ============================================================
# S3 File Uploader
# Author: Umair Ali | CIST Student | 3rd Year
# Project: AWS S3 File Uploader (Portfolio Project #1)
# ============================================================

# NOTE TO SELF:
# I struggled a LOT figuring out what boto3 even was. I kept confusing it
# with the AWS console (the website). Boto3 is just the Python library that
# lets your *code* talk to AWS instead of you clicking around on the website.
# Think of it like a remote control for AWS from inside your Python script.


def create_bucket(s3_client, bucket_name, region="us-east-1"):
    """
    Creates an S3 bucket if it doesn't already exist.

    # NOTE TO SELF:
    # I didn't understand why region mattered at first. Turns out AWS has
    # data centers all over the world ("regions"), and us-east-1 is Virginia.
    # Keeping your bucket close to your users = faster load times.
    # Also -- us-east-1 is the default and has the most features, so I
    # just defaulted to it here until I learn more.
    """
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"[✓] Bucket '{bucket_name}' created successfully.")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "BucketAlreadyOwnedByYou":
            print(f"[i] Bucket '{bucket_name}' already exists and you own it. Moving on.")
            return True
        elif error_code == "BucketAlreadyExists":
            # NOTE TO SELF:
            # S3 bucket names are GLOBAL -- meaning no two people in the world
            # can have the same bucket name. I kept getting this error because
            # I was using names like "my-bucket" which are already taken.
            # Fix: make names unique, like "yourname-project-2024"
            print(f"[!] That bucket name is already taken globally. Try a more unique name.")
            return False
        else:
            print(f"[!] Error creating bucket: {e}")
            return False


def upload_file(s3_client, file_path, bucket_name, s3_key=None):
    """
    Uploads a local file to an S3 bucket.

    file_path  -- path to the file on your computer
    bucket_name -- the S3 bucket to upload to
    s3_key     -- the name the file will have in S3 (defaults to filename)

    # NOTE TO SELF:
    # The 's3_key' thing confused me. Think of it like the file's "address"
    # inside your bucket. If I upload 'C:/Users/Me/resume.pdf' and don't set
    # an s3_key, it'll just be called 'resume.pdf' in the bucket.
    # You can also make folders like: 'documents/2024/resume.pdf'
    """
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return False

    # If no custom name given, just use the original filename
    if s3_key is None:
        s3_key = os.path.basename(file_path)

    try:
        file_size = os.path.getsize(file_path)
        print(f"[~] Uploading '{file_path}' ({file_size} bytes) to s3://{bucket_name}/{s3_key} ...")

        s3_client.upload_file(file_path, bucket_name, s3_key)

        print(f"[✓] Upload successful!")
        print(f"    Location: https://{bucket_name}.s3.amazonaws.com/{s3_key}")
        return True

    except NoCredentialsError:
        # NOTE TO SELF:
        # This error destroyed me for two days. It means AWS can't find your
        # credentials (your AWS Access Key + Secret Key).
        # How I fixed it:
        #   1. Ran `aws configure` in my terminal
        #   2. Pasted in my Access Key ID and Secret Access Key from the AWS Console
        #   3. Set region to us-east-1
        # You get these keys from: AWS Console > IAM > Users > Your User > Security Credentials
        # WARNING: NEVER paste your keys directly in your code. Never commit them to GitHub.
        print("[!] AWS credentials not found.")
        print("    Fix: Run 'aws configure' in your terminal and enter your AWS keys.")
        return False

    except ClientError as e:
        print(f"[!] Upload failed: {e}")
        return False


def list_bucket_files(s3_client, bucket_name):
    """
    Lists all files currently stored in the bucket.

    # NOTE TO SELF:
    # I added this mostly so I could verify my uploads actually worked.
    # 'Paginator' was a new concept -- basically if you have thousands of files,
    # AWS won't return them all at once. The paginator handles fetching them
    # in chunks automatically. I don't fully get it yet but it works.
    """
    print(f"\n[~] Files in bucket '{bucket_name}':")
    print("-" * 45)

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name)

        file_count = 0
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    size_kb = round(obj["Size"] / 1024, 2)
                    print(f"  📄 {obj['Key']}  ({size_kb} KB)  | Modified: {obj['LastModified'].strftime('%Y-%m-%d')}")
                    file_count += 1

        if file_count == 0:
            print("  (bucket is empty)")
        else:
            print(f"\n  Total: {file_count} file(s)")

    except ClientError as e:
        print(f"[!] Could not list files: {e}")


def delete_file(s3_client, bucket_name, s3_key):
    """
    Deletes a file from the S3 bucket.

    # NOTE TO SELF:
    # I was scared to add this at first because I thought I'd accidentally
    # delete something important. But S3 doesn't have a recycle bin by default,
    # so once it's gone, it's gone. I added a confirmation prompt to be safe.
    # Lesson learned: always add a sanity check before destructive operations.
    """
    confirm = input(f"\n  Are you sure you want to delete '{s3_key}' from '{bucket_name}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("  [i] Deletion cancelled.")
        return

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
        print(f"  [✓] '{s3_key}' deleted successfully.")
    except ClientError as e:
        print(f"  [!] Delete failed: {e}")


def main():
    # ----------------------------------------------------------------
    # CONFIGURATION -- change these to match your setup
    # ----------------------------------------------------------------
    BUCKET_NAME = "yourname-cist-portfolio-2024"   # Must be globally unique!
    REGION      = "us-east-1"
    FILE_TO_UPLOAD = "test_file.txt"               # Put any file path here
    # ----------------------------------------------------------------

    # NOTE TO SELF:
    # boto3.client() is how you "connect" to an AWS service.
    # 's3' tells it we want to work with S3 specifically.
    # AWS has tons of other services too: 'ec2', 'lambda', 'rds', etc.
    print("=" * 50)
    print("  AWS S3 File Uploader | CIST Portfolio Project")
    print("=" * 50)

    s3 = boto3.client("s3", region_name=REGION)

    # Step 1 -- make sure our bucket exists
    bucket_ok = create_bucket(s3, BUCKET_NAME, REGION)
    if not bucket_ok:
        print("\n[!] Could not create or access bucket. Exiting.")
        return

    # Step 2 -- create a small test file if one doesn't exist
    # NOTE TO SELF:
    # I created this just so there's always something to upload when testing.
    # In a real project you'd remove this and pass in an actual file.
    if not os.path.exists(FILE_TO_UPLOAD):
        with open(FILE_TO_UPLOAD, "w") as f:
            f.write("Hello from my first AWS project!\nUploaded with Python + boto3.\n")
        print(f"[i] Created sample file: {FILE_TO_UPLOAD}")

    # Step 3 -- upload the file
    upload_file(s3, FILE_TO_UPLOAD, BUCKET_NAME)

    # Step 4 -- show everything in the bucket
    list_bucket_files(s3, BUCKET_NAME)

    print("\n[✓] Done! Check your AWS Console > S3 to see the file.")
    print("    https://s3.console.aws.amazon.com/s3/buckets/" + BUCKET_NAME)


if __name__ == "__main__":
    main()
