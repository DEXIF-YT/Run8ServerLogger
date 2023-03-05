import discord
import time

# Replace with your own values (Channel ID does not require quotes)
# IMPORTANT: NEVER SHARE YOUR BOT TOKEN WITH ANYONE!
TOKEN = 'bot-token-here'
CHANNEL_ID = 1234567890
FILE_LOCATION = 'C:/Run8Studios/Run8 Train Simulator V3/Run8.log'

intents = discord.Intents.default()

client = discord.Client(intents=intents)

# Add your triggers here
# This set is designed to work for a server host's Run8.log file
# Singleplayer has a completely different string-set and should really only be used for testing purposes
triggers = [{'emoji': ':vertical_traffic_light:', 'string': 'AIDS Toggled by'},
            {'emoji': ':face_with_symbols_over_mouth:', 'string': 'Train has an integrity problem'},
            {'emoji': ':fuelpump:', 'string': 'LocoFailure Message Sent'},
            {'emoji': ':lock:', 'string': 'This guy tried to join with a Bad Password'},
            {'emoji': ':no_entry_sign:', 'string': 'kicked and added to the Banned List'},
            {'emoji': ':white_check_mark:', 'string': 'Current Player List'},
            {'emoji': ':white_check_mark:', 'string': 'ClientID'},
            {'emoji': ':octagonal_sign:', 'string': 'an MOW Flag or Object'},
            {'emoji': ':construction_worker:', 'string': 'has spawned a random AI train'},
            {'emoji': ':hash:', 'string': 'used DTMF'},
            {'emoji': ':no_bicycles:', 'string': 'has just deleted a train'},
            {'emoji': ':steam_locomotive:', 'string': 'has attempted to spawn a train into the world'},
            {'emoji': ':wave:', 'string': 'has exited the session'},
            {'emoji': ':ballot_box_with_check:', 'string': 'has joined the session'},
            {'emoji': ':ballot_box_with_check:', 'string': 'Name:'}]

# Function to read last line from log file
def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(5)
            continue
        yield line

# Function to send message to Discord channel
async def send_message(message):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)

# Function to run the bot
async def run_bot():
    with open(FILE_LOCATION, 'r') as f:
        loglines = tail(f)
        for line in loglines:
            for trigger in triggers:
                if trigger['string'] in line:
                    emoji_line = f"{trigger['emoji']} {line}"
                    if emoji_line != run_bot.last_message:
                        await send_message(emoji_line)
                        run_bot.last_message = emoji_line
                    break
            else:
                # Add the :speech_balloon: emoji before any line that doesn't contain the specified strings
                if not line.startswith(':') and 'Track 210' not in line and 'Track 10' not in line and 'EOT Not Added' not in line and 'New EOT' not in line:
                    speech_balloon_line = f":speech_balloon: {line}"
                    if speech_balloon_line != run_bot.last_message:
                        await send_message(speech_balloon_line)
                        run_bot.last_message = speech_balloon_line
                        break

# Initialize last message variable to empty string
run_bot.last_message = ''

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await send_message('`Run8 Server Logger has successfully connected to this channel`')
    await run_bot()

client.run(TOKEN)