import json

f = open("restaurant.json", 'r')
json_data = json.load(f)
f.close()


class Restaurant:
    def __init__(self, rating=0, category='', price=0, phone='', yelp_id='',url='',review_num=0,
                name='', city='', city_id='', state='', is_closed = None):
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




def build_restaurant(jsonfile):
    
    CACHE_DICT = open_cache(jsonfile)
    restaurants = []
    
    for key in CACHE_DICT.keys():
        if 'businesses' in CACHE_DICT[key].keys():
            for business in CACHE_DICT[key]['businesses']:
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
                city = business['location']['city']
                is_closed = business['is_closed']
                instance = Restaurant(rating=rating, price=price, phone=phone, category=category, yelp_id=yelp_id, 
                                      url=url, review_num=review_num, name=name, 
                                      city=city, state=state, is_closed=is_closed)
                restaurants.append(instance)
    return restaurants
restaurants = build_restaurant('restaurant.json')


# category = []
# num = 0
# for i in restaurants:
#     category.append(i.category)
#     num += 1
# category = (set(category))

# category


# price = []
# num = 0
# for i in restaurants:
#     price.append(i.price)
#     num += 1
# price = (set(price))

# price


criteria = ['rating', 'review_num', "is_closed", "price"]




organized_dict = {}
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]


for restaurant in restaurants:
    if restaurant.rating > 4:
        if restaurant.review_num > 100:
            if restaurant.is_closed == False:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    a.append(restaurant.__dict__)
                else:
                    b.append(restaurant.__dict__)
            else:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    c.append(restaurant.__dict__)
                else:
                    d.append(restaurant.__dict__)
        else:
            if restaurant.is_closed == False:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    e.append(restaurant.__dict__)
                else:
                    f.append(restaurant.__dict__)
            else:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    g.append(restaurant.__dict__)
                else:
                    h.append(restaurant.__dict__)
    else:
        if restaurant.review_num > 100:
            if restaurant.is_closed == False:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    i.append(restaurant.__dict__)
                else:
                    j.append(restaurant.__dict__)
            else:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    k.append(restaurant.__dict__)
                else:
                    l.append(restaurant.__dict__)
        else:
            if restaurant.is_closed == False:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    m.append(restaurant.__dict__)
                else:
                    n.append(restaurant.__dict__)
            else:
                if (restaurant.price != None) and (restaurant.price >= 3):
                    o.append(restaurant.__dict__)
                else:
                    p.append(restaurant.__dict__)




with open("organized_data.json", "w") as outfile:
        json.dump(organized_dict, outfile)



questions = ["Do you prefer a restaurant with rating 4 and higher?",
             "Do you prefer a restaurant with more than 100 reviews?",
             "Do you need the restaurant is currently open?",
             "Do you mind if the restaurant costs 100$ and higher per person?"
            ]


tree =     ["Do you prefer a restaurant with rating 4 and higher?", 
        ["Do you prefer a restaurant with more than 100 reviews?", 
            ["Do you need the restaurant is currently open?", 
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [a,None,None],[b,None,None]],
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [c,None,None],[d,None,None]]], 
            ["Do you prefer louder music? (Y/N)",
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [e,None,None],[f,None,None]],
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [g,None,None],[h,None,None]]]],
        ["Do you prefer a restaurant with more than 100 reviews?", 
            ["Do you need the restaurant is currently open?",
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [i,None,None],[j,None,None]],
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [k,None,None],[l,None,None]]], 
            ["Do you need the restaurant is currently open?",
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [m,None,None],[n,None,None]],
                ["Do you mind if the restaurant costs 100$ and higher per person?",
                    [o,None,None],[p,None,None]]]]]




def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")
printTree(tree)


# In[115]:


with open("mytree.json", "w") as outfile:
        json.dump(tree, outfile)

