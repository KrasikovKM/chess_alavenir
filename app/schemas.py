from typing import Optional

from pydantic import BaseModel


class ImageCreate(BaseModel):
    im_number: int
    x1: Optional[int] = None
    y1: Optional[int] = None
    x2: Optional[int] = None
    y2: Optional[int] = None


class ImageResponse(ImageCreate):
    id: int
    im_number: int
    x1: Optional[int] = None
    y1: Optional[int] = None
    x2: Optional[int] = None
    y2: Optional[int] = None
