from bushlog.utils import clean_twitter_text


def crawler(api, reserve, query, since_id=0):

    # get the reserve's center point
    coordinates = reserve.bounds['centre_point']

    # query the twitter api
    results = api.media_search(lat=coordinates['latitude'], lng=coordinates['longitude'], distance=5000, count=250)

    # parse the results into a usable dict
    parsed_results = []

    for result in results:
        result_tags = [t.name for t in getattr(result, 'tags', [])]
        caption = getattr(getattr(result, 'caption'), 'text', '').lower()

        if query.lower() in result_tags or query.lower() in caption:
            parsed_result = {
                'bot': 'instagram',
                'id': result.id,
                'date': result.created_time,
                'text': clean_twitter_text(caption),
                'location': {
                    'latitude': '%.6f' % (result.location.point.latitude),
                    'longitude': '%.6f' % (result.location.point.longitude)
                },
                'user': {
                    'username': result.user.username.lower(),
                    'avatar': result.user.profile_picture,
                    'biography': result.user.bio
                },
                'species': query,
                'reserve': reserve.name,
                'image': result.images['standard_resolution'].url if result.images else None
            }

            # ensure that the result do infact occur in the give reserve
            if reserve.sighting_in_reserve(parsed_result['location']):
                parsed_results.append(parsed_result)

    return parsed_results
