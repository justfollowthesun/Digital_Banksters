import vk
import time

from src.parsing import *
from src.parsing_settings import KEYWORDS,KEYWORD_CITIES, COUNT





session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)


def get_users(group_id):
    good_id_list = []
    offset = 0
    max_offset = get_offset(group_id)
    while offset < max_offset:
        response = requests.get('https://api.vk.com/method/groups.getMembers', params={
            'access_token':token,
            'v':5.103,
            'group_id': group_id,
            'sort':'id_desc',
            'offset':offset,
            'fields':'last_seen'
        }).json()['response']
        offset += 1
        for item in response['items']:
            try:
                if item['last_seen']['time'] >= 1605571200:
                    good_id_list.append(item['id'])
            except Exception as E:
                continue
    return good_id_list

for group in group_list:
    try:
        users = get_users(group)
        all_users.extend(users)
        time.sleep(1)
    except KeyError as E:
        print(group, E)
        continue

all_users = list(set(all_users))




def get_offset(group_id):
    count = requests.get('https://api.vk.com/method/groups.getMembers', params={
            'access_token':token,
            'v':5.103,
            'group_id': group_id,
            'sort':'id_desc',
            'offset':0,
            'fields':'last_seen'
        }).json()['response']['count']
    return count // 1000

all_users = []

group_list = []
for city in KEYWORD_CITIES:
    CITY_ID = api.database.getCities(country_id=1, q=city)['items'][0]['id']
    group_city= list_gropus(KEYWORDS, COUNT, CITY_ID)
    group_list = group_city + group_city

for group in group_list:
    print(group)
    try:
        users = get_users(group)
        all_users.extend(users)
        time.sleep(1)
    except KeyError as E:
        print(group, E)
        continue

all_users = list(set(all_users))

with open('users.txt', 'w') as f:
    for item in all_users:
        f.write("%s\n" % item)


# keyword_city = "Балашиха"
# keywords_groups = ['ремонт', 'потолки', 'мебель', 'двери']
#
# # Подключение к VK API
# session = vk.Session(access_token=token)
# api = vk.API(session, v=v)
#
# # Запрос списка городов России (Cities) по ключевому слову
# Cities = api.database.getCities(country_id=1, q=keyword_city)['items']