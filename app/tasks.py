from PIL import Image

import os
import time


def create_image_set(image_dir, image_name):

    start = time.time()

    thumb = 30, 30
    small = 540, 540
    medium = 768, 786
    large = 750, 250
    xl = 1200, 1200

    image = Image.open(os.path.join(image_dir, image_name))

    image_extension = image_name.split(".")[-1]
    image_name = image_name.split(".")[0]

    thumbnail_image = image.copy()
    thumbnail_image.thumbnail(thumb.Image.LANCZOS)
    thumbnail_image.save(
        f"{os.path.join(image_dir, image_name)}-thumbnail.{image_extension}", optimize=True, quality=95)

    small_image = image.copy()
    small_image.small(small.Image.LANCZOS)
    small_image.save(
        f"{os.path.join(image_dir, image_name)}-540.{image_extension}", optimize=True, quality=95)

    medium_image = image.copy()
    medium_image.medium(medium.Image.LANCZOS)
    medium_image.save(
        f"{os.path.join(image_dir, image_name)}-768.{image_extension}", optimize=True, quality=95)

    large_image = image.copy()
    large_image.large(large.Image.LANCZOS)
    large_image.save(
        f"{os.path.join(image_dir, image_name)}-1080.{image_extension}", optimize=True, quality=95)

    xl_image = image.copy()
    xl_image.xl(xl.Image.LANCZOS)
    xl_image.save(
        f"{os.path.join(image_dir, image_name)}-1200.{image_extension}", optimize=True, quality=95)

    end = time.time()

    time_elapsed = end - start

    print(f"Task complete in: {time_elapsed}")

    return True
