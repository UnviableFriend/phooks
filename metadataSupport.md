# Supported Fields Comparison
These are the fields supported by various players/submission tools from my testing in January 2024, they may have changed since.

| Field                                                | This script | eavesdropfm | foobar2000 | jellyfin | lastfm | musicbee | navidrome | panoscrobbler | spotify |
|------------------------------------------------------|-------------|-------------|------------|----------|--------|----------|-----------|---------------|---------|
| track_metadata.artist_name                           | ✔           | ✔          | ✔         | ✔       | ✔     | ✔       | ✔        | ✔            | ✔      |
| track_metadata.track_name                            | ✔           | ✔          | ✔         | ✔       | ✔     | ✔       | ✔        | ✔            | ✔      |
| track_metadata.release_name                          | ✔           | ✔          | ✔         | ✔       | ✔     | ✔       | ✔        | ✔            | ✔      |
| track_metadata.additional_info.submission_client     | ✔           |             | ✔         | ✔       | ✔     | ✔       | ✔        | ✔            | ✔      |
| track_metadata.additional_info.duration_ms           | ✔           |             | ✔         | ✔       |        | ✔       | ✔        | ✔            | ✔      |
| track_metadata.additional_info.submission_client_version | ✔      |             | ✔         | ✔       |        |          | ✔        | ✔            |         |
| track_metadata.additional_info.release_mbid          | ✔           |             | ✔         | ✔       |        | ✔       | ✔        |               |         |
| track_metadata.additional_info.artist_mbids          | ✔           |             | ✔         | ✔       |        | ✔       | ✔        |               |         |
| track_metadata.additional_info.recording_mbid        | ✔           |             | ✔         | ✔       |        | ✔       | ✔        |               |         |
| track_metadata.additional_info.tracknumber           | ✔           |             | ✔         | ✔       |        |          | ✔        |               | ✔      |
| track_metadata.additional_info.media_player          | ✔           |             | ✔         | ✔       |        | ✔       |           |               |         |
| track_metadata.additional_info.release_group_mbid    | ✔           |             | ✔         | ✔       |        | ✔       |           |               |         |
| track_metadata.additional_info.isrc                  | ✔           |             | ✔         | ✔       |        |          |           |               | ✔      |
| track_metadata.additional_info.track_mbid            | ✔           |             | ✔         | ✔       |        |          |           |               |         |
| track_metadata.additional_info.discnumber            | ✔           |             | ✔         |          |        |          |           |               | ✔      |
| track_metadata.additional_info.listening_from        |             | ✔          |            |          |        |          |           |               |         |
| track_metadata.additional_info.work_mbids            | ✔           |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.albumartist           | ✔           |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.date                  | ✔           |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.media_player_version  |             |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.totaltracks           | ✔           |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.totaldiscs            | ✔           |             | ✔         |          |        |          |           |               |         |
| track_metadata.additional_info.tags                  |             |             |            | ✔       |        |          |           |               |         |
| track_metadata.additional_info.lastfm_track_mbid     |             |             |            |          | ✔     |          |           |               |         |
| track_metadata.additional_info.lastfm_artist_mbid    |             |             |            |          | ✔     |          |           |               |         |
| track_metadata.additional_info.trackNumber           |             |             |            |          |        | ✔       |           |               |         |
| track_metadata.additional_info.release_artist_name   |             |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.spotify_album_id      |             |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.release_artist_names  |             |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.artist_names          |             |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.spotify_artist_ids    |             |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.spotify_album_artist_ids |        |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.music_service         |            |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.origin_url            |            |             |            |          |        |          |           |               | ✔      |
| track_metadata.additional_info.spotify_id            |             |             |            |          |        |          |           |               | ✔      |
