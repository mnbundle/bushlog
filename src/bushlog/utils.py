from cStringIO import StringIO
import Image as pil
import os
import random
import string

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.hashcompat import md5_constructor

def form_handler(form_class, request):
    """
    Generic form handler. 
    """
    form = form_class()
    if request.POST:
        post_data = request.POST.copy()
        form = form_class(post_data)
        if form.is_valid():
            form.save(request)
    return form

def send_email(cleaned_data, success_msg=None):
    """
    Generic method to send plain text emails.
    """
    subject = "Email from website."
    message = "%s sent you a message from the website:\r\n\r\n" % cleaned_data.get('full_name')
    
    # form the message str by iterating through the form data
    for key, val in cleaned_data.iteritems():
        if key == "product":
            message += "%s: %s\r\n" % (key.title().replace("_", " "), val.name)
        elif key != "honeypot":
            message += "%s: %s\r\n" % (key.title().replace("_", " "), val)
    
    from_email = "%s <%s>" % (cleaned_data.get('full_name', ''), cleaned_data.get('email', ''))
    to_email = "%s <%s>" % (settings.COMPANY, settings.COMPANY_EMAIL)
    
    # send the actual email, add a success message and return the response
    success = send_mail(subject, message, from_email, [to_email])
    if success and success_msg:
        messages.add_message(request, messages.INFO, success_msg)
    return success
    
def list_to_tuple(list_input, sort=True):
    """
    Convert a list to a tuple and sort if required.
    """
    if sort:
        list_input.sort()
    return tuple([(x,x) for x in list_input])

def random_str():
    return md5_constructor(
        string.join(
            [random.choice(string.letters) for i in xrange(50)]
        )
    ).hexdigest()
    
def image_resize(image, width, height):
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
