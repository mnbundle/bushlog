from cStringIO import StringIO
from datetime import datetime
import os

from dateutil.relativedelta import relativedelta

import Image as pil
from PIL.ExifTags import GPSTAGS, TAGS

EXIF_INCLUDE_KEYS = ['Make', 'DateTimeOriginal', 'Model']


def choices(item_list):
    """
    Convert a list to a choices tuple
    """
    return tuple((i, i) for i in item_list)


def historical_date(*args, **kwargs):
    return datetime.now() - relativedelta(*args, **kwargs)


def image_resize(image, width=None, height=None):
    """
    Resizes images on the fly. If width and height args are 0 (zero) they will be ignored.
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


def get_exif_data(image_path, exif_include_keys=EXIF_INCLUDE_KEYS):
    """
    Returns all the image's exif data as a dict.
    """
    print exif_include_keys
    image_file = pil.open(image_path)
    raw_exif_data = image_file._getexif()
    if not raw_exif_data:
        return None

    exif_data = {}
    for key, value in raw_exif_data.items():
        decoded_key = TAGS.get(key, key)
        if decoded_key in exif_include_keys:
            if decoded_key == "DateTimeOriginal":
                value = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            exif_data[decoded_key] = value

    return exif_data


def convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    """
    degrees = float(value[0][0]) / float(value[0][1])
    minutes = float(value[1][0]) / float(value[1][1])
    seconds = float(value[2][0]) / float(value[2][1])

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def get_coordinates(gps_data):
    """
    Returns the latitude and longitude, from the provided gps_data, if available.
    """
    latitude = None
    longitude = None

    gps_latitude = gps_data.get('GPSLatitude', None)
    gps_latitude_ref = gps_data.get('GPSLatitudeRef', None)
    gps_longitude = gps_data.get('GPSLongitude', None)
    gps_longitude_ref = gps_data.get('GPSLongitudeRef', None)

    if all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
        latitude = convert_to_degress(gps_latitude)
        if gps_latitude_ref != "N":
            latitude = 0 - latitude

        longitude = convert_to_degress(gps_longitude)
        if gps_longitude_ref != "E":
            longitude = 0 - longitude

    return {
        'latitude': latitude,
        'longitude': longitude
    }


def get_gps_data(image_path):
    """
    Return GPS data.
    """
    exif_data = get_exif_data(image_path, exif_include_keys=['GPSInfo'])
    print exif_data
    if not exif_data:
        return None

    raw_gps_data = exif_data.get('GPSInfo', None)
    if not raw_gps_data:
        return None

    gps_data = {}
    for key, value in raw_gps_data.items():
        decoded_key = GPSTAGS.get(key, key)
        gps_data[decoded_key] = value

    return get_coordinates(gps_data)
