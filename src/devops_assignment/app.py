from pathlib import Path

from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from threading import Thread
import os
from devops_assignment.s3_phone_book_manager import S3PhoneBookManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Slack bot token
slack_token = os.getenv("SLACK_API_TOKEN")
slack_client = WebClient(token=slack_token)

# S3 configuration
bucket_name = os.getenv("BUCKET_NAME")
s3_file = os.getenv("S3_FILE")

# Initialize S3 PhoneBook Manager
s3_manager = S3PhoneBookManager(bucket_name=bucket_name, s3_file=s3_file)


@app.route("/slack/command", methods=["POST"])
def handle_slack_command():
    """Handle Slack slash commands."""
    command = request.form.get("command")
    text = request.form.get("text")
    user_id = request.form.get("user_id")

    if command == "/add":
        try:
            print(f"Received /add command with text: {text}")
            name, phone, email = map(str.strip, text.split(","))
            print(f"Parsed values - Name: {name}, Phone: {phone}, Email: {email}")
            s3_manager.add_record(name, phone, email)
            return jsonify({
                "response_type": "in_channel",
                "text": f"Added: Name: {name}, Phone: {phone}, Email: {email}"
            })
        except ValueError:
            return jsonify({
                "response_type": "ephemeral",
                "text": "Invalid format. Use `/add name,phone,email`."
            })

    elif command == "/get":
        name = text.strip()
        record = s3_manager.retrieve_record(name)
        if record:
            return jsonify({
                "response_type": "in_channel",
                "text": f"Record Found: Name: {record['Name']}, Phone: {record['Phone']}, Email: {record['Email']}"
            })
        else:
            return jsonify({
                "response_type": "ephemeral",
                "text": f"No record found for {name}."
            })

    elif command == "/download":
        try:
            # Respond to Slack immediately
            response_text = "Processing your request. The PhoneBook CSV will be sent shortly."
            Thread(target=process_download, args=(user_id,)).start()
            return jsonify({"response_type": "ephemeral", "text": response_text})
        except Exception as e:
            print(f"Error in /download command: {e}")
            return jsonify({
                "response_type": "ephemeral",
                "text": f"An error occurred while processing the command: {str(e)}"
            })

    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Unknown command. Use `/add`, `/get`, or `/download`."
        })


def process_download(user_id):
    """Process the /download command in the background."""
    try:
        # Define the local file path in the Downloads folder
        downloads_folder = str(Path.home() / "Downloads")
        local_file = os.path.join(downloads_folder, "phonebook.csv")  # Full path to the file

        # Step 1: Download the file from S3
        s3_manager.download_to_local(local_file)
        print(f"File downloaded locally to: {local_file}")
        # Step 3: Upload the file to Slack
        with open(local_file, "rb") as file_content:
            slack_client.files_upload_v2(
                file=file_content,
                title="PhoneBook CSV",
                filename="phonebook.csv",
                initial_comment="Here is the PhoneBook CSV file:",
            )
        print(f"File successfully uploaded to user: {user_id}")
        slack_client.chat_postMessage(
            channel=user_id,
            text=f"The PhoneBook CSV file has been successfully downloaded to {local_file}."
        )

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        slack_client.chat_postMessage(
            channel=user_id,
            text="An error occurred: The file could not be found."
        )

    except ValueError as e:
        print(f"ValueError: {e}")
        slack_client.chat_postMessage(
            channel=user_id,
            text="An error occurred: The file is empty and could not be uploaded."
        )

    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        slack_client.chat_postMessage(
            channel=user_id,
            text=f"An error occurred while processing your request: {e.response['error']}"
        )

    except Exception as e:
        print(f"Unexpected Error: {e}")
        slack_client.chat_postMessage(
            channel=user_id,
            text=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    app.run(port=3000)
