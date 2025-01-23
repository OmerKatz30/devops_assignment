import click
import boto3
import os
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class S3PhoneBookManager:
    def __init__(self, bucket_name, s3_file):
        """Initialize with the S3 bucket and file details."""
        self.bucket_name = bucket_name
        self.s3_file = s3_file
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def download_file(self):
        """Download the CSV file from S3 into memory as a Pandas DataFrame."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.s3_file)
            csv_content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            return df
        except Exception as e:
            print(f"Error downloading file: {e}")
            return pd.DataFrame(columns=['Name', 'Phone', 'Email'])  # Return an empty DataFrame if file not found

    def upload_file(self, df):
        """Upload the modified DataFrame back to S3 as a CSV file."""
        try:
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            self.s3_client.put_object(Bucket=self.bucket_name, Key=self.s3_file, Body=csv_buffer.getvalue())
            print(f"File '{self.s3_file}' successfully updated on S3.")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def add_record(self, name, phone, email):
        """Add a new record to the S3 PhoneBook CSV."""
        df = self.download_file()
        new_record = pd.DataFrame([{'Name': name, 'Phone': phone, 'Email': email}])
        df = pd.concat([df, new_record], ignore_index=True)
        self.upload_file(df)
        print(f"Record added: {new_record.to_dict('records')[0]}")

    def retrieve_record(self, name):
        """Retrieve a record by name from the S3 PhoneBook CSV."""
        df = self.download_file()
        record = df[df['Name'] == name]
        if not record.empty:
            print(f"Record found: {record.to_dict('records')[0]}")
            return record.to_dict('records')[0]
        else:
            print("Record not found.")
            return None

    def download_to_local(self, local_path):
        """Download the CSV file from S3 to a local path."""
        try:
            self.s3_client.download_file(self.bucket_name, self.s3_file, local_path)
            print(f"File downloaded locally to {local_path}")
        except Exception as e:
            print(f"Error downloading file locally: {e}")
            raise e


@click.group()
def cli():
    """CLI group for managing the PhoneBook."""
    pass


@cli.command()
@click.argument('name')
@click.argument('phone')
@click.argument('email')
def add(name, phone, email):
    """Add a new record to the PhoneBook."""
    bucket_name = os.getenv("BUCKET_NAME")
    s3_file = os.getenv("S3_FILE")
    manager = S3PhoneBookManager(bucket_name, s3_file)
    manager.add_record(name, phone, email)


@cli.command()
@click.argument('name')
def get(name):
    """Retrieve a record by name from the PhoneBook."""
    bucket_name = os.getenv("BUCKET_NAME")
    s3_file = os.getenv("S3_FILE")
    manager = S3PhoneBookManager(bucket_name, s3_file)
    manager.retrieve_record(name)


@cli.command()
@click.argument('local_path', type=click.Path())
def download(local_path):
    """Download the PhoneBook CSV to a local path."""
    bucket_name = os.getenv("BUCKET_NAME")
    s3_file = os.getenv("S3_FILE")
    manager = S3PhoneBookManager(bucket_name, s3_file)
    manager.download_to_local(local_path)


if __name__ == "__main__":
    cli()
