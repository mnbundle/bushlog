import time
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import flickrapi

import twitter

from bushlog.apps.location.models import Coordinate
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.crawlers.flickr import crawler as flickr_crawler
from bushlog.apps.sighting.crawlers.twitter import crawler as twitter_crawler
from bushlog.apps.sighting.models import Sighting, SightingImage
from bushlog.apps.wildlife.models import Species
from bushlog.utils import image_from_url, random_string


class Command(BaseCommand):
    args = 'crawler querylist startdate'
    help = "Run the sighting's social media spider."

    def handle(self, *args, **options):

        try:
            crawler = args[0]
        except IndexError:
            crawler = None

        try:
            query_list = args[1].split(',')
        except IndexError:
            query_list = None

        try:
            startdate = args[2].split(',')
        except IndexError:
            startdate = None

        # get the query string
        if not query_list:
            query_list = [
                'caracal', 'serval', 'wild dog', 'cheetah', 'leopard', 'lion', 'badger', 'hyaena', 'roan', 'sable',
                'elephant', 'giraffe', 'hippo', 'buffalo', 'nyala', 'zebra', 'baboon', 'sitatunga', 'puku', 'lechwe'
            ]

        # initiate the twitter api wrapper
        twitter_api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )

        # initiate the flickr api wrapper
        flickr_api = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='json')

        # iterate through all reserves and query the api for results
        for reserve in Reserve.objects.all().order_by('?'):
            print ""
            print "Searching: %s..." % reserve.name

            relevant_query_list = [q for q in query_list if reserve.species.filter(common_name__icontains=q)]
            reserve_results = []
            for query in relevant_query_list:

                if not crawler or crawler == 'twitter':

                    # retrieve the last id spidered from cache
                    cache_key = hashlib.md5('%s:%s' % (reserve.name, query)).hexdigest()
                    since_id = cache.get(cache_key, 0)

                    # get the result from the twitter crawler
                    twitter_results = twitter_crawler(twitter_api, reserve, query, since_id=since_id)

                    # set the last spidered id to cache
                    try:
                        cache.set(cache_key, twitter_results[0]['id'])
                    except IndexError:
                        pass

                    print "Found %s Results for '%s' on Twitter" % (len(twitter_results), query)

                    reserve_results += twitter_results

                if not crawler or crawler == 'flickr':

                    # get the result from the flickr crawler
                    flickr_results = flickr_crawler(flickr_api, reserve, query, min_taken_date=startdate)

                    print "Found %s Results for '%s' on Flickr" % (len(flickr_results), query)

                    reserve_results += flickr_results

            print "-" * 20
            print "Found %s Results in %s" % (len(reserve_results), reserve.name)
            print ""
            print "Saving results to the database..."

            count = 0
            report_message = ["The following sightings were found while spidering. Please moderate them: ", ""]
            for result in reserve_results:
                coordinate, coordinate_created = Coordinate.objects.get_or_create(
                    latitude=result['location']['latitude'],
                    longitude=result['location']['longitude']
                )

                if coordinate_created:

                    #create the user
                    user, user_created = User.objects.get_or_create(
                        username=result['user']['username']
                    )
                    user.profile.biography = result['user']['biography']

                    # create the users avatar
                    avatar_url = result['user']['avatar']
                    avatar = image_from_url(avatar_url)
                    user.profile.avatar.save("%s.%s" % (random_string(), avatar_url[:-3]), avatar, save=True)

                    user.profile.save()

                    # lookup the species and reserve
                    species = Species.objects.filter(common_name__icontains=result['species'])[0]
                    reserve = Reserve.objects.filter(name__icontains=result['reserve'])[0]

                    date_of_sighting = result['date']

                    sighting, sighting_created = Sighting.objects.get_or_create(
                        user=user,
                        location=coordinate,
                        reserve=reserve,
                        species=species,
                        date_of_sighting=date_of_sighting
                    )

                    if sighting_created:
                        sighting.description = result['text']
                        sighting.is_active = False
                        sighting.save()

                        sightingimage_url = result['image']
                        if sightingimage_url:
                            image = image_from_url(sightingimage_url)
                            if image:
                                sightingimage = SightingImage(
                                    sighting=sighting
                                )
                                sightingimage.image.save(
                                    "%s.%s" % (random_string(), sightingimage_url[:-3]), image, save=True
                                )
                                sightingimage.save()

                        count += 1
                        report_message.append("%s%s" % (settings.HOST, sighting.get_absolute_url()))

            print "=" * 20
            print "%s Sightings Saved" % (count)

            # email admins for sightings moderation
            if count:
                mail_admins("Spider Report: %s" % (reserve.name), "\n\r".join(report_message), fail_silently=True)

            # give twitter a bit of a break
            time.sleep(10)

