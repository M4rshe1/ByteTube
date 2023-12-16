import os
import pytube


def download(link: str, only_audio, progress, total: int = 1):
    if not os.path.exists(os.path.expanduser("~/Downloads/ByteTube")):
        os.mkdir(os.path.expanduser("~/Downloads/ByteTube"))
    if "playlist" in link:
        try:
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
    else:
        try:
            progress["total"] = total
            yt = pytube.YouTube(link)
            print(f"Downloading: {yt.title}")
            if only_audio == "1":
                stream = yt.streams.get_audio_only()
                stream.download(os.path.expanduser("~/Downloads/ByteTube"), 
                                filename=yt.title.replace("/", "").replace("\\", "") + ".mp3")
            else:
                stream = yt.streams.get_highest_resolution()
                stream.download(os.path.expanduser("~/Downloads/ByteTube"))
            if total == 1:
                progress["total"] = 0
            progress["total"] = 0
        except Exception as e:
            print(e)


def download_multi(links: list, only_audio, progress):
    total = len(links)
    progress["total"] = total
    print(links)
    for link in links:
        print(link)
        download(link, only_audio, progress, total)
        progress["progress"] += 1
    progress["progress"] = 0
    progress["total"] = 0
