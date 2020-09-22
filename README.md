# Miracle the Quizzical Lyrical Finder 

![Miracle's Picture](/images/MiraclePicture.png)

Miracle is a bot created using [Discord.py](https://discordpy.readthedocs.io/en/latest/), an API wrapper for Discord! Summoning Miracle will cause him to prompt you to give him something to look up, which is done by simply sending another message in the channel where you initially summoned Miracle.

![Miracle Summoned](/images/MiracleSummoned.png)

Your message can be anything, from a random word, a genre, or an artist that you would like to look up. Miracle will take this key word and find the top 200 results on the iTunes store associated to your word by using the [iTunes Search API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/). Miracle will store the top 200 results in the background and prompt you with each result 1-by-1, asking if the sent result is the song you would like to proceed with. You can respond "Yes" to continue to the next step, or "No" to be prompted with the next result from the list of 200.   

![Miracle Prompting With iTunes Result](/images/iTunesPrompt.png)

If you say "Yes" to any of the results, Miracle will then proceed to search for the top music video result when looking up your chosen song using the [IMVDb API](https://imvdb.com/developers/api). Note that not every song has a music video made for it. Miracle will send you the top result that appears when looking up your chosen song. If a music video has been made for your chosen song, then Miracle will likely send you the link to this music video. However, if no music video was ever made for your chosen song, you will likely be given a music video from the same artist of the song you chose. 

![Music Video Results](/images/MiracleMusicVideo.png)

After having sent the top IMVDb result, Miracle will use the [Genius API](https://docs.genius.com/) to look up your chosen song on their website. The Genius API will return a large amount of information pertaining to your song, but what matters to Miracle is the URL path to the Genius page for the song you chose. Using the URL path from the results, Miracle will get the page, and using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), it will parse through the page's HTML code and find the tag named "Lyrics," a common tag that Genius uses on all its pages to denote where in the HTML the lyrical content for the song is. Miracle will then send you over the Discord channel the content found within the "Lyrics" tag. 

![Miracle Presents Some Lyrics](/images/MiracleLyrics.png)

After this, Miracle will send you over the Discord channel an interesting part of the song that we often don't think about: how many times the artist actually says each word in the song, as seen below

![Miracle Present Lyric Occurences](/images/LyricOccurences.png)


## How to set up Miracle
This bot has not yet been released publicly to put into every server. However, in this section, I will explain how to set up Miracle on your computer so you can use him in his current state!

### Packages Needed
***Discord.py***  
`python3 -m pip install -U discord.py`

***Requests***
`python3 -m pip install requests`

***Beautiful Soup***
`python3 -m pip install beautifulsoup4`

### Environment Variables and API Tokens  
To have a Discord bot and use the Genius API, you will need to register your bot and sign up at Genius. Below is a detailed explanation for how to do both  

***Discord***  
Head over to the [Discord Developer Page](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and log in using your Discrod account (or create an account if you do not have one yet). You will find yourself in the Applications portal. In the top right click on the button that says "New Application" 

![ApplicationPortal](/images/ApplicationPortal.png)

Name your application whatever you want. I, of course, named this application "Miracle the Quizzical Lyrical Finder." Once in, you will be in your Application's page. On the menu on the side, click on the tab that says "Bot"

![Discord App Menu](/images/DiscordMenu.png)

Click on the button that says "Add Bot," and give it a name. My bot's name was "Miracle." At the bottom, you will find what permissions your bot will have. 

![Bot Permissions](/images/botpermissions.png)

These are all options for what your bot can do. I simply clicked "Administrator." Second, if you go to your Application's "General Information" you will see a blue text that says "Click to Reveal." This is the client token needed to run your bot. Reveal it, copy it, and do not post it anywhere, this is meant to be a secret token. 

![Secret Token](/images/secrettoken.png)

Head over to the "OAuth2" tab, and at the bottom, under "Scopes", click "bot." "Bot Permissions" will appear underneath, click on "Administrator." When you have done this, click "Copy" next to the link that appeared in the "Scopes" section.

![Bot Scopes](/images/botscopes.png)

Open a new tab in your browser and paste the link you copied. Discord will prompt you to add your bot to whatever server you want to add this bot to.

![Server Prompt](/images/serverprompt.png)

Select whatever server you want and you are done with this section!

***Discord Environment Variable***  
Like said before, the secret token should be kept to yourself and never posted. It is for this reason that in the code, we import `os` and use it to access our system's environment variables. To be able to do this, we must set the Discord secret client we were given in an earlier step. To do this, navigate to your `.bash_profile` or `.bashrc` file in your home directory and open it. At the very bottom, add the following line:  

`export DISCORD_TOKEN=YOUR_ID_THAT_YOU_COPIED_FROM_BEFORE`

Now, when running the bot, it will work as it is using the correct secret client ID. 

***Genius API***  
The process for using Genius's API is similar to that of Discord's. Navigate to the [Genius API Website](https://docs.genius.com/). From there, click the tab that says "Manage Clients" on the side.

![Genius API Menu](/images/GeniusMenu.png)

Genius will ask you to register, and then create an Application with a name and website URL. The URL does not have to be anything specific, I used this GitHub link, but it can be anything. For the App name, I put MiracleLyrical. Once you are done registering your App, you will need to access your authorization token. On the "API Clients" page, at the bottom, you will see a blue text that says "Generate Access Token." Click on this and copy it.

![Client Access Token](/images/geniusaccess.png)

***Genius Environment Variable***
Again, we will need to make an environment variable. Again, navigate to either your `bash_profile` or `.bashrc` file, and at the bottom, add:  

`export GENIUS_TOKEN=ACCESS_TOKEN_THAT_YOU_COPIED`

## You're done!

You have finished setting up Miracle the Quizzical Lyrical Finder! Simply run the attached Python file and Miracle will be up and ready to help in whatever server you sent him to!