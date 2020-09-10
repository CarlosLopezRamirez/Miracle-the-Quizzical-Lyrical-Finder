import discord
import sys
import requests

client = discord.Client()

@client.event
async def respond_to_initial_mention(message):
    channel = message.channel
    if client.user in message.mentions:
        await channel.send('Music Man, at your service!')

        def check(m):
            return m.author != client.user and m.channel == message.channel
                
        msg = await client.wait_for('message', check=check)

        if client.user in msg.mentions:
            await channel.send('You\'ve already mentioned me! Let\'s start over!')
        else:
            await channel.send('Looking for "' + msg.content + '"')
            await itunes_query(msg.content, msg)


@client.event
async def itunes_query(query, message):
    channel = message.channel
    newQuery = query.lower().replace(" ", "+").strip()
    itunes_request = "https://itunes.apple.com/search?term=" + newQuery + "&limit=200&media=music"
    query_results = requests.get(itunes_request).json()
    await question_user(query_results['results'], message)

@client.event
async def question_user(results, message):
    channel = message.channel
    tracks = []
    track_art = []
    for i in range(0, len(results), 1):
        tracks.append(results[i]['trackName'])
        track_art.append(results[i]['artworkUrl100'])
    for i in range(0,len(results), 1):
        await channel.send(track_art[i])
        await channel.send(tracks[i])

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    else:
        await respond_to_initial_mention(message)

client.run(#YOUR BOT TOKEN HERE)
