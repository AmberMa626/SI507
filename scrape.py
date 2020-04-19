#################################
##### Name: Yue Ma ##############
##### Uniqname: maamber #########
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets

CACHE_FILENAME = "cache.json"
CACHE_DICT = {}

base_url='https://www.broadway.org'

class Theater:
    def __init__(self, name, address,city,state,zipcode,box_office_hours,website,latitude,longitude):       
            self.name=name
            self.address=address
            self.city=city
            self.state=state
            self.zipcode=zipcode
            self.box_office_hours=box_office_hours
            self.website=website
            self.latitude=latitude
            self.longitude=longitude
    def info(self):
        return {'latitude':self.latitude,'longitude':self.longitude}

def build_show_url_dict():
    show_url_dict={}
    response=requests.get(base_url)
    text=response.text
    soup=BeautifulSoup(text,'html.parser')
    touring_show=soup.find('div',id='all-touring-show-listD')
    show_div=touring_show.find_all('div',class_='col-lg-3')
    for div in show_div:
        child_ul=div.find_all('ul',class_='list-group')
        for ul in child_ul:
            child_li=ul.find_all('li')
            for li in child_li:
                show_url_dict[li.text.lower().strip()]=base_url+li.a.get('href')
    # print(show_url_dict)
    return show_url_dict


def create_theater_instance(theatre_url):
    if theatre_url in CACHE_DICT.keys():
        print("Using Cache")
        text= CACHE_DICT[theatre_url]
    else:
        print("Fetching")
        response = requests.get(theatre_url)
        text=response.text
        CACHE_DICT[theatre_url] = text
        save_cache(CACHE_DICT)
    soup = BeautifulSoup(text, 'html.parser')
    try:
        name= soup.find('div',class_='try-disp-table').h2.text.strip()
    except:
        name='None'
    try:
        address=soup.find('input',attrs={'name':'address','type':'hidden'})['value'].strip()
    except:
        address='None'
    try:
        city=soup.find('input',attrs={'name':'city','type':'hidden'})['value'].split(',')[0].strip()
    except:
        city='None'
    try:
        state=soup.find('input',attrs={'name':'city','type':'hidden'})['value'].split(',')[1].split()[0]
    except:
        state='None'
    try:
        zipcode=soup.find('input',attrs={'name':'city','type':'hidden'})['value'].split(',')[1].split()[1]
    except:
        zipcode='None'
    try:
        box_office_hours=soup.find('div',class_='box-office-hours').text.strip()
    except:
        box_office_hours='None'
    try:
        website=soup.find('input',attrs={'name':'website','type':'hidden'})['value'].strip()
    except:
        website='None'
    try:
        latitude=soup.find('input',attrs={'name':'latitude','type':'hidden'})['value'].strip()
    except:
        latitude='None'
    try:
        longitude=soup.find('input',attrs={'name':'longitude','type':'hidden'})['value'].strip()
    except:
        longitude='None'
    theater_instance=Theater(name, address,city,state,zipcode,box_office_hours,website,latitude,longitude)
    return theater_instance

def build_theatre_url_dict(show_url):
    theatre_url_dict={}
    if show_url in CACHE_DICT.keys():
        print("Using Cache")
        text= CACHE_DICT[show_url]
    else:
        print("Fetching")
        response = requests.get(show_url)
        text=response.text
        CACHE_DICT[show_url] = text
        save_cache(CACHE_DICT)
    soup=BeautifulSoup(text,'html.parser')   
    show_div=soup.find_all('div',class_='col-md-4')
    for div in show_div:
        theatre_info=div.find_all('a',recursive=False)
        for theatre in theatre_info:
            if theatre.text.lower().strip() !='buy tickets':
                theatre_url_dict[theatre.text.lower().strip()]=base_url+theatre['href']
    return(theatre_url_dict)

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def get_nearby_restaurants(theater_object):
    latitude=theater_object.info()['latitude']
    longitude=theater_object.info()['longitude']
    base_url= "https://api.yelp.com/v3/businesses/search"
    headers={
        "Authorization": f"Bearer {secrets.API_KEY}"
    }
    params={
        "term":'restaurant',
        "latitude": latitude,
        "longitude": longitude,
        "sort_by":'rating',
        "radius":4800,
        "limit":10
    }
    request_key = construct_unique_key(base_url, params)
    if request_key in CACHE_DICT.keys():
        print("Using Cache")
        return CACHE_DICT[request_key]
    else:
        print("Fetching")
        response=requests.get(base_url,params,headers=headers)
        result=response.json()
        CACHE_DICT[request_key] = result
        save_cache(CACHE_DICT)
        return result

def get_restaurant_list(site_object):
    restaurant_list=[]
    try: 
        result= get_nearby_restaurants(x[1])['businesses']
        for item in result:
            restaurant_info={}
            restaurant_info['name']=item['name'] if item['name']!='' else "No name"
            restaurant_info['review_count']=item['review_count'] if item['review_count']!='' else None
            restaurant_info['raing']=item['rating'] if item['rating']!='' else None
            try:
                restaurant_info['price']=item['price'] if item['rating']!='' else 'No price'
            except: 
                restaurant_info['price'] ="No price"
            restaurant_info['location']=item['location']['display_address'][0] if item['location']['display_address'][0]!='' else 'No address'
            restaurant_info['phone']=item['display_phone'] if item['display_phone'] !='' else 'No phone number'
            restaurant_list.append(restaurant_info)
    except:
        restaurant_list.append("No restaurants near this Theater.")
    return restaurant_list

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
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


if __name__ == "__main__":
    CACHE_DICT = open_cache()
    url_dict={}
    show_theatre_dict={}
    theater_info={}
    restaurant_dict={}
    show_url_dict=build_show_url_dict()
    for value in show_url_dict.items():
        show_theatre_dict[value[0]]=build_theatre_url_dict(value[1])
        url_dict=(build_theatre_url_dict(value[1]))
        for theater in url_dict.items():
            if theater[0] not in theater_info.keys():
                theater_info[theater[0]]=create_theater_instance(theater[1])
            else:
                continue
    for x in theater_info.items():
        restaurant_dict[x[0]]=get_restaurant_list(x[1])
    # print(theater_info)

    ## write into json

    dumped_show_theatre=json.dumps(show_theatre_dict)
    fw = open('show_theatre.json',"w")
    fw.write(dumped_show_theatre)
    fw.close()

    # dumped_theater_info=json.dumps(theater_info)
    # fw = open('theater_info.json',"w")
    # fw.write(dumped_theater_info)
    # fw.close()

    dumped_restaurant_dict=json.dumps(restaurant_dict)
    fw = open('restaurant_info.json',"w")
    fw.write(dumped_restaurant_dict)
    fw.close()




