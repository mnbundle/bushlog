from bushlog.apps.sighting.scrapers.base import BaseScraper


class LatestSightingScraper(BaseScraper):
    def get_sightings(self, query):
        sightings = []
        for sighting in self.scraper.find_all('li', attrs={'class': 'activity-item'}):
            sighting_data = {}
            for paragraph in sighting.find_all('p'):
                if 'sight_image_container' in paragraph.get('class', []):
                    img_src = paragraph.img.get('src') if not "none.gif" in paragraph.img.get('src', '') else None
                    if img_src:
                        sighting_data['image'] = "%s%s" % (self.img_hostname, img_src.split('image=')[1].split('&width')[0])
                    else:
                        sighting_data['image'] = None
                else:
                    clean_data = [line.strip() for line in paragraph.get_text().splitlines() if line.strip()]
                    if clean_data:
                        sighting_data['user'] = {
                            'username': clean_data[0].replace('Tinged by: ', '')
                        }
                        sighting_data['date'] = clean_data[1].replace('On ', '')
                        sighting_data['description'] = clean_data[2][:-1].strip()
                    else:
                        sighting_data['coordinates'] = {
                            'latitude': float(paragraph.img.get('onclick').split('item.lat=')[1].split(';')[0]),
                            'longitude': float(paragraph.img.get('onclick').split('item.lng=')[1].split(';')[0])
                        }

            if query in sighting_data['description']:
                sightings.append(sighting_data)

        return sightings
