import os
import pytube


def download(link):
    error = False

    try:
        yt = pytube.YouTube(link)
        print(f"Downloading {yt.title}")
        stream = yt.streams.get_highest_resolution()
        # download to the downloads folder of the current user
        stream.download(os.path.expanduser("~/Downloads/ByteTube"))
    except Exception as e:
        print(e)
        error = True
    return error
