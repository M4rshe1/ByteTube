import models
import json
import os
import csv


def do(db, convert: str):
    if not os.path.exists(os.path.expanduser("~/Downloads/ByteTube")):
        os.mkdir(os.path.expanduser("~/Downloads/ByteTube"))
    try:
        data = db.query(models.Videos).all()
        converted_data = []
        for video in data:
            converted_data.append({
                "title": video.title,
                "url": video.url,
                "views": video.views,
                "channel": video.channel,
                "channel_url": video.channel_url,
                "upload_date": video.upload_date,
                "duration": video.duration,
                "thumbnail": video.thumbnail,
                "size": video.size,
                "selected": video.selected,
                "downloaded": video.downloaded,
                "failed": video.failed,
            })
        if convert == "csv":
            with open(os.path.expanduser("~/Downloads/ByteTube/export.csv"), "w", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=converted_data[0].keys(), delimiter=";")
                writer.writeheader()
                for data in converted_data:
                    writer.writerow(data)
        elif convert == "json":
            with open(os.path.expanduser("~/Downloads/ByteTube/export.json"), "w") as f:
                json.dump(converted_data, f, indent=4)
        elif convert == "txt":
            with open(os.path.expanduser("~/Downloads/ByteTube/export.txt"), "w", encoding="utf-8") as f:
                for data in converted_data:
                    f.write(f"{data['title']}\n{data['url']}\n{data['views']}\n{data['channel']}\n{data['channel_url']}\n{data['upload_date']}\n{data['duration']}\n{data['thumbnail']}\n{data['size']}\n{data['selected']}\n{data['downloaded']}\n{data['failed']}\n\n")
        return True
    except Exception as e:
        print(e)
        return False
