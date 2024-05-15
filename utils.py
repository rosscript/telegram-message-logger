# utils.py

import os
import csv
import json
import re
from datetime import datetime
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto, PeerChannel, PeerChat, PeerUser

def create_folder_name(chat_id, chat_title):
    sanitized_title = re.sub(r'\s+', '', chat_title)  # Rimuovi spazi
    folder_name = f'[{chat_id}]_{sanitized_title}'
    return folder_name

def save_message_csv(csv_file_path, message_data, include_header=False):
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['sender_id', 'username', 'message_type', 'message', 'timestamp', 'media_path', 'chat_type', 'chat_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow(message_data)

def save_message_json(json_file_path, message_data):
    messages = []
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
            messages = json.load(jsonfile)
    messages.append(message_data)
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(messages, jsonfile, ensure_ascii=False, indent=4)

def save_message(base_folder, folder_name, message, sender_id, username, message_type, timestamp, chat_type, chat_name, media_path=None):
    folder_path = os.path.join(base_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    csv_file_path = os.path.join(folder_path, 'messages.csv')
    json_file_path = os.path.join(folder_path, 'messages.json')
    global_csv_file_path = os.path.join('./chats', 'messages.csv')
    global_json_file_path = os.path.join('./chats', 'messages.json')

    message_data = {
        'sender_id': sender_id,
        'username': username or 'unknown',
        'message_type': message_type,
        'message': message.replace('\n', '\\n'),
        'timestamp': timestamp,
        'media_path': media_path,
        'chat_type': chat_type,
        'chat_name': chat_name  # Aggiunta del nome della chat
    }

    save_message_csv(csv_file_path, message_data)
    save_message_json(json_file_path, message_data)
    save_message_csv(global_csv_file_path, message_data)
    save_message_json(global_json_file_path, message_data)

def get_media_type_and_filename(media):
    if isinstance(media, MessageMediaPhoto):
        return 'photo', f"{datetime.now().strftime('%d%m%Y%H%M%S')}.jpg"
    elif isinstance(media, MessageMediaDocument):
        mime_type = media.document.mime_type
        if media.document.attributes:
            for attr in media.document.attributes:
                if hasattr(attr, 'file_name') and attr.file_name:
                    return 'document', attr.file_name
        if mime_type.startswith('audio'):
            return 'audio', f"{datetime.now().strftime('%d%m%Y%H%M%S')}.{mime_type.split('/')[-1]}"
        elif mime_type.startswith('video'):
            return 'video', f"{datetime.now().strftime('%d%m%Y%H%M%S')}.{mime_type.split('/')[-1]}"
        else:
            return 'document', f"{datetime.now().strftime('%d%m%Y%H%M%S')}.{mime_type.split('/')[-1]}"
    else:
        return 'unknown', None

async def get_chat_name_and_type(event):
    chat = await event.get_chat()
    if event.is_private:
        chat_name = chat.username if chat.username else chat.first_name
        chat_type = 'Private'
    else:
        chat_name = chat.title
        if isinstance(event.message.to_id, PeerChannel):
            if chat.megagroup:
                chat_type = 'Groups'
            else:
                chat_type = 'Channels'
        elif isinstance(event.message.to_id, PeerChat):
            chat_type = 'Groups'
        else:
            chat_type = 'Unknown'
    return chat_name, chat_type

def create_file_name(timestamp, extension):
    return f"{timestamp.strftime('%d%m%Y%H%M%S')}.{extension}"
