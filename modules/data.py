import pytube


def get_video_data(link: str):
    print(link)
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
        print(playlist.title)
        tmp_data = [video_data(video.watch_url) for video in playlist.videos]
        return tmp_data
    except Exception as e:
        print(e)
        return [{
            "title": "Error",
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
            "failed": False,
        }]


def video_data(link: str):
    try:
        yt = pytube.YouTube(link)
        print(yt.title)

        calc_duration = int(yt.length)

        hours = calc_duration // 3600
        calc_duration %= 3600
        minutes = calc_duration // 60
        seconds = calc_duration % 60

        if seconds < 10:
            seconds = f"0{seconds}"
        if minutes < 10:
            minutes = f"0{minutes}"
        if hours < 10:
            hours = f"0{hours}"

        if hours == "00":
            duration = f"{minutes}:{seconds}"
        else:
            duration = f"{hours}:{minutes}:{seconds}"

        return {
            "title": yt.title,
            "url": yt.watch_url,
            "views": yt.views,
            "channel": yt.author,
            "channel_url": yt.channel_url,
            "upload_date": yt.publish_date,
            "duration": duration,
            "thumbnail": yt.thumbnail_url,
            "size": yt.length,
            "selected": True,
            "downloaded": False,
            "failed": False,
        }
    except Exception as e:
        print(e)
        return {
            "title": "Error",
            "url": "Error",
            "views": "Error",
            "channel": "Error",
            "channel_url": "Error",
            "upload_date": "Error",
            "duration": 0,
            "thumbnail": "Error",
            "size": "Error",
            "selected": False,
            "downloaded": False,
            "failed": False,
        }
