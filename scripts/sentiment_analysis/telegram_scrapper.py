from telethon import TelegramClient, events
import pandas as pd

# Telegram API credentials
api_id = "your_api_id"
api_hash = "your_api_hash"

# Function to scrape messages from a Telegram channel
async def scrape_messages(channel_name, limit):
    # Authenticate with Telegram API
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    # Find the specified channel
    channel = await client.get_entity(channel_name)

    # Scrape messages from the channel
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        messages.append([message.date, message.message])

    # Store messages in a dataframe
    message_df = pd.DataFrame(messages, columns=['date', 'text'])

    await client.disconnect()

    return message_df
