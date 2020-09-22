import discord
import sys
import requests
import urllib.parse
import re
import os
from bs4 import BeautifulSoup as bs

miracle_mentioned = False

client = discord.Client()

# Environment Variables
discord_token = os.environ.get('DISCORD_TOKEN')
genius_headers = {'Authorization': 'BEARER ' + str(os.environ.get('GENIUS_TOKEN'))}

# Checks if Miracle is mentioned, and proceeds accordingly if so
@client.event
async def respond_to_initial_mention(message):

    global miracle_mentioned

    channel = message.channel
    
    if client.user in message.mentions and miracle_mentioned == False:

        miracle_mentioned = True 

        await channel.send('Music Man, at your service!')

        def check(m):
            return m.author != client.user and m.channel == message.channel
                
        msg = await client.wait_for('message', check=check)

        if client.user in msg.mentions:
            await channel.send('You\'ve already mentioned me! Let\'s start over!')
            miracle_mentioned = False
        else:
            await channel.send('Looking for "' + msg.content + '"')
            await itunes_query(msg.content, msg)

# Uses the ITunes Search API to find top 200 results that correspond
# to the message sent by the user
@client.event
async def itunes_query(query, message):

    newQuery = query.lower().replace(' ', '+').strip()
    itunes_request = 'https://itunes.apple.com/search?term=' + newQuery + '&limit=200&media=music'
    query_results = requests.get(itunes_request).json()

    await question_user(query_results['results'], message)

# Cycles through the top 200 results 1-by-1, sending them to the user
# and asking if that item is the item the user would like to proceed with
@client.event
async def question_user(results, message):

    global miracle_mentioned

    channel = message.channel
    tracks, track_art, artists = [], [], []

    for i in range(0, len(results), 1):
        tracks.append(results[i]['trackName'])
        track_art.append(results[i]['artworkUrl100'])
        artists.append(results[i]['artistName'])
    for i in range(0,len(results), 1):

        if i == (len(results) - 1):
            await channel.send('This is the last result!')

        await channel.send(track_art[i])
        await channel.send(tracks[i] + ' by ' + artists[i])
        await channel.send('Is that what you\'re looking for?')

        def check(m):
            return m.author != client.user and m.channel

        msg = await client.wait_for('message', check=check)

        if msg.content.lower() == 'yes':
            await channel.send('You\'ve chosen ' + tracks[i] + ' by ' + artists[i])
            await music_vid(tracks[i], artists[i], message)
            miracle_mentioned = False
            break
        elif msg.content.lower() == 'no':
            await channel.send('Moving on!')
            continue
        else:
            await channel.send('Not a valid input! I\'ll be leaving now!')
            miracle_mentioned = False
            break

# After the user has chosen which song they would like to proceed with,
# Miracle finds the top music video that corresponds to querying that song
# with the IMVdb API
@client.event
async def music_vid(trackName, artistName, message):

    global miracle_mentioned

    channel = message.channel

    track_request_string = trackName.replace(" ","+")
    artist_request_string = artistName.replace(" ", "+") + "+"
    imvdb_request = 'http://imvdb.com/api/v1/search/videos?q=' + artist_request_string + track_request_string
    imvdb_results = requests.get(imvdb_request).json()

    top_result_url = imvdb_results['results'][0]['url']

    await channel.send('This is the top result I get when I search ' + trackName + ' by ' + artistName + ' on IMVDb' )
    await channel.send(top_result_url)
    await lyrics(trackName, artistName, message)
    miracle_mentioned = False

# Using the song chosen in question_user(), Miracle uses the Genius API to find the 
# url path to Genius's webpage for said song. Once the url path is found, Miracle 
# scrapes the HTML lyrics tag for the content of the lyrics and sends them to the user
@client.event
async def lyrics(trackName, artistName, message):

    global miracle_mentioned
    global genius_headers

    channel = message.channel

    base_url = "https://api.genius.com"
    search_url = base_url + "/search"

    trackName = re.sub(r"[\(\[].*?[\)\]]", "", trackName).strip()
    genius_params = {'q': trackName}

    results = requests.get(search_url, params=genius_params, headers=genius_headers)
    json = results.json()

    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artistName:
            song_info = hit
            break

    if song_info:
        # Genius API
        api_path = song_info["result"]["api_path"]
        song_url = base_url + api_path
        results2 = requests.get(song_url, headers=genius_headers)
        json2 = results2.json()
        song_path = json2["response"]["song"]["path"]

        # Genius Webscrap
        lyrics_page = requests.get("http://genius.com" + song_path)
        html = bs(lyrics_page.text, "html.parser")
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics", recursive=True).get_text()

        # Discord Side
        for i in range(0, len(lyrics), 2000):
            message_to_send = lyrics[i:min(len(lyrics), i + 2000)]
            await channel.send(message_to_send)
        
        lyrics = re.sub(r"[\(\[].*?[\)\]]", "", lyrics)

        lyrics_list = lyrics.replace('?', ' ')\
        .replace('!', ' ')\
        .replace('.', ' ')\
        .replace(',', ' ')\
        .replace('\\', '')\
        .replace('-', ' ')\
        .replace('—', ' ')\
        .replace('"', ' ')\
        .lower().split()

        miracle_mentioned = False
        await lyrical_makeup(lyrics_list, message)

# Miracle then analyzes the lyrical makeup of the song
@client.event
async def lyrical_makeup(lyrics_list, message):

    channel = message.channel
    lyric_dict = {}

    for lyric in lyrics_list:
        if lyric in lyric_dict:
            lyric_dict[lyric] = lyric_dict[lyric] + 1
        else:
            lyric_dict[lyric] = 1

    sort_lyrics = sorted(lyric_dict.items(), key=lambda x: x[1], reverse=True)

    await channel.send("The following is how many times each lyric in the song appears:")

    for lyric_tuple in sort_lyrics:
        await channel.send("Lyric: " + lyric_tuple[0] + "\tOccurences: " + str(lyric_tuple[1]))

# Whenever a message is sent
@client.event
async def on_message(message):

    if message.author == client.user:
        return
    else:
        await respond_to_initial_mention(message)

# Runs Miracle
client.run(discord_token)