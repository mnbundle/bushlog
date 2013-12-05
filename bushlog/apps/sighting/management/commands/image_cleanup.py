import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from bushlog.apps.sighting.models import Sighting


class Command(BaseCommand):
    args = ''
    help = "Cleanup all zombie images."

    def img_identifier(self, img_path):
        return os.path.basename(img_path)[:-4].split("_")[0]

    def handle(self, *args, **options):
        valid_img_ids = []
        media_path = os.path.join(settings.MEDIA_ROOT, 'sightings/')

        for obj in Sighting.objects.all():
            valid_img_ids += [self.img_identifier(img.image.path) for img in obj.images.all() if img]

        invalid_img_paths = [
            img for img in glob.glob('%s*/*/*.jpg' % media_path) if self.img_identifier(img) not in valid_img_ids
        ]

        print "Deleting %s zombie images..." % (len(invalid_img_paths))

        for img_path in invalid_img_paths:
            os.remove(img_path)
