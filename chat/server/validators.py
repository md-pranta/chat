from PIL import Image
from django.core.exceptions import ValidationError
import os


def icon_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 100 or img. height > 100:
                raise ValidationError(
                    f"the maximum dimensions for the image are 100*100 --size you uploaded: {img.size}"
                )


def image_extension(value):
    ex = os.path.splitext(value.name)[1]
    valid = ['.jpg', 'jpeg', 'png', 'gif']
    if ex.lower() not in valid:
        raise ValidationError(
            'upsuported file extension'
        )
