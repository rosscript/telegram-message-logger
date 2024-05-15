import os
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
from utils import (
    create_folder_name,
    save_message,
    get_media_type_and_filename,
    get_chat_name_and_type,
    create_file_name
)

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Accesso al client Telegram
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('none', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_id = event.chat_id
        sender = await event.get_sender()
        sender_id = sender.id
        username = sender.username if sender.username else 'unknown'
        chat_title, chat_type = await get_chat_name_and_type(event)
        folder_name = create_folder_name(chat_id, chat_title)
        base_folder = os.path.join('./chats', chat_type)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"Nuovo messaggio ricevuto da {username} in chat {chat_title} (ID: {chat_id}, Tipo: {chat_type})")

        # Gestione messaggio di testo con o senza media
        if event.message.message and event.message.media:
            media_type, file_name = get_media_type_and_filename(event.message.media)
            if file_name:  # Se il nome del file è valido
                file_path = await event.message.download_media(file=f'./chats/{chat_type}/{folder_name}/{media_type}/{file_name}')
                save_message(base_folder, folder_name, event.message.message, sender_id, username, f'{media_type.capitalize()} con testo', timestamp, chat_type, chat_title, file_path)
            else:
                save_message(base_folder, folder_name, event.message.message, sender_id, username, 'text', timestamp, chat_type, chat_title)
        
        # Gestione solo messaggio di testo
        elif event.message.message:
            save_message(base_folder, folder_name, event.message.message, sender_id, username, 'text', timestamp, chat_type, chat_title)
        
        # Gestione solo media
        elif event.message.media:
            media_type, file_name = get_media_type_and_filename(event.message.media)
            if file_name:  # Se il nome del file è valido
                file_path = await event.message.download_media(file=f'./chats/{chat_type}/{folder_name}/{media_type}/{file_name}')
                save_message(base_folder, folder_name, media_type.capitalize(), sender_id, username, media_type, timestamp, chat_type, chat_title, file_path)
            else:
                save_message(base_folder, folder_name, 'Unknown Media', sender_id, username, 'unknown', timestamp, chat_type, chat_title)
        
        else:
            save_message(base_folder, folder_name, 'Unknown Media', sender_id, username, 'unknown', timestamp, chat_type, chat_title)
    
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {str(e)}\n')
        print(f"Errore: {e}")

# Avvio del client
client.start()
print("Client Telegram avviato e in ascolto per nuovi messaggi...")
client.run_until_disconnected()
