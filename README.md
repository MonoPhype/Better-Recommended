<p align="center"><img alt="Video Preview" src="./showcase.gif" width="640" height="360"/></p>
             
## How to use:  

Line 6 in scrape.py change tor_cmd to your Tor path(Tor itself, not the browser) probably at ...tor-browser_en-US/Browser/TorBrowser/Tor/tor  
  
Then you can input Youtube/Twitch/Bitchute channel urls into the channel_input file on different lines.  

It doesn't matter what the format of a Youtube url is.  
It also doesn't matter if there is text before the youtube.com/twitch.tv/bitchute.com, and after the [insert channel here].  
E.g. "https://www.twitch.tv/loltyler1/videos?filter=archives&sort=timeLOL" would be the same as "twitch.tv/loltyler".  
Also not every line in the file has to be a url.  

Then run scrape.py and open the html files.
