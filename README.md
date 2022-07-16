<p><img align="right" alt="gif" src="https://github.com/MonoPhype/Better-Recommended/blob/main/showcase.gif" width="640" height="360"/></p>
             
              
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
How to use:  
Line 6 in scrape.py change tor_cmd to your tor path(tor itself, not the browser) probably at ...tor-browser_en-US/Browser/TorBrowser/Tor/tor
Then you can input youtube/twitch/bitchute channel urls into the channel_input file on different lines. It doesn't matter what the format of a youtube url is. It also doesn't matter if there is text before the youtube.com/twitch.tv/bitchute.com and after the [insert channel here]. E.g. "https://www.twitch.tv/loltyler1/videos?filter=archives&sort=timeLOL" would be the same as "twitch.tv/loltyler". Also not every line in the file has to be a url.
Then run scrape.py and open the html files.
