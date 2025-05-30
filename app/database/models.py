from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

base = declarative_base()
metadata_chess = base.metadata


class ChessImage(base):
    __tablename__ = "image_records"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    result = Column(String)  # <-- Добавляем поле для хранения FEN
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
