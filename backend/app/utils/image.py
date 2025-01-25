from random import choice
from app.constants import valid_chars, filename_length
from PIL import Image
from fastapi import File, Form
from typing_extensions import Annotated


async def generate_filename() -> str:
    return "".join(choice(valid_chars) for _ in range(filename_length))


async def process_image(file: Annotated[bytes, File()],
                        extension: Annotated[str, Form()] = "png") -> dict:
    filename = await generate_filename()

    with open(f"app/static/images/{filename}.{extension}", "wb") as new_file:
        new_file.write(file)

    image = Image.open(f"app/static/images/{filename}.{extension}")
    image = image.convert("RGB")

    image.save(f"app/static/links/{filename}.webp", "webp", optimize=True, quality=90)

    image_link = f"static/links/{filename}.webp"

    return {"image_link": image_link, "file_name": filename}
