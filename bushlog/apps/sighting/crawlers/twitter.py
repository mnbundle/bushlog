from bushlog.utils import clean_twitter_text, twitter_date


def crawler(api, reserve, query, since_id=0):

    # get the reserve's center point
    coordinates = reserve.bounds['centre_point']

    # query the twitter api
    results = api.GetSearch(
        term=query,
        geocode=(coordinates['latitude'], coordinates['longitude'], '100mi'),
        per_page=100,
        include_entities=True,
        since_id=since_id
    )

    # filter out results without geo coordinates
    geo_tagged_results = [result for result in results if result.geo]

    # parse the results into a usable dict
    parsed_results = []
    for status in geo_tagged_results:
        parsed_result = {
            'bot': 'twitterbot',
            'id': status.id,
            'date': twitter_date(status.created_at),
            'text': clean_twitter_text(status.text),
            'location': {
                'latitude': '%.2f' % (status.geo['coordinates'][0]),
                'longitude': '%.2f' % (status.geo['coordinates'][1])
            },
            'user': {
                'username': status.user.screen_name
            },
            'species': query if query != 'hyaena' else "spotted hyaena",
            'reserve': reserve.name,
            'image': status.media[0].get('media_url') if status.media else None
        }

        # ensure that the result do infact occur in the give reserve
        if reserve.sighting_in_reserve(parsed_result['location']):
            parsed_results.append(parsed_result)

    return parsed_results

