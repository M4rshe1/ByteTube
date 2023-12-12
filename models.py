from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base


class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)
    views = Column(String, index=True)
    channel = Column(String, index=True)
    channel_url = Column(String, index=True)
    upload_date = Column(String, index=True)
    duration = Column(Integer, index=True)
    thumbnail = Column(String, index=True)
    size = Column(String, index=True)
    selected = Column(Boolean, index=True)
    downloaded = Column(Boolean, index=True)
    failed = Column(Boolean, index=True)


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    setting = Column(String, index=True)
    value = Column(String, index=True)
