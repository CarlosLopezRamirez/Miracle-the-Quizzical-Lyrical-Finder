# Miracle the Quizzical Lyrical Finder 

![Miracle's Picture](/images/MiraclePicture.png)

Miracle is a bot created using [Discord.py](https://discordpy.readthedocs.io/en/latest/), an API wrapper for Discord! Summoning Miracle will cause him to prompt you to give him something to look up, which is done by simply sending another message in the channel where you initially summoned Miracle.

![Miracle Summoned](/images/MiracleSummoned.png)

Your message can be anything, from a random word, a genre, or an artist that you would like to look up. Miracle will take this key word and find the top 200 results on the iTunes store associated to your word by using the [iTunes Search API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/). Miracle will store the top 200 results in the background and prompt you with each result 1-by-1, asking if the sent result is the song you would like to proceed with. You can respond "Yes" to continue to the next step, or "No" to be prompted with the next result from the list of 200.   

![Miracle Prompting With iTunes Result](/images/iTunesPrompt.png)

If you say "Yes" to any of the results, Miracle will then proceed to search for the top music video result when looking up your chosen song using the [IMVDb API](https://imvdb.com/developers/api). Note that not every song has a music video made for it. Miracle will send you the top result that appears when looking up your chosen song. If a music video has been made for your chosen song, then Miracle will likely send you the link to this music video. However, if no music video was ever made for your chosen song, you will likely be given a music video from the same artist of the song you chose. 

![Music Video Results](/images/MiracleMusicVideo.png)
