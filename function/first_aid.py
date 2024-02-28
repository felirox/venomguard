import openai
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
def tell_first_aid(snake_type, location):
    
    # nearby hospital
    gmaps = googlemaps.Client(key=google_maps_api_key)
    places_result = gmaps.places_nearby(location=location, keyword="形成外科|救急科", radius=5000, type='hospital')

    # 検索結果から病院の情報を抽出
    hospitals = []
    for place in places_result['results']:
        print(place)
        name = place['name']
        address = place.get('vicinity', '住所不明')
        hospitals.append(f"{name} - {address}")
    print(places_result)
    
    #check if hospital list is still empty
    if hospitals == []:
        print("INFO: No hospitals found in search #1. Retrying with a different query")
        places_result = gmaps.places_nearby(location=location, keyword="Emergency Hospital", radius=40000, type='hospital')
        print(places_result)
        for place in places_result['results']:
            print(place)
            name = place['name']
            address = place.get('vicinity', '住所不明')
            hospitals.append(f"{name} - {address}")
    # first aid

    sys_prompt_first_aid = f"""
    Please provide first aid measures for a bite from a {snake_type}.
    """
    
    messages = [{"role": "system", "content": sys_prompt_first_aid}]

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        temperature=0,
        messages=messages,
    )
    first_aid = response['choices'][0]['message']['content']
    return first_aid, hospitals