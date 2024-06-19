import logging
from flask import Flask, request, jsonify
from plexapi.server import PlexServer
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.easymp4 import EasyMP4
import requests
import time
import yaml
import json
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

PLEX_URL = config.get('plex', {}).get('baseurl', '')
PLEX_TOKEN = config.get('plex', {}).get('token', '')
LISTENBRAINZ_URL = 'https://api.listenbrainz.org/1/submit-listens'
LISTENBRAINZ_TOKEN = config.get('listenbrainz', {}).get('token', '')
TARGET_USERNAME = config.get('user', {}).get('target_username', '')
LIBRARY_SECTION_IDS = config.get('user', {}).get('library_section_ids', [])

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

def get_file_metadata(file_path):
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=EasyID3)
        elif file_path.endswith('.flac'):
            audio = FLAC(file_path)
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
        elif file_path.endswith('.m4a') or file_path.endswith('.aac'):
            audio = EasyMP4(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return None

        tags = ['artist', 'title', 'album', 'musicbrainz_trackid', 'musicbrainz_releasegroupid', 'musicbrainz_albumid', 'musicbrainz_releasetrackid', 'isrc', 'discnumber', 'albumartist', 'date', 'tracktotal', 'disctotal']
        metadata = {tag: audio.get(tag, [None])[0] for tag in tags}
        metadata['duration'] = int(audio.info.length)
        metadata['work_mbids'] = audio.get('musicbrainz_workid', [])
        metadata['artist_mbids'] = audio.get('musicbrainz_artistid', [])
        
        return metadata
    except Exception as e:
        logger.error(f"Failed to read metadata from {file_path}: {e}")
        return None

def build_listen_payload(playback, metadata, listen_type="single"):
    additional_info = { 
        'duration_ms': metadata.get('duration', 0) * 1000,
        'recording_mbid': metadata.get('musicbrainz_trackid'),
        'release_group_mbid': metadata.get('musicbrainz_releasegroupid'),
        'release_mbid': metadata.get('musicbrainz_albumid'),
        'track_mbid': metadata.get('musicbrainz_releasetrackid'),
        'work_mbids': metadata.get('work_mbids', []),
        'artist_mbids': metadata.get('artist_mbids', []),
        'isrc': metadata.get('isrc'),
        'media_player': "Plex",
        'submission_client': "Plex to ListenBrainz with Webhooks",
        'submission_client_version': "1.0.0",
        'tracknumber': playback.index,
        'discnumber': int(metadata['discnumber']) if metadata.get('discnumber') is not None else None,
        'albumartist': metadata.get('albumartist'),
        'date': metadata.get('date'),
        'totaltracks': int(metadata['tracktotal']) if metadata.get('tracktotal') is not None else None,
        'totaldiscs': int(metadata['disctotal']) if metadata.get('disctotal') is not None else None
    }

    # Remove keys with None values
    additional_info = {k: v for k, v in additional_info.items() if v is not None}

    track_metadata = {
        "artist_name": metadata['artist'],
        "track_name": metadata['title'],
        "release_name": metadata.get('album'),
        "additional_info": additional_info
    }

    payload = {
        "listen_type": listen_type,
        "payload": [{
            "track_metadata": track_metadata
        }]
    }

    if listen_type == "single":
        payload["payload"][0]["listened_at"] = int(time.time())

    return payload

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.form.to_dict(flat=False)
        json_data = json.loads(data['payload'][0])
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Invalid payload: {e}")
        return jsonify({"status": "failed", "reason": f"Invalid payload: {e}"}), 400

    logger.info(f"Webhook received from {json_data['Account']['title']}")

    if json_data['Account']['title'] != TARGET_USERNAME:
        logger.info("Ignored: Not target user")
        return jsonify({"status": "ignored", "reason": "not target user"}), 200

    if LIBRARY_SECTION_IDS and json_data['Metadata']['librarySectionID'] not in LIBRARY_SECTION_IDS:
        logger.info("Ignored: Not target library section")
        return jsonify({"status": "ignored", "reason": "not target library section"}), 200

    if json_data['Metadata']['type'] != 'track':
        logger.info("Ignored: Not a track")
        return jsonify({"status": "ignored", "reason": "not a track"}), 200

    track_key = json_data['Metadata']['key']
    event = json_data['event']

    logger.info(f"Event: {event}")

    try:
        track = plex.fetchItem(track_key)
    except Exception as e:
        logger.error(f"Failed to fetch item from Plex: {e}")
        return jsonify({"status": "failed", "reason": f"Failed to fetch item from Plex: {e}"}), 500

    media_file = track.media[0].parts[0].file

    metadata = get_file_metadata(media_file)
    if not metadata:
        return jsonify({"status": "failed", "reason": "metadata extraction failed"}), 500

    if event == 'media.play':
        listen_payload = build_listen_payload(track, metadata, listen_type="playing_now")
    elif event == 'media.scrobble':
        listen_payload = build_listen_payload(track, metadata, listen_type="single")
    else:
        logger.info("Ignored: Unsupported event")
        return jsonify({"status": "ignored", "reason": "unsupported event"}), 200

    logger.info(f"Prepared listen payload: {listen_payload}")

    auth_header = {"Authorization": f"Token {LISTENBRAINZ_TOKEN}"}
    response = requests.post(LISTENBRAINZ_URL, json=listen_payload, headers=auth_header)

    if response.status_code == 200:
        logger.info(f"Submission successful: {response.json()}")
        return jsonify({"status": "success"}), 200
    else:
        logger.error(f"Submission failed: {response.text}")
        return jsonify({"status": "failed", "reason": "submission failed"}), 500

if __name__ == '__main__':
    app.run(port=5000)
