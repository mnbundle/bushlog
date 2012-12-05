from cStringIO import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
import Image as pil
import os


def choices(item_list):
    """
    Convert a list to a choices tuple
    """
    return tuple((i, i) for i in item_list)


def historical_date(*args, **kwargs):
    return datetime.now() - relativedelta(*args, **kwargs)


def image_resize(image, width=None, height=None):
    """
    Resizes images on the fly. If width and height args are 0 (zero) they will be
    ignored.
    """
    image_base, image_ext = os.path.splitext(image.path)

    # use the dimensions to construct the resized images path
    path_extra = '_%s%s%s' % (
        str(width) if width else '',
        '_' if width and height else '',
        str(height) if height else ''
    )
    resized_image_path = "".join([image_base, path_extra, image_ext])

    # get the image url
    resized_image_url = "".join([os.path.splitext(image.url)[0], path_extra, image_ext])

    # check if resized image and stored image exists for use - double check permissions are correct
    if os.path.exists(resized_image_path):
        return resized_image_url

    if not os.path.exists(image.path):
        return ""

    # open the file and store the format
    image_file = pil.open(image.path)
    image_format = image_file.format

    # store the original image width and height
    image_width, image_height = image_file.size

    # use the original size if no size given
    resized_image_width = float(width if width else image_width)
    resized_image_height = float(height if height else image_height)

    # find the closest bigger proportion to the maximum size
    image_scale = max(
        resized_image_width / float(image_width), resized_image_height / float(image_height)
    )

    # return the original image if it is smaller than the required dimensions
    if image_scale > 1:
        return image.path

    # if the image is not bigger than the original size, calculate proportions and resize
    resized_width = int(image_width * image_scale)
    resized_height = int(image_height * image_scale)
    resized_image = image_file.resize((resized_width, resized_height), pil.ANTIALIAS)

    # crop the image as required
    crop_left = int((resized_width - resized_image_width) / 2)
    crop_top = int((resized_height - resized_image_height) / 2)
    crop_right = int(crop_left + resized_image_width)
    crop_bottom = int(crop_top + resized_image_height)
    resized_image = resized_image.crop((crop_left, crop_top, crop_right, crop_bottom))

    # save the image object
    resized_image.save(resized_image_path, image_format, quality=80)

    # change the image file permissions
    os.chmod(resized_image_path, 0755)

    # save the image object to file
    final_file = StringIO()
    resized_image.save(final_file, image_format, quality=95)
    final_file.close()

    return resized_image_url
