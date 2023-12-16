import json
import csv
import models


def do_import(db, file, delete_before_import=False):
    """
    :param delete_before_import: If all videos should be deleted before importing
    :param db: SQLAlchemy session
    :param file: File to import
    :return: If import was successful
    """
    # read the file

    file_extension = file.filename.split(".")[-1]
    # print(file_extension)

    if delete_before_import:
        db.query(models.Videos).delete()
        db.commit()

    if file_extension == "json":
        data = json.loads(file.file.read())
        for video in data:
            db.add(models.Videos(
                url=video.get("url"),
                selected=video.get("selected"),
                downloaded=video.get("downloaded"),
                title=video.get("title"),
                thumbnail=video.get("thumbnail"),
                channel_url=video.get("channel_url"),
                duration=video.get("duration"),
                channel=video.get("channel"),
                views=video.get("views"),
                upload_date=video.get("upload_date"),
                size=video.get("size")
            ))
        db.commit()
        return True
    elif file_extension == "csv":
        data = csv.reader(file.file.read().decode("utf-8").split("\n"), delimiter=";")
        return read_txt_files(db, data)
    elif file_extension == "txt":
        data = file.file.read().decode("utf-8").split("\r\n\r\n")
        new_data = []
        for video in data:
            new_data.append(video.split("\r\n"))
        return read_txt_files(db, new_data)


def to_bool(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return value


def read_txt_files(db, data):
    j = 0
    for video in data:
        if j == 0:
            j += 1
            continue
        if len(video) < 1:
            continue
        if len(video) < 11:
            continue
        db.add(models.Videos(
            title=video[0],
            url=video[1],
            views=video[2],
            channel=video[3],
            channel_url=video[4],
            upload_date=video[5],
            duration=video[6],
            thumbnail=video[7],
            size=video[8],
            selected=to_bool(video[9]),
            downloaded=to_bool(video[10])
        ))
    db.commit()
    return True