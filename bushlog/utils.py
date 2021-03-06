from cStringIO import StringIO
from datetime import datetime, date
import hashlib
import json
import os
import random
import re
import string
from time import mktime, strptime
import urllib2

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.utils.translation import ungettext, ugettext

from dateutil.relativedelta import relativedelta

import Image as pil
from PIL.ExifTags import GPSTAGS, TAGS

import httplib2

EXIF_INCLUDE_KEYS = ['Make', 'DateTimeOriginal', 'Model', 'Orientation']


def choices(item_list, sort=False):
    """
    Convert a list to a choices tuple
    """
    if sort:
        item_list.sort()
    return tuple((i, i) for i in item_list)


def generate_key(instance, method):
    return hashlib.md5("%s|%s|%s" % (instance.__class__.__name__, instance.pk, method)).hexdigest()


def historical_date(*args, **kwargs):
    return datetime.now() - relativedelta(*args, **kwargs)


def twitter_date(date_string):
    date_obj = datetime.fromtimestamp(mktime(strptime(date_string, '%a %b %d %H:%M:%S +0000 %Y')))
    return date_obj + relativedelta(hours=2)


def scraper_date(date_string):
    date_obj = datetime.fromtimestamp(mktime(strptime(date_string, '%d/%m/%Y %H:%M')))
    return date_obj


def clean_twitter_text(text):
    return re.sub("(#[A-Za-z0-9_]+)|([A-Za-z0-9_]+\:[A-Za-z0-9_]+)|(@)|\.|(http[A-Za-z0-9_\.\:\/]+)", "", text).strip()


def clean_flickr_json(response):
    return json.loads(response.replace('jsonFlickrApi(', '')[:-1])


def fuzzydate(timestamp, to=None):
    if not timestamp:
        return ""

    compare_with = to or date.today()
    delta = timestamp - compare_with

    if delta.days == 0:
        return u"today"
    elif delta.days == -1:
        return u"yesterday"
    elif delta.days == 1:
        return u"tomorrow"

    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n: ungettext('week', 'weeks', n)),
        (1.0, lambda n: ungettext('day', 'days', n)),
    )

    for i, (chunk, name) in enumerate(chunks):
        if abs(delta.days) >= chunk:
            count = abs(round(delta.days / chunk, 0))
            break

    date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}

    if delta.days > 0:
        return "in " + date_str
    else:
        return date_str + " ago"


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

    # rotate the image depending on the orientation
    try:
        image_orientation = get_exif_data(image.path).get('Orientation')
    except AttributeError:
        image_orientation = 1

    image_orientation_map = {
        3: 180,
        6: 270,
        8: 90
    }
    try:
        rotated_image = image_file.rotate(image_orientation_map[image_orientation], expand=True)
    except KeyError:
        rotated_image = image_file

    # store the original image width and height
    image_width, image_height = rotated_image.size

    # use the original size if no size given
    resized_image_width = float(width if width else image_width)
    resized_image_height = float(height if height else image_height)

    # find the closest bigger proportion to the maximum size
    image_scale = max(
        resized_image_width / float(image_width), resized_image_height / float(image_height)
    )

    # return the original image if it is smaller than the required dimensions
    if image_scale > 1:
        return image.url

    # if the image is not bigger than the original size, calculate proportions and resize
    resized_width = int(image_width * image_scale)
    resized_height = int(image_height * image_scale)
    resized_image = rotated_image.resize((resized_width, resized_height), pil.ANTIALIAS)

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


def image_from_url(url):
    try:
        return ContentFile(urllib2.urlopen(url).read())
    except urllib2.URLError:
        return None


def get_exif_data(image_path, exif_include_keys=EXIF_INCLUDE_KEYS):
    """
    Returns all the image's exif data as a dict.
    """
    image_file = pil.open(image_path)
    try:
        raw_exif_data = image_file._getexif()
    except AttributeError:
        raw_exif_data = None

    if not raw_exif_data:
        return None

    exif_data = {}
    for key, value in raw_exif_data.items():
        decoded_key = TAGS.get(key, key)
        if decoded_key in exif_include_keys:
            if decoded_key == "DateTimeOriginal":
                try:
                    value = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    value = datetime.now()
            exif_data[decoded_key] = value

    return exif_data

    [{TAGS.get(key, key): value}for key, value in raw_exif_data.items()]


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


def point_in_polygon(latitude, longitude, polygon):
    """
    Determine whether or not a point can be found in a poyligon.
    """
    polygon_length = len(polygon)
    is_inside =False

    polygon_latitude_start, polygon_longitude_start = polygon[0]
    for i in range(polygon_length + 1):
        polygon_latitude_current, polygon_longitude_current = polygon[i % polygon_length]
        if longitude > min(polygon_longitude_start, polygon_longitude_current):
            if longitude <= max(polygon_longitude_start, polygon_longitude_current):
                if latitude <= max(polygon_latitude_start, polygon_latitude_current):
                    if polygon_longitude_start != polygon_longitude_current:
                        latitude_intersect = (
                            (longitude-polygon_longitude_start) *
                            (polygon_latitude_current-polygon_latitude_start) /
                            (polygon_longitude_current-polygon_longitude_start) +
                            polygon_latitude_start
                        )
                    if polygon_latitude_start == polygon_latitude_current or latitude <= latitude_intersect:
                        is_inside = not is_inside
        polygon_latitude_start, polygon_longitude_start = polygon_latitude_current, polygon_longitude_current

    return is_inside


def random_string():
    return "".join(random.choice(string.hexdigits + string.digits) for r in [i for i in range(16)])


def fahrenheit_to_celsius(fahrenheit):
    """
    Convert fahrenheit tempreture to celsius.
    """
    if fahrenheit:
        return int(round((fahrenheit - 32.0) * (5.0 / 9.0)))
    return None


def default_weather_icon(icon):
    """
    Validate and return the appropriate icon.
    """
    icon_set = [
        'clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind', 'fog', 'cloudy', 'partly-cloudy-day',
        'partly-cloudy-night'
    ]
    if icon == 'sleet':
        return 'snow'

    if icon not in icon_set:
        return None

    return icon


def get_weather_data(latitude, longitude):
    """
    Get the current wether from cache or the API.
    """
    cache_key = hashlib.md5("%s|%s|%s" % (latitude, longitude, "weather")).hexdigest()
    current_weather = cache.get(cache_key)

    if not current_weather:
        connection = httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = connection.request("%s/%s,%s" % (settings.FORCAST_URL, latitude, longitude), "GET")
        current_weather = json.loads(content).get('currently', {})
        cache.set(cache_key, current_weather, 60 * 60)

    return {
        'temperature': fahrenheit_to_celsius(current_weather.get('temperature')),
        'icon': default_weather_icon(current_weather.get('icon')),
        'summary': current_weather.get('summary')
    }
