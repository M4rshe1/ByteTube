import os
import pytube


def download(link: str, only_audio, progress, total: int = 1) -> bool:
    error = False
    if "playlist" in link:
        try:
            print(link)
            playlist = pytube.Playlist(link)
            print(f"Downloading: {playlist.title}")
            print(len(playlist.videos))
            progress.total = len(playlist.videos)
            for video in playlist.videos:
                progress["progress"] += 1
                if only_audio == "1":
                    stream = video.streams.get_audio_only()
                    stream.download(os.path.expanduser("~/Downloads/ByteTube"), filename=video.title + ".mp3")
                else:
                    stream = video.streams.get_highest_resolution()
                    stream.download(os.path.expanduser("~/Downloads/ByteTube"))
            progress["progress"] = 0
            progress["total"] = 0
        except Exception as e:
            print(e)
            error = True
    else:
        try:
            progress["total"] = total
            yt = pytube.YouTube(link)
            print(f"Downloading: {yt.title}")
            if only_audio == "1":
                stream = yt.streams.get_audio_only()
                stream.download(os.path.expanduser("~/Downloads/ByteTube"), filename=yt.title + ".mp3")
            else:
                stream = yt.streams.get_highest_resolution()
                stream.download(os.path.expanduser("~/Downloads/ByteTube"))
            progress["progress"] = 0
            progress["total"] = 0
        except Exception as e:
            print(e)
            error = True
    return error


def download_multi(links: list, only_audio, progress):
    progress["total"] = len(links)
    print(links)
    for link in links:
        download(link, only_audio, progress, len(links))
        progress["progress"] += 1
    progress["progress"] = 0
    progress["total"] = 0
