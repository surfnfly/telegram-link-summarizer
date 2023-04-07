from telethon import TelegramClient, events
import openai

import logging

from urlextract import URLExtract

from gsheets import save_to_google_sheets as stgs

import configparser

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
sessionname = config['Telegram']['sessionname']
openai.api_key = config['OpenAI']['openai_api_key']

client = TelegramClient(sessionname, api_id, api_hash)


def gpting(linky):
    openai.api_key = openai.api_key
    prompty = f'Summarize what is about this webpage: {linky} and describe in 3-5 sentences.'

    response = openai.ChatCompletion.create(
        # model="text-davinci-003",
        model="gpt-4",
        messages=[
            {'role' : 'system', 'content' : 'You are assistant who can find the essence of the information on the web sites.'},
            {'role' : 'user', 'content' : prompty}
        ],
        # prompt=prompty,
        temperature=0.9,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    return response['choices'][0]['message']['content']


@client.on(events.NewMessage)
async def my_event_handler(event):
    extractor = URLExtract()
    if extractor.has_urls(event.text):
        logging.info(f'URL Extraactor found this: {extractor.find_urls(event.text)}')
        urls = extractor.find_urls(event.text).reverse()[0]
        # chat = await event.get_chat()
        comments = event.raw_text
        sender = await event.get_sender()
        nn_answer = gpting(urls)
        logging.info(f'From GPT i got this: {nn_answer}')

        await event.reply(nn_answer, parse_mode='HTML')

        # stgs(nn_answer, urls, sender.username, comments, sender.id)


client.start()
client.run_until_disconnected()


