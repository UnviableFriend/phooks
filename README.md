# phooks
Local Plex to ListenBrainz python script using web hooks and file lookups.

This was created by ChatGPT 4o. I will not and can not support this. Take it, use it, share it, claim it as your own.


## Potential ListenBrainz options with Plex:
* Have Plex [add native support](https://forums.plex.tv/t/feature-request-support-listenbrainz-replacement-for-last-fm/226426)
  * [According to the developer of Eavesdrop.fm](https://forums.plex.tv/t/eavesdrop-fm-sync-plex-music-listens-to-listenbrainz/580467/5) "ListenBrainz support has been discussed internally with the Plex team, and isn’t something they’re able to implement at this time." -*June 16th, 2020*
* Submit to [Last.fm](https://www.last.fm/) and [import your history into ListenBrainz](https://listenbrainz.org/settings/import/)
  * While this works, it lacks detailed information, as last.fm itself does not support much [information](https://www.last.fm/api/show/track.scrobble)(And I have no idea what of the optional items Plex actually sends)
* Use [eavesdrop.fm](https://eavesdrop.fm/).
  * This has a limitation in what it can send as Plex [Webhooks](https://support.plex.tv/articles/115002267687-webhooks/) do not contain much information about the media
* Use [Web Scrobbler](https://web-scrobbler.com/)
  * As far as I know this would submit very limited information such as Artist, Album, Title. But have not tested.
* ~~Have Tautulli submit them. This request was deemed out of scope by the author of Tautulli.~~
  * ~~It already runs on users Plex servers monitoring and tracking playback. This seems like an ideal way to handle it short of native support in Plex.~~

## Limitations
This script uses [Plex webhooks](https://support.plex.tv/articles/115002267687-webhooks/) so it is limited by them.
* Listen Submission percent is limited. The Plex docs state "`media.scrobble` – Media is viewed (played past the 90% mark).", however in my experience testing this script the webhook happens at 50%, and I see no way to configure that.
* Looping tracks. While `media.scrobble` will happen if you have a song on repeat, `media.play` only seems to happen the first play. So your "Now Playing" on ListenBrainz may stop showing you are actively listening to something

## How to use
**THIS SCRIPT NEEDS TO RUN ON THE SAME SYSTEM AS YOUR PLEX SERVER**. The way it works is the webhook contains a Plex ID for the track you are listening to, it then takes that ID and looks it up with the [PlexAPI](https://github.com/pkkid/python-plexapi) to get the location of the file, which it then reads the tags from. If the file paths do not match for what this script sees, *it will not work*.
* Install dependencies `pip install flask plexapi mutagen requests PyYAML`
* Edit `config.yaml`
  *  `baseurl: "http://127.0.0.1:32400"` Unless you have some strange setup this is pretty much the only option
  *  `token: "your-plex-token"` Put your [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) here. Required to use PlexAPI to find the file.
  *  `token: "your-listenbrainz-token"` Put your [ListenBrainz Token](https://listenbrainz.readthedocs.io/en/latest/users/api/index.html#get-the-user-token) here. Required to submit listens.
  *  `target_username: "specific-plex-username"` Put your Plex username here. Required to filter out other users on your server as webhooks happen for *all* users on your server.
  *  `library_section_ids: [1224]` Put the library ID here(click ... menu in plex web for a song, Get Info, view XML, find `librarySectionID`. This is used to filter out other audio libraries, such as audiobooks.
* `python phooks.py` Run the script

**BIG NOTE** If you want to use this, you will likely want to run it as a service so it starts with your server and is always running. I can not help you here. Ask Google/ChatGPT/your IT friend how to do that for your particular Operating System/Environment. 
