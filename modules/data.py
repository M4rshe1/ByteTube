import pytube
import models


def get_video_data(link: str, progress: dict, db):
    progress["progress"] = 0
    if "playlist" in link:
        data = get_playlist_videos(link, progress, db)
        if data:
            progress["progress"] = 0
            progress["total"] = 0
        return data
    else:
        progress["total"] = 1
        data = video_data(link, db)
        progress["progress"] = 0
        progress["total"] = 0
        return data


def get_playlist_videos(link: str, progress: dict, db):
    try:
        playlist = pytube.Playlist(link)
        progress["total"] = len(playlist.videos)
        for video in playlist.videos:
            video_data(video.watch_url, db)
            progress["progress"] += 1
        return {"status": 200}
    except Exception as e:
        print(e)
        return {"status": "error"}


def video_data(link: str, db):
    database_links = [video.url for video in db.query(models.Videos).all()]
    # print(database_links)
    tmp_link = str(link).split("&")[0].replace("www.", "")
    if tmp_link not in database_links:
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

            views = str(yt.views)
            views = views[::-1]
            views = [views[i:i+3] for i in range(0, len(views), 3)]
            views = "'".join(views)
            views = views[::-1]

            video = {
                "title": yt.title,
                "url": yt.watch_url,
                "views": views,
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

            db_video = models.Videos(**video)
            db.add(db_video)
            db.commit()
            return {"status": 200}
        except Exception as e:
            print(e)
            return []
