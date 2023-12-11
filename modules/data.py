import pytube


def get_video_data(link: str):
    if "playlist" in link:
        data = get_playlist_videos(link)
        if data:
            return data
    else:
        data = video_data(link)
        if data:
            return [data]


def get_playlist_videos(link: str):
    try:
        playlist = pytube.Playlist(link)
        tmp_data = [video_data(video.watch_url) for video in playlist.videos]
        return tmp_data
    except Exception as e:
        print(e)
        return [{
            "title": "Error",
            "description": "Error",
            "url": "Error",
            "views": "Error",
            "channel": "Error",
            "channel_url": "Error",
            "upload_date": "Error",
            "duration": "Error",
            "thumbnail": "Error",
            "size": "Error",
            "selected": False,
            "downloaded": False,
        }]


def video_data(link: str):
    try:
        yt = pytube.YouTube(link)

        return {
            "title": yt.title,
            "description": yt.description,
            "url": yt.watch_url,
            "views": yt.views,
            "channel": yt.author,
            "channel_url": yt.channel_url,
            "upload_date": yt.publish_date,
            "duration": yt.length,
            "thumbnail": yt.thumbnail_url,
            "size": yt.length,
            "selected": False,
            "downloaded": False,
        }
    except Exception as e:
        print(e)
        return {
            "title": "Error",
            "description": "Error",
            "url": "Error",
            "views": "Error",
            "channel": "Error",
            "channel_url": "Error",
            "upload_date": "Error",
            "duration": "Error",
            "thumbnail": "Error",
            "size": "Error",
            "selected": False,
            "downloaded": False,
        }
