from bushlog.utils import scraper_date


def crawler(api, reserve, query, since_id=0):

    # query the scaper api
    results = api.get_sightings(query)

    # parse the results into a usable dict
    parsed_results = []
    for result in results:
        parsed_result = {
            'bot': 'scraper',
            'date': scraper_date(result['date']),
            'text': result['description'],
            'location': {
                'latitude': '%.6f' % (result['coordinates']['latitude']),
                'longitude': '%.6f' % (result['coordinates']['longitude']),
            },
            'user': {
                'username': result['user']['username'],
                'avatar': None,
                'biography': None
            },
            'species': query,
            'reserve': reserve.name,
            'image': result.get('image')
        }

        # ensure that the result do infact occur in the give reserve
        if reserve.sighting_in_reserve(parsed_result['location']):
            parsed_results.append(parsed_result)

    return parsed_results
