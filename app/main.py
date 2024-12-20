import boto3
import psycopg2
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS Clients
s3 = boto3.client('s3')
glue = boto3.client('glue')

# Configuration
S3_BUCKET = "your-s3-bucket-name"
S3_KEY = "data/file.csv"
RDS_HOST = "your-rds-host"
RDS_DATABASE = "your-database"
RDS_USER = "your-username"
RDS_PASSWORD = "your-password"

def read_from_s3():
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        data = response['Body'].read().decode('utf-8')
        return data.splitlines()
    except NoCredentialsError:
        print("AWS credentials not available.")
        return None
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return None

def write_to_rds(data):
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_DATABASE,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = conn.cursor()
        for line in data:
            cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", line.split(","))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data pushed to RDS successfully.")
    except Exception as e:
        print(f"Error writing to RDS: {e}")
        return False
    return True

def write_to_glue(data):
    try:
        # Use Glue's APIs to write data (placeholder logic)
        print("Writing data to AWS Glue...")
        # Add Glue-specific implementation here
        return True
    except Exception as e:
        print(f"Error writing to Glue: {e}")
        return False

def main():
    data = read_from_s3()
    if data:
        if not write_to_rds(data):
            write_to_glue(data)

if __name__ == "__main__":
    main()

