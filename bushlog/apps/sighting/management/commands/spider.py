import hashlib
from optparse import make_option
import time

from django.conf import settings
from django.core.cache import cache
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify

import flickrapi

from instagram import InstagramAPI

import twitter

from bushlog.apps.location.models import Coordinate
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.crawlers.flickr import crawler as flickr_crawler
from bushlog.apps.sighting.crawlers.instagram import crawler as instagram_crawler
from bushlog.apps.sighting.crawlers.scraper import crawler as scraper_crawler
from bushlog.apps.sighting.crawlers.twitter import crawler as twitter_crawler
from bushlog.apps.sighting.scrapers import latestsightings
from bushlog.apps.sighting.models import Sighting, SightingImage
from bushlog.apps.wildlife.models import Species
from bushlog.utils import historical_date, image_from_url, random_string


class Command(BaseCommand):
    args = ''
    help = "Run the sighting's social media spider"
    option_list = BaseCommand.option_list + (
        make_option('--reserve', dest='reserve', default=None, help='Set the reserve to spider - defaults to all'),
        make_option('--crawler', dest='crawler', default=None, help='Set the crawler [twitter|instagram|flickr]'),
        make_option('--query-list', dest='query_list', default=None, help='Set the queries you want to perform')
    )

    def handle(self, *args, **options):

        # initiate the twitter api wrapper
        twitter_api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )

        # initiate the flickr api wrapper
        flickr_api = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='json')
        token, frob = flickr_api.get_token_part_one(perms='read')
        if not token:
            print "Flickr: Tokenized auth failed."
        flickr_api.get_token_part_two((token, frob))

        # initiate the instagram api wrapper
        instagram_api = InstagramAPI(
            client_id=settings.INSTAGRAM_CLIENT_ID, client_secret=settings.INSTAGRAM_CLIENT_SECRET
        )

        # initiate the scaper api wrapper
        scraper_api = latestsightings.LatestSightingScraper(
            url=settings.LATESTSIGHTING_URL, img_hostname=settings.LATESTSIGHTING_IMG_HOST
        )

        # iterate through all reserves and query the api for results
        if options.get('reserve'):
            reserve_list = Reserve.objects.filter(name__icontains=options.get('reserve'))
        else:
            reserve_list = Reserve.objects.all().order_by('?')

        for reserve in reserve_list:
            print
            print "Searching: %s..." % reserve.name

            # get the query string
            if options.get('query_list'):
                relevant_query_list = [
                    q for q in options.get('query_list').split(',') if reserve.species.filter(common_name__icontains=q)
                ]
            else:
                relevant_query_list = [obj.common_name for obj in reserve.species.public().order_by('?')][:15]

            reserve_results = []
            for query in relevant_query_list:

                # remove common words from the query
                query = " ".join(q for q in query.split() if q not in settings.IGNOREABLE_WORDS)

                if not options.get('crawler') or options.get('crawler') == 'twitter':

                    # retrieve the last id spidered from cache
                    cache_key = hashlib.md5('%s:%s:twitter' % (reserve.name, query)).hexdigest()
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

                if not options.get('crawler') or options.get('crawler') == 'flickr':

                    # retrieve the last id spidered from cache
                    cache_key = hashlib.md5('%s:%s:flickr' % (reserve.name, query)).hexdigest()
                    min_upload_date = cache.get(cache_key, 0)

                    # get the result from the flickr crawler
                    flickr_results = flickr_crawler(flickr_api, reserve, query, min_upload_date=min_upload_date)

                    # set the last spidered historical date to cache
                    try:
                        cache.set(cache_key, str(historical_date(months=6)))
                    except IndexError:
                        pass

                    print "Found %s Results for '%s' on Flickr" % (len(flickr_results), query)

                    reserve_results += flickr_results

                if not options.get('crawler') or options.get('crawler') == 'instagram':

                    # retrieve the last id spidered from cache
                    cache_key = hashlib.md5('%s:%s:instagram' % (reserve.name, query)).hexdigest()
                    since_id = cache.get(cache_key, 0)

                    # get the result from the instagram crawler
                    instagram_results = instagram_crawler(instagram_api, reserve, query, since_id=since_id)

                    # set the last spidered id to cache
                    try:
                        cache.set(cache_key, instagram_results[0]['id'])
                    except IndexError:
                        pass

                    print "Found %s Results for '%s' on Instagram" % (len(instagram_results), query)

                    reserve_results += instagram_results

                if not options.get('crawler') or options.get('crawler') == 'scraper':

                    # get the result from the scraper
                    scraper_results = scraper_crawler(scraper_api, reserve, query)

                    print "Found %s Results for '%s' on LatestSightings" % (len(scraper_results), query)

                    reserve_results += scraper_results

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
                        username=slugify(unicode(result['user']['username'][:30]))
                    )
                    if not user_created and not user.is_active:
                        pass

                    else:
                        user.profile.biography = unicode(result['user']['biography'])

                        # create the users avatar
                        avatar_url = result['user']['avatar']
                        if avatar_url:
                            avatar = image_from_url(avatar_url)
                            if avatar:
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
                            sighting.description = unicode(result['text'])
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

            # give the web services a bit of a break
            time.sleep(10)
