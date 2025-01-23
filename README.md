📖 Slack Bot for PhoneBook Management
This project is a Slack bot integrated with AWS S3 to manage a PhoneBook stored in a CSV file.
It allows you to add, retrieve, and download entries directly from Slack using simple commands.


🚀 Features
Add a Contact: /add <name>,<phone>,<email>
Example: /add John Doe,1234567890,johndoe@example.com

Retrieve a Contact: /get <name>
Example: /get John Doe

Download the PhoneBook: /download
Downloads the PhoneBook CSV file directly.


Here’s the README rewritten in a clean and visually appealing format:

📖 Slack Bot for PhoneBook Management
This project is a Slack bot integrated with AWS S3 to manage a PhoneBook stored in a CSV file. It allows you to add, retrieve, and download entries directly from Slack using simple commands.

🚀 Features
Add a Contact: /add <name>,<phone>,<email>
Example: /add John Doe,1234567890,johndoe@example.com

Retrieve a Contact: /get <name>
Example: /get John Doe

Download the PhoneBook: /download
Downloads the PhoneBook CSV file directly.

🛠 Prerequisites
Before you begin, make sure you have the following installed:

Python (3.9 or above)
Docker (for containerization)
ngrok (to expose local services to Slack)
AWS S3 Bucket (to store the PhoneBook CSV)
A Slack App configured for your workspace


Here’s the README rewritten in a clean and visually appealing format:

📖 Slack Bot for PhoneBook Management
This project is a Slack bot integrated with AWS S3 to manage a PhoneBook stored in a CSV file. It allows you to add, retrieve, and download entries directly from Slack using simple commands.

🚀 Features
Add a Contact: /add <name>,<phone>,<email>
Example: /add John Doe,1234567890,johndoe@example.com

Retrieve a Contact: /get <name>
Example: /get John Doe

Download the PhoneBook: /download
Downloads the PhoneBook CSV file directly.

🛠 Prerequisites
Before you begin, make sure you have the following installed:

Python (3.9 or above)
Docker (for containerization)
ngrok (to expose local services to Slack)
AWS S3 Bucket (to store the PhoneBook CSV)
A Slack App configured for your workspace


⚙️ Setup Instructions
Step 1: Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Step 2: Create a Slack App
Go to the Slack API and create a new app.
Add the following Bot Token Scopes under OAuth & Permissions:
chat:write
commands
files:write
Create Slash Commands for /add, /get, and /download with a request URL placeholder (to be updated later).
Install the app in your workspace and copy the Bot User OAuth Token.

Step 3: Create a .env File
Create a .env file in the root directory and add the following environment variables:
SLACK_API_TOKEN=your_slack_bot_token
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
BUCKET_NAME=your_s3_bucket_name
S3_FILE=phonebook.csv
⚠️ Note: Do not commit the .env file to version control. Use .gitignore to exclude it.

Step 4: Run the Application
🖥️ Option 1: Run Locally
Install dependencies:
pip install -r requirements.txt
Start the Flask app:
python src/devops_assignment/app.py

🐳 Option 2: Run with Docker
Build the Docker image:
docker build -t slack-bot .
docker run -d -p 3000:3000 --name slack-bot-container --env-file .env -v C:\Users\your-username\Downloads:/root/Downloads slack-bot

Step 5: Expose the App with ngrok
Start ngrok:
ngrok http 3000
Copy the public URL provided by ngrok.
Update your Slack app’s Request URL under Slash Commands:
https://<ngrok-url>/slack/command


🛡️ Using the Bot
Commands:
Add a Contact:
/add <name>,<phone>,<email>
Example: /add John Doe,1234567890,johndoe@example.com

Retrieve a Contact:
/get <name>
Example: /get John Doe

Download the PhoneBook:
/download


🗂️ Project Structure
devops_assignment/
├── src/
│   ├── devops_assignment/
│   │   ├── __init__.py
│   │   ├── s3_phone_book_manager.py
│   │   └── app.py           # Flask app entry point
├── tests/
│   ├── test_manager.py      # Tests phone manager
├── .env.example             # Example environment file
├── .gitignore               # Git ignore file
├── .dockerignore            # Docker ignore file
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # Documentation



🧪 Testing
You can add and run automated tests using pytest:
Install pytest:
pip install pytest
Run the tests:
pytest tests/


🤔 Troubleshooting
The bot doesn't respond:
Ensure the .env file is correctly configured.
Verify the ngrok URL is updated in your Slack app.

File not downloading:
Check your AWS S3 credentials in .env.
Ensure the bucket and file exist in S3.

Docker issues:
Confirm the .env file is correctly passed using --env-file.
Use the docker logs command to debug:
docker logs slack-bot-container







