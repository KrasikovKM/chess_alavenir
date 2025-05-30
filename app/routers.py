import uuid
from pathlib import Path

import numpy as np
from PIL import Image
from fastapi import APIRouter, HTTPException, Depends
from fastapi import UploadFile, File, Form
from keras.models import load_model
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.models import ChessImage
from log import logger
from utils import class_names, SIZE, SIZE_TO_CROP

main_router = APIRouter()

probability_model = load_model("model_chess_prediction.h5")

MEDIA_FOLDER = Path("media")
LAST_MEDIA_FOLDER = Path("media/last_recognition")
MEDIA_FOLDER.mkdir(exist_ok=True)
LAST_MEDIA_FOLDER.mkdir(exist_ok=True)


@main_router.post("/upload")
async def upload_chess_image(
    file: UploadFile = File(...),
    x1: int = Form(...),
    y1: int = Form(...),
    x2: int = Form(...),
    y2: int = Form(...),
    is_white: bool = Form(True),
    db: AsyncSession = Depends(get_db),
):

    try:
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        unique_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = MEDIA_FOLDER / unique_name

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        image_id = await db.scalar(
            insert(ChessImage)
            .values(
                filename=unique_name,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
            )
            .returning(ChessImage.id)
        )

        await db.commit()

        fen = await process_chess_board(file_path, x1, y1, x2, y2, is_white)

        await db.execute(
            update(ChessImage)
            .where(ChessImage.id == image_id)
            .values(result=fen)
        )
        await db.commit()

        lichess_url = f"https://lichess.org/editor/{fen} w KQkq - 0 1"
        return {"fen": fen, "lichess_url": lichess_url}

    except Exception as e:
        logger.error(f"Error in upload: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


async def process_chess_board(image_path: Path, x1: int, y1: int, x2: int, y2: int, is_white: bool = True):
    try:
        board_image = Image.open(image_path)

        if image_path.suffix.lower() == ".png":
            board_image = board_image.convert("RGB")

        # 1️⃣ Обрезаем по координатам
        board_image = board_image.crop((x1, y1, x2, y2))
        width, height = board_image.size

        fen = ""

        for i in range(8):
            row = ""
            for j in range(8):
                # Для чёрных инвертируем индексы
                ii = i if is_white else 7 - i
                jj = j if is_white else 7 - j

                cell = board_image.crop(
                    (
                        int(width / 8 * jj),
                        int(height / 8 * ii),
                        int(width / 8 * (jj + 1)),
                        int(height / 8 * (ii + 1)),
                    )
                )
                resized = cell.resize(SIZE, resample=Image.Resampling.LANCZOS).crop(SIZE_TO_CROP)
                cell.save(f"media/last_recognition/{i}_{j}.png")
                I = np.array(resized) / 255.0
                I = np.expand_dims(I, axis=0)

                predictions = probability_model.predict(I)
                predicted_label = np.argmax(predictions[0])
                row += class_names[predicted_label]

            fen += row + "/"

        fen = fen[:-1]
        for i in range(8, 0, -1):
            fen = fen.replace("0" * i, str(i))

        return fen

    except Exception as e:
        logger.error(f"Error processing chess board: {e}")
        raise
