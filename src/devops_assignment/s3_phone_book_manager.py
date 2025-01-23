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
            print(csv_content)
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
        df = pd.concat([df, new_record], ignore_index=True)  # Use pd.concat instead of df.append
        self.upload_file(df)
        print(f"Record added: {new_record.to_dict('records')[0]}")

    def retrieve_record(self, name):
        """Retrieve a record by name from the S3 PhoneBook CSV."""
        df = self.download_file()
        record = df[df['Name'] == name]
        if not record.empty:
            return record.to_dict('records')[0]
        else:
            return None

    def download_to_local(self, local_path):
        """Download the CSV file from S3 to a local path."""
        try:
            self.s3_client.download_file(self.bucket_name, self.s3_file, local_path)
            print(f"File downloaded locally to {local_path}")
        except Exception as e:
            print(f"Error downloading file locally: {e}")
            raise e


if __name__ == "__main__":
    #Sanity testing

    # Load environment variables for bucket and file
    bucket_name = os.getenv("BUCKET_NAME")
    s3_file = os.getenv("S3_FILE")

    # Initialize the S3PhoneBookManager
    manager = S3PhoneBookManager(bucket_name, s3_file)

    # Test adding records
    print("\nTesting add_record...")
    manager.add_record("Alice", "1234567890", "alice@example.com")
    print("Added record: Alice, 1234567890, alice@example.com")
    manager.add_record("Bob", "9876543210", "bob@example.com")
    print("Added record: Bob, 9876543210, bob@example.com")

    # Test retrieving records
    print("\nTesting retrieve_record...")
    alice_record = manager.retrieve_record("Alice")
    if alice_record:
        print(f"Record found for Alice: {alice_record}")
    else:
        print("No record found for Alice.")

    bob_record = manager.retrieve_record("Bob")
    if bob_record:
        print(f"Record found for Bob: {bob_record}")
    else:
        print("No record found for Bob.")

    # Test downloading the updated file to a local path
    print("\nTesting download_to_local...")
    local_path = "./local_phonebook.csv"
    manager.download_to_local(local_path)

    # Verify the updated file was downloaded locally
    if os.path.exists(local_path):
        print(f"Updated PhoneBook successfully downloaded to: {local_path}")
        with open(local_path, 'r') as f:
            print("Updated PhoneBook contents:")
            print(f.read())
    else:
        print("Updated file download failed.")
