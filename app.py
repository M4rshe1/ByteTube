from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

import modules

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    videos = db.query(models.Videos).all()
    return templates.TemplateResponse("index.html", {"request": request, "videos": videos})


@app.post("/add")
def add(request: Request, db: Session = Depends(get_db), link: str = Form(...)):
    data = modules.get_video_data(link)
    if data:
        for video in data:
            db_video = models.Videos(**video)
            db.add(db_video)
        db.commit()
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/download")
async def download(request: Request, db: Session = Depends(get_db)):
    error = False
    for video in db.query(models.Videos).all():
        if not video.selected:
            tmp = modules.download(video.url)
            if not tmp:
                error = True
            db.query(models.Videos).filter(models.Videos.url == video.url).update({models.Videos.downloaded: True})
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/uncheck")
def uncheck(request: Request, db: Session = Depends(get_db), links: str = Form(...)):
    links = links.split("\r\n")
    for link in links:
        db.query(models.Videos).filter(models.Videos.url == link).update({models.Videos.selected: False})
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/check")
def check(request: Request, db: Session = Depends(get_db), links: str = Form(...)):
    links = links.split("\r\n")
    for link in links:
        db.query(models.Videos).filter(models.Videos.url == link).update({models.Videos.selected: True})
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


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


@app.exception_handler(405)
async def method_not_allowed(request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(404)
async def not_found(request, exc):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

