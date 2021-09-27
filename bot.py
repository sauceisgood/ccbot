# VC PLAYER TG

import os
from pytgcalls import GroupCall
import ffmpeg
from config import Config
from datetime import datetime
from pyrogram import filters, Client, idle

VOICE_CHATS = {}
DEFAULT_DOWNLOAD_DIR = 'downloads/vcbot/'

# logging
api_id=Config.API_ID
api_hash=Config.API_HASH
session_name=Config.STRING_SESSION
app = Client(session_name, api_id, api_hash)

# userbot and contacts filter by dashezup's tgvc-userbot
self_or_contact_filter = filters.create(
    lambda
    _,
    __,
    message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)


# start message
@app.on_message(filters.command('start') & self_or_contact_filter)
async def start(client, message):
    await message.reply("**Heya, I'm DogeDrinks Player is online 🎵**")

# ping checker
@app.on_message(filters.command('ping') & self_or_contact_filter)
async def ping(client, message):
    start = datetime.now()
    tauk = await message.reply('Pong!')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await tauk.edit(f'**Pong!**\n> `{m_s} ms`')

# play songs
@app.on_message(filters.command('play') & self_or_contact_filter)
async def play_track(client, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    a = await message.reply('Downloading...')
    ffmpeg.input(audio_original).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k',
    ).overwrite_output().run()
    os.remove(audio_original)
    if VOICE_CHATS and message.chat.id in VOICE_CHATS:
        text = f'▶️ Playing **{audio.title}** at **{message.chat.title}** by DogeDrinks Player...'
    else:
        try:
            group_call = GroupCall(client, input_filename)
            await group_call.start(message.chat.id)
        except RuntimeError:
            await message.reply('Group Call doesnt exist')
            return
        VOICE_CHATS[message.chat.id] = group_call
    await a.edit(f'▶️ Playing **{audio.title}** at **{message.chat.title}** by DOGEDRINKS Player...')


@app.on_message(filters.command('stopvc') & self_or_contact_filter)
async def stop_playing(_, message):
    group_call = VOICE_CHATS[message.chat.id]
    group_call.stop_playout()
    os.remove('downloads/vcbot/input.raw')
    await message.reply('Stopped Playing ❌')


@app.on_message(filters.command('joinvc') & self_or_contact_filter)
async def join_voice_chat(client, message):
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    if message.chat.id in VOICE_CHATS:
        await message.reply('Already joined to Voice Chat 🛠')
        return
    chat_id = message.chat.id
    try:
        group_call = GroupCall(client, input_filename)
        await group_call.start(chat_id)
    except RuntimeError:
        await message.reply('Error ❌')
        return
    VOICE_CHATS[chat_id] = group_call
    await message.reply('Joined the Voice Chat ✅')


@app.on_message(filters.command('leavevc') & self_or_contact_filter)
async def leave_voice_chat(client, message):
    chat_id = message.chat.id
    group_call = VOICE_CHATS[chat_id]
    await group_call.stop()
    VOICE_CHATS.pop(chat_id, None)
    await message.reply('Left Voice Chat ✅')

app.start()
print('>>> DOGEDRINKS PLAYER STARTED <<<')
idle()
app.stop()
print('\n>>> DOGEDRINKS PLAYER STOPPED <<<')
