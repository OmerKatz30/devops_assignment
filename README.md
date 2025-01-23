# 📖 Slack Bot for PhoneBook Management

This project is a **Slack bot** integrated with **AWS S3** to manage a PhoneBook stored in a CSV file.
 It allows you to add, retrieve, and download entries directly from Slack using simple commands.

## 🚀 Features
- **Add a Contact**: Use the `/add` command to add a new contact. Example: `/add John Doe,1234567890,johndoe@example.com`
- **Retrieve a Contact**: Use the `/get` command to fetch contact details. Example: `/get John Doe`
- **Download the PhoneBook**: Use the `/download` command to download the entire PhoneBook as a CSV file.

## 🛠 Prerequisites
Before you begin, ensure you have the following installed:
1. **Python** (3.9 or above)
2. **Docker** (for containerization)
3. **ngrok** (to expose local services to Slack)
4. **AWS S3 Bucket** (to store the PhoneBook CSV)
5. A **Slack App** configured for your workspace

## ⚙️ Setup Instructions
### Step 1: Clone the Repository
`git clone https://github.com/your-username/your-repo-name.git`  
`cd your-repo-name`

### Step 2: Create a Slack App
1. Go to the [Slack API](https://api.slack.com/apps) and create a new app.
2. Add the following **Bot Token Scopes** under **OAuth & Permissions**: `chat:write`, `commands`, `files:write`
3. Create Slash Commands: `/add`, `/get`, `/download`
4. Install the app in your workspace and copy the **Bot User OAuth Token**.

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory with the following values:  
SLACK_API_TOKEN=your_slack_bot_token  
AWS_ACCESS_KEY_ID=your_aws_access_key  
AWS_SECRET_ACCESS_KEY=your_aws_secret_key  
BUCKET_NAME=your_s3_bucket_name  
S3_FILE=you_s3_file_name


**⚠️ Note:** Do not commit the `.env` file to version control. Add it to `.gitignore`.

Step 4: Run the Application
🖥️ Option 1: Run Locally:  
Install dependencies: `pip install -r requirements.txt`  
Start the Flask app: `python src/devops_assignment/app.py`

🐳 Option 2: Run with Docker:  
Build the Docker image: `docker build -t slack-bot .`  
Run the container: `docker run -d -p 3000:3000 --name slack-bot-container --env-file .env -v C:\Users\your-username\Downloads:/root/Downloads slack-bot`

### Expose with ngrok
`ngrok http 3000`  
Copy the public URL provided by ngrok and update your Slack app’s **Request URL** for commands: `https://<ngrok-url>/slack/command`

## 🗂️ Project Structure
devops_assignment/  
├── src/  
│   ├── devops_assignment/  
│   │   ├── __init__.py  
│   │   ├── s3_phone_book_manager.py  
│   │   └── app.py  
├── .env.example  
├── .gitignore  
├── .dockerignore  
├── Dockerfile  
├── requirements.txt  
└── README.md



## 🛡️ Commands
1. **Add a Contact**: `/add <name>,<phone>,<email>`  
   Example: `/add John Doe,1234567890,johndoe@example.com`
2. **Retrieve a Contact**: `/get <name>`  
   Example: `/get John Doe`
3. **Download the PhoneBook**: `/download`

## 🖥️ CLI Usage

You can also manage the PhoneBook using the CLI.

1. **Add a record**:
   python src/devops_assignment/s3_phone_book_manager.py add "John Doe" "1234567890" "johndoe@example.com"
2. **Retrieve a record**:
   python src/devops_assignment/s3_phone_book_manager.py get "John Doe"
3.  **Download the PhoneBook CSV**:
   python src/devops_assignment/s3_phone_book_manager.py download ./local_phonebook.csv


## 🤔 Troubleshooting
1. **The bot doesn’t respond**:
   - Ensure the `.env` file is correctly configured.
   - Verify the ngrok URL is updated in your Slack app.
2. **File not downloading**:
   - Check your AWS S3 credentials in `.env`.
   - Ensure the bucket and file exist in S3.
3. **Docker issues**:
   - Confirm the `.env` file is correctly passed using `--env-file`.
   - Use the `docker logs` command to debug: `docker logs slack-bot-container`

