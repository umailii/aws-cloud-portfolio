# 📦 AWS S3 File Uploader
> **Portfolio Project #1** | Python + AWS | CIST Student

A command-line Python tool that uploads files to Amazon S3.
Built to learn the basics of cloud storage and the AWS SDK for Python (boto3).

---

## 💡 What This Does

- Creates an S3 bucket (cloud storage container)
- Uploads a local file to that bucket
- Lists all files currently in the bucket
- Deletes files with a safety confirmation

---

## 🧠 What I Learned

- How AWS S3 works (buckets, objects, keys)
- How to authenticate Python scripts with AWS credentials
- How to use `boto3`, the official AWS SDK for Python
- How to handle cloud-specific errors like missing credentials or duplicate bucket names
- Why you should **never** hardcode AWS keys in your code

---

## ⚙️ Requirements

- Python 3.7+
- An AWS account (free tier works fine)
- AWS CLI installed

Install dependencies:
```bash
pip install boto3
pip install awscli
```

---

## 🔐 Setup: AWS Credentials

Before running, configure your AWS credentials:

```bash
aws configure
```

You'll be prompted for:
- **AWS Access Key ID** — found in AWS Console > IAM > Users > Security Credentials
- **AWS Secret Access Key** — same place (only shown once when created!)
- **Default region** — use `us-east-1`
- **Output format** — use `json`

> ⚠️ **Never paste your keys directly in your code or push them to GitHub.**

---

## 🚀 Usage

1. Clone this repo
2. Open `s3_uploader.py` and update the config section at the top:

```python
BUCKET_NAME    = "yourname-cist-portfolio-2024"  # must be globally unique
REGION         = "us-east-1"
FILE_TO_UPLOAD = "test_file.txt"
```

3. Run it:

```bash
python s3_uploader.py
```

---

## 📁 Project Structure

```
s3_uploader/
├── s3_uploader.py   # main script
├── README.md        # this file
└── test_file.txt    # auto-generated sample file (gitignored)
```

---

## 🗺️ What's Next (Project #2 Preview)

- Automate uploads with a folder watcher
- Add a config file so settings aren't hardcoded
- Deploy a Lambda function that triggers on upload

---

*Built by a 3rd-year CIST student learning Cloud/DevOps. Part of an ongoing AWS portfolio series.*
