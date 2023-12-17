from __future__ import annotations

import webbrowser

from fastapi import FastAPI, Depends, Request, Form, status, BackgroundTasks, File, UploadFile

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

import modules

models.Base.metadata.create_all(bind=engine)

progress: dict = {"progress": 0, "total": 0}

# start a browser window with the app
webbrowser.open("http://localhost:8000", new=2)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    # print(progress)

    videos = db.query(models.Videos).all()

    stats = {"videos": len(videos), "selected": 0}
    for video in videos:
        if video.selected:
            stats["selected"] += 1
    only_audio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    if only_audio is None:
        only_audio = models.Settings(setting="onlyAudio", value="False")
        db.add(only_audio)
        db.commit()
        only_audio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "videos": videos,
        "onlyAudio": only_audio.value,
        "progress": progress.get("progress"),
        "total": progress.get("total"),
        "stats": stats,
    })


@app.post("/add")
def add(request: Request, background_tasks: BackgroundTasks,
        db: Session = Depends(get_db), links: str = Form(...)):
    background_tasks.add_task(modules.get_video_data, links, progress, db)
    # data = modules.get_video_data(links, progress)
    # if data:
    #     for video in data:
    #         db_video = models.Videos(**video)
    #         db.add(db_video)
    #     db.commit()
    return {"status": 200}


# @app.post("/stop_app")
# def stop_app(request: Request, db: Session = Depends(get_db)):
#     global IN_PROGRESS
#     global IS_DOWNLOADING
#     IN_PROGRESS = False
#     IS_DOWNLOADING = False
#     return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/settings")
def settings(request: Request, db: Session = Depends(get_db), value: bool = Form(...), setting: str = Form(...)):
    db.query(models.Settings).filter(models.Settings.setting == setting).update({models.Settings.value: value})
    db.commit()
    return {"status": 200, "message": "Settings updated"}


@app.post("/download")
async def download(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                   links: str = Form(...)):
    only_audio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    background_tasks.add_task(modules.download, links, only_audio.value, progress, 1)
    db.query(models.Videos).filter(models.Videos.url == links).update({models.Videos.downloaded: True})
    return {"status": 200}


@app.post("/download_all")
def download_all(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    only_audio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    links = db.query(models.Videos.url).all()

    background_tasks.add_task(modules.download_multi, links, only_audio.value, progress)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/download_selected", )
def download_selected(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    links = db.query(models.Videos).filter(models.Videos.selected == True).all()
    links = [link.url for link in links]
    # print(links)
    only_audio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    # links = [link.url for link in links]
    background_tasks.add_task(modules.download_multi, links, only_audio.value, progress)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/check")
def check(request: Request, db: Session = Depends(get_db), links: str = Form(...)):
    links = links.split("\r\n")
    for link in links:
        db.query(models.Videos).filter(models.Videos.url == link).update(
            {models.Videos.selected: ~models.Videos.selected})
    db.commit()
    return {"status": 200}


@app.post("/delete")
def delete(request: Request, db: Session = Depends(get_db), links: str = Form(...)):
    links = links.split("\r\n")
    for link in links:
        db.query(models.Videos).filter(models.Videos.url == link).delete()
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/delete_all")
def delete_all(request: Request, db: Session = Depends(get_db)):
    for video in db.query(models.Videos).all():
        db.delete(video)
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/reverse_selection")
def reverse_selection(request: Request, db: Session = Depends(get_db)):
    for video in db.query(models.Videos).all():
        db.query(models.Videos).filter(models.Videos.url == video.url).update(
            {models.Videos.selected: ~models.Videos.selected})
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/select_all")
def select_all(request: Request, db: Session = Depends(get_db)):
    for video in db.query(models.Videos).all():
        db.query(models.Videos).filter(models.Videos.url == video.url).update(
            {models.Videos.selected: True})
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/export")
def export(request: Request, db: Session = Depends(get_db), convert: str = Form(...)):
    if modules.export.do(db, convert):
        return {"status": 200, "message": f'Exported file successfully to ~/Downloads/ByteTube/export.{convert}'}
    else:
        return {"status": 500, "message": "Something went wrong"}


@app.post("/import")
def import_(db: Session = Depends(get_db), file: UploadFile = File(...),
            delete_before_import: bool = Form(...)):

    if modules.import_.do_import(db, file, delete_before_import):
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"status": 500, "message": "Something went wrong"}


@app.post("/progress")
def get_progress():
    return progress


@app.exception_handler(405)
async def method_not_allowed(request: Request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(404)
async def not_found(request: Request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
