from rest_framework.exceptions import ValidationError


def validate_image(self, data):
    max_img_size = (2000, 2000)
    if data.image.size > max_img_size:
        raise ValidationError(
            f'Image size is too large. '
            f'Maximum photo size {max_img_size[0]}x{max_img_size[1]}')
    return data
