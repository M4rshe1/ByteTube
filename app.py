from fastapi import FastAPI, Depends, Request, Form, status, BackgroundTasks

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

import modules

models.Base.metadata.create_all(bind=engine)

IN_PROGRESS = False
IS_DOWNLOADING = False


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
    videos = db.query(models.Videos).all()
    onlyaudio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    if onlyaudio is None:
        onlyaudio = models.Settings(setting="onlyAudio", value="False")
        db.add(onlyaudio)
        db.commit()
        onlyaudio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "videos": videos,
        "onlyAudio": onlyaudio.value,
        "inProgress": IN_PROGRESS,
        "isDownloading": IS_DOWNLOADING
    })


@app.post("/add")
def add(request: Request, db: Session = Depends(get_db), link: str = Form(...)):
    data = modules.get_video_data(link)
    if data:
        for video in data:
            db_video = models.Videos(**video)
            db.add(db_video)
        db.commit()
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/settings")
def settings(request: Request, db: Session = Depends(get_db), value: bool = Form(...), setting: str = Form(...)):
    db.query(models.Settings).filter(models.Settings.setting == setting).update({models.Settings.value: value})
    db.commit()
    return {"status": 200, "message": "Settings updated"}


@app.post("/download")
async def download(request: Request, db: Session = Depends(get_db), links: str = Form(...)):
    error = False
    links = links.split("\r\n")
    onlyaudio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    
    for link in links:
        error = modules.download(link, onlyaudio.value)
        if error:
            db.query(models.Videos).filter(models.Videos.url == link).update({models.Videos.failed: True})
        else:
            db.query(models.Videos).filter(models.Videos.url == link).update({models.Videos.downloaded: True})
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/download_all")
def download_all(request: Request, db: Session = Depends(get_db)):
    error = False
    onlyaudio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    links = db.query(models.Videos).all()
    for link in links:
        error = modules.download(link.url, onlyaudio.value)
        if error:
            db.query(models.Videos).filter(models.Videos.url == link.url).update({models.Videos.failed: True})
        else:
            db.query(models.Videos).filter(models.Videos.url == link.url).update({models.Videos.downloaded: True})
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/download_selected")
def download_selected(request: Request, db: Session = Depends(get_db)):
    error = False
    links = db.query(models.Videos).filter(models.Videos.selected == True).all()
    onlyaudio = db.query(models.Settings).filter(models.Settings.setting == "onlyAudio").first()
    for link in links:
        error = modules.download(link.url, onlyaudio.value)
        if error:
            db.query(models.Videos).filter(models.Videos.url == link.url).update({models.Videos.failed: True})
        else:
            db.query(models.Videos).filter(models.Videos.url == link.url).update({models.Videos.downloaded: True})
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


@app.exception_handler(405)
async def method_not_allowed(request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(404)
async def not_found(request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
