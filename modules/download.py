import os
import pytube


def download(link: str, onlyaudio) -> bool:
    error = False
    if "playlist" in link:
        try:
            playlist = pytube.Playlist(link)
            print(f"Downloading: {playlist.title}")
            for video in playlist.videos:
                if onlyaudio == "1":
                    stream = video.streams.get_audio_only()
                else:
                    stream = video.streams.get_highest_resolution()
                # download to the downloads folder of the current user
                stream.download(os.path.expanduser("~/Downloads/ByteTube"))
        except Exception as e:
            print(e)
            error = True
        return error
    else:
        try:
            yt = pytube.YouTube(link)
            print(f"Downloading: {yt.title}")
            if onlyaudio == "1":
                stream = yt.streams.get_audio_only()
            else:
                stream = yt.streams.get_highest_resolution()
            # download to the downloads folder of the current user
            stream.download(os.path.expanduser("~/Downloads/ByteTube"))
        except Exception as e:
            print(e)
            error = True
        return error

