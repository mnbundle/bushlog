from bushlog.utils import clean_flickr_json


def crawler(api, reserve, query, min_upload_date=None):

    # query the twitter api
    try:
        results = clean_flickr_json(
            api.photos_search(
                bbox=reserve.bounding_box,
                text=query,
                per_page=500,
                min_upload_date=min_upload_date,
                sort='date-taken-desc',
                accuracy=1,
                extras='description,date_taken,owner_name,icon_server,geo,url_c'
            )
        )
    except:
        return []

    # parse the results into a usable dict
    parsed_results = []
    for result in results['photos']['photo']:

        # form the description
        title = result['title']
        description = result['description']['_content']
        if description and title:
            description = "%s. %s" % (title, description)
        elif title and not description:
            description = title

        parsed_result = {
            'bot': 'flickrbot',
            'id': result['id'],
            'date': result['datetaken'],
            'text': description,
            'location': {
                'latitude': '%.6f' % (result['latitude']),
                'longitude': '%.6f' % (result['longitude'])
            },
            'user': {
                'username': result['ownername'][:30].replace(' ', '').lower(),
                'avatar': "http://farm{iconfarm}.staticflickr.com/{iconserver}/buddyicons/{owner}.jpg".format(**result),
                'biography': ''
            },
            'species': query,
            'reserve': reserve.name,
            'image': result.get(
                'url_c', "http://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg".format(**result)
            )
        }

        # ensure that the result do infact occur in the give reserve
        if reserve.sighting_in_reserve(parsed_result['location']):
            parsed_results.append(parsed_result)

    return parsed_results

