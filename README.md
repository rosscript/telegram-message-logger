
# Telegram Message Logger

This Python script is a Telegram message logger that saves received and sent messages in chats, groups, and channels in CSV and JSON formats.
- Chats are monitored in real-time, and messages are saved in a log file.
- Chats are saved in separate folders by type (chats, groups, channels), and a folder is created for each chat.
- Messages are saved in CSV and JSON files. Additionally, a folder is created for each type of attachment.
- When a message with an attachment is received, the file path is saved in the corresponding field.

## Requirements

- Python 3.7+
- Telegram API ID and Hash
- Required Python libraries (telethon / python-dotenv)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rosscript/telegram-message-logger.git
   cd telegram-message-logger
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate # Linux / macOS
   .\venv\Scripts\activate # Windows
   ```

3. **Install the required libraries**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment variables**

   ```bash
   cp .env.example .env
   nano .env # Linux / macOS
   notepad .env # Windows
   ```

   Edit the variables with your own data:
   - `API_ID` and `API_HASH` (available at https://my.telegram.org)

5. **Run the program**

   ```bash
   python app.py
   ```
