from sqlalchemy import Column, String, DateTime, Integer, func
from database.connection import Base


class ChessImage(Base):
    __tablename__ = "image_records"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    result = Column(String(255))  # <-- Добавляем поле для хранения FEN
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
