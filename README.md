<p align="center"><img alt="Video Preview" src="./showcase.gif" width="640" height="360"/></p>
             
## How to use  

On line 7 in scrape.py change tor_cmd to your Tor path(Tor itself, not the browser) probably at ...tor-browser_en-US/Browser/TorBrowser/Tor/tor  
  
Then you can input Youtube/Twitch/Bitchute channel urls into the channel_input file on different lines.  

It doesn't matter what the format of a Youtube url is.  
It also doesn't matter if there's text before the domain or after the channel name/index.  
E.g. "https://www.twitch.tv/loltyler1/videos?filter=archives&sort=timeLOL" would be the same as "twitch.tv/loltyler1".  
Not every line in the file has to be a url.  

Open the HTML files after running scrape.py  
  
Tor browser must be closed before running the script.  
If a problem occurs, quitting Tor(with the system monitor) would probably fix it.
