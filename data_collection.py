class City:
    def __init__(self, id_pos=0, name=None, state=None, population=0, area=0, latitude='', longitude=''):
        self.id_pos = id_pos
        self.name = name
        self.state = state
        self.population = population
        self.area = area
        self.latitude = latitude
        self.longitude = longitude


class Restaurant:
    def __init__(self, rating=0, category='', price=0, phone='', yelp_id='',url='',review_num=0,
                name='', city='', city_id='', state='', is_closed=None):
        self.rating = rating
        self.category = category
        self.price = price
        self.phone = phone
        self.yelp_id = yelp_id
        self.url = url
        self.review_num = review_num
        self.name = name
        self.city = city
        self.city_id = city_id
        self.state = state
        self.is_closed = is_closed



def open_cache(CACHE_FILENAME):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict,CACHE_FILENAME):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 



import requests
import json

API_KEY = 'Hidden'
base_url='https://api.yelp.com/v3/businesses/search'


headers = {'Authorization': 'Bearer %s' % API_KEY}

params = {'term':'restaurants','location':'New York City', 'limit': 5}


response = requests.get(base_url, params=params, headers = headers)
result = json.loads(response.text)




CACHE_DICT = open_cache('restaurant.json')


def make_url_request_using_cache(url_or_uniqkey, params=None):
    '''Given a url, fetch if cache not exist, else use the cache.
    
    Parameters
    ----------
    url: string
        The URL for a specific web page
    cache_dict: dictionary
        The dictionary which maps url to response text
    params: dictionary
        A dictionary of param: param_value pairs
    
    Returns
    -------
    cache[url]: response
    '''
    if url_or_uniqkey in CACHE_DICT.keys():
        print('Using cache')
        return CACHE_DICT[url_or_uniqkey]

    print('Fetching')
    if params == None: # dictionary: url -> response.text
        # time.sleep(1)
        response = requests.get(url_or_uniqkey, headers=headers)
        CACHE_DICT[url_or_uniqkey] = response.text
    else: # dictionary: uniqkey -> response.json()
        endpoint_url = 'https://api.yelp.com/v3/businesses/search'
        response = requests.get(endpoint_url, headers = headers, params=params)
        CACHE_DICT[url_or_uniqkey] = response.json()
        save_cache(CACHE_DICT, 'restaurant.json')
    return CACHE_DICT[url_or_uniqkey]




from bs4 import BeautifulSoup

def build_city_instance():
    
    CACHE_DICT = open_cache('city.json')
    city_instances = []
    site_url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    url_text = make_url_request_using_cache(url_or_uniqkey=site_url)
    soup = BeautifulSoup(url_text, 'html.parser')
    tr_list = soup.find('table', class_='wikitable sortable').find('tbody').find_all('tr')[1:] # total 314 cities in the list, each in a row
    id_ = 1
    for tr in tr_list: # each tr is a city row, td is the data in each column
        td_list = tr.find_all('td')
        id_pos = id_
        name = str(td_list[0].find('a').text.strip())
        id_ += 1
        try:
            state = str(td_list[1].find('a').text.strip())
        except:
            state = td_list[1].text.strip()
        population = int(td_list[2].text.strip().replace(',', ''))
        area = float(td_list[6].text.strip().split('\xa0')[0].replace(',', ''))
        lati_longi = td_list[9].find('span', class_='geo-dec').text.strip().split(' ')
        latitude = str(lati_longi[0])
        longitude = str(lati_longi[1])
        instance = City(id_pos=id_pos, name=name, state=state, population=population, 
                        area=area, latitude=latitude, longitude=longitude
        )
        city_instances.append(instance)
    
    return city_instances

cities = build_city_instance()

def build_restaurant(city_instances):
    
    # CACHE_DICT = load_cache(CACHE_FILE)
    restaurants = []
    url = 'https://api.yelp.com/v3/businesses/search'
    for c in city_instances:
        city = c.name
        params = {'location': city + ',' + c.state , 'term': 'restaurants', 'limit': 50}
        #uniqkey = construct_unique_key(url, params)
        results = make_url_request_using_cache(url_or_uniqkey=url, params=params)
        #save_cache(results, "restaurant.json")

        if 'businesses' in results.keys():
            for business in results['businesses']:
                rating = business['rating']
                try:
                    price = len(business['price'].strip())
                except:
                    price = None
                phone = business['display_phone']
                try:
                    category = business['categories'][0]['title']
                except:
                    category = ''
                yelp_id = business['id']
                url = business['url']
                review_num = business['review_count']
                name = business['name']
                state = business['location']['state']
                is_closed = business['is_closed']

                instance = Restaurant(rating=rating, price=price, phone=phone, category=category, yelp_id=yelp_id, 
                                      url=url, review_num=review_num, name=name, 
                                      city=city, state=state, city_id=c.id_pos, is_closed=is_closed)
                restaurants.append(instance)

    
    return restaurants
restaurants = build_restaurant(cities)









