from bushlog.utils import clean_flickr_json


def crawler(api, reserve, query, min_taken_date=None):

    # query the twitter api
    try:
        results = clean_flickr_json(
            api.photos_search(
                bbox=reserve.bounding_box,
                tags=query,
                licence='1,2,3,4,5,6,7',
                per_page=200,
                min_taken_date=min_taken_date,
                sort='date-posted-desc'
            )
        )
    except:
        return []

    # parse the results into a usable dict
    parsed_results = []
    for result in results['photos']['photo']:
        try:
            result.update({
                'info': clean_flickr_json(api.photos_getInfo(photo_id=result['id']))['photo'],
            })
        except:
            return []

        # form the description
        title = result['info']['title']['_content']
        description = result['info']['description']['_content']
        if description and title:
            description = "%s: %s" % (title, description)
        elif title and not description:
            description = title

        parsed_result = {
            'bot': 'flickrbot',
            'id': result['id'],
            'date': result['info']['dates']['taken'],
            'text': description,
            'location': {
                'latitude': '%.2f' % (result['info']['location']['latitude']),
                'longitude': '%.2f' % (result['info']['location']['longitude'])
            },
            'user': {
                'username': result['info']['owner']['username'].replace(' ', '').lower(),
                'avatar': "http://farm{iconfarm}.staticflickr.com/{iconserver}/buddyicons/{nsid}.jpg".format(
                    **result['info']['owner']
                ),
                'biography': ''
            },
            'species': query if query != 'hyaena' else "spotted hyaena",
            'reserve': reserve.name,
            'image': "http://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg".format(**result)
        }

        # ensure that the result do infact occur in the give reserve
        if reserve.sighting_in_reserve(parsed_result['location']):
            parsed_results.append(parsed_result)

    return parsed_results

